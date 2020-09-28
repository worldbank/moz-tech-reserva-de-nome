from django.http import JsonResponse

from reserva.core.models import NameApplication as NameApp


def name_available(request):
    return JsonResponse(
        {
            "available": NameApp.objects.is_available(request.POST["name"]),
            "name": request.POST["name"],
        }
    )
