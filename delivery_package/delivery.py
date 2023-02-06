from django.contrib import messages
import requests
import json
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

# API key
api_file = open(os.path.join(BASE, 'api_file.txt'), 'r')
API_KEY = api_file.read()
api_file.close()

# Uses Google Maps Distance API to retrieve the correct distance from the restaurant to delivery address


def delivery_distance(street_number, street_name, city, zipcode):

    # formats address correctly for url
    delivery_address = f'{street_number}+{street_name}+{city}+{zipcode}'

    # base url with the restaurant address included
    restaurant_address = 'https://maps.googleapis.com/maps/api/directions/json?origin=3750+Austell+Rd+SW+Marietta,+GA+30008'

    # gets the HTTPS request
    r = requests.get(restaurant_address + '&destination=' +
                     delivery_address + '&key=' + API_KEY)

    # turns the request into a JSON file
    j = r.json()

    # retrieves the distance in miles from the json file and splits the number and the unit into a list
    json_list = j["routes"][0]["legs"][0]["distance"]["text"].split()

    # gets the numbers of miles from the list and converts into a float
    distance = float(json_list[0])

    return distance

# Retrieves the delivery time from restaurant to delivery address


def delivery_time(street_number, street_name, city, zipcode):

    # formats address correctly for url
    delivery_address = f'{street_number}+{street_name}+{city}+{zipcode}'

    # base url with the restaurant address included
    restaurant_address = 'https://maps.googleapis.com/maps/api/directions/json?origin=3750+Austell+Rd+SW+Marietta,+GA+30008'

    # gets the HTTPS request
    r = requests.get(restaurant_address + '&destination=' +
                     delivery_address + '&key=' + API_KEY)

    # turns the request into a JSON file
    j = r.json()

    # retrieves the distance time as a string and the number of seconds as a int
    time = j["routes"][0]["legs"][0]["duration"]["text"]
    seconds = int(j["routes"][0]["legs"][0]["duration"]["value"])

    return time


# if all requirements for delivery is fulfilled, returns total order price + delivery fee
# else function is exited
def delivery_total(request, distance, total):
    if distance > 6:
        # needs a message to say distance is too far for delivery
        messages.error(request, f'address is too far for delivery')
        return
    elif distance < 5 and total < 20:
        # needs a message to say order total is too low for delivery
        messages.error(request, f'total is too low for delivery')
        return
    elif distance >= 5 and distance <= 6 and total < 35:
        # needs a message to say order total is too low for delivery
        messages.error(request, f'total is too low for delivery')
        return
    else:
        return delivery_fee(distance)

# Return delivery fee based on distance


def delivery_fee(distance):
    if distance < 5:
        return + 3
    elif distance >= 5 and distance <= 6:
        return + 5
