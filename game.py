from tkinter import BOTTOM, BooleanVar, Button, Canvas, DISABLED, Frame, GROOVE, HORIZONTAL, IntVar, Label, LEFT, NORMAL, RAISED, RIDGE, RIGHT, Scale, StringVar, TOP, Toplevel, X, Y
from tkinter.messagebox import showinfo, askyesno
from math import sqrt
from random import randrange
from time import sleep
from tkinter.ttk import LabelFrame, Separator
from csata import Utkozet
from card import *

class Jatekos():
    """Leír egy játékost."""
    def __init__(self, boss, tabla, nev, szin, sajatkikoto, hajo = 'schooner', legenyseg = 10, pozicio = None, kincs = 0, statusz = [], utolsodobas = 6, kimarad = 0, kincskeresesKesz = True, elfogottHajok = {}):
        self.tabla = tabla
        self.boss = boss
        self.nev = nev
        self.szin = szin
        self.masodikszin = [int(self.szin[1:3], 16), int(self.szin[3:5], 16), int(self.szin[5:], 16)] # a játékos színét rgbvé bontjuk
        if sqrt(self.masodikszin[0]**2*0.241+self.masodikszin[1]**2*0.691+self.masodikszin[2]**2*0.068) > 127: # megállapítjuk hozzá az optimális gombócszínt
            self.masodikszin = 'black'
        else:
            self.masodikszin = 'white'
        if sajatkikoto in self.boss.tabla.helyszotar.keys():
            self.sajatkikoto = self.boss.tabla.helyszotar[sajatkikoto][0]
        else:
            self.sajatkikoto = self.boss.tabla.helyszotar[self.boss.zaszloszotar[sajatkikoto]][0]
        self.zaszlo = self.boss.get_empire_by_capital_coordinates(self.sajatkikoto)
        print(self.nev,"zászlaja:",self.zaszlo)
        self.hajo = hajo
        self.legenyseg = IntVar()
        self.legenyseg.set(legenyseg)
        self.legenyseg_max = IntVar()
        if not pozicio:
            self.pozicio = self.sajatkikoto
        else:
            self.pozicio = pozicio
        self.kincs = IntVar()
        self.kincs.set(kincs)
        self.kincskeresesKesz = kincskeresesKesz
        self.statuszlista = statusz
        self.utolsodobas = utolsodobas
        self.kimarad = IntVar()
        self.kimarad.set(kimarad)
        self.hajotar = {}
        for zaszlo in self.boss.zaszloszotar2.keys():
            self.hajotar[zaszlo] = IntVar()
        if elfogottHajok != {}:
            for elfogottHajo in elfogottHajok.keys():
                self.hajotar[elfogottHajo].set(elfogottHajok[elfogottHajo])
        
    def set_hajo(self, tipus):
        "A megadott típusúra állítja be a játékos hajóját."
        self.hajo = tipus
        self.boss.tabla.figuratLetrehoz(self.nev, self.pozicio[0], self.pozicio[1], self.hajo, self.szin, 1)
        
    def set_legenyseg(self, modosito):
        "Módosítja a legénység létszámát"
        self.legenyseg.set(self.legenyseg.get() + modosito)
        
    def set_legenyseg_max(self, szam):
        "Módosítja a legénység maximális létszámát"
        self.legenyseg_max.set(szam)
        
    def set_kincs(self, modosito):
        "Módosítja a kincs mennyiségét."
        self.kincs.set(self.kincs.get() + modosito)
        
    def set_statusz(self, statusz, ertek = 1):
        "Ad vagy megvon egy adott státuszt."
        #print(self.nev,"státusza módosítás előtt:", self.statuszlista)
        if ertek:
            self.statuszlista.append(statusz)
        else:
            self.statuszlista.remove(statusz)
        #print(self.nev,"státusza módosítás után:", self.statuszlista)
            
    def set_utolsodobas(self, ertek):
        "Megadja az utoljára dobott értéket."
        self.utolsodobas = ertek
        
    def set_kimarad(self, ertek = -1):
        "Beállítja, hány körből marad ki a játékos. Argumentum nélkül hívva levon egy kört."
        self.kimarad.set(self.kimarad.get()+ertek)
        
    def set_hajoszam(self, birodalom, szam):
        "Jóváírja a hajópontok változását."
        self.hajotar[birodalom].set(self.hajotar[birodalom].get()+szam)
        
    def set_birodalom(self):
        "Beállítja a játékos birodalmát."
        self.birodalom = self.boss.get_empire_by_capital_coordinates(self.sajatkikoto)
        
    def set_kincskereses(self, ertek):
        "Kívülről hívható függvény, amely megváltoztatja a kincskeresesKesz paraméter értékét."
        self.kincskeresesKesz = ertek
            
    def export(self):
        "Átadja a mentőrutinnak az adatokat."
        zaszloexport = []
        for zaszlo in sorted(list(self.hajotar.keys())):
            zaszloexport.append((zaszlo, self.hajotar[zaszlo].get()))
        return [self.nev, self.szin, self.sajatkikoto, self.hajo, self.legenyseg.get(), self.pozicio, self.kincs.get(), self.statuszlista, self.utolsodobas, self.kimarad.get(), zaszloexport, self.kincskeresesKesz]

