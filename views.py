from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserUpdateForm, CheckoutLoginForm
from django.contrib.auth import authenticate, login
from .models import user, Food, order, card
from formtools.wizard.views import SessionWizardView
from . import options, functions
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min
from random import randint


categories = {}
lunch_categories = {}
for c in Food.categories:
    if c[0] != 'Free':
        categories[c[0]] = None
        if 'Lunch' in c[0]:
            lunch_categories[c[0]] = None


# Create your views here.


def index(request):
    return render(request, "luckydragon_app/index.html", {})


'''
Function: About
    This function renders the Google Map API for the business location

'''


def about(request):
    return render(request, 'luckydragon_app/about.html')


'''
Function: Register
    This function creates a UserRegistrationForm and passes it to the register.html template
    No validation needed since the UserRegistration handles error checking

'''


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # #Saving the user's info
            # form.save()
            # return redirect('index')

            clean_info = form.cleaned_data
            phone_results = user.CustomUser.objects.filter(
                user_phone_number=clean_info['phone_number']).exists()
            if phone_results:
                messages.error(
                    request, f'Phone already associated with an account')
            else:
                # Saving the user's info
                form.save()
                messages.success(request, f'Account Created Successfully!')
                return redirect('/login/')
    else:
        form = UserRegistrationForm()
    return render(request, 'luckydragon_app/register.html', {'form': form})


'''
Function: Profile
    This function creates a UserUpdateForm and passes it to the profile.html template
'''


@login_required(login_url='/login/')
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Account has been updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)

    return render(request, 'luckydragon_app/profile.html', {'form': user_form})


def checkout_login(request):
    if 'order_confirmation' not in request.session:
        return redirect('cart')
    if request.user.is_authenticated:
        return redirect('checkout')  # go to payment processing page
    login_form = CheckoutLoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('checkout')
        else:
            messages.error(request, f'Username/password incorrect')
    # login or checkout as user
    return render(request, 'luckydragon_app/checkout_login.html', {'form': login_form})


def checkout_confirm(request):
    del request.session['cart_visited']
    del request.session['shopping_cart']
    del request.session['total']
    del request.session['tax']
    del request.session['order_confirmation']
    return render(request, 'luckydragon_app/checkout_confirm.html')


'''
Function: Cart
    This function displays the menu items the user added in the shopping cart
'''


def cart(request):
    if 'shopping_cart' in request.session:
        shopping_cart = request.session.get('shopping_cart')
    else:
        shopping_cart = {}

    print(f"Shopping cart: {shopping_cart}")
    # i - unique key(int)
    # j - dict contains of food_name, quantity, unit_price, special_instruction, and options list
    for i, j in shopping_cart.items():
        # Check if 'options' is provided by the customer
        if 'options' in j and type(j['options']) is dict and not j['add_once_flag']:
            option_str = ""
            unit_cost = j['unit_price']
            # Find the cost of all added options
            for option, cost in j['options'].items():
                unit_cost += cost
                option_str += option + ", "
            j['unit_price'] = round(unit_cost, 2)
            j['options_string'] = option_str[:-2]
            # Already added the total for this dish, set this to False to prevent adding when hitting Refresh icon
            j['add_once_flag'] = True
            # print(f"Unit price: {unit_cost}")

    if request.method == 'POST':
        # print(request.POST.get("tip"))
        # print(request.POST)
        if request.POST.get("add"):
            dish = request.POST.get("add")
            if dish in shopping_cart:
                shopping_cart[dish]['quantity'] += 1
        if request.POST.get("subtract"):
            dish = request.POST.get("subtract")
            if dish in shopping_cart:
                shopping_cart[dish]['quantity'] -= 1
                if shopping_cart[dish]['quantity'] <= 0:
                    shopping_cart.pop(dish)
        if request.POST.get("delete"):
            dish = request.POST.get("delete")
            if dish in shopping_cart:
                shopping_cart.pop(dish)
        if request.POST.get("checkout"):
            request.session['order_confirmation'] = True
            # if tip is a negative number, tip is defaulted to 0
            if float(request.POST.get("tip")) < 0:
                request.session['tip'] = 0
            else:
                request.session['tip'] = float(request.POST['tip'])
            request.session['total'] = round(
                request.session['total'] + float(request.session['tip']), 2)
            return redirect('checkout-login')
    if request.session.get('order_confirmation'):
        del request.session['order_confirmation']
    # find total cost and total quantity of cart
    total_cost = 0
    quantity = 0
    for i, j in shopping_cart.items():
        j['subtotal'] = round(j['unit_price']*j['quantity'], 2)
        total_cost += j['subtotal']
        quantity += j['quantity']

    # Find the subtotal (No tax)
    subtotal = round(total_cost, 2)
    # print(f"Subtotal: {subtotal}")
    request.session['subtotal'] = subtotal
    tip_ten = round(subtotal*0.1, 2)
    tip_fifteen = round(subtotal*0.15, 2)
    tip_twenty = round(subtotal*0.20, 2)

    # Find tax (6%) based on subtotal
    tax = round(subtotal*.06, 2)

    # Find total_cost by adding subtotal and tax together
    total_cost = round(tax+subtotal, 2)

    # food_items = Food.objects.all()

    request.session['tax'] = tax
    request.session['shopping_cart'] = shopping_cart
    request.session['total'] = total_cost
    request.session['cart_visited'] = True
    return render(request, 'luckydragon_app/cart.html', {"cart": shopping_cart, "subtotal": subtotal, "tax": tax, "total": total_cost, "quantity": quantity, "tip_ten": tip_ten, "tip_fifteen": tip_fifteen, "tip_twenty": tip_twenty})


