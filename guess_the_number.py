import math
import random


def ask_for_range():
    print("Please enter lower bound")
    lower_bound = get_the_number()
    print("Please enter upper bound")
    while True:
        upper_bound = get_the_number()
        if upper_bound > lower_bound:
            break
        print('It seems that lower bound is greater or equal to upper bound. Please try again.')
    return lower_bound, upper_bound


def get_the_number():
    while True:
        try:
            number = int(input())
            break
        except ValueError:
            print('Please enter valid integer number.')
    return number


def main():
    lower_bound, upper_bound = ask_for_range()
    print(f"Awesome! Let's play. You've chose range between {lower_bound} and {upper_bound}")

    number_of_tries = int(math.log(upper_bound - lower_bound, 2))
    print(f"You have {number_of_tries} attempt. Good luck!")
    searched_number = random.randint(lower_bound, upper_bound)

    while number_of_tries > 0:
        print("Please type number:")
        guessed_number = get_the_number()
        if guessed_number == searched_number:
            print("Congratulation, you found the number!")
            break
        number_of_tries -= 1
        if number_of_tries == 0:
            print(f"Sorry, you did not guess the number. Seached number was: {searched_number}")
        elif guessed_number < searched_number:
            print(f"Not this time. Searched number is greater. You have {number_of_tries} attempt left.")
        else:
            print(f"Not this time. Searched number is lower. You have {number_of_tries} attempt left.")


if __name__ == '__main__':
    main()
