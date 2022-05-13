from pprint import pprint

file_name = 'recipes.txt'


def recipies_dict(recipies):
    with open(recipies, encoding='utf-8') as file:
        cook_book = {}
        for line in file:
            line = line.strip()
            if line.isdigit() or line == '':
                continue
            elif '|' in line:
                ingredient_name, quantity, measure = map(str.strip, line.split('|'))
                cook_book[dish].append({'ingredient_name': ingredient_name, 'quantity': int(quantity), 'measure': measure})
            else:
                dish = line
                cook_book[dish] = []
        return cook_book


def recipies_dict_2(recipies):
    with open(recipies, encoding='utf-8') as file:
        cook_book = {}
        for line in file:
            dish = line.strip()
            cook_book[dish] = []
            item_quantity = int(file.readline().strip())
            for i in range(item_quantity):
                ingredient_name, quantity, measure = map(str.strip, file.readline().split('|'))
                cook_book[dish].append({'ingredient_name': ingredient_name,
                                        'quantity': int(quantity),
                                        'measure': measure})
            file.readline()

        return cook_book


def get_shop_list_by_dishes(dishes, person_count):
    grocery_list = {}
    for dish in dishes:
        if dish in cook_book:
            for ingredients in cook_book[dish]:
                ingredient, quantity, measure = ingredients
                if ingredients[ingredient] in grocery_list:
                    grocery_list[ingredients[ingredient]]['quantity'] += ingredients[quantity]*person_count
                else:
                    grocery_list[ingredients[ingredient]] = {'measure': ingredients[measure],
                                                             'quantity': ingredients[quantity]*person_count}
        else:
            print(f'Такого блюда, как "{dish}" нету в книге рецептов. Оно не было добавлено в список покупок')
    return grocery_list


cook_book = recipies_dict(file_name)
pprint(cook_book, sort_dicts=False)
groceries = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет', 'qwe'], 2)
pprint(groceries)