'''
Menu Function:
    Retrieves all food items from the db and filters them into specific categories and sends them to menu.html
    Order dictionary to store food items the user adds to cart
'''


def menu(request):
    lunchFlag = functions.lunchTime()
    for category in categories:
        if not lunchFlag and category in lunch_categories:
            categories[category] = None
            continue
        categories[category] = Food.objects.filter(food_category=category)
    if request.method == 'POST':
        if 'shopping_cart' in request.session:
            shopping_cart = request.session.get('shopping_cart')
        else:
            shopping_cart = {}

        if request.POST.get("add"):
            dish_id = request.POST.get("add")
            dish = Food.objects.get(food_id=dish_id)
            # Generate random number for key purposes
            key = randint(0, 1000)
            # Make sure to generate unique number for the key
            while key in shopping_cart:
                key = randint(0, 1000)
            # Add a key(random int) : value(dict)
            shopping_cart[key] = {'food_name': dish.food_name, 'food_id': int(dish_id), 'food_image': dish.food_image,
                                  'quantity': 1, 'unit_price': dish.food_price}

            if dish.food_category == 'Traditional Plate':
                if dish.food_name == 'Pepper Steak':
                    shopping_cart[key]['options'] = {
                        "Beef": 0, 'White Rice': 0}
                    shopping_cart[key]['add_once_flag'] = False
                else:
                    shopping_cart[key]['options'] = {
                        "Chicken": 0, 'White Rice': 0}
                    shopping_cart[key]['add_once_flag'] = False
            elif dish.food_name == 'Pot Sticker (6)':
                shopping_cart[key]['options'] = {"Pan Fried": 0}
                shopping_cart[key]['add_once_flag'] = False
            elif dish.food_category == 'Dinner Special':
                if 'Pepper Steak' in dish.food_name:
                    shopping_cart[key]['options'] = {
                        "Beef": 0, 'Fried Rice': 0}
                    shopping_cart[key]['add_once_flag'] = False
                else:
                    shopping_cart[key]['options'] = {
                        "Chicken": 0, 'Fried Rice': 0}
                    shopping_cart[key]['add_once_flag'] = False
            elif 'Wings' in dish.food_name:
                if dish.food_category == 'Appetizer':
                    shopping_cart[key]['options'] = {"Fried": 0, '8pc': 0}
                    shopping_cart[key]['add_once_flag'] = False
                else:
                    shopping_cart[key]['options'] = {"Fried": 0, '6pc': 0}
                    shopping_cart[key]['add_once_flag'] = False
            elif dish.food_category == 'Egg Foo Young':
                shopping_cart[key]['options'] = {'White Rice': 0}
                shopping_cart[key]['add_once_flag'] = False
            elif dish.food_category == 'Japanese Kitchen':
                shopping_cart[key]['options'] = {
                    "Salad": 0, 'Miso Soup': 0, 'White Rice': 0}
                shopping_cart[key]['add_once_flag'] = False
            if dish.food_category == 'Thai Kitchen':
                shopping_cart[key]['options'] = {"Chicken": 0, 'White Rice': 0}
                shopping_cart[key]['add_once_flag'] = False
            elif dish.food_name == 'Wonton Soup' or dish.food_name == 'Egg Drop Soup' or dish.food_name == 'Hot & Sour Soup':
                shopping_cart[key]['options'] = {"Small": 0}
                shopping_cart[key]['add_once_flag'] = False
            elif dish.food_category == 'Chow Mein' or dish.food_category == 'Vegetable' or dish.food_category == 'House Specialty':
                shopping_cart[key]['options'] = {"White Rice": 0}
                shopping_cart[key]['add_once_flag'] = False
            elif dish.food_category == 'Lunch Special':
                if 'Wings' not in dish.food_name:
                    if 'Pepper Steak' in dish.food_name:
                        shopping_cart[key]['options'] = {
                            "Beef": 0, 'Fried Rice': 0}
                        shopping_cart[key]['add_once_flag'] = False
                    else:
                        shopping_cart[key]['options'] = {
                            "Chicken": 0, 'Fried Rice': 0}
                        shopping_cart[key]['add_once_flag'] = False
            elif dish.food_category == 'Lunch Noodle':
                shopping_cart[key]['options'] = {"Fried Rice": 0}
                shopping_cart[key]['add_once_flag'] = False
            elif dish.food_category == 'Drink':
                shopping_cart[key]['options'] = {"Coke": 0}
                shopping_cart[key]['add_once_flag'] = False

            messages.success(request, 'Item added to cart')

        request.session['shopping_cart'] = shopping_cart
        print("request.session['shopping_cart]: ",
              request.session['shopping_cart'])
    return render(request, 'luckydragon_app/menu.html', {'categories': categories})


