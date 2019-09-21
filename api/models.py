from django.db import models
from django.db.models import Q


class CategoryManager(models.Manager):
    def get_family(self, id):
        my_category = self.get(id=id)
        # Формирование списка родителей с проверкой на их наличие
        parents = []
        if my_category.parent_id != None:
            parents = [my_category.parent]
            # Последовательное получение родителей родителя
            while (parents[-1].parent_id != None):
                parents.append(self.get(id=parents[-1].parent_id))
        # Получение списка братьев и сестер(без my_category)
        siblings = (self.filter(~Q(id=my_category.id), parent_id=my_category.parent_id))
        children = self.filter(parent=my_category)

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

        return result

    def add_categories(self, tree):
        # преобразуем словарь в list по необходимости, так как json может являться и объектом и списком объектов
        if type(tree) == dict:
            tree = [tree]

        res = []
        self.__parse(tree, res)
        # Словарь индексов категорий
        ids_dict = {category: i + 1 for i, category in enumerate(res)}

        self.__record_to_db(tree, None, ids_dict)

    # Запись дерева в базу данных
    def __record_to_db(self, tree, parent_id, ids_dict):
        for i in tree:
            self.create(id=ids_dict[i['name']], name=i['name'], parent_id=parent_id)
            if 'children' in i.keys():
                self.__record_to_db(i['children'], ids_dict[i['name']], ids_dict)

    # Получение списка категорий без вложенности
    def __parse(self, tree, res):
        for i in tree:
            res.append(i['name'])
            if 'children' in i:
                self.__parse(i['children'], res)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
