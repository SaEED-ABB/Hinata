from customer.models import SelectedProduct


def total_price(basket):
    total = 0
    for i in SelectedProduct.objects.filter(basket=basket):
        total += int(i.price)
    return total
