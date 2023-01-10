#Sanuli

A finnish version of the popular Wordle-game, built with Python pygame. My first game project.


Installation

Install pygame from: https://www.pygame.org/wiki/GettingStarted

Gameplay

The goal of the game is to guess the hidden 5-letter word. The game will show one of three different colours for each letter:

    Grey means the letter doesn't appear in the word.
    Yellow means the letter appears in the word, but is in the wrong slot.
    Green means the letter appears and is in the right slot.

You can access a list of good guesses by pressing the § key. The initial set of suggestions is stored in memory, as the process of finding ideal words takes CPU time and the suggestions are the same on the first try anyway. After the first guess, an algorithm finds the best candidates for the next guess, which are all possible correct guesses. The algorithm almost always finds an answer, but it is possible to fail even while using it. 

The x key may be used to reset the game with the same word as the hidden word. This is useful for testing and finding bugs. Also a fun fact, there are no five letter words in finnish that have the letter x.

The basic idea of the hint algorithm is to check every possible remaining guess against every other, so that the first hint on average reduces the number of remaining words the most. So if there are 300 possible guesses remaining, the algorithm assumes for each guess that it is correct and then checks how much each word reduces the size of the guess list. These values are then added together and the one with the lowest value is the first recommendation.

Known issues

There were some issues with the .csv and .txt files and the finnish letters such as ä and ö, so the code might need to fix the csv file to work properly. I does this automatically, so no worries there.

A lof of the code is in Finnish and there aren't a lot of comments. I would fix these issues if the game had a future. For now, it is just a portfolio entry.




https://user-images.githubusercontent.com/115335825/210356482-b180eadc-5781-4779-a5eb-b60b1bc9c90a.mp4

