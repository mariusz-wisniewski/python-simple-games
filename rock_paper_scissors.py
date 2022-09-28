import random
from enum import Enum

import pytest as pytest

MAKE_CHOICE_MESSAGE = """Let's start!
            
Please select action:'
    - ROCK
    - PAPER
    - SCISSORS"""

STARTUP_MESSAGE = """Hello to the "Rock paper scissors" game!

You will have opportunity to play with the computer.
Each of you have 5 lives.

Will you be able to win? Good luck!

Let's start with selection of the amount of lives each player shall have.
Please enter the number between 1 and 10.

Each time someone is losing the amount of lives decrease. Draw will not change amount of lives.
User won't receive additional live for winning."""


def main():
    print(STARTUP_MESSAGE)
    user_wants_to_play = True
    player_name = input("Please enter your name: ")
    while user_wants_to_play:
        number_of_lives = ask_number_of_lives()
        computer = Player("Computer", number_of_lives)
        player = Player(player_name, number_of_lives)
        game = Game(computer, player)
        game.play_game()
        user_wants_to_play = ask_wants_to_continue()


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Player:
    def __init__(self, name, no_of_lives):
        self.name = name
        self._no_of_lives = no_of_lives

    @property
    def no_of_lives(self) -> int:
        return self._no_of_lives

    @no_of_lives.setter
    def no_of_lives(self, no_of_lives: int):
        self._no_of_lives = no_of_lives

    @property
    def is_alive(self) -> bool:
        return self._no_of_lives > 0

    def deduct_one_live(self):
        self._no_of_lives -= 1
        if self.is_alive:
            print(f"{self.name} lost this part.")


def ask_wants_to_continue() -> bool:
    decision = input("Do you want to play one more time? Please enter 'YES' to continue")
    return decision.upper() == 'YES'


def ask_number_of_lives() -> int:
    no_of_lives = 0
    while not 0 < no_of_lives < 11:
        try:
            no_of_lives = int(input('Please enter amount of lives between 1 and 10: '))
        except ValueError:
            print("Ups! It seems that you did not enter the number. Please try again")
    return no_of_lives


class Game:
    def __init__(self, computer: Player, player: Player):
        self.computer = computer
        self.player = player

    def _determine_looser(self, player_action: Hand, computer_action: Hand):
        if player_action == computer_action:
            print('Draw!')
            return None
        elif (
            (player_action == Hand.ROCK and computer_action == Hand.SCISSORS)
            or (player_action == Hand.SCISSORS and computer_action == Hand.PAPER)
            or (player_action == Hand.PAPER and computer_action == Hand.ROCK)
        ):
            return self.computer
        return self.player

    def print_final_result(self):
        if self.player.is_alive:
            print(f"Congratulation {self.player.name}! You won with {self.player.no_of_lives} live(s) remaining.")
        else:
            print(f"Unfortunately. {self.computer.name} won with {self.computer.no_of_lives} live(s) remaining.")

    def play_round(self):
        action = input().upper()
        if action not in Hand.__members__.keys():
            print('Unknown action')
            return
        computer_action = random.choice(list(Hand))
        print(f"{self.computer.name} chose {computer_action.name}")
        looser = self._determine_looser(Hand[action], computer_action)
        if looser:
            looser.deduct_one_live()

    def play_game(self):
        print(MAKE_CHOICE_MESSAGE)
        while self.computer.is_alive and self.player.is_alive:
            self.play_round()
        self.print_final_result()


if __name__ == '__main__':

    main()


@pytest.mark.parametrize(
    "player_hand, computer_hand, correct_looser",
    [
        # draw
        [Hand.ROCK, Hand.ROCK, None],
        # computer looses
        [Hand.PAPER, Hand.ROCK, "computer"],
        [Hand.ROCK, Hand.SCISSORS, "computer"],
        [Hand.SCISSORS, Hand.PAPER, "computer"],
        # player looses
        [Hand.ROCK, Hand.PAPER, "player"],
        [Hand.PAPER, Hand.SCISSORS, "player"],
        [Hand.SCISSORS, Hand.ROCK, "player"],
    ],
)
def test_check_result(player_hand, computer_hand, correct_looser):
    computer = Player("computer", 1)
    player = Player("player", 1)
    g = Game(computer, player)
    looser = g._determine_looser(player_hand, computer_hand)
    if looser:
        assert looser.name == correct_looser
    else:
        assert looser == correct_looser
