# Automated Wordle Solver

This project is an automated solver for the Wordle-like puzzle game. The program interacts with the Wordle API, guesses words, and visualizes each guess using color feedback based on Wordle's rules (green for correct letters, yellow for present letters, and gray for absent letters). The wordle_api_interaction_word.py file is used by users to input words for others to guess.

## Features

- Connects to the Wordle API to get feedback for each guess.
- Automatically guesses words based on previous feedback.
- Visualizes the guesses and their feedback in a graphical interface.
- Uses a dictionary of common five-letter words to make guesses.

## Requirements

To run the project, you need the following:

- Python 3
- `nltk` library
- `requests` library
- `matplotlib` library

You can install these dependencies using the provided `requirements.txt` file.

## Installation

Follow the steps below to set up the project and install the required libraries:

1. Clone the repository or download the project files to your local machine.
   
   If you are using Git, you can clone the repository:
   ```bash
   git clone https://github.com/NTUJackie/wordle_api_interaction
