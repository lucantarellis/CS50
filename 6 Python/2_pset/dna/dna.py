import csv
from sys import argv


def main():

    # TODO: Check for command-line usage
    if len(argv) != 3:
        print("Please, input the correct number of arguments.")
        exit()

    # TODO: Read database file into a variable
    else:
        with open(argv[1]) as file:
            reader = csv.reader(file)
            database = list(reader)

    # TODO: Read DNA sequence file into a variable
        with open(argv[2]) as txt:
            sequence = txt.read()

    # TODO: Find longest match of each STR in DNA sequence
        match = []
        for i in range(1, len(database[0])):
            match.append(longest_match(sequence, database[0][i]))

    # TODO: Check database for matching profiles
        counter = 0
        for i in range(1, len(database)):
            for j in range(len(match)):
                if match[j] == int(database[i][j + 1]):
                    counter += 1
            if counter == len(match):
                print(f"{database[i][0]}")
                exit()
            else:
                counter = 0
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
