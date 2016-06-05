from PIL.ImageTk import PhotoImage
from PIL.Image import ANTIALIAS, BICUBIC
from tkinter import BooleanVar, Canvas, CENTER, Frame, NW
from colorize import *
from time import sleep

class Tabla(Frame):
    """A tábla leképezése"""
    def __init__(self,boss,meret=768,szelindex=6):
        Frame.__init__(self, master = boss)
        self.boss = boss
        # beolvassuk a megadott méretet
        self.meret = meret-meret%9 # a kilences osztási maradékot lecsippentjük a leendő táblaméretről
        self.jatekter = Canvas(self, width = self.meret, #bg = 'blue',
                               height = self.meret,
                               bd=0, highlightthickness=0, relief='ridge'
                               )
        self.jatekter.grid()
        self.jatekter.bind("<Button-1>",self.klikk)
        # kijelöljük a játékmezőket
        self.mezomeret = int(meret/9)
        self.mezolista = []
        for sor in (1,5,9): # teljes sorok
           for oszlop in range(1,10):
               self.mezolista.append((sor,oszlop))
        for sor in (2,3,4,6,7,8): # átvezető szakaszok
           for oszlop in (1,5,9):
               self.mezolista.append((sor,oszlop))
        self.mezolista.sort() # sorba rendezzük
        self.keptar = {}
        self.helyszotar = dict([('csata_francia',   [(5,9)]),
                                ('csata_angol',     [(9,5)]),
                                ('csata_holland',   [(1,5)]),
                                ('csata_spanyol',   [(5,1)]),
                                ('portroyal',       [(5,5)]),
                                ('curacao',         [(1,9)]),
                                ('tortuga',         [(9,1)]),
                                ('havanna',         [(1,1)]),
                                ('martinique',      [(9,9)]),
                                ('szelplusz90',     [(7,1),(9,7)]),
                                ('szelminusz90',    [(1,7),(3,5)]),
                                ('szelplusz45',     [(1,3),(5,7),(7,9),(9,3)]),
                                ('szelminusz45',    [(3,1),(5,3),(7,5),(3,9)]),
                                ('bermuda',         [(9,4)]),
                                ('foldfold',        [(1,6),(2,9),(5,4),(9,2)]),
                                ('vihar',           [(2,5),(5,6),(9,6)]),
                                ('uszadek',         [(1,8),(2,1),(6,5),(9,8)]),
                                ('szelcsend',       [(4,5),(8,9)]),
                                ('taino',           [(4,1),(6,9)]),
                                ('kincsessziget',   [(1,2),(4,9),(8,1),(8,5)]),
                                ('aramlat',         [(1,4),(5,8),(6,1)]),
                                ('szamuzottek',     [(5,2)])
                                ])
        self.helyszotarR = {}
        for birodalom in self.boss.birodalomszotar.keys():
            v = self.boss.birodalomszotar[birodalom].varos
            self.boss.birodalomszotar[birodalom].set_koordinatak(self.helyszotar[v][0])
        for hely in self.helyszotar.keys():
            for ertek in self.helyszotar[hely]:
                self.helyszotarR[ertek] = hely
        self.kikotolista = ['portroyal', 'curacao', 'tortuga', 'havanna', 'martinique']
        self.kikototarR = {} # A városok koordináta alapú meghatározására szolgál.
        self.kikotok = self.kikotokfeltolt()
        self.hajotar = {}
        self.figuraszotar = {}
        self.villogasaktiv = 0
        self.xlatszik = BooleanVar()
        self.xlatszik.set(0)
        #                 e  ek   k  dk  d  dny  ny  eny
        self.szelirany = [2,  1, -3,  1, 2,   1,  0,   1]
        while self.szelirany[szelindex] != 0:
            self.szelirany.append(self.szelirany.pop(0))            

    def lekepez(self):
        "Megjeleníti a tábla tartalmát"
        print('leképezés indul')
        # A háttér betöltése
        self.keptar['hatter'] = PhotoImage(open('img/map.png').resize((self.meret,self.meret), ANTIALIAS))
        self.jatekter.create_image(0,0, image = self.keptar['hatter'], anchor = NW)
        # A félig áttetsző mezőhátterek leképezése
        self.keptar['mezohatter'] = PhotoImage((open('img/mezo.png').resize((self.mezomeret,self.mezomeret), ANTIALIAS)).convert("RGBA"))
        for (mezox,mezoy) in self.mezolista:
            self.jatekter.create_image(int((mezox-0.5)*self.mezomeret),int((mezoy-0.5)*self.mezomeret), image = self.keptar['mezohatter'], anchor = CENTER)
        # A mezőikonok betöltése
        for elem in self.helyszotar:
            aktualis = open('img/'+elem+'.png')
            aktualis = aktualis.resize((int(self.mezomeret*0.9),int(self.mezomeret*0.9)), ANTIALIAS)
            aktualis = PhotoImage(image=aktualis)
            self.keptar[elem]=aktualis
        self.mezoszotar = {} # ebben tároljuk a mezőket
        for elem in self.helyszotar.keys():
            self.mezoszotar[elem] = Mezo(self, self.helyszotar[elem], elem)
        for jatekos in self.boss.jatekostar.keys():
            self.figuratLetrehoz(self.boss.jatekostar[jatekos].nev,
                                 self.boss.jatekostar[jatekos].pozicio[0],
                                 self.boss.jatekostar[jatekos].pozicio[1],
                                 self.boss.jatekostar[jatekos].hajo,
                                 self.boss.jatekostar[jatekos].szin)
        # Az úticéljelölő betöltése
        self.xkep = open('img/X.png')
        magassagszorzo = self.xkep.size[1]/self.xkep.size[0]
        self.keptar['x'] = PhotoImage(image=self.xkep.resize((self.mezomeret, int(self.mezomeret*magassagszorzo)), ANTIALIAS))
        # A szélrózsa betöltése
        self.keptar['compass'] = PhotoImage((open('img/compass.png').resize((self.mezomeret*3-10,self.mezomeret*3-10), ANTIALIAS)).convert("RGBA"))
        self.jatekter.create_image(int(6.5*self.mezomeret),int(2.5*self.mezomeret), image = self.keptar['compass'], anchor = CENTER)
        self.szeliranykep = open('img/szelirany.png')
        szeliranySzelessegszorzo = self.szeliranykep.size[0]/self.szeliranykep.size[1]
        self.szeliranykep = self.szeliranykep.resize((int(self.mezomeret*2*szeliranySzelessegszorzo),int(self.mezomeret*2)), ANTIALIAS).convert("RGBA")
        for i in range(8):
            self.keptar['szelirany'+str(i)] = PhotoImage(self.szeliranykep.rotate(i*-45, resample = BICUBIC, expand = 1))
        self.szelmutato = self.jatekter.create_image(0,0, image = None)
        self.szel_megjelenit()
        # A pénzek betöltése
        a = open('img/penz-1.png')
        penzszorzo = a.size[1]/a.size[0]
        self.keptar['penz-1'] = PhotoImage((a.resize((int(self.meret/40),int(self.meret/40*penzszorzo)), ANTIALIAS)).convert("RGBA"))
        a = int(self.meret/20)
        for penzfajta in ['8','d','d2']:
            self.keptar['penz-'+penzfajta] = PhotoImage((open('img/penz-'+penzfajta+'.png').resize((a,a), ANTIALIAS)).convert("RGBA"))
        # A kikötőképek betöltése
        for kikoto in self.kikotolista:
            self.keptar[kikoto+'full'] = PhotoImage(open('img/'+kikoto+'.png').convert("RGBA"))
        # A matrózok betöltése
        self.keptar['matrozok'] = PhotoImage((open('img/matrozok.png').resize((a,a), ANTIALIAS)).convert("RGBA"))
        # Hajók betöltése a hajóács gombjaihoz, és az ellenfelekhez.
        for hajotipus in ['brigantin','fregatt','szkuner','galleon']:
            hajokep = open('img/'+hajotipus+'.png')
            magassagszorzo = hajokep.size[1]/hajokep.size[0]
            hajokep = hajokep.resize((self.mezomeret, int(self.mezomeret*magassagszorzo)), ANTIALIAS)
            self.keptar[hajotipus] = PhotoImage(hajokep)
        # A zászlók betöltése.
        for birodalom in self.boss.birodalomszotar.keys():
            zNev = 'zaszlo_'+birodalom
            zKep = open(('img/'+zNev+'.png'))
            magassagszorzo = zKep.size[0]/zKep.size[1]
            self.keptar[zNev] = PhotoImage(zKep.resize((int(self.meret/20*magassagszorzo),int(self.meret/20)), ANTIALIAS))
        # Matrózok betöltése.
        self.keptar['matroz1'] = open('img/matroz1.png')
        self.keptar['matroz0'] = PhotoImage((open('img/transparent.png')).resize((self.keptar['matroz1'].size[0], self.keptar['matroz1'].size[1]), ANTIALIAS))
        self.keptar['matroz1'] = PhotoImage(self.keptar['matroz1'])  
        self.keptar['matroz2'] = PhotoImage(open('img/matroz2.png'))
        # Csatagombok betöltése.
        for i in ['pisztoly', 'puska', 'labtovis', 'granat', 'kartacs', 'gorogtuz', 'majom', 'szirenkurt', 'szirenek', "alvarez"]:
            self.keptar['ikon_'+i] = PhotoImage(open('img/ikon_'+i+'.png'))
        print('leképezés kész')
    
    def kartyakep(self, pakli, prefix):
        "Leképezi a kártyákhoz szükséges képeket."
        for elem in pakli:
            self.keptar[elem] = PhotoImage(open('img/'+prefix+elem+'.png'))

    def kartyakep2(self, kep):
        "Leképezi a kártyákhoz szükséges képeket. A Kartya3-mal kompatibilis."
        self.keptar[kep] = open('img/'+kep+'.png')
        self.keptar[kep[kep.rfind('_')+1:]+'_i'] = PhotoImage(self.keptar[kep].resize((30,30),ANTIALIAS))
        self.keptar[kep] = PhotoImage(self.keptar[kep])
        
    def figuratLetrehoz(self, username, x, y, hajotipus, szin, korabbiTorlese = 0):
        "Leképezi a felhasználó figuráját a táblán."
        hajokep = open('img/'+hajotipus+'-h.png')
        magassagszorzo = hajokep.size[1]/hajokep.size[0]
        hajokep = hajokep.resize((self.mezomeret, int(self.mezomeret*magassagszorzo)), ANTIALIAS)
        vitorlakep = (image_tint('img/'+hajotipus+'-v.png',szin).resize((self.mezomeret, int(self.mezomeret*magassagszorzo)), ANTIALIAS))
        hajokep.paste(vitorlakep, (0,0), vitorlakep)
        self.hajotar[username] = PhotoImage(hajokep)
        if korabbiTorlese == 1:
            self.jatekter.delete(self.figuraszotar[username])
        self.figuraszotar[username] = self.jatekter.create_image((x-0.5)*self.mezomeret,(y-0.5)*self.mezomeret, image = self.hajotar[username], anchor = CENTER)

    def kormanyos(self,mostanioszlop,mostanisor,dobas,szellel = 1):
        "Meghatározza a lépések lehetséges kimenetelét."
        iranyok = {"e":(0,-1),
                   "d":(0,1),
                   "k":(1,0),
                   "ny":(-1,0)} # az irányok rácson való értelmezése
        szelirany = self.szel()
        celok = [] # ide írjuk majd az eredményeket (x,y) formában
        # leképezzük a lehetséges lépéseket
        utak = [] # az utak során meglátogatott mezők listája
        lepes = 1
        for (irany,(oszlop,sor)) in iranyok.items(): # leképezzük az első szomszédos mezőket, és beírjuk a kiindulási irányt, így a további mezőkből meg lehet tudni, hogy merről értük el őket
            elsomezo = (mostanioszlop+oszlop,mostanisor+sor,lepes,irany)
            if self.hajozhato(elsomezo[0],elsomezo[1]):
                utak.append(elsomezo)
        lepes = 2 # a további mezők következnek
        while lepes <= dobas+2:
            for elem in utak:
                lehetsegesUtak = [] # a vizsgálat alatt álló szomszédos mezők listája
                if elem[2] == lepes-1: # csak azokat a mezőket vizsgáljuk, amelyeket még nem néztünk meg (CPU takarékos)
                    for (irany,(oszlop,sor)) in iranyok.items(): # leképezzük a szomszédos mezőket, és felvesszük őket a vizsgálólistára 
                        lehetsegesUtak.append((elem[0]+oszlop,elem[1]+sor,lepes,elem[3]),)
                    for lehetsegesUt in lehetsegesUtak: # elvégzünk mindegyik lehetséges úton egy ellenőrzést
                        if self.hajozhato(lehetsegesUt[0],lehetsegesUt[1]) == False:
                            lehetsegesUtak[lehetsegesUtak.index(lehetsegesUt)] = 0 # ha a mező nincs rajta a táblán, megjelöljük
                        else: # megnézzük, a maradék mező nincs-e már rajta az útlistán
                            for ut in utak:
                                if (lehetsegesUt[0],lehetsegesUt[1]) == (ut[0],ut[1]) and lehetsegesUt[2] >= ut[2] and (lehetsegesUt[0],lehetsegesUt[1]) not in self.kikotok:
                                    lehetsegesUtak[lehetsegesUtak.index(lehetsegesUt)] = 0 # ha a mező már szerepel a listán, megjelöljük             
                    # ezzel kinyertük a utak listában tárolt mezők használható szomszédos mezőit
                for lehetsegesUt in lehetsegesUtak:
                    if lehetsegesUt:
                        utak.append(lehetsegesUt)
            lepes += 1
        if szellel:
            for ut in utak:
                if ut[2] == (dobas + self.szel(ut[3])):
                    celok.append((ut[0],ut[1]))
                elif ((ut[0],ut[1]) in self.kikotok) and ut[2] < (dobas + self.szel(ut[3])):
                    celok.append((ut[0],ut[1]))
        else:
            for ut in utak:
                if ut[2] == dobas:
                    celok.append((ut[0],ut[1]))
                elif ((ut[0],ut[1]) in self.kikotok) and ut[2] < dobas:
                    celok.append((ut[0],ut[1]))
        if (mostanioszlop,mostanisor) in celok: # Ha kiindulómező cél lenne, töröljük.
            celok.remove((mostanioszlop,mostanisor))
        if (mostanioszlop,mostanisor) in self.kikotok and szellel: # Ha kikötőből indulunk, visszatesszük / hozzáadjuk.
            celok.append((mostanioszlop,mostanisor))
        for cel in celok:
            if celok.count(cel) > 1:
                celok.remove(cel)
        self.celok = celok
        return celok

    def hajozhato(self,x,y):
        "Ellenőrzi, hogy az adott mező része-e a táblának"
        if (x,y) in self.mezolista:
            return 1
        else:
            return 0

    def szel(self,irany="x"):
        "A szél erejét visszaadó függvény"
        szeliranyszotar = {"e":   self.szelirany[0],
                           "ek":  self.szelirany[1],
                           "k":   self.szelirany[2],
                           "dk":  self.szelirany[3],
                           "d":   self.szelirany[4],
                           "dny": self.szelirany[5],
                           "ny":  self.szelirany[6],
                           "eny": self.szelirany[7],
                           "x":   0}
        return szeliranyszotar[irany]
        
    def szel_megjelenit(self):
        "Megjeleníti a szélirányt jelző mutatót."
        mutatoirany = str(self.szelirany.index(0))
        self.jatekter.delete(self.szelmutato)
        self.szelmutato = self.jatekter.create_image(int(6.5*self.mezomeret),int(2.5*self.mezomeret), image = self.keptar['szelirany'+mutatoirany], anchor = CENTER)
        
    def szel_valtoztat(self, szog = 0):
        "Megváltoztatja a szél irányát."
        ujszeliranyindex = (self.szelirany.index(0) + int(szog/45))%8
        while self.szelirany[ujszeliranyindex] != 0:
            self.szelirany.append(self.szelirany.pop(0))
        self.szel_megjelenit()
        
    def kikotokfeltolt(self):
        "Városlistázó függvény."
        kikotok = []
        for varos in self.kikotolista:
            kikotok.append(self.helyszotar[varos][0])
            self.kikototarR[self.helyszotar[varos][0]] = varos
        return sorted(kikotok)
    
    def celkereso(self, mezolista):
        "Megmutatja a játékosnak azokat a négyzeteket, ahová majd lépni lehet."
        self.xlista = []
        for mezox,mezoy in mezolista:
            self.xlista.append(self.jatekter.create_image((mezox-0.5)*self.mezomeret,(mezoy-0.5)*self.mezomeret, image = self.keptar['x'], anchor = CENTER))
            self.xlatszik.set(True)
        self.villogasaktiv = 1
        self.villogas = None
        self.villogas = Mutatrejt(self)
        self.villogas.start()
          
    def klikk(self,event):
        "A mezőválasztást kezelő függvény."
        if not self.boss.jatekmenet.dobasMegtortent.get():
            return
        if self.boss.menu.fold_fold_dobas:
            self.boss.naplo.ir('')
            self.boss.menu.ful1tartalom.kockamezo.config(relief = "sunken")
            self.boss.menu.fold_fold_dobas_null()
        klikkx,klikky = int(event.x/self.mezomeret)+1,int(event.y/self.mezomeret)+1
        if (klikkx,klikky) not in self.celok:
            return
        else:
            self.villogaski()
            self.hajotathelyez(klikkx,klikky)
            self.boss.jatekmenet.szakasz_mezoesemeny()
            
    def villogaski(self):
        "Kikapcsolja a célnégyzetek villogását."
        self.boss.tabla.villogasaktiv = 0
        if self.xlatszik.get():
            for x in self.xlista:
                self.jatekter.itemconfigure(x,state='hidden')
            self.xlatszik.set(False)
            self.xlista = []
            
    def hajotathelyez(self, celx, cely):
        "Végrehajtja a kijelölt lépést."
        self.jatekter.coords(self.figuraszotar[self.boss.jatekmenet.aktivjatekos.nev], (celx-0.5)*self.mezomeret,(cely-0.5)*self.mezomeret)
        self.boss.jatekmenet.aktivjatekos.pozicio = (celx, cely)
        
