from pyfiglet import Figlet
import sys
import random

randomFont = False

if len(sys.argv) == 1:
    randomFont = True
elif len(sys.argv) == 3:
    randomFont = False
else:
    sys.exit("None or one command-line argument expected.")

figlet = Figlet()

if randomFont == False:
    if sys.argv[1] not in ['-f', '--font']:
        sys.exit("Command-line argument not correct.")
    try:
        selFont = figlet.setFont(font = sys.argv[2])
    except:
        sys.exit("Font does not exist.")

else:
    figlet.setFont(font = random.choice(figlet.getFonts()))

text = input("Input: ")
print(figlet.renderText(text))