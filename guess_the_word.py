import random
import requests


WORD_SITE = "https://www.mit.edu/~ecprice/wordlist.10000"


WELCOME_MESSAGE = """Hello to the 'Guess the word' game!
System will select one of the 10000 word and your job will to be guess it!
You will have 12 chances. 
You are not allowed to enter the same character twice."""


def get_new_word():
    response = requests.get(WORD_SITE)
    words = response.content.splitlines()
    return random.choice(words).decode()


def print_with_separator(iterable, separator = ' '):
    print(separator.join(iterable))


def find_char_positions(char, word):
    return [index for index in range(len(word)) if char == word[index]]


def get_new_letter():
    while True:
        letter = input('Type letter: ')
        if len(letter) == 1 and letter.isalpha():
            return letter
        else:
            print("It seems that you did not correct letter. Please enter single, non-numeric character")


def main():
    print(WELCOME_MESSAGE)

    while True:
        word_to_quess = get_new_word()
        word_length = len(word_to_quess)
        guessed = ['*' for i in range(word_length)]
        print(f"Your word has {word_length} letter! Let's start.")
        print_with_separator(guessed)

        used_letters = set()
        remaining_tries = 12

        while remaining_tries > 0:
            letter = get_new_letter()
            if letter in used_letters:
                print("Sorry. You've already used that letter.")
            else:
                used_letters.add(letter)
                if letter in word_to_quess:
                    for i in find_char_positions(letter, word_to_quess):
                        guessed[i] = letter
                    print_with_separator(guessed)
                    if "*" not in guessed:
                        break
                else:
                    remaining_tries -= 1
                    print(f'Sorry. That letter is not part of the word.')
                    if remaining_tries > 0:
                        print(f"Remaining number of tries: {remaining_tries}")

        if remaining_tries > 0:
            print("Congratulation, you've guessed the word!")
        else:
            print(f"Unfortunately. You did not guess the word. We've been looking for word: {word_to_quess}")
        decision = input("Do you want you continue? Please type 'YES' to play one more time").upper()
        if decision != "YES":
            break


if __name__ == '__main__':

    main()
