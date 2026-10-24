#!/usr/bin/env python3
"""Hangman - a console word guessing game.

Run:  python hangman.py

Optional: place an English word list named 'words.txt' (one word per line)
next to this file. If it's missing, a built-in word list is used.
"""

import os
import random

MAX_MISTAKES = 6
MIN_WORD_LENGTH = 4

FALLBACK_WORDS = [
    "python", "variable", "function", "keyboard", "algorithm", "compiler",
    "debugging", "terminal", "software", "developer", "iteration", "database",
    "network", "program", "elephant", "mountain", "chocolate", "adventure",
    "library", "universe", "calendar", "umbrella", "notebook", "triangle",
]

# One ASCII stage per number of mistakes (0-6)
STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """,
]


def load_words():
    """Load words from words.txt if available, else use the built-in list."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")
    try:
        with open(path, encoding="utf-8") as f:
            words = [w.strip().lower() for w in f
                     if w.strip().isalpha() and len(w.strip()) >= MIN_WORD_LENGTH]
        if words:
            return words
    except OSError:
        pass
    return FALLBACK_WORDS


def mask_word(word, guessed):
    """Return the word with unguessed letters shown as underscores."""
    return " ".join(ch if ch in guessed else "_" for ch in word)


def get_guess(guessed):
    """Prompt until the player enters a single new letter."""
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("  Please enter a single letter (a-z).")
        elif guess in guessed:
            print(f"  You already guessed '{guess}'. Try another letter.")
        else:
            return guess


def display(word, guessed, mistakes):
    wrong = sorted(g for g in guessed if g not in word)
    print(STAGES[mistakes])
    print(f"  Word:   {mask_word(word, guessed)}")
    print(f"  Wrong:  {' '.join(wrong) if wrong else '-'}")
    print(f"  Lives:  {MAX_MISTAKES - mistakes} / {MAX_MISTAKES}\n")


def show_victory(word, mistakes):
    print("\n" + "=" * 40)
    print("  *** VICTORY! You saved him! ***")
    print(f"  The word was: {word.upper()}")
    print(f"  Mistakes made: {mistakes}")
    print("=" * 40)


def show_defeat(word):
    print(STAGES[MAX_MISTAKES])
    print("=" * 40)
    print("  xxx GAME OVER - you've been hanged! xxx")
    print(f"  The word was: {word.upper()}")
    print("=" * 40)


def play_round(words):
    word = random.choice(words)
    letters = set(word)
    guessed = set()
    mistakes = 0

    print("\nI'm thinking of a word with", len(word), "letters.")

    while mistakes < MAX_MISTAKES and not letters <= guessed:
        display(word, guessed, mistakes)
        guess = get_guess(guessed)
        guessed.add(guess)

        if guess in word:
            print(f"\n  Good! '{guess}' is in the word.")
        else:
            mistakes += 1  # only new wrong guesses reach here, so no duplicate penalty
            print(f"\n  Sorry, '{guess}' is not in the word.")

    if letters <= guessed:
        display(word, guessed, mistakes)
        show_victory(word, mistakes)
    else:
        show_defeat(word)


def main():
    words = load_words()
    print("=" * 40)
    print("          H A N G M A N")
    print("=" * 40)

    while True:
        play_round(words)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")
