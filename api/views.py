from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Category
from django.db.models import Q


# POST /categories/
@csrf_exempt
@require_POST
def add_categories(request):
    tree = json.loads(request.POST['tree'])
    # преобразуем словарь в list по необходимости, так как json может являться и объектом и списком объектов
    if type(tree) == dict:
        tree = [tree]

    res = []
    parse(tree, res)
    # Словарь индексов категорий
    ids_dict = {category: i + 1 for i, category in enumerate(res)}

    record_to_db(tree, None, ids_dict)

    return HttpResponse(status=200)


# Запись дерева в базу данных
def record_to_db(tree, parent_id, ids_dict):
    for i in tree:
        category = Category(id=ids_dict[i['name']], name=i['name'], parent_id=parent_id)
        category.save()
        if 'children' in i.keys():
            record_to_db(i['children'], ids_dict[i['name']], ids_dict)


# Получение списка категорий без вложенности
def parse(tree, res):
    for i in tree:
        res.append(i['name'])
        if 'children' in i:
            parse(i['children'], res)


# GET /categories/<id>/​
@require_GET
def get_category(request, id):
    try:
        my_category = Category.objects.get(id=id)
        # Формирование списка родителей с проверкой на их наличие
        parents = []
        if my_category.parent_id != None:
            parents = [my_category.parent]
            # Последовательное получение родителей родителя
            while (parents[-1].parent_id != None):
                parents.append(Category.objects.get(id=parents[-1].parent_id))
        # Получение списка братьев и сестер(без my_category)
        siblings = (Category.objects.filter(~Q(id=my_category.id), parent_id=my_category.parent_id))
        children = Category.objects.filter(parent=my_category)

        # Перевод списков в необходимый вид списков словарей
        parents = [{'id': i.id, 'name': i.name} for i in parents]
        children = [{'id': i.id, 'name': i.name} for i in children]
        siblings = [{'id': i.id, 'name': i.name} for i in siblings]

        result = {
            'id': my_category.id,
            'name': my_category.name,
            'parents': parents,
            'children': children,
            'siblings': siblings
        }

        return JsonResponse(result)
    except:
        raise Http404


# Очистка БД
# GET /categories/delete/​
@require_GET
def delete_everything(self):
    Category.objects.all().delete()
    return HttpResponse(status=200)
