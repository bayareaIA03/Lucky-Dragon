from django.urls import path
from . import views
from .forms import EmailValidationOnForgotPassword
from .checkout_form import ContactWizard, FORMS, show_address_form_condition
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


'''
Forgot Password Functionality
    This requires 4 different URLs followed by 4 templates
        1. password-reset: this allows users to request password reset using the user's email
        2. pass-reset/done: informs the user to check his email after submitting the password reset request
        3. password-reset-confirm/<uidb64>/<token>/: used to identify the user and are passed in by Django from the link in the email => can reset password
        4. password-reset-complete: prompts the user after they have successfully reset his password
'''


urlpatterns = [
    path("", views.index, name='index'),
    path("register/", views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='luckydragon_app/login.html',
        redirect_authenticated_user=True), name="login"),
    path('accounts/profile/', views.profile, name="profile"),
    path("menu/", views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('checkout-login/', views.checkout_login, name='checkout_login'),
    path('checkout/', ContactWizard.as_view(FORMS, 
            condition_dict={'address': show_address_form_condition }
        ), name="checkout"),
    path('checkout-confirm/', views.checkout_confirm, name="checkout_confirm"),
    path('logged-out/', auth_views.LogoutView.as_view(
        template_name='luckydragon_app/logout.html'), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="luckydragon_app/password_reset.html", form_class=EmailValidationOnForgotPassword), name="password_reset"),
    path("password-reset/done", auth_views.PasswordResetDoneView.as_view(
        template_name="luckydragon_app/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="luckydragon_app/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="luckydragon_app/password_reset_complete.html"), name="password_reset_complete"),
    path('cart/', views.cart, name='cart'),
    path('checkout-login/', views.checkout_login, name='checkout-login'),
    path('menu/<int:foodID>', views.dish_display, name='dish_display'),
    path('catering/', views.catering, name='catering'),
]

urlpatterns += staticfiles_urlpatterns()