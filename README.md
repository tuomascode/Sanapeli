# sanuli
A finnish version of the popular Wordle-game.

#What?

Game build with Python pygame. Install pygame from: https://www.pygame.org/wiki/GettingStarted

The game has two key featurues.

First is the game itself. The goal is to guess the hidden 5-letter word. The game will show one of three different colours for each letter. Grey means the letter doesn't appear in the word. Yellow means the letter appears in the word, but is in the wrong slot. Green means the letter appears and is in the right slot.

The second feature may be accessed with the § key. The game will expand and show you a list of good guesses. The inital set of suggestions is stored in memory, as the process of finding ideal words takes cpu time and the suggestions are the same on the first try anyway. I precomputed this in the process of building the game. 

After the first guess, an algorithm finds the best candidates for the next guess, which are all possible words. The upside of the algorithm is that every guess reduces ideally the remaining possible guesses while being a candidate answer. The downside is that the algorithm doesn't consider any words which aren't in the candidate list, which could however reduces the list of possible words even further. Thus, it is possible to fail even while using the algorithm. Consider for example the following suggestion list and two remaining guesses.

Karja
Sarja
Harja

If the correct answer is Harja, guessing the first two ones will fail in winning the game. A smarter algorithm would first use a guess to deduce which letter K, S or H is in the word, and guess the last one correctly. However, the algorithm almost always does find an answer.

#Why?

The motivation for this project came from interest in building a slightly more complex game. I also found the idea of implementing the search algorithm very appealing. Altho the algorithm could be improved even further, I am currently satisfied with it. Improvements could be made using a faster language, f.e. c++ and expanding the scope of the search.




