import pygame
from random import choice
from sanat import palauta_sanat, korjaa_csv, palauta_tulos

#Testi muuutos kommentille

class Kirjainlaatikot:
    def __init__(self, positiokoko):
        self.vari =(80, 80, 80)
        self.posko=positiokoko
        self.vihrea=False
        self.uusimuuttuja=1
    def vaihda_vihrea(self):
        self.vari=(180,255,190)
        self.vihrea=True
    def vaihda_harmaa(self):
        self.vari=(200, 200, 200)
    def vaihda_kelt(self):
        self.vari=(255, 255, 51)
    def vaihda_musta(self):
        self.vari=(100, 100, 100)
    def resetoi(self):
        self.vari=(80, 80, 80)
class pointteri:
    def __init__(self,positiokoko):
        self.vari=(240,240,240)
        self.posko=positiokoko
class kirjain:

    def __init__(self,positio):
        self.on=False
        self.kirjain=""

        self.fontti = pygame.font.SysFont("Georgia", 40)
        self.teksti = self.fontti.render(self.kirjain, True, (20, 20, 20))
        self.paikka=positio
    def lisaa_kirjain(self,kirjain):
        self.on=True
        self.kirjain=kirjain
        self.teksti = self.fontti.render(self.kirjain.upper(), True, (20, 20, 20))
    def backspace(self):
        self.on=False
        self.kirjain=""
        self.teksti = self.fontti.render(self.kirjain, True, (20, 20, 20))
    def resetoi(self):
        self.kirjain=""
        self.on=False
class nappaimisto:

    def __init__(self,positio,kirjain):
        self.posko=positio,(33,33)
        self.kirjain=kirjain
        self.vari=(120,120,120)
        self.fontti = pygame.font.SysFont("Georgia", 25)
        self.teksti = self.fontti.render(self.kirjain, True, (20, 20, 20))
        self.paikka=(positio[0]+8,positio[1]+3)

    def vaihda_vihrea(self):
        self.vari=(180,255,190)
    def vaihda_harmaa(self):
        self.vari=(200, 200, 200)
    def vaihda_kelt(self):
        self.vari=(255, 255, 51)
    def vaihda_musta(self):
        self.vari=(50, 50, 50)
    def resetoi(self):
        self.vari=(120, 120, 120)
def vaihda_varit(kirjaimet,sana,laatikot,rivi,nappaimet,tiedot):
    arvaus=""
    for i  in kirjaimet:
        arvaus+=i.kirjain
    tiedot.arvaus=arvaus
    
    sana=list(sana)
    indeksit=[]
    oikeat=0
    for i in laatikot[rivi]:
        i.vaihda_musta()
    for i in kirjaimet:
        for j in nappaimet:
            if j.kirjain.lower() == i.kirjain:
                j.vaihda_musta()

    for i in range(len(kirjaimet)):
        if kirjaimet[i].kirjain == sana[i]:
            oikeat+=1
            laatikot[rivi][i].vaihda_vihrea()
            
            for nappain in nappaimet:
                if nappain.kirjain.lower()==sana[i]:
                    nappain.vaihda_vihrea()
                    
        else:
            indeksit.append(i)
    uusisana=[]
    for i in indeksit:
        uusisana.append(sana[i])
    sana=uusisana
    for i in range(len(kirjaimet)):
        for nappain in nappaimet:
            if kirjaimet[i].kirjain in sana and nappain.kirjain.lower()==kirjaimet[i].kirjain:
                nappain.vaihda_kelt()
    for i in range(len(kirjaimet)):
        if kirjaimet[i].kirjain in sana:
            if not laatikot[rivi][i].vihrea:
                laatikot[rivi][i].vaihda_kelt()
            sana.pop(sana.index(kirjaimet[i].kirjain))
    voitto=False
    if oikeat==5:
        voitto=True
    if tiedot.rivi-1==0:
        laske_parhaat(tiedot)
    elif tiedot.rivi-1>0:
        laske_parhaat(tiedot)
    
    return voitto
def tarkista(lista,sanalista):

    apulista="".join([i.kirjain for i in lista])
    if apulista in sanalista:
        return True
    else: return False
