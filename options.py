# Options lists: key = option, value = price


"""
ONLY 1 selection:
"""
# select chicken by default
protein = {'Chicken': 0, 'Pork': 0, 'Vegetable': 0,
           'Tofu': 0, 'Beef': 1, 'Shrimp': 2}

wingcount = {'8pc': 0, '10 pc.': 2, '20 pc.': 11, '50 pc.': 39}

# select chicken by default
lunchprotein = {'Chicken': 0, 'Pork': 0, 'Vegetable': 0,
                'Tofu': 0, 'Beef': 0.3, 'Shrimp': 0.3}

lunchsoup = {'Wonton Soup (Lunch)': 0.59, 'Egg Drop Soup (Lunch)': 0.59,
             'Hot & Sour Soup (Lunch)': 0.59}

lunchrice = {'No Rice': 0, 'White Rice': 0, 'Fried Rice': 0, 'Plain Fried Rice': 0.99, 'Shrimp Fried Rice': 2.59,
             'Chicken Fried Rice': 2.59, 'Pork Fried Rice': 2.59, 'Vegetable Fried Rice': 2.59,
             'Beef Fried Rice': 2.59, 'House Fried Rice': 2.99, 'Lo Mein': 2.29}

ricecombo = {'Shrimp fried rice': 1, 'Chicken fried rice': 0.50, 'Beef fried rice': 1, 'Vegetable fried rice': 0.5,
             'Pork fried rice': 0.5, 'Jumbo shrimp fried rice': 3, 'House fried rice': 1.2, 'Plain fried rice': 0, 'White rice': 0, "French fries": 0}

dinnerrice = {'No Rice': 0, 'White Rice': 0, 'Fried Rice': 0, 'Large White Rice': 1.99, 'Large Fried Rice': 2.99, 'Plain Fried Rice': 0, 'Shrimp Fried Rice': 3.99,
              'Chicken Fried Rice': 3.99, 'Pork Fried Rice': 3.99, 'Vegetable Fried Rice': 3.99,
              'Beef Fried Rice': 3.99, 'House Fried Rice': 4.29, 'Lo Mein': 2.29}

comboside = {'No side': 0, 'No egg roll': 0, 'No wonton': 0, 'Change spring roll': 0,
             '2 wonton': 0, '2 egg rolls': 0.69, '2 spring rolls': 0.69}

rice = {'No Rice': 0, 'White Rice': 0, 'Fried Rice': 0.99, 'Large White Rice': 1.99, 'Large Fried Rice': 2.99, 'Plain Fried Rice': 0.99, 'Shrimp Fried Rice': 3.99,
        'Chicken Fried Rice': 3.99, 'Pork Fried Rice': 3.99, 'Vegetable Fried Rice': 3.99,
        'Beef Fried Rice': 3.99, 'House Fried Rice': 4.29, 'Lo Mein': 2.29}

soup = {'Small (Pint)': 0, 'Large (Quart)': 1.7}

wing = {'Fried': 0, 'Buffalo': 0, 'Lemon Pepper': 0,
        'BBQ': 0, 'Hot Braised': 0, 'Honey': 0, 'Teriyaki': 0}

potsticker = {'Pan Fried': 0, 'Steamed': 0, 'Fried': 0}

fountain = {'Coke': 0, 'Diet Coke': 0, 'Sprite': 0,
            'Orange Fanta': 0, 'Dr. Pepper': 0, 'Lemonade': 0, 'Sweat Tea': 0}

soda = {'Coke': 0, 'Sprite': 0}

japaneseside = {'Egg roll': 0, 'Spring roll': 0, 'Salad': 0, 'No side': 0}

japanesesoup = {'Egg drop soup': 0, 'Wonton soup': 0,
                'Hot & sour soup': 0, 'Miso soup': 0, 'No soup': 0}

flavordrink = {'Peach': 0, 'Passion Fruit': 0, 'Strawberry': 0,
               'Pineapple': 0, 'Mango': 0, 'Green Apple': 0, 'Coconut': 0, 'Taro': 0}

tapioca = {'Tapioca': 0.59}

