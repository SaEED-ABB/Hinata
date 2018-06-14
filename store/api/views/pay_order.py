from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from zeep import Client

from ratelimit.decorators import ratelimit

from customer.models import Basket
from customer.decorators import check_permission_api


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
LEAST_AMOUNT_PAY = 20000  # ۲۰ هزار تومن


# @require_http_methods(['POST'])
# @ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
# @check_permission_api(['user'])
def pay_order(request):
    basket_code = request.POST.get('basket_code')

    try:
        basket = Basket.objects.get(code=basket_code)
    except Basket.DoesNotExist:
        res_body = {
            "error": "no such basket found for user {}".format(request.user.get_full_name())
        }
        return JsonResponse(res_body, status=404)

    if request.user != basket.user:
        res_body = {
            "error": "permission denied. request.user is not the same as basket.user"
        }
        return JsonResponse(res_body, status=403)

    if basket.payment_type == 'pay_online':
        amount = basket.total_price
        description = "توضیحات:‌ پرداخت کامل پول آنلاین"  # Required
    elif basket.payment_type == 'pay_at_home':
        amount = basket.total_price if basket.total_price < LEAST_AMOUNT_PAY else LEAST_AMOUNT_PAY
        description = "توضیحات: پرداخت حداقل ۲۰,۰۰۰ هزار تومان باوجود پرداخت درب منزل"  # Required
    else:
        res_body = {
            "error": "payment type is unknown."
        }
        status = 400
        return JsonResponse(res_body, status=status)

    CallbackURL = reverse('store:verify_pay_order')  # Important: need to edit for realy server.

    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)

    if result.Status == 100:
        if basket.payment_type == 'pay_online':
            basket.how_much_paid_online = amount
            basket.paid_online_at = timezone.now()
            basket.save()
        elif basket.payment_type == 'pay_at_home':
            basket.how_much_paid_at_home = amount
            basket.paid_at_home_at = timezone.now()
            basket.save()
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        res_body = {
            "error": str(result.Status)
        }
        status = 400
        return JsonResponse(res_body, status)


def verify_pay_order(request):
    if request.GET.get('Status') == 'OK':
        amount = request.GET.get('amount', 0)
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')