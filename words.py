def return_wordlist():
    word_list = []
    with open("sanat.txt") as tiedosto:
         for i in tiedosto:
            i=i.strip(";")
            i=i.strip("\n")
            i=i.replace("Ã¤","ä")
            i=i.replace("Ã¶","ö")
            word_list.append(i)
    return word_list

def solve_most_common_letters():
    all_words = return_wordlist()
    letter_freq_dict = {}
    for word in all_words:
        for letter in word:
            if letter not in letter_freq_dict:
                letter_freq_dict[letter] = 1
            else:
                letter_freq_dict[letter] += 1
    letters_with_score = sorted([(key, value) for key, value in letter_freq_dict.items()], key= lambda x:x[1], reverse=True)
    return [letter for letter, score in letters_with_score]
