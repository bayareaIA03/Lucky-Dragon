from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import user, order
from .delivery_package import delivery
from django import forms


'''
----- Class UserRegistration -----

    UserCreationForm
        o- A model available from Django for creating a new user
        o- It has 3 fields: username (from the user model), password1, and password2
        o- It includes password validation and username uniqueness in the user model

    UserRegistration
        o- Inherits attributes and functionalities from UserCreationForm
        o- 8 fields added in this class: email, first_name, last_name, etc.

    Meta
        o- Metadata options
        o- Provide a model (User) to be stored when a user is created
        o- fields: the fields in which we want the form to display in browser (in order)
'''


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=20)
    street_number = forms.CharField(max_length=10, required=False)
    street = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)
    zipcode = forms.CharField(max_length=5, required=False)

    class Meta:
        model = user.CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'street_number',
                  'street', 'city', 'zipcode',  'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.user_phone_number = self.cleaned_data['phone_number']
        user.user_street_number = self.cleaned_data['street_number']
        user.user_street = self.cleaned_data['street']
        user.user_city = self.cleaned_data['city']
        user.user_zipcode = self.cleaned_data['zipcode']
        if commit:
            user.save()
        return user


'''
----- Class UserUpdateForm -----
    UserUpdateForm
        o- Inherits attributes and functionalities from ModelForm
        o- 8 fields added in this class: email, first_name, last_name, etc.
'''


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    user_phone_number = forms.CharField(max_length=20)
    user_street_number = forms.CharField(max_length=10, required=False)
    user_street = forms.CharField(max_length=50, required=False)
    user_city = forms.CharField(max_length=50, required=False)
    user_zipcode = forms.CharField(max_length=5, required=False)

    class Meta:
        model = user.CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_phone_number', 'user_street_number',
                  'user_street', 'user_city', 'user_zipcode']

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.user_phone_number = self.cleaned_data['user_phone_number']
        user.user_street_number = self.cleaned_data['user_street_number']
        user.user_street = self.cleaned_data['user_street']
        user.user_city = self.cleaned_data['user_city']
        user.user_zipcode = self.cleaned_data['user_zipcode']
        if commit:
            user.save()
        return user


'''
----- Class EmailValidationOnForgotPassword -----
    This class will overwrite the default PasswordResetForm to raise error if an email does not exist in db
    If an email does not exist in the db, it will raise error and show it on the screen
'''


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not user.CustomUser.objects.filter(email__iexact=email, is_active=True).exists():
            msg = ("There is no user registered with the specified email address.")
            self.add_error('email', msg)
        return email


class CheckoutLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CheckoutLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
    ))

class OrderTypeForm(forms.Form):
    order_types = [('Pick-up', 'Pick-up'), ('Delivery', 'Delivery')]
    order_type = forms.ChoiceField(choices=order_types)

class ContactForm(forms.Form):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20, validators=[RegexValidator(r'^[0-9]+$')], error_messages={'invalid': 'invalid phone number'})
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

class AddressForm(forms.Form):
    street_number = forms.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]+$')])
    street = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    zipcode = forms.CharField(max_length=5, validators=[RegexValidator(r'^[0-9]+$')])
    delivery_instructions = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    
class PaymentForm(forms.Form):
    payment_types = [('Card', 'Card'), ('Cash', 'Cash')]
    order_payment_type = forms.ChoiceField(choices=payment_types, widget = forms.Select(attrs = {'onchange' : "hide()"}))
    card_types = [('Visa', 'Visa'), ('MasterCard', 'MasterCard'),
                  ('AmericanExpress', 'AmericanExpress'), ('Discover', 'Discover')]
    card_type = forms.ChoiceField(choices=card_types, disabled=True, required=False)
    card_number = forms.CharField(max_length=20, disabled=True, required=False)
    card_exp_date = forms.CharField(max_length=5, disabled=True, required=False)
    card_cvv = forms.CharField(max_length=5, disabled=True, required=False)
    card_billing_zipcode = forms.CharField(max_length=5, disabled=True, required=False)

