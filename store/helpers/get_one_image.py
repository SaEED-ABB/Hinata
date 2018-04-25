from store.models import ProductImage


def get_one_image(product):
    this_image = ProductImage.objects.filter(product=product).last()
    return this_image.image.image.url
