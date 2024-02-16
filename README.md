#Sanuli

A finnish version of the popular Wordle-game, built with Python pygame. My first game project.


Installation

Install pygame from: https://www.pygame.org/wiki/GettingStarted

Gameplay

The goal of the game is to guess the hidden 5-letter word. The game will show one of three different colours for each letter:

    Grey means the letter doesn't appear in the word.
    Yellow means the letter appears in the word, but is in the wrong slot.
    Green means the letter appears and is in the right slot.

You can access a list of good guesses by pressing the § key. The initial set of suggestions is stored in memory, as the process of finding ideal words takes CPU time and the suggestions are the same on the first try anyway. After the first guess, an algorithm finds the best candidates for the next guess. The algorithm always finds an answer. 

The x key may be used to reset the game with the same word as the hidden word. This is useful for testing and finding bugs. Also a fun fact, there are no five letter words in finnish that have the letter x.

## Changes 16.2.2024
* Refactored everything. Before all the code was in one file. Now refactored code is divided by responsility.
* New unittests allow for safe developing. These provide quite good coverage and should aid in future development.
* Improved efficiency and speed of the solve_clues algorithm.
* Improved code readability and reuse options


https://user-images.githubusercontent.com/115335825/210356482-b180eadc-5781-4779-a5eb-b60b1bc9c90a.mp4