class parametrit:
    def __init__(self):
        korjaa_csv()
        self.vihjesanat=['kasti'.upper(),'taksi'.upper(),'ratki'.upper(), 'kausi'.upper(),'kilta'.upper(),'kitua'.upper(),'kiusa'.upper(),'rasti'.upper(),'silta'.upper(),'raksi'.upper()]
        self.mahdolliset=[]
        self.vihjeet=True
        self.arvaus=""
        self.sanalista=[]
        with open("vitoset.csv") as tiedosto:
            for i in tiedosto:
                i=i.strip(";")
                i=i.strip("\n")
                self.sanalista.append(i)
        self.sana=choice(self.sanalista)
        self.indeksi=0
        self.rivi=0
        self.taysi=False
        self.havio=False
        self.voitto=False
        self.back=False
        self.eisanakirjassa=True
        self.merkit="abcdefghijklmnopqrstuwvyzåäö"
        self.laatikot=[]
        self.kirjaimet=[]
        self.nappaimet=[]
        ekarivi="qwertyuiop".upper()
        tokarivi="asdfghjklöä".upper()
        kolmosrivi="zxcvbnm".upper()
        for i in range(5):
            self.laatikot.append([])
            self.kirjaimet.append([])
            for j in range(5):
                self.laatikot[i].append(Kirjainlaatikot((50+(j*60), 50+(i*60),50,50)))
                self.kirjaimet[i].append(kirjain((50+(j*60)+8, 50+(i*60)+3)))

        for i in range(len(ekarivi)):
            self.nappaimet.append(nappaimisto((22+i*36,440),ekarivi[i]))
        for i in range(len(tokarivi)):
            self.nappaimet.append(nappaimisto((5+i*36,480),tokarivi[i]))
        for i in range(len(kolmosrivi)):
            self.nappaimet.append(nappaimisto((72+i*36,520),kolmosrivi[i]))
    def indeksiplus(self):
        if self.indeksi<4:
            self.indeksi+=1
    def indeksimiinus(self):
        if self.indeksi>0:
            self.indeksi-=1
class nappi:
    def __init__(self):
        self.vari=(240,240,240)
        self.posko=((50,600),(200,50))
def hae_sanat():
    sanalista=[]
    with open("vitoset.csv") as tiedosto:
        for i in tiedosto:
            i=i.strip(";")
            i=i.strip("\n")
            sanalista.append(i)
    return sanalista
def testaa():
    sanalista=[]
    ohitukset="abcdefghijk"
    with open("vitoset.csv") as tiedosto:
        for i in tiedosto:
            i=i.strip(";")
            i=i.strip("\n")
            sanalista.append(i)
    jako=len(sanalista)

    # pituus=0
    # for i in sanalista:
    #     pituus+=len(palauta_sanat("kasti",i,sanalista))
    # print(pituus,pituus/jako)

    vihjesanat=[]
    for i in sanalista:
        if i[0] in ohitukset:
            continue
        pituus=0
        print(i)
        for j in sanalista:
            pituus+=palauta_tulos(j,i,sanalista)
            if pituus/jako>80:
                break
        if pituus/jako<=80:
            print((i,pituus/jako))
            vihjesanat.append((i,pituus/jako))
    print(vihjesanat)
def laske_parhaat(tiedot):
    if len(tiedot.mahdolliset)==0:
        tiedot.mahdolliset=palauta_sanat(tiedot.arvaus,tiedot.sana,tiedot.sanalista)
        lista=[]
        jako=len(tiedot.mahdolliset)
        takaraja=0
        poisto=False
        for i in tiedot.mahdolliset:
            skip=False
            pituus=0
            for j in tiedot.mahdolliset:
                pituus+=palauta_tulos(j,i,tiedot.mahdolliset)
                if takaraja!=0 and (pituus/jako)>takaraja:
                    skip=True
                    break
            if not skip:
                lista.append((i,pituus/jako))
                lista.sort(key = lambda x:x[1])
                if poisto:
                    lista=lista[:-1]
            if len(lista)>9:
                takaraja=lista[-1][1]
                poisto=True
        tiedot.vihjesanat=[]
        for i in lista:
            tiedot.vihjesanat.append(i[0].upper())


    else:
        tiedot.mahdolliset=palauta_sanat(tiedot.arvaus,tiedot.sana,tiedot.mahdolliset)
        lista=[]
        jako=len(tiedot.mahdolliset)
        takaraja=0
        poisto=False
        for i in tiedot.mahdolliset:
            skip=False
            pituus=0
            for j in tiedot.mahdolliset:
                pituus+=palauta_tulos(j,i,tiedot.mahdolliset)
                if takaraja!=0 and (pituus/jako)>takaraja:
                    skip=True
                    break
            if not skip:
                lista.append((i,pituus/jako))
                lista.sort(key = lambda x:x[1])
                if poisto:
                    lista=lista[:-1]
            if len(lista)>9:
                takaraja=lista[-1][1]
                poisto=True
        tiedot.vihjesanat=[]
        for i in lista:
            tiedot.vihjesanat.append(i[0].upper())
