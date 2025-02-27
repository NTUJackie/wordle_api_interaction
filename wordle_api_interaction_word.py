import requests
import random
import nltk
import matplotlib.pyplot as plt
import numpy as np

# nltk.download('words')
from nltk.corpus import words

url_api = "https://wordle.votee.dev:8000"

# Get words with 5 letters from the dictionary
dict_words = [word for word in words.words() if len(word) == 5]

def guess_word(guess: str, word):
    # Send a request to the API and get feedback
    url = f"{url_api}/word/{word}"
    params = {"guess": guess}
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed: {response.status_code}")
        return None


# Generate the next legal word based on the feedback
def select_word_for_guess(feedback):
    absent = set()  # "absent"
    present = {}  # "present"
    correct = {}  # "correct"

    for i, item in enumerate(feedback):
        result = item["result"]
        letter = item["guess"]
        if result == "absent":
            # Letters cannot appear in new guesses
            absent.add(letter)
        elif result == "present":
            # Record the letters that need to be in the word but are not in the current position
            present[i] = letter
        elif result == "correct":
            # Record the correct letter.
            correct[i] = letter

    # Randomly select a word from dict_words and check if it matches the feedback
    while True:
        guess = random.choice(dict_words)

        match = True

        # Check that the "correct" letter is in the correct position
        for i, letter in correct.items():
            if guess[i] != letter:
                match = False
                break

        # Check if the "present" letters are in the correct position
        if match:
            for i, letter in present.items():
                if guess[i] == letter or letter not in guess:  # The present letter cannot be in the original position and must exist
                    match = False
                    break

        # Check if the letter "absent" appears in the word
        if match:
            for letter in absent:
                if letter in guess:
                    match = False
                    break

        # If the word matches the feedback, return it
        if match:
            return guess


def visualize_feedback(feedback, guess, attempts):
    # Create a plot to visualize the Wordle feedback
    colors = {'correct': 'green', 'present': 'yellow', 'absent': 'gray'}

    plt.clf()

    # Create a new graph to display feedback
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Create a list of feedback results
    for i, item in enumerate(feedback):
        result = item["result"]
        letter = item["guess"]
        color = colors[result]

        # Display each letter in the appropriate color
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
        ax.text(i + 0.5, 0.5, letter.upper(), ha='center', va='center', fontsize=20, color='black')

    # Show the guess and feedback visualization
    ax.set_title(f"Attempt {attempts + 1}: Guess: {guess.upper()}")
    plt.draw()
    plt.pause(1)


def main():
    # Initial guess. The word can be selected by yourself or replaced by system input.
    guess = random.choice(dict_words)  # Randomly select an initial word from the dictionary
    attempts = 0
    correct_word = False
    feedback = None
    word = input()
    plt.ion()  # Turn on interactive mode to dynamically update the plot

    while attempts < 6 and not correct_word:
        print(f"\nAttempt {attempts + 1}: Guessing word - {guess}")

        # Get the feedback
        feedback = guess_word(guess, word)

        if feedback:
            print("Feedback:", feedback)
            correct_word = all(item['result'] == 'correct' for item in feedback)

            # Visualize the feedback with colors
            visualize_feedback(feedback, guess, attempts)

            # If all letters are guessed correctly, exit
            if correct_word:
                print(f"\nCongratulations, you guessed the word correctly: {guess}!")
                break

            # Generate the next legal word based on the feedback
            guess = select_word_for_guess(feedback)

        attempts += 1

    plt.ioff()  # Turn off interactive mode when done


if __name__ == "__main__":
    main()
