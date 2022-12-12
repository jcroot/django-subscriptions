from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from customers.forms import CustomerForm
from customers.models import Orders, CustomerCards, Cart
from data_providers.bancard.request import BancardAPI
from products.models import Product, PlanProducts


# Create your views here.
def index(request):
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'pages/index.html', context)


def checkout(request, code):
    cart = get_object_or_404(Cart, session_code=code)
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            new_customer = form.save()

            product_plan = PlanProducts.objects.get(pk=cart.product_plan.id)
            new_order = Orders(profile=new_customer, product_plan=product_plan)
            new_order.save()

            if new_order:
                return redirect(reverse('order_pay', kwargs={'code': new_order.order_code}))
    else:
        form = CustomerForm()

    context = {
        'form': form,
        'code': code,
        'product_plan': cart.product_plan,
    }

    return render(request, 'pages/checkout.html', context)


def order_pay(request, code):
    order = get_object_or_404(Orders, order_code=code)

    bancard = BancardAPI()

    customer_card = CustomerCards.objects.create(customer=order.profile)

    context = {
        'process_id': ''
    }

    response = bancard.cards_new(card_id=customer_card.id, user_id=order.profile.id,
                                 phone_number=order.profile.phone, email_addr=order.profile.email_address)

    if response:
        response_json = response.json()
        process_id = response_json['process_id']

        context.update({
            'process_id': process_id,
            'order': order
        })

    return render(request, 'pages/order-pay.html', context)


def card_return_url(request, user_id):
    context = {}
    if request.method == 'GET':
        status = request.GET['status']

        if 'add_new_card_success' in status:
            bancard = BancardAPI()
            response = bancard.users_cards(user_id)

            if response:
                response_json = response.json()

                if response_json['status'] == 'success':
                    for card in response_json['cards']:
                        card_customer = CustomerCards.objects.get(pk=card['card_id'])
                        if card_customer:
                            card_customer.alias_token = card['alias_token']
                            card_customer.card_masked_number = card['card_masked_number']
                            card_customer.expiration_date = card['expiration_date']
                            card_customer.card_brand = card['card_brand']
                            card_customer.card_type = card['card_type']
                            card_customer.save(update_fields=['alias_token', 'card_masked_number',
                                                              'expiration_date', 'card_brand', 'card_type'])

                            context.update({
                                'status': 'success',
                                'message': 'You card now is recorded'
                            })

        if 'add_new_card_fail' in status:
            description = request.GET['description']

            context.update({
                'status': 'failed',
                'message': description
            })

    return render(request, 'pages/card-status.html', context)


def add_item_to_cart(request):
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        product_plan = PlanProducts.objects.get(pk=plan_id)

        cart = Cart.objects.create_cart(product_plan=product_plan)

        if cart:
            return redirect(reverse('checkout', kwargs={'code': cart.session_code}))