class Varos():
    """A kikötőket működtető osztály."""
    def __init__(self, parent=None, master=None, nev = '', matrozokszama = 5):
        self.matrozokszama = IntVar()
        self.matrozokszama.set(matrozokszama)
        self.boss = parent
        self.master = master
        self.nev = nev
        self.zaszlo = self.master.zaszloszotar2R[self.nev]
    
    def aktival(self):
        "Működteti a kikötőt."
        self.letrehoz()
            
    def letrehoz(self):
        self.ablak = Toplevel()
        if self.nev == 'portroyal':
            self.ablak.title((self.master.szotar['port']+' - Port Royal'))
        else:
            self.ablak.title((self.master.szotar['port'], '-', self.nev.capitalize()))
        self.ablak.transient(self.master)
        self.ablak.grab_set()
        self.ujMatrozok() # A játékos belépésekor a kocka által mutatott számot hozzáadjuk a helyi matrózok létszámához.
        self.tevekenysegek = Frame(self.ablak) # Főkeret: tartalma panelek és gombok
        self.tevekenysegek.pack(side = TOP, ipadx = 5)
        # A kép panel
        self.kep = Label(self.tevekenysegek, image = self.master.tabla.keptar[self.nev])
        self.kep.pack(side = LEFT, pady = 5, padx = 5, fill = Y)
        # A fogadó panel
        self.fogado = LabelFrame(self.tevekenysegek, text=self.master.szotar['tavern'])
        line1 = Frame(self.fogado) # a bérelhető létszám
        Label(line1, text=(self.master.szotar['sailors_to_hire']+':')).pack(side = LEFT)
        self.matrozokszama_kiirva = Label(line1, textvariable=self.matrozokszama).pack(side = RIGHT)
        line1.pack(side = TOP, fill = X)
        line2 = Frame(self.fogado) # legénység / hajó max. kapacitás
        Label(line2, text=(self.master.szotar['crew']+':')).pack(side = LEFT)
        Label(line2, textvariable=self.boss.aktivjatekos.legenyseg_max).pack(side = RIGHT)
        Label(line2, text='/').pack(side = RIGHT)
        Label(line2, textvariable=self.boss.aktivjatekos.legenyseg).pack(side = RIGHT)
        line2.pack(side = TOP, fill = X)
        berskalahossz = min(self.boss.aktivjatekos.legenyseg_max.get(), self.matrozokszama.get(), self.boss.aktivjatekos.kincs.get())
        Separator(self.fogado, orient = HORIZONTAL).pack(side = TOP, fill = X, pady = 5, padx = 5)
        line3 = Frame(self.fogado) # a skála címe
        szoveg = self.master.szotar['crew_new']
        szoveg = szoveg + ' '*(33-len(szoveg))
        Label(line3, text=szoveg).pack(side = LEFT)
        line3.pack(side = TOP, fill = X)
        self.line4 = Frame(self.fogado) # a skála
        self.berskala = Scale(self.line4)
        self.line4.pack(side = TOP, fill = X)
        self.line5 = Frame(self.fogado) # a skálán beállított értéket érvényesítő gomb
        self.skalaCimke = Label(self.line5)
        self.felberel = Button(self.line5, text = self.master.szotar['crew_hire'], command = self.matrozFelberelese)
        self.felberel.pack(side = RIGHT, padx = 5, pady = 5)
        self.line5.pack(side = TOP, fill = X)
        self.fogado.pack(side = LEFT, pady = 5, padx = 5, fill = Y)
        # A hajóács panel
        self.hajoacs = LabelFrame(self.tevekenysegek, text = self.master.szotar['shipwright'])
        self.hajoacs_lekepez()
        self.hajoacs.pack(side = LEFT, fill = Y, pady = 5)
        # A kormányzó panel
        pontok = 0
        kormanyzo_mondja = StringVar()
        for pontforras in self.boss.aktivjatekos.hajotar.keys():
            pontok += self.boss.aktivjatekos.hajotar[pontforras].get()
        self.kormanyzo = LabelFrame(self.tevekenysegek, text=self.master.szotar['governor'])
        if self.zaszlo == 'pirate':
            elsullyesztettHelyiHajok = 0 # A kalózok nem birodalom, nem büntetnek az elsüllyedt kalózhajókért
        else:
            elsullyesztettHelyiHajok = self.boss.aktivjatekos.hajotar[self.zaszlo].get()
        if elsullyesztettHelyiHajok > 0:
            kormanyzo_mondja.set(self.master.szotar['governor_punish'] % elsullyesztettHelyiHajok)
            self.boss.aktivjatekos.set_kimarad(elsullyesztettHelyiHajok)
            self.boss.aktivjatekos.set_hajoszam(self.zaszlo,-elsullyesztettHelyiHajok)
        else:
            maxJutalom = self.jutalomszamolo()*8
            kormanyzo_mondja.set(self.master.szotar['governor_reward'] % maxJutalom)
            self.boss.aktivjatekos.set_kincs(maxJutalom)
            self.penzszamolo()
            for birodalom in self.boss.aktivjatekos.hajotar.keys():
                fizetve = self.boss.aktivjatekos.hajotar[birodalom].get()
                self.boss.aktivjatekos.set_hajoszam(birodalom,-fizetve)
        Label(self.kormanyzo, wraplength = 125, textvariable = kormanyzo_mondja).pack(side = LEFT)
        if self.zaszlo != 'pirate' and pontok > 0:
            self.kormanyzo.pack(side = LEFT, pady = 5, padx = 5, fill = Y)
        # Gombok
        Button(self.ablak, text=self.master.szotar['done'], command = self.ablak.destroy).pack(side = BOTTOM, pady = 5)
        self.ablak.update_idletasks()
        w, h = self.ablak.winfo_width(),self.ablak.winfo_height()
        bx, by = self.master.helymeghatarozas()
        bh, bw = self.master.height,self.master.width        
        self.ablak.geometry('+'+str(int(bx+(bw+(bh/3)-w)/2))+'+'+str(int(by+(bh-h)/2)))
        self.master.wait_window(self.ablak)
        
    def hajoacs_lekepez(self):
        "A hajóácspanel."
        self.hajoframek = {}
        self.hajogombok = {}
        for hajo in self.boss.vehetoHajok:
            self.hajoframek[hajo] = Frame(self.hajoacs)
            self.hajogombok[hajo] = Button(self.hajoframek[hajo], image = self.master.tabla.keptar[hajo], command = lambda hajo = hajo: self.ujHajo(hajo))
            self.hajogombok[hajo].pack(side = LEFT)
            if self.boss.aktivjatekos.hajo in self.boss.vehetoHajok:
                if self.boss.vehetoHajok.index(self.boss.aktivjatekos.hajo) < self.boss.vehetoHajok.index(hajo):
                    ar = self.boss.hajotipustar[hajo].price - self.boss.hajotipustar[self.boss.aktivjatekos.hajo].price
                    Label(self.hajoframek[hajo], text = '%s: %i %s' % (self.master.szotar['price'], ar, self.master.szotar['gold'])).pack(side = LEFT, fill = X)
                else:
                    Label(self.hajoframek[hajo], text = self.master.szotar['already_bought']).pack(side=LEFT, fill=X)
            else:
                Label(self.hajoframek[hajo], text = '%s: %i %s' % (self.master.szotar['price'], self.boss.hajotipustar[hajo].price, self.master.szotar['gold'])).pack(side = LEFT, fill = X)
            self.hajoframek[hajo].pack(side = TOP, pady = 5, padx = 5, fill = X)
        self.penzszamolo()
        self.hajoacs.pack(fill = Y, pady = 5)

        
    def jutalomszamolo(self):
        "Megmutatja, mennyi jutalmat vehet át a játékos legfeljebb."
        hajotar = self.boss.aktivjatekos.hajotar
        pontszam = 0
        for birodalom in hajotar.keys():
            helyiPontszam = hajotar[birodalom].get()
            if helyiPontszam / 5 > 0:
                pontszam += int(helyiPontszam / 5)*7
                helyiPontszam = helyiPontszam%5
            if helyiPontszam / 3 > 0:
                pontszam += int(helyiPontszam / 3)*4
                helyiPontszam = helyiPontszam%3
            pontszam += helyiPontszam
        return pontszam
        
    def penzszamolo(self):
        "A játékos anyagi lehetőségeinek fényében engedélyezi a hajók vásárlását."
        if self.boss.aktivjatekos.hajo in self.boss.vehetoHajok:
            for hajo in self.boss.vehetoHajok:
                if hajo == self.boss.aktivjatekos.hajo:
                    self.hajogombok[hajo].config(state = DISABLED)
                elif self.boss.hajotipustar[hajo].price < self.boss.hajotipustar[self.boss.aktivjatekos.hajo].price:
                    self.hajogombok[hajo].config(state = DISABLED)
                elif self.boss.hajotipustar[hajo].price - self.boss.hajotipustar[self.boss.aktivjatekos.hajo].price > self.boss.aktivjatekos.kincs.get():
                    self.hajogombok[hajo].config(state = DISABLED)
                else:
                    self.hajogombok[hajo].config(state = NORMAL)
        else:
            for hajo in self.boss.vehetoHajok:
                if self.boss.hajotipustar[hajo].price > self.boss.aktivjatekos.kincs.get():
                    self.hajogombok[hajo].config(state = DISABLED)
                else:
                    self.hajogombok[hajo].config(state = NORMAL)
        self.berskalat_letrehoz()
                    
    def berskalat_letrehoz(self):
        "Létrehozza a skálát, a felbérelendő matrózok számának kijelöléséhez."
        berskalahossz = min((self.boss.hajotipustar[self.boss.aktivjatekos.hajo].crew_limit - self.boss.aktivjatekos.legenyseg.get()), self.matrozokszama.get(), self.boss.aktivjatekos.kincs.get())
        self.berskala.destroy()
        self.skalaCimke.destroy()
        if not berskalahossz:
            if self.boss.hajotipustar[self.boss.aktivjatekos.hajo].crew_limit - self.boss.aktivjatekos.legenyseg.get() == 0:
                visszajelzes = self.master.szotar['crew_ship_full']
            elif self.matrozokszama.get() == 0:
                visszajelzes = self.master.szotar['crew_port_empty']
            else:
                visszajelzes = self.master.szotar['crew_no_money']
            self.berskala = Label(self.line4, text = visszajelzes)
            self.felberel.config(state = DISABLED)
        else:
            self.berskala = Scale(self.line4, from_ = 0, to = berskalahossz,
                                  orient = HORIZONTAL, resolution = 1, takefocus = 0,
                                  showvalue = 0, command = self.berskalaErtek)
            self.skalaCimke = Label(self.line5)
            self.skalaCimke.pack()
            self.felberel.config(state = NORMAL)
        self.berskala.pack(side = TOP, fill = X)
        
    def berskalaErtek(self, event):
        self.skalaCimke.config(text = str(self.berskala.get()))
            
    def ujMatrozok(self):
        "A mezőre lépéskor módosítja a helyben elérhető matrózok számát."
        self.matrozokszama.set(self.matrozokszama.get() + self.boss.boss.menu.ful1tartalom.kocka.export_ertek())
        
    def matrozFelberelese(self):
        "Lebonyolítja a metrózok felbérelésével járó tranzakciót"
        delta = self.berskala.get()
        if not delta:
            return
        else:
            self.boss.aktivjatekos.set_legenyseg(delta)
            self.boss.aktivjatekos.set_kincs(-delta)
            self.matrozokszama.set(self.matrozokszama.get() - delta)
            self.berskalat_letrehoz()
        self.penzszamolo()
        
    def ujHajo(self, tipus = ''):
        "Lebonyolítja az új hajó vásárlásával járó tranzakciót"
        ar = self.boss.hajotipustar[tipus].price - self.boss.hajotipustar[self.boss.aktivjatekos.hajo].price
        self.boss.aktivjatekos.set_hajo(tipus)
        self.boss.aktivjatekos.set_kincs(-ar)
        self.boss.aktivjatekos.set_legenyseg_max(self.boss.hajotipustar[tipus].crew_limit)
        for hajo in self.boss.vehetoHajok:
            self.hajoframek[hajo].destroy()
            self.hajogombok[hajo].destroy()
        self.hajoacs_lekepez()
        
    def export_matroz(self):
        "Átadja saját adatait a mentéshez."
        return self.matrozokszama.get()
        
