# TODO
import re

# User input
paragraph = input("Text: ").lower()
# Calculating number of words
words = len(paragraph.split())
# print(f"N° words: {words}")
# Calculating number of sentences
sentences = len(re.split(r'[.!?]+', paragraph)) - 1
# print(f"N° sentences: {sentences}")
# Calculating number of letters in paragraph. Only counting alphabet letters, not spaces nor punctuation
letter = sum(1 for l in paragraph if l.isalpha())
# print(f"N° letters: {letter}")
# Calculating average letters per 100 words
avgLet = letter / words * 100
# print(f"avgLet: {avgLet}")
# Calculating average of sentences per 100 words
avgSen = sentences / words * 100
# print(f"N° avgSen: {avgSen}")
# Calculating index
index = round(0.0588 * avgLet - 0.296 * avgSen - 15.8)

if index < 0:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")