nutallergy = {'No nuts': 0}

spicelevel = {'No spicy': 0, 'Extra Spicy': 0}

extrameat = {'Extra $2 Protein': 2,
             'Extra $3 Protein': 3, 'Extra $4 Protein': 4}

extraveg = {"Extra $1 Veg": 1, 'Extra $2 Veg': 2,
            'Extra $3 Veg': 3, 'Extra $4 Veg': 4}

pancake = {'Extra 4 pancakes': 1, 'Extra 8 pancakes': 2}

""" 
Multi-selections:
"""

veg = {'No mixed vegetable': 0,
       'Add mixed vegetable': 2, 'Add broccoli': 1, 'Add baby corn': 1, 'Add waterchestnuts': 1,
       'Add onion': 0, 'Add bell pepper': 1, 'Add snowpeas': 1, 'Add carrots': 0,
       'Add mushroom': 1, "Add jalapeno": 1, 'Add beansprout': 1,
       'Add green onion': 0}

ricenoodleveg = {'No vegetable': 0, 'No onion': 0,
                 'Add egg': 0.89}

wingopt = {'All drums': 2, 'All flats': 2, 'Extra 2 Wing': 2.40, 'Extra 4 Wing': 4.80,
           'Extra Crispy': 0}

meatopt = {'Add $2 chicken': 2, 'Add $3 chicken': 3,
           'Add $2 pork': 2, 'Add $3 pork': 3,
           'Add $2 shrimp': 2, 'Add $3 shrimp': 3,
           'Add $2 beef': 2, 'Add $3 beef': 3,
           'Add 2pc. jumbo shrimp': 1.5, 'Add 4pc. jumbo shrimp': 3, 'Add 6pc. jumbo shrimp': 4.5,
           'Add $2 vegetable': 2, 'Add $1 tofu': 1, 'Add $2 tofu': 2}

soupchip = {'1 Small bag': 0.59, '2 Small bags': 1.18,
            '1 Large bag': 0.89, '2 Large bags': 1.78}

# Mapping of string to var
OPTION_MAP = {'protein': protein, 'veg': veg, 'ricenoodleveg': ricenoodleveg, 'wingopt': wingopt,
              'lunchprotein': lunchprotein, 'lunchsoup': lunchsoup, 'lunchrice': lunchrice,
              'meatopt': meatopt, 'ricecombo': ricecombo, 'spicelevel': spicelevel,
              'comboside': comboside, 'rice': rice, 'soup': soup, 'wing': wing, 'potsticker': potsticker,
              'fountain': fountain, 'soda': soda, 'japaneseside': japaneseside,
              'japanesesoup': japanesesoup, 'flavordrink': flavordrink, 'wingcount': wingcount,
              'soupchip': soupchip, 'tapioca': tapioca, 'nutallergy': nutallergy, 'dinnerrice': dinnerrice,
              'extrameat': extrameat, 'pancake': pancake, 'extraveg': extraveg}

OPTION_STRING = {'protein': 'Choice of Protein', 'veg': 'Vegetable Option', 'ricenoodleveg': 'Vegetable Option', 'wingopt': 'Wing Option',
                 'lunchprotein': 'Choice of Protein', 'lunchsoup': 'Lunch Soup', 'lunchrice': 'Choice of Rice',
                 'meatopt': 'Meat Option', 'ricecombo': 'Choice of Rice', 'spicelevel': 'Spice Level',
                 'comboside': 'Choice of Side', 'rice': 'Choice of Rice', 'soup': 'Size', 'wing': 'Wing Flavor', 'potsticker': '',
                 'fountain': 'Choices', 'soda': 'Choices', 'japaneseside': 'Choice of Side',
                 'japanesesoup': 'Choice of Soup', 'flavordrink': 'Flavors', 'wingcount': 'Wing Count',
                 'soupchip': 'Extra Crispy Noodles', 'tapioca': 'Add-ons', 'nutallergy': 'Nut Allergy',
                 'dinnerrice': 'Choice of Rice', 'extrameat': 'Meat Option', 'pancake': 'Pancake Option', 'extraveg': 'Vegetable Option'}
