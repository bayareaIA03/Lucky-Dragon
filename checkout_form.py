from .forms import OrderTypeForm, AddressForm, PaymentForm, ContactForm
from formtools.wizard.views import SessionWizardView
from django.shortcuts import redirect, render
from .models import user, Food, order, card
from .delivery_package import delivery
from django import forms
from django.core.exceptions import SuspiciousOperation

import datetime
from django.template.loader import get_template, render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags


FORMS = [("ordertype", OrderTypeForm),
         ("address", AddressForm),
         ("contact", ContactForm),
         ("payment", PaymentForm)]

TEMPLATES = {"ordertype": "../templates/luckydragon_app/checkout.html",
             "address": "../templates/luckydragon_app/checkout.html",
             "contact": "../templates/luckydragon_app/checkout.html",
             "payment": "../templates/luckydragon_app/checkout.html"}


class ContactWizard(SessionWizardView):
    def get(self, request):
        if 'cart_visited' not in request.session or 'order_confirmation' not in request.session:
            return redirect('cart')
        
        request.session['delivery_fee'] = 0.0
        self.storage.reset()

        self.storage.current_step = self.steps.first
        return self.render(self.get_form())

    def post(self, request):
        """
        This method handles POST requests.

        The wizard will render either the current step (if form validation
        wasn't successful), the next step (if the current step was stored
        successful) or the done view (if no more steps are available)
        """
        # Look for a wizard_goto_step element in the posted data which
        # contains a valid step name. If one was found, render the requested
        # form. (This makes stepping back a lot easier).
        wizard_goto_step = self.request.POST.get('wizard_goto_step', None)
        if wizard_goto_step and wizard_goto_step in self.get_form_list():
            return self.render_goto_step(wizard_goto_step)

        # Check if form was refreshed
        management_form = ManagementForm(self.request.POST, prefix=self.prefix)
        if not management_form.is_valid():
            raise SuspiciousOperation(
                ('ManagementForm data is missing or has been tampered.'))

        form_current_step = management_form.cleaned_data['current_step']
        if (form_current_step != self.steps.current and
                self.storage.current_step is not None):
            # form refreshed, change current step
            self.storage.current_step = form_current_step

        # get the form for the current step
        form = self.get_form(data=self.request.POST, files=self.request.FILES)

        # and try to validate
        if form.is_valid():
            if self.steps.current == 'address':
                data = form.cleaned_data
                distance = delivery.delivery_distance(
                    data['street_number'], data['street'], data['city'], data['zipcode'])
                delivery_fee = delivery.delivery_total(
                    request, distance, request.session['total'])
                if not delivery_fee:
                    return self.render(form)
                request.session['delivery_fee'] = delivery_fee

            # if the form is valid, store the cleaned data and files.
            self.storage.set_step_data(
                self.steps.current, self.process_step(form))
            self.storage.set_step_files(
                self.steps.current, self.process_step_files(form))

            # check if the current step is the last step
            if self.steps.current == self.steps.last:
                # no more steps, render done view
                return self.render_done(form)
            else:
                # proceed to the next step
                return self.render_next_step(form)
        return self.render(form)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context.update({'total': '$' + str(self.request.session['total'])})
        context.update(
            {'delivery_fee': '$' + str(self.request.session['delivery_fee'])})
        return context

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        # gets user info and autofills checkout page if user is authenticated
        if self.request.user.is_authenticated:
            user_info = user.CustomUser.objects.filter(
                username=self.request.user
            )
            if step == 'address':
                initial.update({
                    'street_number': user_info.values('user_street_number')[0]['user_street_number'],
                    'street': user_info.values('user_street')[0]['user_street'],
                    'city': user_info.values('user_city')[0]['user_city'],
                    'zipcode': user_info.values('user_zipcode')[0]['user_zipcode']
                })
            elif step == 'contact':
                initial.update({
                    'email': user_info.values('email')[0]['email'],
                    'phone_number': user_info.values('user_phone_number')[0]['user_phone_number'],
                    'first_name': user_info.values('first_name')[0]['first_name'],
                    'last_name': user_info.values('last_name')[0]['last_name']
                })
        return initial

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        # Process data here
        # Extract data from forms
        address = {}
        if form_dict.get('address'):
            address = form_dict['address'].cleaned_data
        ordertype = form_dict['ordertype'].cleaned_data
        payment = form_dict['payment'].cleaned_data
        contact = form_dict['contact'].cleaned_data
        self.request.session['total'] += float(
            self.request.session['delivery_fee'])
        user_order_obj = None
        guest_order_obj = None
        # create order objects
        if self.request.user.is_authenticated:
            user_order_obj = order.Order(
                order_user=self.request.user,
                order_total=self.request.session['total'],
                order_tip=self.request.session['tip'],
                order_delivery_fee=self.request.session['delivery_fee'],
                order_type=ordertype['order_type'],
                order_payment_type=payment['order_payment_type'],
            )
            user_order_obj.save()
        else:
            guest_order_obj = order.GuestOrder(
                guest_order_name=contact['first_name'] +
                ' ' + contact['last_name'],
                guest_order_phone_number=contact['phone_number'],
                guest_order_email=contact.get('email'),
                guest_order_total=self.request.session['total'],
                guest_order_tip=self.request.session['tip'],
                guest_order_delivery_fee=self.request.session['delivery_fee'],
                guest_order_type=ordertype['order_type'],
                guest_order_payment_type=payment['order_payment_type'],
                guest_order_street_number=address.get('street_number'),
                guest_order_street=address.get('street'),
                guest_order_city=address.get('city'),
                guest_order_zipcode=address.get('zipcode')
            )
            guest_order_obj.save()

        cart = self.request.session['shopping_cart']
        tax = self.request.session['tax']
        # create order details for the food
        order_detail_list = []
        for obj in cart:
            food = cart[obj]
            food_object = Food.objects.filter(
                food_name=food['food_name']
            )
            food_info_list = food_object.values()
            option_string = ''
            if food.get('special_instruction'):
                option_string += food.get('special_instruction')
                option_string += ":"
            options = food.get('options')
            if options:
                for option in options:
                    option_string += option + '-'
                option_string = option_string[:len(option_string) - 1]
            order_detail = order.OrderDetail(
                order_detail_order_id=user_order_obj,
                order_detail_guest_order_id=guest_order_obj,
                order_detail_food=food_object[0],
                order_detail_quantity=food['quantity'],
                order_detail_options=option_string,
                order_detail_price=food['unit_price']
            )
            order_detail.save()
            order_detail_list.append([
                order_detail.order_detail_quantity,
                order_detail.order_detail_food.food_name,
                food_info_list[0]['food_price'],
                food['subtotal'],
                food.get('special_instruction'),
                food.get('options')
            ])
        if self.request.user.is_authenticated:
            c = {'order_id': user_order_obj.order_id,
                 'name': contact['first_name'] + ' ' + contact['last_name'],
                 'phone_number': contact['phone_number'],
                 'email': contact.get('email'),
                 'order_type': user_order_obj.order_type,
                 'payment_type': user_order_obj.order_payment_type,
                 'time': user_order_obj.order_timestamp,
                 'total': user_order_obj.order_total,
                 'subtotal': self.request.session['subtotal'],
                 'tip': user_order_obj.order_tip,
                 'delivery_fee': user_order_obj.order_delivery_fee,
                 'delivery_instructions': address.get('delivery_instructions'),
                 'order_items': order_detail_list,
                 'tax': tax,
                 'street_number': address.get('street_number'),
                 'street': address.get('street'),
                 'city': address.get('city'),
                 'zipcode': address.get('zipcode'),
                 }
        else:
            c = {'order_id': guest_order_obj.guest_order_id,
                 'order_type': guest_order_obj.guest_order_type,
                 'payment_type': guest_order_obj.guest_order_payment_type,
                 'name': contact['first_name'] + ' ' + contact['last_name'],
                 'phone_number': contact['phone_number'],
                 'email': contact.get('email'),
                 # TODO: correct spelling of timestamp field
                 'time': guest_order_obj.guest_order_timestamp,
                 'total': guest_order_obj.guest_order_total,
                 'subtotal': self.request.session['subtotal'],
                 'tip': guest_order_obj.guest_order_tip,
                 'delivery_fee': guest_order_obj.guest_order_delivery_fee,
                 'delivery_instructions': address.get('delivery_instructions'),
                 'order_items': order_detail_list,
                 'tax': tax,
                 'street_number': address.get('street_number'),
                 'street': address.get('street'),
                 'city': address.get('city'),
                 'zipcode': address.get('zipcode'),
                 }
        # Restaurant needs to login to email account before taking orders
        html_message = render_to_string('luckydragon_app/order_email.html', c)
        plain_message = strip_tags(html_message)
        send_mail('Lucky Dragon Order Receipt', plain_message, 'luckydragonteam@gmail.com',
                  [c.get('email'), 'luckydragonteam@gmail.com'], fail_silently=False, html_message=html_message)

        return redirect('checkout_confirm')


class ManagementForm(forms.Form):
    """
    ``ManagementForm`` is used to keep track of the current wizard step.
    """
    current_step = forms.CharField(widget=forms.HiddenInput)


def show_address_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('ordertype') or {}
    return cleaned_data.get('order_type') == 'Delivery'