'''
Function: dish_display
    This function will display a dish with its corresponding information + add on if applicable

    Steps to populate options_dict (a list of options + prices)
        o- Call functions.GetOption(dish) to return a dictionary of options for a specific dish
        o- Iterate through the keys of the dictionary options:
            - Get a list of options that the user has clicked/entered and store it in curKeyVal
            - Iterate through each option in curKeyVal to populate 'options_dict'
'''


def dish_display(request, foodID):
    if request.method == "POST":
        if 'shopping_cart' in request.session:
            shopping_cart = request.session.get('shopping_cart')
        else:
            shopping_cart = {}

        if request.POST.get("add"):
            # Get all important details from the menu
            dish_id = request.POST.get("add")               # Extract dish_id
            # Query a food object based on the dish_id to get the options
            dish = Food.objects.get(food_id=dish_id)
            food_options = functions.GetOptions(dish)       # Get food options
            # Get special instruction that user specified
            special_instruction = request.POST.get("special-instruction")
            quantity = request.POST.get("quantity")         # Get the quantity
            # Stores a list of option(key): price(value) pair
            options_dict = {}

            for opt in food_options.values():
                # Each opt has 1 (key, value) pair
                for key in opt.keys():
                    # Get the current list of options
                    curKeyVal = request.POST.getlist(key)
                    # Loop through each key option to get its add on price
                    for k in curKeyVal:
                        cur_option = options.OPTION_MAP[key]
                        options_dict[k] = cur_option[k]

            # Generate random number for key purposes
            key = randint(0, 1000)
            # Make sure to generate unique number for the key
            while key in shopping_cart:
                key = randint(0, 1000)

            # Default dish
            if not special_instruction and not options_dict:
                shopping_cart[key] = {'food_name': dish.food_name, 'quantity': int(
                    quantity), 'unit_price': dish.food_price}
            # Special instruction is provided, options_dict not provided
            elif special_instruction and not options_dict:
                shopping_cart[key] = {'food_name': dish.food_name, 'quantity': int(quantity),
                                      'unit_price': dish.food_price, 'special_instruction': special_instruction.strip()}
            # Special instruction not provided, options_dict is provided
            # INCLUDE 'add_once_flag' when 'options' is provided to prevent adding multiple times to the total (Refresh bug fixed)
            elif not special_instruction and options_dict:
                shopping_cart[key] = {'food_name': dish.food_name, 'quantity': int(quantity),
                                      'unit_price': dish.food_price, 'options': options_dict, 'add_once_flag': False}
            # Both special instruction and options_dict are provided
            # INCLUDE 'add_once_flag' when 'options' is provided to prevent adding multiple times to the total (Refresh bug fixed)
            else:
                shopping_cart[key] = {'food_name': dish.food_name, 'quantity': int(quantity), 'unit_price': dish.food_price,
                                      'special_instruction': special_instruction.strip(), 'options': options_dict, 'add_once_flag': False}
            shopping_cart[key]['food_id'] = int(foodID)
            shopping_cart[key]['food_image'] = dish.food_image
            messages.success(request, 'Item added to cart')

        request.session['shopping_cart'] = shopping_cart
        print("request.session['shopping_cart]: ",
              request.session['shopping_cart'])
        return redirect('menu')

    # Check food_id boundary before proceeds to the page (find max and min food_id)
    all_items = Food.objects.all()
    lowerBound = all_items.aggregate(Min('food_id'))['food_id__min']
    upperBound = all_items.aggregate(Max('food_id'))['food_id__max']
    if foodID < lowerBound or foodID > upperBound:
        messages.error(request, f'Index out of range')
    else:
        # For extracting food_options in this function
        food_item = Food.objects.get(food_id=foodID)

        # Error accessing lunch item during non-lunch time, redirect to menu with error msg
        if not functions.lunchTime() and food_item.food_category in lunch_categories:
            messages.error(request, f'Item not available at this time')
            return redirect('menu')

        food_options = functions.GetOptions(food_item)

        # Shows radio button instead of checkboxes
        only_one_option = {
            'one_option': ['protein', 'wingcount', 'lunchprotein', 'lunchsoup', 'lunchrice', 'ricecombo', 'comboside', 'rice',
                           'soup', 'wing', 'potsticker', 'fountain', 'soda', 'japaneseside', 'japanesesoup', 'flavordrink',
                           'tapioca', 'dinnerrice', 'nutallergy', 'spicelevel', 'extrameat', 'extraveg', 'pancake']
        }
        return render(request, 'luckydragon_app/dish_display.html', {'dish_display': food_item, 'options_dict': food_options, 'one_option': only_one_option})
    return redirect('menu')


def catering(request):
    return render(request, 'luckydragon_app/catering.html')
