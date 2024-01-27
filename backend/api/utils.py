from django.db.models import Sum

from recipes.models import RecipeIngredient


def generate_shopping_list(user):
    """Generate a list of products that need to be bought."""

    ingredients = RecipeIngredient.objects.filter(
        recipe__cart__user=user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))

    shopping_list = f'{user.first_name}, You need to buy the following:\n\n'

    shopping_list += '\n'.join([
        f'- {ingredient["ingredient__name"]} '
        f'({ingredient["ingredient__measurement_unit"]})'
        f' - {ingredient["amount"]}'
        for ingredient in ingredients
    ])

    shopping_list += '''\n
We look forward to seeing you again on our website!
'''

    return shopping_list
