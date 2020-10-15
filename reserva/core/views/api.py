from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from reserva.core.forms import CheckForm


@require_GET
@cache_page(60 * 60 * 6)  # 6h cache
def available(request):
    form = CheckForm(request.GET)
    if form.is_valid():
        available = True
        name = form.cleaned_data["name"]
    else:
        available = False
        name = request.GET["name"]

    return JsonResponse({"available": available, "name": name})
