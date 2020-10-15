from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods

from reserva.core.forms import CheckForm, PayForm, SendForm
from reserva.core.models import Nationality


DEFAULT_NATIONALITY = Nationality.objects.default().pk


@require_GET
def home(request):
    return redirect(reverse("name_application:check"))


@require_http_methods(("GET", "POST"))
def check(request):
    if request.method == "GET":
        form = CheckForm()
        return render(request, "name_application/check.html", {"form": form})

    form = CheckForm(request.POST)
    if not form.is_valid():
        return render(request, "name_application/check.html", {"form": form})

    request.session["form"] = {"name": form.cleaned_data["name"]}
    return redirect(reverse("name_application:send"))


@require_http_methods(("GET", "POST"))
def send(request):
    if "form" not in request.session or "name" not in request.session["form"]:
        raise Http404()

    if request.method == "GET":
        request.session["form"]["nationality"] = DEFAULT_NATIONALITY
        nationality_list = Nationality.objects.values_list("pk", "name")
        form = SendForm(request.session["form"])
        return render(request, "name_application/send.html", {"form": form, "nationality_list": nationality_list})

    form = SendForm(request.POST)
    if not form.is_valid():
        return render(request, "name_application/send.html", {"form": form})

    data = form.cleaned_data.copy()
    data["name"] = request.session["form"]["name"]
    data["nationality"] = data["nationality"].pk  # serialize for session
    data["dob"] = data["dob"].strftime("%Y-%m-%d")  # serialize for session

    request.session["form"] = data
    return redirect(reverse("name_application:pay"))


@require_http_methods(("GET", "POST"))
def pay(request):
    if "form" not in request.session or "name" not in request.session["form"]:
        raise Http404()

    if not set(SendForm._meta.fields).issubset(request.session["form"]):
        raise Http404()

    if request.method == "GET":
        form = PayForm()
        return render(request, "name_application/pay.html", {"form": form})

    form = PayForm(request.POST)
    if not form.is_valid():
        return render(request, "name_application/pay.html", {"form": form})

    return redirect(reverse("name_application:done"))


@require_GET
def done(request):
    if "form" not in request.session or "name" not in request.session["form"]:
        raise Http404()

    if not set(SendForm._meta.fields).issubset(request.session["form"]):
        raise Http404()

    form = SendForm(request.session["form"])
    assert form.is_valid()  # form was validated before storing in session

    name_application = form.save(commit=False)
    name_application.name = request.session["form"]["name"]
    name_application.save()
    context = {"name_application": name_application}

    return render(request, "name_application/done.html", context)


@require_GET
def success(request):
    return render(request, "name_application/success.html")
