from django.http import JsonResponse
from django.views.decorators.http import require_POST

from reserva.core.forms import CheckForm


@require_POST
def available(request):
    form = CheckForm(request.POST)
    if form.is_valid():
        available = True
        name = form.cleaned_data["name"]
    else:
        available = False
        name = request.POST["name"]

    return JsonResponse({"available": available, "name": name})