def main():

    pygame.init()
    naytto = pygame.display.set_mode((400, 700))
    naytto.fill((200, 200, 200))
    tiedot=parametrit()
    tiedot.vihjeet=False
    pygame.display.flip()
    x=40
    y=650
    while True:
        for tapahtuma in pygame.event.get():
            mx,my=pygame.mouse.get_pos()
            if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                if x<mx<x+130 and y<my<y+40:
                    if not tiedot.vihjeet:
                        naytto = pygame.display.set_mode((565, 700))
                        tiedot.vihjeet=True
                    else:
                        naytto = pygame.display.set_mode((400, 700))
                        tiedot.vihjeet=False

                continue
            if tapahtuma.type == pygame.KEYDOWN:
                character = tapahtuma.unicode
                if tapahtuma.key==pygame.K_x:
                    sana=tiedot.sana
                    tiedot=parametrit()
                    tiedot.sana=sana
                if character=="§":
                    if not tiedot.vihjeet:
                        naytto = pygame.display.set_mode((565, 700))
                        tiedot.vihjeet=True
                    else:
                        naytto = pygame.display.set_mode((400, 700))
                        tiedot.vihjeet=False
                if tapahtuma.key == pygame.K_BACKSPACE:
                    tiedot.eisanakirjassa=True
                    if tiedot.indeksi==4:
                        if tiedot.kirjaimet[tiedot.rivi][tiedot.indeksi].on:
                            tiedot.kirjaimet[tiedot.rivi][tiedot.indeksi].kirjain=""
                            tiedot.kirjaimet[tiedot.rivi][tiedot.indeksi].on=False
                            tiedot.taysi=False

                        else:
                            tiedot.indeksimiinus()
                            tiedot.kirjaimet[tiedot.rivi][tiedot.indeksi].kirjain=""
                            tiedot.kirjaimet[tiedot.rivi][tiedot.indeksi].on=False
                    else:
                        tiedot.indeksimiinus()
                        tiedot.kirjaimet[tiedot.rivi][tiedot.indeksi].kirjain=""
                        tiedot.kirjaimet[tiedot.rivi][tiedot.indeksi].on=False
                elif tiedot.taysi or tiedot.voitto or tiedot.havio:
                    if tapahtuma.key==pygame.K_RETURN:
                        if tiedot.voitto or tiedot.havio:
                            tiedot=parametrit()
                        else:
                            if tarkista(tiedot.kirjaimet[tiedot.rivi],tiedot.sanalista):
                                tiedot.rivi+=1
                                tiedot.indeksi=0
                                tiedot.taysi=False
                                tiedot.voitto=vaihda_varit(tiedot.kirjaimet[tiedot.rivi-1],tiedot.sana,tiedot.laatikot,tiedot.rivi-1,tiedot.nappaimet,tiedot)
                                tiedot.eisanakirjassa=True
                                if not tiedot.voitto and tiedot.rivi==5:
                                    tiedot.havio=True
                            else:
                                tiedot.eisanakirjassa=False

                else:
                    if character in tiedot.merkit and character !="":
                        tiedot.kirjaimet[tiedot.rivi][tiedot.indeksi].lisaa_kirjain(character)
                        tiedot.back=False
                        if tiedot.indeksi<4:
                            tiedot.indeksiplus()
                        else:
                            tiedot.taysi=True
            if tapahtuma.type == pygame.QUIT:
                exit()

        

        naytto.fill((150, 150, 150))
        pointer=pointteri((45+(tiedot.indeksi*60), 45+(tiedot.rivi*60),60,60))
        pygame.draw.rect(naytto,(80,80,80),((x-3,y-3),(136,44)))
        pygame.draw.rect(naytto,(200,200,200),((x,y),(130,38)))
        naytto.blit(pygame.font.SysFont("Georgia", 20).render("Vihjeet (§)",True,(20,20,20)),(x+5,y+5))

        if not tiedot.voitto:
            if tiedot.rivi!=5:
                pygame.draw.rect(naytto,pointer.vari,pointer.posko)
            if not tiedot.eisanakirjassa and tiedot.taysi:
                naytto.blit(pygame.font.SysFont("Georgia", 20).render("Sanaa ei löytynyt",True,(20,20,20)),(50,350))
            elif tiedot.havio==True:
                naytto.blit(pygame.font.SysFont("Georgia", 20).render("Hävisit pelin, oikea sana oli:",True,(20,20,20)),(50,350))
                naytto.blit(pygame.font.SysFont("Georgia", 20).render(tiedot.sana,True,(20,20,20)),(50,380))
                naytto.blit(pygame.font.SysFont("Georgia", 20).render("Paina enter pelataksesi uudestaan",True,(20,20,20)),(50,410))
        else:
            naytto.blit(pygame.font.SysFont("Georgia", 20).render("Voitit pelin!",True,(20,20,20)),(50,350))
            naytto.blit(pygame.font.SysFont("Georgia", 20).render("Paina enteriä pelataksesi uudestaan!",True,(20,20,20)),(50,380))
        for i in tiedot.laatikot:
            for j in i:
                pygame.draw.rect(naytto, j.vari, j.posko)
        for j in tiedot.kirjaimet:
            for i in j:
                if i.on:
                    naytto.blit(i.teksti, i.paikka)
        for i in tiedot.nappaimet:
            pygame.draw.rect(naytto, i.vari, i.posko)
            naytto.blit(i.teksti, i.paikka)
        
        if tiedot.vihjeet:
            naytto.blit(pygame.font.SysFont("Georgia", 40).render("Vihjeet:",True,(20,20,20)),(400,50))
            for i in range(len(tiedot.vihjesanat)):
                naytto.blit(pygame.font.SysFont("Georgia", 28).render(f"{i+1}. {tiedot.vihjesanat[i]}",True,(20,20,20)),(415,150+i*40))

        pygame.display.flip()
        del pointer

if __name__=="__main__":
    # testaa()

    main()
 






