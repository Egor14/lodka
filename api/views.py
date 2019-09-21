from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Category


# POST /categories/
@csrf_exempt
@require_POST
def add_categories(request):
    try:
        tree = json.loads(request.POST['tree'])
        Category.objects.add_categories(tree)
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)


# GET /categories/<id>/​
@require_GET
def get_category(request, id):
    try:
        result = Category.objects.get_family(id)
        return JsonResponse(result)
    except:
        raise Http404


# Очистка БД
# GET /categories/delete/​
@require_GET
def delete_everything(self):
    Category.objects.all().delete()
    return HttpResponse(status=200)
