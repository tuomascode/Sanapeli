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