class Vezerlo(Frame):
    """Gondoskodik a játék folyamatáról."""
    def __init__(self, master = None, soros_jatekos = None, fogadoszotar = {}):
        Frame.__init__(self, master)
        # Alapváltozók
        self.methodeNo = 0
        self.unfinishedMethodes = []
        self.boss = master
        self.grogbaroLegyozve = BooleanVar()
        self.grogbaroLegyozve.set(False)
        self.hadnagyElokerult = BooleanVar()
        self.hadnagyElokerult.set(False)
        self.kincsKiasva = 0
        self.dobasMegtortent = BooleanVar()
        self.dobasMegtortent.set(False)
        self.korokSzama = 0
        self.nemKartyaStatusz = ["fold_fold"]
        # Hol mi történik
        self.teendotar = dict([('csata_francia',   lambda : self.csata("b0")),
                               ('csata_angol',     lambda : self.csata("b3")),
                               ('csata_holland',   lambda : self.csata("b1")),
                               ('csata_spanyol',   lambda : self.csata("b2")),
                               ('portroyal',       lambda : self.varos('portroyal')),
                               ('curacao',         lambda : self.varos('curacao')),
                               ('tortuga',         lambda : self.varos('tortuga')),
                               ('havanna',         lambda : self.varos('havanna')),
                               ('martinique',      lambda : self.varos('martinique')),
                               ('szelplusz90',     lambda : self.boss.tabla.szel_valtoztat(90)),
                               ('szelminusz90',    lambda : self.boss.tabla.szel_valtoztat(-90)),
                               ('szelplusz45',     lambda : self.boss.tabla.szel_valtoztat(45)),
                               ('szelminusz45',    lambda : self.boss.tabla.szel_valtoztat(-45)),
                               ('bermuda',         self.bermuda),
                               ('foldfold',        self.foldfold),
                               ('vihar',           self.vihar),
                               ('uszadek',         self.uszadek),
                               ('szelcsend',       self.szelcsend),
                               ('taino',           self.taino),
                               ('kincsessziget',   self.kincsessziget),
                               ('aramlat',         self.aramlat),
                               ('szamuzottek',     self.szamuzottekKozvetlen)
                               ])
        #A paklik előkészítése
        self.eventszotar = {}
        self.eventdeck = []
        self.eventstack = []
        self.kincsszotar = {}
        self.treasurestack = []
        eventtar, kincstar, penztar, fuggvenytar = self.boss.data_reader.load_cards_data()
        for lap in eventtar.keys():
            self.boss.tabla.kartyakep2(eventtar[lap])  # betöltjük a képet
            self.eventszotar[lap] = Kartya3(self, self.boss, lap, eventtar[lap], 'event', fuggvenytar[lap])
            self.eventdeck.append(lap)
        print("Kihúzható események:", len(self.eventdeck),"/ 52")
        self.csataszotar = self.boss.data_reader.load_battle_data()
        for csata in self.csataszotar.keys():
            if csata[0] != 'b':
                self.eventdeck.append(csata)
        print("Kihúzható események:", len(self.eventdeck),"/ 52")
        for penz in penztar.keys():
            iPenz = 0
            for i in range(penztar[penz]):
                self.kincsszotar['treasure'+penz+'_'+str(iPenz)] = Kartya3(self, self.boss, 'treasure', kincstar['treasure'], 'treasure', fuggvenytar["treasure"], int(penz))
                iPenz += 1
        print("kihúzható kincsek:", len(self.kincsszotar.keys()), "/ 30")
        for lap in kincstar.keys():
            self.boss.tabla.kartyakep2(kincstar[lap]) # betöltjük a képet
            if lap != 'treasure':
                self.kincsszotar[lap] = Kartya3(self, self.boss, lap, kincstar[lap], 'treasure', fuggvenytar[lap])
        self.kincspakli = list(self.kincsszotar.keys())
        print("kihúzható kincsek:", len(self.kincsszotar.keys()), "/ 52\n", self.kincspakli)
        # Hajók elkészítése
        self.hajotipustar = self.boss.data_reader.get_ship_types()
        for jatekos in self.boss.jatekossor:
            p = self.boss.jatekostar[jatekos]
            p.set_legenyseg_max(self.hajotipustar[p.hajo].crew_limit)
        self.vehetoHajok = []
        hajoarak = []
        for hajo in self.hajotipustar.keys():
            if self.hajotipustar[hajo].price > 0:
                hajoarak.append(self.hajotipustar[hajo].price)
                hajoarak = sorted(hajoarak)
                arPozicio = hajoarak.index(self.hajotipustar[hajo].price)
                self.vehetoHajok.insert(arPozicio,hajo)
        print('-'*40+'\nVásárolható hajók:',self.vehetoHajok,'\n'+'-'*40)
        # Városablakok előkészítése
        self.varostar = {}
        if fogadoszotar == {}:
            for varos in self.boss.tabla.kikotolista:
                self.varostar[varos] = Varos(self, self.boss, varos)
        else:
            for varos in self.boss.tabla.kikotolista:
                self.varostar[varos] = Varos(self, self.boss, varos, fogadoszotar[varos])
    
    def methodeNo_get(self):
        "Szekvenciát képez, amellyel figyelhető, hogy mikor melyik metódus hívódik meg."
        n = self.methodeNo
        self.methodeNo += 1
        self.unfinishedMethodes.append(n)
        return n
    
    def get_korokSzama(self):
        self.korokSzama += 1
        return self.korokSzama
        
    def set_hadnagyElokerult(self):
        "True-ra állítja a változó állapotát. Kizárólag Az áruló hadnagy nevű kártya hívhatja és a játékbetöltés."
        self.hadnagyElokerult.set(True)
        
    def set_grogbaroLegyozve(self):
        "True-ra állítja a változó állapotát. Kizárólag Az áruló hadnagy nevű kártya hívhatja és a játékbetöltés."
        self.grogbaroLegyozve.set(True)
    
    def szakasz_0(self):
        "A lépés előtti rész, szünet két játékos lépése között. Adminisztráljuk a váltást."
        id = self.methodeNo_get()
        #print("**MetódusID = " + str(id) + " - szakasz_0")
        if self.kincsKiasva:
            print('Vége a játéknak. A győztes:',self.aktivjatekos)
        if self.dobasMegtortent.get():
            self.boss.jatekossor.append(self.boss.jatekossor.pop(0)) # A legutóbb lépett játékost leghátra dobja, ha már lépett az aktív játékos
        self.aktivjatekos = self.boss.jatekostar[self.boss.jatekossor[0]]
        print('-'*20+'\n'+str(self.aktivjatekos.nev),'köre jön\n'+'-'*20) # logoláshoz
        self.master.naplo.log(self.master.szotar["new_turn"] % self.aktivjatekos.nev)
        self.dobasMegtortent.set(False)
        self.boss.menu.ful1feltolt(self.aktivjatekos)
        if "scurvy" in self.aktivjatekos.statuszlista:
            self.aktivjatekos.set_legenyseg(-1)
        self.boss.set_jatekforduloFolyamatban(0)
        if not self.aktivjatekos.kincskeresesKesz:
            if askyesno(self.boss.szotar["dig_for_treasure_label"], self.boss.szotar["dig_for_treasure_question"]):
                self.kincsesszigetAsas()
            else:
                self.aktivjatekos.set_kincskereses(True)
        #print("**MetódusID = " + str(id)+ " - szakasz_0 lezárva")
        self.unfinishedMethodes.remove(id)
        
    def szakasz_mezoevent(self):
        "A mező indukálta feladat elvégzése."
        id = self.methodeNo_get()
        #print("**MetódusID = " + str(id) + " - szakasz_mezoevent")
        self.boss.naplo.log('')
        if self.boss.kilepesFolyamatban:
            return
        #print(self.aktivjatekos.nev,'a(z)',self.boss.tabla.helyszotarR[self.aktivjatekos.pozicio],'mezőre lépett.')
        if 'grog_riot' in self.aktivjatekos.statuszlista:
            if self.boss.tabla.helyszotarR[self.aktivjatekos.pozicio] in self.master.tabla.kikotolista:
                self.aktivjatekos.set_statusz("grog_riot", 0)
                self.eventstack.append("grog_riot")
            else:
                self.eventszotar['grog_riot'].megjelenik()
        self.hivas = self.teendotar[self.boss.tabla.helyszotarR[self.aktivjatekos.pozicio]]()
        if self.hivas == False:
            self.szakasz_0()
        elif self.hivas == None:
            self.szakasz_kartyaevent()
        #print("**MetódusID = " + str(id) + " - szakasz_mezoevent lezárva")
        self.unfinishedMethodes.remove(id)
        
    def szakasz_kartyaevent(self):
        "Egy kártya húzása, és az általa hordozott feladat elvégzése."
        id = self.methodeNo_get()
        #print("**MetódusID = " + str(id) + " - szakasz_kartyaevent")
        if not self.eventdeck:
            for elem in self.eventstack:
                self.eventdeck.append(elem)
            self.eventstack = []
        kovetkezoLap = randrange(len(self.eventdeck))
        huz = self.eventdeck.pop(kovetkezoLap)
        if len(huz) < 4: #3
            #print('A kihúzott lap:',huz,';',self.csataszotar[huz])
            self.eventstack.append(huz) # eldobjuk a kártyát
            self.harc = Utkozet(self, self.boss, self.csataszotar[huz]) # lejátsszuk a csatát
        else:
            self.eventszotar[huz].megjelenik()
        #print("**MetódusID = " + str(id) + " - szakasz_kartyaevent lezárva")
        self.unfinishedMethodes.remove(id)
    
    def kimaradas(self):
        "Vezérli a kimaradást."
        self.aktivjatekos.set_kimarad()
        self.dobasMegtortent.set(True)
        self.szakasz_0()
    
    def set_paklik(self, pakli):
        "Visszatölti a mentésből származó paklieloszlásokat."
        ep, et, kp, kt = pakli
        self.eventdeck = ep
        self.eventstack = et
        self.kincspakli = kp
        self.treasurestack = kt
        print(self.eventdeck, self.eventstack, self.kincspakli, self.treasurestack)

    def set_dobasMegtortent(self):
        "Híváskor érvényteleníti a kockát."
        self.dobasMegtortent.set(True)
        if self.unfinishedMethodes:
            print("HIBA - Beragadt metódus:", self.unfinishedMethodes)
    
    def mozgas(self, dobas, szellel = 1):
        "Irányítja a mozgás folyamatát."
        if szellel:
            celok = self.boss.tabla.kormanyos(self.aktivjatekos.pozicio[0], self.aktivjatekos.pozicio[1], dobas)
        else:
            celok = self.boss.tabla.kormanyos(self.aktivjatekos.pozicio[0], self.aktivjatekos.pozicio[1], dobas, 0)
        self.boss.tabla.celkereso(celok)
        
    def kincsetHuz(self):
        if not self.kincspakli:
            print("Kincspakli keverése.")
            for elem in self.treasurestack:
                self.kincspakli.append(elem)
            self.treasurestack = []
        kovetkezoLap = randrange(len(self.kincspakli))
        huz = self.kincspakli.pop(kovetkezoLap)
        self.kincsszotar[huz].megjelenik()

    def varos(self, varosneve):
        "A várost működtető függvény."
        if "scurvy" in self.aktivjatekos.statuszlista:
            self.aktivjatekos.set_statusz("scurvy", 0)
        self.varostar[varosneve].aktival()
        return False
        
    def bermuda(self):
        "A Bermuda mező roppant izgalmas függvénye."
        showinfo(self.boss.szotar['info'], self.boss.szotar['bermuda'])
        
    def csata(self, csataId):
        "A csatát inicializáló függvény."
        harc = Utkozet(self, self.boss, self.csataszotar[csataId])
        return True

    def foldfold(self):
        "A játékos újra dobhat a következő körben, ha az eredeti dobás kedvezőtlen."
        showinfo(self.boss.szotar['info'], self.boss.szotar['land'])
        self.aktivjatekos.set_statusz("fold_fold")
        if "scurvy" in self.aktivjatekos.statuszlista:
            self.aktivjatekos.set_statusz("scurvy", 0)
        return

    def vihar(self):
        "A vihar mező függvénye."
        viharEreje = self.boss.menu.ful1tartalom.kocka.dob() # Dobunk, ez adja meg a vihar erejét.
        self.aktivjatekos.set_utolsodobas(viharEreje) # Mentjük a kocka állapotát.
        if "levasseur" in self.aktivjatekos.statuszlista: # Ha a játékos hajóján ott utazik Jacques Levasseur, több esélye van sikeresen navigálni.
            maxSiker = 4
        else:
            maxSiker = 3
        if viharEreje > maxSiker:
            if "spare_sail" in self.aktivjatekos.statuszlista: # Ha a játékosnak van pótvitorlája, megússza, hogy kimaradjon.
                self.aktivjatekos.set_statusz("spare_sail", 0) # Eldobja a vitorlát.
                self.treasurestack.append("spare_sail") # A vitorlakártya a talonba kerül.
                uzenet = self.boss.szotar["storm_sail_damage"]
                return
            else:
                self.aktivjatekos.set_kimarad(1) # Beállítjuk, hogy kimarad egy körből.
                uzenet = self.boss.szotar["storm_miss_turn"]
            showinfo(self.boss.szotar["info"], uzenet) # Kiírjuk, a történteket.
            return
        else:
            self.boss.naplo.log(self.boss.szotar["storm_success"])
            self.mozgas(viharEreje)
            self.szakasz_mezoevent()
            return True

    def uszadek(self):
        "Vajon sikerül kincsre bukkanni?"
        dobas = self.boss.menu.ful1tartalom.kocka.dob() # Szerencsét próbálunk.
        self.aktivjatekos.set_utolsodobas(dobas) # Mentjük a kocka állapotát.
        if dobas == 6:
            self.aktivjatekos.set_kincs(1)
            self.boss.naplo.log(self.boss.szotar["driftwood_success"])
        else:
            self.boss.naplo.log(self.boss.szotar["driftwood"])
        return

    def szelcsend(self):
        "Egy körből kimarad a játékos."
        self.aktivjatekos.set_kimarad(1) # Beállítjuk, hogy kimarad egy körből.
        showinfo(self.boss.szotar["info"], self.boss.szotar["calm"])
        return

    def taino(self):
        "Bennszülöttek csatlakoznak a legénységhez."
        maxFelvehetoBennszulott = self.aktivjatekos.legenyseg_max.get() - self.aktivjatekos.legenyseg.get()
        if maxFelvehetoBennszulott:
            dobas = self.boss.menu.ful1tartalom.kocka.dob() # Szerencsét próbálunk.
            self.aktivjatekos.set_utolsodobas(dobas) # Mentjük a kocka állapotát.
            if dobas >= maxFelvehetoBennszulott:
                self.aktivjatekos.set_legenyseg(maxFelvehetoBennszulott)
                felveve = maxFelvehetoBennszulott
            else:
                self.aktivjatekos.set_legenyseg(dobas)
                felveve = dobas
            if felveve < 2:
                self.boss.naplo.log(self.boss.szotar["taino_one"])
            else:
                self.boss.naplo.log(self.boss.szotar["taino_some"] % felveve)
        else:
            self.boss.naplo.log(self.boss.szotar["taino_none"])
        return

    def kincsessziget(self):
        "Egy mező, ahol kincset lehet ásni."
        self.aktivjatekos.set_kincskereses(False)
        self.boss.naplo.log(self.boss.szotar["dig_for_treasure"])
        
    def kincsesszigetAsas(self):
        "A teendők, ha már kincses szigeten áll az ember."
        self.boss.set_jatekforduloFolyamatban(1)
        self.dobasMegtortent.set(True)
        dobas = self.boss.menu.ful1tartalom.kocka.dob() # Szerencsét próbálunk.
        self.aktivjatekos.set_utolsodobas(dobas) # Mentjük a kocka állapotát.
        if dobas == 6:
            self.aktivjatekos.set_kincskereses(True)
            self.kincsetHuz()
        else:
            showinfo(self.boss.szotar["dig_for_treasure_label"], self.boss.szotar["dig_for_treasure_nothing"])
        self.szakasz_0()
    
    def aramlat(self):
        "Az áramlat függvénye"
        dobas = self.boss.menu.ful1tartalom.kocka.dob()
        self.aktivjatekos.set_utolsodobas(dobas)
        self.mozgas(dobas, 0)
        return True

    def szamuzottek(self, esent = None):
        "Ez történik, ha valaki legénység nélkül van a száműzöttek szigetén."
        self.boss.set_jatekforduloFolyamatban(1)
        self.dobasMegtortent.set(True)
        dobas = self.boss.menu.ful1tartalom.kocka.dob() # Szerencsét próbálunk.
        self.aktivjatekos.set_utolsodobas(dobas) # Mentjük a kocka állapotát.
        celokSzotar = dict([(1, "martinique"),
                            (2, "curacao"),
                            (3, "havanna"),
                            (4, "tortuga"),
                            (5, "portroyal")])
        if dobas == 6:
            uzenet = self.boss.szotar["castaway_no_hope"]
        else:
            if dobas == 5:
                varos = "Port Royal"
            else:
                varos = celokSzotar[dobas].capitalize()
            uzenet = self.boss.szotar["castaway_success"] % varos
            x,y = self.boss.tabla.helyszotar[celokSzotar[dobas]][0]
            self.boss.tabla.hajotathelyez(x,y)
            if self.aktivjatekos.kincs.get() < 10:
                self.aktivjatekos.kincs.set(0)
            else:
                self.aktivjatekos.kincs.set(self.aktivjatekos.kincs.get() - 10)
            self.aktivjatekos.set_legenyseg(10)
        showinfo(self.boss.szotar["info"], uzenet)
        self.master.jatekmenet.szakasz_0()
        return False
        
    def szamuzottekKozvetlen(self):
        "Teendő belelépés esetén."

    def leviathan_kijatszasa(self):
        "A leviatán megmenti a játékost a kimaradástól."
        self.aktivjatekos.set_statusz("leviathan", 0)
        self.eventstack.append("leviathan")
        self.aktivjatekos.set_kimarad()
        self.szakasz_0()
    
    
