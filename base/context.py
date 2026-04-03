from django.db import models
from base import models as base_models


def default(request):
    services = base_models.Service.objects.all()

    return {
        "services": services
    }