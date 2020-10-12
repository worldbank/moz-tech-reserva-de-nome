from django.http import HttpResponseNotAllowed, JsonResponse

from reserva.core.forms import CheckForm


def available(request):
    if request.method != "POST":
        raise HttpResponseNotAllowed(("POST",))

    form = CheckForm(request.POST)
    if form.is_valid():
        available = True
        name = form.cleaned_data["name"]
    else:
        available = False
        name = request.POST["name"]

    return JsonResponse({"available": available, "name": name})