class Dobokocka(Canvas):
    """Megjelenít egy dobókockát, amely gombnyomásra létrehoz egy értéket."""
    def __init__(self, master, meret, szin, masodikszin, utolsodobas):
        Canvas.__init__(self, master = master, width = meret, height = meret, bd = 1, relief = RIDGE)
        self.ertek = utolsodobas
        self.boss = master
        self.meret = meret
        self.szin = szin
        self.masodikszin = masodikszin
        self.gomboclista = []
        self.helylista = [[(5,5)],
                          [(2,2), (8,8)],
                          [(8,2), (5,5), (2,8)],
                          [(2,2), (2,8), (8,2), (8,8)],
                          [(5,5), (2,2), (2,8), (8,2), (8,8)],
                          [(2,2), (2,8), (8,2), (8,8), (2,5), (8,5)]]
        self.x,self.y,self.c = self.meret/2,self.meret/2,self.meret/2 # a kocka középpontja és a fél oldalhossz
        self.create_rectangle(self.x - self.c + 2,
                              self.y - self.c + 2,
                              self.x + self.c + 2,
                              self.y + self.c + 2,
                              fill=szin, width=0)
        self.r = self.meret/10 # a gombócok sugarának mérete
        self.rajzol()
            
    def torol(self):
        "törli a gombócokat"
        for gomboc in self.gomboclista:
            self.delete(gomboc)
            
    def rajzol(self):
        "kirajzolja a gombócokat"
        for gombocx,gombocy in self.helylista[self.ertek-1]:
            self.gomboclista.append(self.create_oval((gombocx-1)*self.r + 2, (gombocy-1)*self.r + 2, (gombocx+1)*self.r + 2, (gombocy+1)*self.r + 2, fill = self.masodikszin))
            
    def dob(self):
        "elvégzi a dobást"  
        for i in range(6):
            self.torol()
            self.ertek = randrange(6)+1
            self.rajzol()
            self.update_idletasks()
            sleep(0.075)
        return self.ertek
    
    def export_ertek(self):
        "Átadja a kocka értékét."
        return self.ertek
