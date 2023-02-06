from pytz import timezone
from datetime import datetime, time
from . import options


def GetOptions(food):
    # Dictionary to store each option for a specific food - There are 5 options total
    # Key: pretty-print of food option based on category obtained by extracting food_op1 -> food_op5
    # Value: dict of option-map as key and list of options extracted by passing the food key to OPTION_MAP in options.py
    food_options = {}
    if food.food_op1 != None:
        food_options[options.OPTION_STRING[food.food_op1]] = {
            food.food_op1: options.OPTION_MAP[food.food_op1]}
    if food.food_op2 != None:
        food_options[options.OPTION_STRING[food.food_op2]] = {
            food.food_op2: options.OPTION_MAP[food.food_op2]}
    if food.food_op3 != None:
        food_options[options.OPTION_STRING[food.food_op3]] = {
            food.food_op3: options.OPTION_MAP[food.food_op3]}
    if food.food_op4 != None:
        food_options[options.OPTION_STRING[food.food_op4]] = {
            food.food_op4: options.OPTION_MAP[food.food_op4]}
    if food.food_op5 != None:
        food_options[options.OPTION_STRING[food.food_op5]] = {
            food.food_op5: options.OPTION_MAP[food.food_op5]}

    return food_options


operationHours = {
    0: (time(11, 0), time(21, 30)),        # Monday (open, close)
    1: None,                               # Tuesday CLOSE
    2: (time(11, 0), time(21, 30)),        # Wednesday (open, close)
    3: (time(11, 0), time(21, 30)),        # Thursday (open, close)
    4: (time(11, 0), time(22, 0)),         # Friday (open, close)
    5: (time(12, 0), time(22, 0)),         # Saturday (open, close)
    6: (time(12, 0), time(21, 30))         # Sunday (open, close)
}

lunch_stop_time = time(15, 30)


# Default timezone of business for time comparison
tz = timezone('US/Eastern')


def compareTime(targetTime, sourceTime):
    if targetTime.hour == sourceTime.hour:
        if targetTime.minute == sourceTime.minute:
            return 0
        elif targetTime.minute > sourceTime.minute:
            return 1
        else:
            return -1
    elif targetTime.hour > sourceTime.hour:
        return 1
    return -1


def inTimeInterval(target, interval):
    startTimeCmp = compareTime(target, interval[0])
    if startTimeCmp == 0:
        return True
    if startTimeCmp == 1:
        endTimeCmp = compareTime(target, interval[1])
        if endTimeCmp == 0 or endTimeCmp == -1:
            return True
    return False


def lunchTime():
    res = compareTime(datetime.now(tz).time(), lunch_stop_time)
    if res == 0 or res == -1:
        return True
    return False


def restaurantOpen():
    timeNow = datetime.now(tz).time()
    day = timeNow.weekday()
    return inTimeInterval(timeNow, operationHours[day])
