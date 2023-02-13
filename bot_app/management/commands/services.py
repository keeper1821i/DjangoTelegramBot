from django.contrib.auth.models import User

from expenses_app.models import Expenses



def add_prodict(user_id, text: str, category: str):
    product_list = text.split()
    summ = int(product_list[1])
    product = product_list[0]
    Expenses.objects.create(
        category=category,
        product=product_list[0],
        money=summ,
        user_id=user_id
    )