class Mutatrejt():
    """A villogást irányító osztály."""
    def __init__(self, parent):
        self.boss = parent
    def start(self):
        while self.boss.villogasaktiv == 1:
            self.fut()
            self.boss.boss.update()
            sleep(0.25)
        if self.boss.villogasaktiv == -1:
            return
        #elif self.boss.xlatszik.get():
        #    for x in self.boss.xlista:
        #        self.boss.jatekter.itemconfigure(x,state='hidden')
        #    self.boss.xlatszik.set(False)
        #self.boss.xlista = []
    
    def fut(self):
        if self.boss.xlatszik.get():
            for x in self.boss.xlista:
                self.boss.jatekter.itemconfigure(x,state='hidden')
            self.boss.xlatszik.set(False)
        else:
            for x in self.boss.xlista:
                self.boss.jatekter.itemconfigure(x,state='normal')
            self.boss.xlatszik.set(True)
    
    def start0(self):
        if self.boss.xlatszik.get():
            for x in self.boss.xlista:
                self.boss.jatekter.itemconfigure(x,state='hidden')
            self.boss.xlatszik.set(False)
            self.boss.boss.update()
            if self.boss.villogasaktiv != 1:
                self.boss.xlista = []
                return
        else:
            if self.boss.villogasaktiv != 1:
                self.boss.xlista = []
                return
            for x in self.boss.xlista:
                self.boss.jatekter.itemconfigure(x,state='normal')
            self.boss.xlatszik.set(True)
            self.boss.boss.update()
        sleep(0.25)
        self.start()
            
class Mezo():
    """Egy játékmező logikai megjelenése."""
    def __init__(self, boss, koordinatlista, mezotipus):
        self.boss = boss
        self.koordinatlista = koordinatlista
        self.mezotipus = mezotipus
        self.lekepez()
        
    def lekepez(self):
        for x,y in self.koordinatlista:
            self.boss.jatekter.create_image(int((x-0.5)*self.boss.mezomeret),int((y-0.5)*self.boss.mezomeret), image = self.boss.keptar[self.mezotipus], anchor = CENTER)   
        
if __name__ == '__main__0':
    from tkinter import Tk
    "A valós működést szimuláló teszthívás."
    a = Tk()
    a.birodalomszotar = {}
    jatek = Tabla(a,890)
    a.jatekostar = {}
    a.title("teszt")
    jatek.grid()
    jatek.lekepez()
    a.mainloop()
