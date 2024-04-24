# TODO
import sys

credit = input("Number: ")
sum1 = []
sum2 = 0
total = 0
if len(credit) > 16:
    print("INVALID")
    sys.exit
elif len(credit) == 16:
    for i in range(1, len(credit), 2):
        sum2 += int(credit[i])

    for i in range(0, len(credit), 2):
        sum1.append(int(credit[i]) * 2)
else:
    for i in range(0, len(credit), 2):
        sum2 += int(credit[i])

    for i in range(1, len(credit), 2):
        sum1.append(int(credit[i]) * 2)

for i in sum1:
    if i >= 10:
        i = (i % 10) + 1
    total += i

total = total + sum2

if total % 10 == 0:
    total = int(str(credit)[:2])
    total2 = int(str(credit)[:1])
    if total2 == 4:
        print("VISA")
        sys.exit
    match total:
        case 34 | 37:
            print("AMEX")
        case 51 | 52 | 53 | 54 | 55:
            print("MASTERCARD")
        case _:
            print("INVALID")

else:
    print("INVALID")