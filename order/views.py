from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from meal.models import Meal
from order.models import Order, Transaction, OrderMeal
from order.extras import generate_order_id, transact, generate_client_token
from customer.models import Customer
from meal.forms import MealForm

import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_customer_pending_order(request):
    customer = get_object_or_404(Customer, user=request.user)
    order = Order.objects.filter(owner=customer, is_ordered=False)
    if order.exists():
        return order[0]
    return 0


@login_required
def add_to_cart(request, **kwargs):
    customer = get_object_or_404(Customer, user=request.user)
    meal = Meal.objects.filter(id=kwargs.get('item_id', "")).first()
    order_meal = OrderMeal.objects.create(meal=meal)

    if request.method == 'POST':
        form = MealForm(request.POST)

        if form.is_valid():
            order_meal.quantity = form.quantity
    else:
        form = MealForm()

    if meal.quantity !=0:
        order_meal.decrease_component_and_order_quantity()
        order_meal.save()
    else:
        messages.info(request, "Meal is out of stock !")
        return redirect(reverse('order:order_summary'), {'form': form})

    customer_order, status = Order.objects.get_or_create(owner=customer, is_ordered=False)
    customer_order.meals.add(order_meal)

    if status:
        customer_order.ref_code = generate_order_id()
        customer_order.save()

    customer.orders.add(customer_order)
    messages.info(request, "Meal added to cart")
    return redirect(reverse('order:order_summary'), {'form': form})


@login_required
def delete_from_cart(request, item_id):
    meal_to_delete = OrderMeal.objects.filter(pk=item_id).first()
    meal_to_delete.increase_component_and_order_quantity()

    if meal_to_delete:
        meal_to_delete.delete()
        messages.info(request,"Meal has been deleted from cart")

    return redirect(reverse('order:order_summary'))


@login_required
def order_details(request, **kwargs):
    existing_order = get_customer_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'order_summary.html', context)


@login_required()
def checkout(request, **kwargs):
    customer_token = generate_client_token()
    existing_order = get_customer_pending_order(request)
    publish_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
            result = transact({
                'amount': existing_order.get_cart_total(),
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                return redirect(reverse('order:update_records',
                                        kwargs={
                                            'token': result.transaction.id
                                        })
                                )
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)

                return redirect(reverse('order:checkout'))

    context = {
        'order': existing_order,
        'client_token': customer_token,
        'STRIPE_PUBLISHABLE_KEY': publish_key
    }

    return render(request, 'checkout.html', context)


@login_required
def update_transaction_records(request, token):
    order_to_purchase = get_customer_pending_order(request)
    customer_profile = get_object_or_404(Customer, user=request.user)

    order_to_purchase.is_ordered = True

    order_to_purchase.order_date = datetime.datetime.now()
    order_to_purchase.save()

    customer_profile.orders.add(order_to_purchase)

    customer_profile.save()

    transaction = Transaction(customer=request.user.customer,
                              token=token,
                              order_id=order_to_purchase.id,
                              amount=order_to_purchase.get_cart_total(),
                              success=True)
    transaction.save()

    messages.info(request, "Thank you! Your purchase was successfull !")
    return redirect('/customer/profile')


@login_required
def success(request, **kwargs):
    return render(request, 'order/purchase_success.html', {})
