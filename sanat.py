def palauta_sanat(testisana,oikeasana,sanalista):
    vihreat_kirjaimet=[]
    uudetsanat=[]
    vaarat=[]
    vihreat=False
    keltaiset=False
    vk=False
    for i in range(len(oikeasana)):
        if oikeasana[i]==testisana[i]:
            vihreat_kirjaimet.append(oikeasana[i])
            vihreat=True
        else:
            vihreat_kirjaimet.append("")
    kelt_kirjaimet=[]

    for i in testisana:                                         #Otetaan talteen 'keltaiset' kirjaimet
        if i in oikeasana and i not in vihreat_kirjaimet:
            keltaiset=True
            kelt_kirjaimet.append(i)
        else:
            kelt_kirjaimet.append("")
    for i in testisana:
        if i not in oikeasana:
            vaarat.append(i)

    vkohdat=[]
    for i in range(5):
        if testisana[i]!=oikeasana[i]:
            vkohdat.append(testisana[i])
            vk=True
        else: vkohdat.append("")

    if len(vaarat)!=0:
        for i in sanalista:
            tarkistus=False
            for j in vaarat:
                if j in i:
                    tarkistus=True
                    break
            if not tarkistus:
                uudetsanat.append(i)
    else: uudetsanat=sanalista
    sanat=[]
    tarkistus=False
    if keltaiset:
        for i in uudetsanat:
            tarkistus=False
            for j in kelt_kirjaimet:
                if j not in i:
                    tarkistus=True
            if not tarkistus:
                sanat.append(i)
    else: sanat=uudetsanat
    sanat2=[]
    if keltaiset or vk:
        for i in sanat:
            tarkistus=False
            for j in range(len(i)):
                if kelt_kirjaimet[j]==i[j]:
                    tarkistus=True
                if vkohdat[j]==i[j] and vkohdat[j]!="":
                    tarkistus=True
            if not tarkistus:
                sanat2.append(i)
    else: sanat2=sanat

    sanat=sanat2
    toisetsanat=[]

    if vihreat:
        for i in sanat:
            tarkistus=False
            for j in range(5):
                if vihreat_kirjaimet[j]!="" and vihreat_kirjaimet[j]!=i[j]:
                    tarkistus=True
            if not tarkistus:
                toisetsanat.append(i)
    else:
        toisetsanat=sanat


    return toisetsanat


def korjaa_csv():
    lista=[]
    with open("sanat.txt") as tiedosto:
         for i in tiedosto:
            i=i.strip(";")
            i=i.strip("\n")
            i=i.replace("Ã¤","ä")
            i=i.replace("Ã¶","ö")
            lista.append(i)
    with open("vitoset.csv","w") as tiedosto:
        for i in lista:
            tiedosto.write(i+"\n")

def return_wordlist():
    lista=[]
    with open("sanat.txt") as tiedosto:
         for i in tiedosto:
            i=i.strip(";")
            i=i.strip("\n")
            i=i.replace("Ã¤","ä")
            i=i.replace("Ã¶","ö")
            lista.append(i)
    return lista

def palauta_tulos(oikeasana,testisana,sanalista):

    sanoja=len(sanalista)
    vaarat=[]
    vihreat=[]
    keltaiset=[]
    toisetvaarat=[]
    for i in testisana:
        if i in oikeasana:
            keltaiset.append(i)
    for i in range(5):
        if testisana[i]!=oikeasana[i]:
            vaarat.append(testisana[i])
            vihreat.append("")
        else:
            vihreat.append(testisana[i])
            vaarat.append("")
    for i in testisana:
        if i not in oikeasana:
            toisetvaarat.append(i)
    for sana in sanalista:
        miinus=False
        for kirjain in toisetvaarat:  #Tässä testataan onko tarkastettavassa sanassa vääriä kirjaimia. Jos on, niin miinustetaan ja jatketaan seuraavasta sanasta
            if kirjain in sana:
                sanoja-=1
                miinus=True
                break
        if miinus: continue

        for indeksi in range(5):    #Testaan sopiiko vihreät kirjaimet testattavan sanan kanssa. Jos ei, niin miinustetaan ja jatketaan.
            if sana[indeksi]!=vihreat[indeksi] and vihreat[indeksi]!="":
                sanoja-=1
                miinus=True
                break
        if miinus: continue

        for indeksi in range(5):            #Tämä ajaa keltaisten väärän paikan testaamisen
            if sana[indeksi]==vaarat[indeksi]:
                sanoja-=1
                miinus=True
                break
        if miinus: continue

        for kirjain in keltaiset:           #Tarkistetaan vielä, että sanasta löytyy kaikki keltaiset kirjaimet
            if kirjain not in sana:
                sanoja-=1
                miinus=True
                break
        if miinus: continue

    return sanoja


        
        
    





  