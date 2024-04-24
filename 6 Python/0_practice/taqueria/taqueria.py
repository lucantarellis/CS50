import sys

menu = {
    'Baja Taco': 4.00,
    'Burrito': 7.50,
    'Bowl': 8.50,
    'Nachos': 11.00,
    'Quesadilla': 8.50,
    'Super Burrito': 8.50,
    'Super Quesadilla': 9.50,
    'Taco': 3.00,
    'Tortilla Salad': 8.00
    }

sumOrder = 0

while True:
    try:
        order = str.title(input(f'${sumOrder:.2f}: '))
        if order not in menu:
            print('Item not in menu')
        else:
            sumOrder += menu[order]
    except EOFError:
        break

print('')
print(f'Total: ${sumOrder:.2f}')