from django.http import JsonResponse
from django.views.decorators.http import require_GET

from reserva.core.forms import CheckForm


@require_GET
def available(request):
    form = CheckForm(request.GET)
    if form.is_valid():
        available = True
        name = form.cleaned_data["name"]
    else:
        available = False
        name = request.GET["name"]

    return JsonResponse({"available": available, "name": name})
