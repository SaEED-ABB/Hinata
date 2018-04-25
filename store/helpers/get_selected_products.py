from customer.models import SelectedProduct
from store.models import ProductImage
from .get_one_image import get_one_image


def get_selected_products(basket):
    context = []
    for i in SelectedProduct.objects.filter(basket=basket):
        context.append({
            "name": i.product.name,
            "color": i.color.name,
            "size": i.size.name,
            "image": get_one_image(i)
        })
    return context
