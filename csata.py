from tkinter import BooleanVar, BOTTOM, Button, CENTER, DISABLED, FLAT, Frame, GROOVE, IntVar, Label, LEFT, NORMAL, Radiobutton, RIGHT, StringVar, SUNKEN, TOP, Toplevel, X, Y
from tkinter.messagebox import askyesno
from random import randrange
from tkinter.tix import Balloon

class Utkozet(Toplevel):
    """Hajócsata függvény."""
    def __init__(self, boss, master, csatainfok, kovetkezoSzakasz = 0):
        Toplevel.__init__(self, master = boss)
        self.boss = boss
        self.master = master
        self.grab_set()
        self.kovetkezoSzakasz = kovetkezoSzakasz
        self.title(self.master.szotar['csata'])
        self.protocol("WM_DELETE_WINDOW", self.ablakBezarasa)
        self.resizable(width=0, height=0)
        self.ellensegesZaszlo, self.ellensegesHajoTipusa, self.ellensegesHajoNeve, self.ellensegesLegenyseg, self.zsakmany, self.kincskartyaHuzas = csatainfok
        if self.ellensegesHajoNeve[0:6] == "pirate":
            self.ellensegesHajoNeve = self.master.szotar["hajonev_"+self.ellensegesHajoNeve]
        self.gombok = ['pisztoly', 'puska', 'labtovis', 'granat', 'kartacs', 'gorogtuz', 'majom', 'szirenkurt', 'szirenek']
        self.jatekosMatrozaiFenn = BooleanVar()
        self.jatekosMatrozaiFenn.set(False)
        self.jatekosMatrozaiFenn.trace('w',self.keszGombConf)
        self.ellenfelSullyed = BooleanVar()
        self.sullyedesigHatravan = -1
        self.kincsMegszerezve = False
        self.kartyaHuzando = False
        self.fokeret()
        self.szabadKockaLista = []
        #-#
        self.update_idletasks()
        w, h = self.winfo_width(),self.winfo_height()
        bx, by = self.master.helymeghatarozas()
        bh, bw = self.master.height,self.master.width        
        self.geometry('+'+str(int(self.master.tabla.mezomeret/2+bx))+'+'+str(self.master.tabla.mezomeret+by))
        self.master.wait_window(self)
        
    def fokeret(self, dummy = 0):
        'Leképezi az ablak tartalmát'
        if dummy == 1:
            print('Győzelem')
            return True
        # játékos
        self.jatekos = Hajoablak(self, self.master, user = 1)
        self.jatekos.pack(side = LEFT, fill = Y, padx = 5, pady = 5, ipadx = 5, ipady = 5)
        # csatatér
        self.csatater = Frame(self, bd = 2, relief = GROOVE)
        gombsor = Frame(self.csatater)
        self.valosCelpontok = []
        self.valosCelpontKockak = []
        gombszotar = {}
        self.gombszotar = {}
        self.gombszotar['pisztoly'] = Pisztoly(self, self.master, gombsor)
        self.gombszotar['puska'] = Puska(self, self.master, gombsor)
        self.gombszotar['labtovis'] = Labtovis(self, self.master, gombsor)
        self.gombszotar['granat'] = Granat(self, self.master, gombsor)
        self.gombszotar['kartacs'] = Kartacs(self, self.master, gombsor)
        self.gombszotar['gorogtuz'] = Gorogtuz(self, self.master, gombsor)
        self.gombszotar['majom'] = Majom(self, self.master, gombsor)
        self.gombszotar['szirenkurt'] = Szirenkurt(self, self.master, gombsor)
        self.gombszotar['szirenek'] = Szirenek(self, self.master, gombsor)
        self.gombszotar['alvarez'] = Alvarez(self, self.master, gombsor)
        gombsor.pack(side = TOP)
        self.tooltip = Frame(self.csatater)
        self.tooltip.label = Label(self.tooltip, relief = SUNKEN, bd=1)
        self.tooltip.label.pack(fill = X)
        self.tooltip.pack(side = TOP, fill = X, padx = 5)
        self.interaktiv = Frame(self.csatater)
        self.textGombok = Frame(self.interaktiv)
        self.korOsszegzo = Label(self.interaktiv)
        self.csataIndulGomb = Button(self.textGombok, text = self.master.szotar['osszecsapas'], command = self.harcikor, state = DISABLED)
        self.csataIndulGomb.pack(side = BOTTOM, pady = 10)
        self.csataIndulGomb.pack_forget()
        self.csatakezdet()
        self.textGombok.pack(side = BOTTOM, pady = 10)
        self.korOsszegzo.pack(side = BOTTOM, pady = 20)
        self.interaktiv.pack(side = BOTTOM)        
        self.csatater.pack(side = LEFT, fill = Y, pady = 5, ipadx = 5, ipady = 5)
        # ellenfél
        self.ellenfel = Hajoablak(self, self.master)
        self.labtovis = 0
        self.ellenfel.pack(side = LEFT, fill = Y, padx = 5, pady = 5, ipadx = 5, ipady = 5)
        
    def csatakezdet(self):
        "Ellátja a játékost a kezdeti információkkal."
        if self.master.jatekmenet.aktivjatekos.zaszlo == 'kaloz':
            tamad = randrange(2)
        elif self.ellensegesZaszlo == "kaloz":
            tamad = 1
        else:
            tamad = 0
        if tamad:
            self.korOsszegzo.config(text = self.master.szotar["hajoalathataron_kaloz"])
        else:
            self.korOsszegzo.config(text = self.master.szotar["hajoalathataron"])
        self.csataGombLista = {}
        for buttonText,command in ("hajoalathataron_agyuzas",self.agyuzas),("hajoalathataron_megcsaklyazas",self.megcsaklyazas),("hajoalathataron_futnihagyas",self.futnihagy),("hajoalathataron_menekules",self.menekules):
            self.csataGombLista[buttonText] = Button(self.textGombok, text = self.master.szotar[buttonText], command = command)
            self.csataGombLista[buttonText].pack(side = LEFT, padx = 3)
        if tamad:
            self.csataGombLista["hajoalathataron_futnihagyas"].pack_forget()
        else:
            self.csataGombLista["hajoalathataron_menekules"].pack_forget()
            
    def futnihagy(self):
        "Elvonulás a csatából harc nélkül."
        if self.ellenfelSullyed.get() and "papagaj" in self.master.aktivjatekos.statuszlista:
            for gomb in self.csataGombLista.keys():
                self.csataGombLista[gomb].pack_forget()
            self.korOsszegzo.config(text = "")
            self.boss.kincsMegszerzese(papagaj = 1)
        else:
            self.bezar()
            
    def menekules(self):
        "Menekülési függvény, ha a játékos hajója kisebb, sikeres a menekülés."
        if self.boss.hajotipustar[self.ellensegesHajoTipusa].ar < self.boss.hajotipustar[self.master.jatekmenet.aktivjatekos.hajo].ar:
            self.megcsaklyazas()
            self.korOsszegzo.config(text = (self.master.szotar["hajoalathataron_menekules_sikertelen"] + "\n" + self.master.szotar["hajoalathataron_harc"]))
        else:
            print(self.master.jatekmenet.aktivjatekos.nev + " elmenekült.")
            self.bezar()
        
    def megcsaklyazas(self):
        "A közelharcot indító függvény."
        self.korOsszegzo.config(text = self.master.szotar["hajoalathataron_harc"])
        for gomb in self.csataGombLista.keys():
            self.csataGombLista[gomb].pack_forget()
        self.csataIndulGomb.pack(side = BOTTOM, pady = 10)
        self.jatekos.skalaablak.pack()
        self.ellenfel.skalaablak.pack()
        
    def agyuzas(self):
        "Az ágyúzás függvénye."
        eredmeny = ""
        visszaloves = True
        # Játékos lő az ellenfélre
        dobas = 1#randrange(1,7)
        minusz = 0
        if self.ellensegesLegenyseg[dobas-1] == 'underWaterHit':
            self.ellenfelSullyed.set(True)
            self.sullyedesigHatravan = 2
            eredmeny += (self.master.szotar["hajoalathataron_veszteseg_sullyed"])
        elif self.ellensegesLegenyseg[dobas-1] == 'powderStore':
            self.ellenfelSullyed.set(True)
            self.sullyedesigHatravan = 0
            for gomb in self.csataGombLista.keys():
                self.csataGombLista[gomb].pack_forget()
            self.harcfeltetelek_vizsgalata()
            self.csataIndulGomb.configure(text = self.master.szotar['kesz'], command = self.bezar, state = NORMAL)
            self.csataIndulGomb.pack()
            eredmeny += (self.master.szotar["hajoalathataron_loporraktar"])
        else:
            if self.ellenfel.skalaszotar[dobas].value.get() > 1:
                minusz = 2
            elif self.ellenfel.skalaszotar[dobas].value.get() == 1:
                minusz = 1
            self.ellenfel.skalaszotar[dobas].erteket_beallit(self.ellenfel.skalaszotar[dobas].value.get()-minusz)
            eredmeny += (self.master.szotar["hajoalathataron_veszteseg_ellenfel"] % minusz)            
        # Ellenfél lő a játékosra
        dobas2 = randrange(1,7)
        lehetsegesCsapatok = self.master.jatekmenet.aktivjatekos.legenyseg.get() / 6
        if lehetsegesCsapatok > dobas2:
            self.master.jatekmenet.aktivjatekos.legenyseg.set(self.master.jatekmenet.aktivjatekos.legenyseg.get()-2)
            self.jatekos.maxLegenyseg = self.master.jatekmenet.aktivjatekos.legenyseg.get()
            if eredmeny != "":
                eredmeny += "\n"
            eredmeny += (self.master.szotar["hajoalathataron_veszteseg_jatekos"])
        # Eredménykijelzés
        self.korOsszegzo.config(text = eredmeny)
        self.jatekos.osszegzoFelirat.vege = '/'+str(self.jatekos.maxLegenyseg)
        self.jatekos.osszegzoFelirat.set(self.jatekos.osszegzoFelirat.eleje+str(self.jatekos.kiosztottLegenyseg.get())+self.jatekos.osszegzoFelirat.vege)
        self.ellenfel.osszegzoFelirat.set(self.ellenfel.osszegzoFelirat.eleje+str(self.ellenfel.kiosztottLegenyseg.get())+'/'+str(self.ellenfel.maxLegenyseg))
        self.csataGombLista["hajoalathataron_agyuzas"].config(state = DISABLED)
        
    def csataIndul(self):
        'Letiltja a csatapok átrendezését.'
        self.jatekos.mindentLetilt()
        self.jatekos.eloszamol()
        self.ellenfel.eloszamol()
        for gomb in self.gombszotar.keys():
            if self.gombszotar[gomb].nev in self.master.jatekmenet.aktivjatekos.statuszlista:
                self.gombszotar[gomb].cooling()
        self.korOsszegzo.config(text = self.master.szotar["hajoalathataron_csataindul"])
        self.csataIndulGomb.configure(state = NORMAL)
        
    def csataIndul2(self):
        'Letiltja a csatapok átrendezését.'
        self.jatekos.mindentLetilt()
        self.jatekos.eloszamol()
        self.ellenfel.eloszamol()
        self.korOsszegzo.config(text = self.master.szotar["hajoalathataron_csataindul"])
        self.csataIndulGomb.configure(state = NORMAL)
    
    def harcikor(self):
        "Levezényel egy harci kört."
        print('-----------------Új kör')
        self.csataIndulGomb.configure(state = DISABLED)
        for gomb in self.gombszotar.keys():
            self.gombszotar[gomb].gomb.configure(state = DISABLED)
        jatekosCsapatai,ellenfelCsapatai = self.jatekos.ertekkeszlet(),self.ellenfel.ertekkeszlet()
        jatekosDobasai,ellenfelDobasai = self.dobas(len(jatekosCsapatai)),self.dobas(len(ellenfelCsapatai)-self.labtovis)
        for kocka in ellenfelDobasai:
            self.jatekos.talalat(kocka)
        self.szabadKockaLista = []
        for kocka in jatekosDobasai:
            talalt = self.ellenfel.talalat(kocka)
            if not talalt:
                self.szabadKockaLista.append(kocka)
        if len(self.szabadKockaLista) > 1:
            self.extra_talalatok()
        else:
            self.harcikor_vege()
        
    def extra_talalatok(self):
        "Implementálja a szabad kockák kezelését"
        self.valosCelpontok = []
        self.valosCelpontKockak = []
        celpontok,celpontKockak = self.szabadKockak(self.szabadKockaLista)
        print("Lehetséges célpontok:",celpontok,"Ahogy a kockákból összeáll:",celpontKockak)
        for celpont in celpontok:
            if self.ellenfel.skalaszotar[celpont].elo.get():
                print('Célba vett csapat: ',celpont,'Ennyi matróz van benne:',self.ellenfel.skalaszotar[celpont].elo.get())
                self.valosCelpontok.append(celpont)
                self.valosCelpontKockak.append(celpontKockak[celpontok.index(celpont)])
            else:
                print('Csapat üres, célpont kizárva.')
        print(self.valosCelpontok, self.valosCelpontKockak)
        if self.valosCelpontok:
            if len(self.valosCelpontok) == 1:
                print("AutoExtra")
                self.ellenfel.valasztottCsapat.set(self.valosCelpontok[0])
                self.ellenfel.celzas()
            else:
                self.ellenfel.celpontotMegjelol(self.valosCelpontok)
                self.korOsszegzo.configure(text = self.master.szotar['extra'])
        else:
            self.harcikor_vege()
        
    def harcikor_vege(self):
        self.korOsszegzo.config(text = self.master.szotar["hajoalathataron_csataindul"])
        vege_a_harcnak = self.harcfeltetelek_vizsgalata()
        if not vege_a_harcnak:
            for gomb in self.gombszotar.keys():
                self.gombszotar[gomb].cooling()
            if self.ellenfelSullyed.get():
                self.sullyedesigHatravan += -1
        self.valosCelpontok = []
        self.valosCelpontKockak = []
        self.csataIndulGomb.configure(state = NORMAL)
    
    def harcfeltetelek_vizsgalata(self):
        "Ellenőrzi, tart-e még a harc."
        if self.harc_vege():
            self.csataIndulGomb.configure(text = self.master.szotar['kesz'], command = self.bezar)
            for gomb in self.gombszotar.keys():
                self.gombszotar[gomb].gomb.configure(state = DISABLED)
            return True
        else:
            return False
    
    def szabadKockak(self, szabadKockak):
        "Kiszámolja a lehetséges szabadkocka felhasználási módokat."
        print('Szabad kockák:',szabadKockak)
        ertekkeszlet = []
        ertekkeszletKockak = []
        for dobas in szabadKockak:
            tobbiKocka = []
            for i in szabadKockak:
                tobbiKocka.append(i)
            tobbiKocka.remove(dobas)
            for dobas2 in tobbiKocka:
                xo = dobas + dobas2     # összeg
                xm = dobas - dobas2     # maradék
                xsz = dobas * dobas2    # szorzat
                xh = dobas / dobas2     # hányados
                for eredmeny in [xo,xm,xsz,xh]:
                    if self.vizsgal(eredmeny) and eredmeny not in ertekkeszlet:
                        ertekkeszlet.append(int(eredmeny))
                        ertekkeszletKockak.append((dobas,dobas2))
        return ertekkeszlet,ertekkeszletKockak
                    
    def vizsgal(self,x):
        if 0 < x < 7 and x == int(x):
            return True
        else:
            return False
        
    def harc_vege(self):
        "Ellenőrzi a felek harcképességét."
        if not self.jatekos.ertekkeszlet():
            print('Vesztítettél.')
            self.korOsszegzo.configure(text = self.master.szotar["csata_elvesztese"])
            self.vereseg()
            return True
        elif (len(self.jatekos.ertekkeszlet()) == 1 and not len(self.ellenfel.ertekkeszlet())) or (len(self.jatekos.ertekkeszlet()) > 1 and len(self.ellenfel.ertekkeszlet()) < 2):
            print('Győztél.')
            self.matroztVisszair() # mentjük a megmaradt matrózok számát a játékos profiljába
            self.master.jatekmenet.aktivjatekos.hajotar[self.ellensegesZaszlo].set(self.master.jatekmenet.aktivjatekos.hajotar[self.ellensegesZaszlo].get()+1) # megnöveljük az elfogott hajók számát
            if not self.kincsMegszerezve:
                self.kincsMegszerzese()
            else:
                self.korOsszegzo.config(text = "")
            return True
        elif self.ellenfelSullyed.get() and not self.sullyedesigHatravan:
            print("Az ellenséges hajó elsüllyedt.")
            self.matroztVisszair() # mentjük a megmaradt matrózok számát a játékos profiljába
            self.master.jatekmenet.aktivjatekos.hajotar[self.ellensegesZaszlo].set(self.master.jatekmenet.aktivjatekos.hajotar[self.ellensegesZaszlo].get()+1) # megnöveljük az elfogott hajók számát
            self.korOsszegzo.config(text = self.master.szotar["csata_elsullyed"])
            return True
        else:
            return False
            
    def vereseg(self):
        "Ez történik, ha a játékost veszít vagy kilép."
        self.matroztVisszair() # mentjük a megmaradt matrózok számát a játékos profiljába
        self.master.tabla.hajotathelyez(5,2) # irány a hajótöröttek szigete
        if "foldfold" in self.master.jatekmenet.aktivjatekos.statuszlista:
            self.master.jatekmenet.aktivjatekos.set_statusz("foldfold", 0)
        self.master.jatekmenet.aktivjatekos.set_kincskereses(True)
            
    def ablakBezarasa(self):
        if askyesno(self.master.szotar["csata_elhagyasa"], self.master.szotar["csata_elhagyasa_szoveg"], parent = self):
            self.vereseg()
            self.bezar()
        else:
            self.focus_set()
            return
        
    def dobas(self, hany):
        'Elvégzi a dobást'
        x = []
        for i in range(hany):
            y = randrange(1,7)
            x.append(y)
        return x

    def keszGombConf(self, x = None, y = None, z = None):
        'Tilja és engedélyezi a csataindító gombot.'
        if self.jatekosMatrozaiFenn.get():
            self.jatekos.kesz.configure(state = NORMAL)
        else:
            self.jatekos.kesz.configure(state = DISABLED)        
            
    def szabadKockaListaCsokkent(self, ertek):
        "Eltávolítja a szabadKockaListából a már elhasznált szabad kockákat, majd újra támad, ha még lehet."
        idx = self.valosCelpontok.index(ertek)
        for elem in self.valosCelpontKockak[idx]:
            self.szabadKockaLista.remove(elem)
            print("A szabad kockák közül törölve:",elem)
        print("Megmaradt szabad kockák:",self.szabadKockaLista)
        if len(self.szabadKockaLista) > 1:
            print('További extra lövésre van lehetőség.')
            self.extra_talalatok()
        else:
            print('Nincs több extra lövésre lehetőség.')
            self.harcikor_vege()
    
    def kincsMegszerzese(self, papagaj = 0):
        "Átadja a zsákmányt a játékosnak."
        if self.kincskartyaHuzas:
            szoveg2 = self.master.szotar["hajoalathataron_jutalom2"]
            self.kartyaHuzando = True
        else:
            szoveg2 = ""
        szoveg = self.master.szotar["hajoalathataron_jutalom"] % (self.zsakmany,szoveg2)
        if papagaj:
            szoveg = self.master.szotar["hajoalathataron_papagaj"] + szoveg
        self.master.jatekmenet.aktivjatekos.kincs.set(self.master.jatekmenet.aktivjatekos.kincs.get()+self.zsakmany)
        print(self.master.jatekmenet.aktivjatekos.kincs.get())
        self.korOsszegzo.config(text = szoveg)
        self.kincsMegszerezve = True

    def matroztVisszair(self):
        "Visszaadja a játékosadatnak a megmaradt matrózok számát."
        visszairando = 0
        for i in self.jatekos.skalaszotar.keys():
            visszairando += self.jatekos.skalaszotar[i].elo.get()
        print("Életben maradt matrózok:",visszairando)
        self.master.jatekmenet.aktivjatekos.legenyseg.set(visszairando)        

    def bezar(self):
        "Bezárja a csataképernyőt."
        self.destroy()
        if self.kartyaHuzando:
            self.master.jatekmenet.kincsetHuz()
        if self.kovetkezoSzakasz == 0:
            self.boss.szakasz_0()
        
class Hajoablak(Frame):
    """A játékosok és ellenfeleik megjelenítésére szolgál."""
    def __init__(self, boss, master, user = 0):
        Frame.__init__(self, master = boss, bd = 2, relief = GROOVE)
        cimStilus = 'helvetica 14 bold'
        self.boss = boss
        self.master = master
        self.maxLegenyseg = self.master.jatekmenet.aktivjatekos.legenyseg.get()
        self.kiosztottLegenyseg = IntVar()
        self.kiosztottLegenyseg.set(0)
        self.osszegzoFelirat = StringVar()
        self.osszegzoFelirat.eleje = self.master.szotar['legenyseg']+': '
        self.osszegzoFelirat.vege = '/'+str(self.maxLegenyseg)
        self.osszegzoFelirat.set(self.osszegzoFelirat.eleje+str(self.kiosztottLegenyseg.get())+self.osszegzoFelirat.vege)
        self.full = BooleanVar()
        self.full.set(False)
        self.full.trace('w',self.csataIndulConf)
        self.skalaszotar = {}
        self.aktivCsapatok = IntVar()
        if user:
            self.kiosztottLegenyseg.trace('w',self.matrozValtozas)
            self.hossz = 6
        else:
            self.valasztottCsapat = IntVar()
            csapatok = []
            for i in boss.ellensegesLegenyseg:
                if isinstance(i, int):
                    csapatok.append(i)
            self.hossz = 6 #max(csapatok)
        # Adatgenerálás
        if user:
            nev = self.master.szotar["hajonev_jatekos"]
            reszletek = '%s %s' % (self.master.szotar[self.master.jatekmenet.aktivjatekos.zaszlo], self.master.szotar[self.master.jatekmenet.aktivjatekos.hajo])
        else:
            nev = boss.ellensegesHajoNeve
            reszletek = '%s %s' % (self.master.szotar[boss.ellensegesZaszlo], self.master.szotar[boss.ellensegesHajoTipusa])
        # Képablak
        kepkeret = Frame(self, height = self.master.tabla.mezomeret, width = self.master.tabla.mezomeret)
        kepkeret.pack_propagate(0)
        if user:
            kep = self.master.tabla.hajotar[self.master.jatekmenet.aktivjatekos.nev]
        else:
            kep = self.master.tabla.keptar[self.boss.ellensegesHajoTipusa]
        Label(kepkeret, image = kep).pack(side = BOTTOM)
        kepkeret.pack()
        # Hajó neve
        Label(self, text = nev, font = cimStilus).pack()
        Label(self, text = reszletek).pack()
        # Skálák
        self.skalaablak = Frame(self)
        for i in range(1,7):
            self.skalaszotar[i] = MatrozSkala(self.skalaablak, self, self.master, user, boss.ellensegesLegenyseg[i-1], radioValue = i, hossz = self.hossz)
            self.skalaszotar[i].pack()
        elosztas = Frame(self.skalaablak)
        Label(elosztas, textvariable = self.osszegzoFelirat).pack()
        pult = Frame(elosztas)
        if user:
            self.auto = Button(pult, text = self.master.szotar['autoElosztas'], command = self.autoElosztas)
            self.auto.pack(side = LEFT, padx = 3)
            self.kesz = Button(pult, text = self.master.szotar['kesz'], command = self.boss.csataIndul, state = DISABLED)
            self.kesz.pack(side = LEFT, padx = 3)
        pult.pack()
        elosztas.pack(fill = X)
        # Utókozmetikázás az ellenfél mutatóján
        if not user:
            self.maxLegenyseg = 0
            for i in range(1,7):
                self.maxLegenyseg += self.skalaszotar[i].value.get()
            self.kiosztottLegenyseg.set(self.maxLegenyseg)
            self.osszegzoFelirat.set(self.osszegzoFelirat.eleje+str(self.kiosztottLegenyseg.get())+'/'+str(self.maxLegenyseg))
            
    def autoElosztas(self):
        "Működteti az automatikus elosztást végző gombot"
        autoLista = [5, 3, 4, 2, 6] # statisztikailag ez kedvez legjobban a játékosnak
        legenyseg = self.maxLegenyseg
        alapletszam = int(legenyseg/6)
        maradek = legenyseg%6
        skalaAlapok = [alapletszam]*6
        if maradek > 0:
            for i in range(maradek):
                skalaAlapok[autoLista[i]-1] += 1
        for i in range(1,7):
            self.skalaszotar[i].erteket_beallit(skalaAlapok[i-1])
    
    def matrozValtozas(self, x=0, y=0, z=0):
        "Ha minden matrózt kiosztott a játékos, megakadályozza, hogy többet osszon ki."
        if self.kiosztottLegenyseg.get() == self.maxLegenyseg:
            for i in range(1,7):
                self.skalaszotar[i].pluszgomb.configure(state = DISABLED)
            self.full.set(True)
        elif self.full.get() and self.kiosztottLegenyseg.get() < self.maxLegenyseg:
            for i in range(1,7):
                self.skalaszotar[i].letilto()
            self.full.set(False)
        self.osszegzoFelirat.set(self.osszegzoFelirat.eleje+str(self.kiosztottLegenyseg.get())+'/'+str(self.maxLegenyseg))
        
    def mindentLetilt(self):
        "Minden változtatást letilt a táblán."
        for i in range(1,7):
            self.skalaszotar[i].letilto(all = 1)
        self.auto.configure(state = DISABLED)
        self.kesz.configure(state = DISABLED)
        
    def mindentEngedelyez(self):
        "Minden változtatást engedélyez a táblán, Alvarez parancsára."
        self.boss.csataIndulGomb.config(state = DISABLED)
        for i in range(1,7):
            self.skalaszotar[i].minuszgomb.config(state = NORMAL)
            self.skalaszotar[i].pluszgomb.config(state = NORMAL)
        self.matrozValtozas()
        self.auto.configure(state = NORMAL)
        self.kesz.configure(state = NORMAL, command = self.boss.csataIndul2)
            
    def csataIndulConf(self, x = None, y = None, z = None):
        "Állítja a szülőkeret azonos paraméterét"
        self.boss.jatekosMatrozaiFenn.set(self.full.get())
        
    def ertekkeszlet(self):
        "Visszaadja az aktív csapatok méretét egy listaként. Amennyiben a csapat inaktív, azaz nem tartalmaz matrózt, nem kerül nulla a listába."
        ertekek = []
        for i in range(1,7):
            x = self.skalaszotar[i].elo.get()
            if x > 0:
                ertekek.append(x)
        return ertekek
    
    def eloszamol(self):
        for i in self.skalaszotar.keys():
            self.skalaszotar[i].eloszamol()
    
    def talalat(self, csapatszam):
        "Végrehajtja a találat ellenőrzését, amennyiben nem történt sérülés, False értékkel tér vissza."
        if self.skalaszotar[csapatszam].elo.get():
            self.skalaszotar[csapatszam].talalat()
            self.csatafelirat()
            return True
        else:
            return False
            
    def celpontotMegjelol(self, megjelolendoCelpontok):
        "Megjelöli a választható célpontokat, és a választottat adja eredményül."
        for i in megjelolendoCelpontok:
            self.skalaszotar[i].radio.configure(state = NORMAL)
    
    def celzas(self):
        "Szabad kockás célzás."
        ertek = self.valasztottCsapat.get()
        self.celzas_sima(ertek)
        if self.boss.valosCelpontKockak:
            self.boss.szabadKockaListaCsokkent(ertek)
    
    def celzas_sima(self, ertek):
        "Végrehajtja a játékos által célzott támadást."
        self.skalaszotar[ertek].talalat()
        self.csatafelirat()
        self.boss.korOsszegzo.configure(text = '')
        self.valasztottCsapat.set(0)
        for i in self.skalaszotar.keys():
            self.skalaszotar[i].radio.configure(state = DISABLED)
        
    def csatafelirat(self):
        "Figyelemmel kíséri a létszámváltozásokat, és frissíti a felületet."
        x = 0
        y = 0
        for i in self.skalaszotar.keys():
            if self.skalaszotar[i].elo.get():
                x += self.skalaszotar[i].elo.get()
                y += 1
        self.osszegzoFelirat.set(self.master.szotar['letszam'] % (x,y))
        
    def maxLegenyseg_set(self, ertek):
        "Állítja a maxLegenyseg változót."
        self.maxLegenyseg = ertek
    
class MatrozSkala(Frame):
    """Matrózok elrendezésére szolgál"""
    def __init__(self, boss2, boss, master, user = 0, ellensegesLegenyseg = 0, radioValue = 0, hossz = 6):
        Frame.__init__(self, master = boss2)
        if isinstance(ellensegesLegenyseg, str):
            ellensegesLegenyseg = 0
        self.boss = boss
        self.root = master
        self.ures = self.root.tabla.keptar['matroz0']
        self.teli = self.root.tabla.keptar['matroz1']
        self.serult = self.root.tabla.keptar['matroz2']
        self.value = IntVar()
        self.elo = IntVar()
        if user:
            self.minuszgomb = Button(self, text = '-', command = self.minusz, state = DISABLED)
            self.minuszgomb.pack(side = LEFT)
        self.matrozszotar = {}
        for i in range(1,hossz+1):
            self.matrozszotar[i] = Label(self, image = self.ures)
            if user:
                self.matrozszotar[i].pack(side = LEFT)
            else:
                self.matrozszotar[i].pack(side = RIGHT)
        if user:
            self.pluszgomb = Button(self, text = '+', command = self.plusz)
            self.pluszgomb.pack(side = LEFT)
            self.value.trace('w',self.letilto)
            self.value.set(0)
        else:
            self.radio = Radiobutton(self, var = self.boss.valasztottCsapat, value = radioValue, state = DISABLED, command = self.boss.celzas)
            self.radio.pack(side = RIGHT)
            self.value.set(0)
            self.erteket_beallit(ellensegesLegenyseg)
            
    def letilto(self, x=0, y=0, z=0, all=0):
        if all:
            self.pluszgomb.configure(state = DISABLED)
            self.minuszgomb.configure(state = DISABLED)
        elif self.value.get() == 6:
            self.pluszgomb.configure(state = DISABLED)
            self.minuszgomb.configure(state = NORMAL)
        elif 0 < self.value.get() < 6 and self.boss.kiosztottLegenyseg.get() < self.boss.maxLegenyseg:
            self.pluszgomb.configure(state = NORMAL)
            self.minuszgomb.configure(state = NORMAL)
        elif self.value.get() == 0:
            self.minuszgomb.configure(state = DISABLED)
            self.pluszgomb.configure(state = NORMAL)
            
    def erteket_beallit(self, ertek):
        'Beállítja a skálát a kívánt értékre'
        if self.value.get() == ertek:
            return
        elif self.value.get() < ertek:
            for i in range(ertek-self.value.get()):
                self.plusz()
        else:
            for i in range(self.value.get()-ertek):
                self.minusz()
    
    def plusz(self):
        'Kijelzi a matrózok létszámának változását.'
        self.value.set(self.value.get()+1)
        self.matrozszotar[self.value.get()].configure(image = self.teli)
        self.boss.kiosztottLegenyseg.set(self.boss.kiosztottLegenyseg.get()+1)
        
    def minusz(self):
        'Kijelzi a matrózok létszámának változását.'
        self.matrozszotar[self.value.get()].configure(image = self.ures)
        self.value.set(self.value.get()-1)
        self.boss.kiosztottLegenyseg.set(self.boss.kiosztottLegenyseg.get()-1)
        
    def eloszamol(self):
        self.elo.set(self.value.get())
    
    def talalat(self):
        "A csapat veszít egy matrózt."
        self.matrozszotar[self.elo.get()].configure(image = self.serult)
        self.elo.set(self.elo.get()-1)

class Gombjektum():
    """Egy-egy gomb/kártya/lehetőség alapvető logikai reprezentációja."""
    def __init__(self, boss, master, hely, nev):
        self.boss = boss
        self.master = master
        self.nev = nev
        self.cooldown = 0
        keret = Frame(hely)
        self.hang = ""
        self.gomb = Button(keret, image = master.tabla.keptar['ikon_'+nev], relief = FLAT, command = self.hasznalat, state = DISABLED)
        self.gomb.pack(side = TOP)
        Label(keret, text = master.kartyaszotar[nev][0], wraplength = 55).pack(side = TOP)
        keret.pack(side = LEFT, fill = Y)
        self.talon = self.master.jatekmenet.kincstalon
        self.tooltipSzoveg = self.master.kartyaszotar[self.nev][1]
        self.gomb.bind("<Enter>", self.tooltipMutat)
        self.gomb.bind("<Leave>", self.tooltipRejt)
        
    def tooltipMutat(self, event):
        "Mutatja a súgómezőben a súgószöveget."
        self.boss.tooltip.label.config(text = self.tooltipSzoveg)
        
    def tooltipRejt(self, event):
        "Törli a súgómezőből a súgószöveget."
        self.boss.tooltip.label.config(text = "")
        
    def cooling(self):
        "Megvalósítja a cooldown-kezelést."
        if self.nev in self.master.jatekmenet.aktivjatekos.statuszlista:
            if self.cooldown > 1:
                self.cooldown += -1
            elif self.cooldown in [0,1]:
                self.cooldown = 0
                self.gomb.configure(state = NORMAL)
            
    def mukodes(self):
        "A gomb fő működésfüggvénye. Minden egyes származtatott osztálynak felül kell írnia ezt a függvényt!"
        pass
        
    def hasznalat(self):
        "Meghívja a működést, majd futtat egy feltételvizsgálatot."
        print(self.hang)
        for i in self.boss.gombszotar.keys():
            self.boss.gombszotar[i].gomb.config(state = DISABLED)
        self.mukodes()
        self.cooldown = self.maxCoolDown
        self.gomb.configure(state = DISABLED)
        vege_a_harcnak = self.boss.harcfeltetelek_vizsgalata()
        
    def eldobas(self):
        "Eldobja a játék kártyáját."
        self.master.jatekmenet.aktivjatekos.statuszlista.remove(self.nev)
        self.talon.append(self.nev)

class Pisztoly(Gombjektum):
    """A pisztoly objektum."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, 'pisztoly')
        self.maxCoolDown = 2
        self.hang = "Piff!"
        
    def mukodes(self):
        dobas = randrange(1,7)
        if self.boss.ellenfel.skalaszotar[dobas].elo.get(): # Ha a dobás talált (van a dobott számú csapatban matróz),
            self.boss.ellenfel.celzas_sima(dobas)           # törlünk belőle egyet.
        
class Puska(Gombjektum):
    """Pisztoly módosulat."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, 'puska')
        self.maxCoolDown = 3
        self.hang = "Puff!"
        
    def mukodes(self):
        self.boss.csataIndulGomb.configure(state = DISABLED)
        # dobunk
        dobas = randrange(1,7)
        # amennyiben értelmes, vesszük a szomszéd értékeket is
        celpontok = [dobas-1, dobas, dobas+1]
        for celpont in celpontok:
            if 7 > celpont > 0:
                pass
            else:
                celpontok.remove(celpont)
        celpontok2 = []
        for celpont in celpontok:
            if self.boss.ellenfel.skalaszotar[celpont].elo.get():
                celpontok2.append(celpont)
            else:
                print('Célpont',celpont,'eltávolítva.')
        if not celpontok2:
            print("Mellé.")
        elif len(celpontok2) == 1:
            print("AutoCélzás.")
            self.boss.ellenfel.celzas_sima(celpontok2[0])
            self.boss.csataIndulGomb.configure(state = NORMAL)
        else:
            self.boss.ellenfel.celpontotMegjelol(celpontok2)
            self.boss.korOsszegzo.configure(text = self.master.szotar['celzas'])
            self.figyelo = self.boss.ellenfel.valasztottCsapat.trace('w',self.mukodes2)
            
    def mukodes2(self, x, y, z):
        self.boss.ellenfel.valasztottCsapat.trace_vdelete('w',self.figyelo)
        self.boss.csataIndulGomb.configure(state = NORMAL)
                
class Labtovis(Gombjektum):
    """Az ellefél eggyel kevesebb kockával játszhat. Egyszeri használat után eldobandó."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, 'labtovis')
        self.maxCoolDown = -1
        self.hang = "**Szétgurul.**"
        
    def mukodes(self):
        self.eldobas()
        self.boss.labtovis = 1
        self.gomb.configure(relief = SUNKEN, command = self.mukodes2)
        
    def mukodes2(self):
        pass
                
class Granat(Gombjektum):
    """Elsöpör egy tetszőleges ellenséges csapatot. Egyszeri használat után eldobandó."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, 'granat')
        self.maxCoolDown = -1
        self.hang = "Durrrrr!"
        
    def mukodes(self):
        self.boss.csataIndulGomb.configure(state = DISABLED)
        self.eldobas()
        celpontok = [] # Ahova lőhet a játékos
        for celpont in range(1,7):
            if self.boss.ellenfel.skalaszotar[celpont].elo.get():
                celpontok.append(celpont)
        if len(celpontok) == 1:
            print("AutoCélzás.")
            for i in self.boss.ellenfel.skalaszotar[celpontok[0]].elo.get():
                self.boss.ellenfel.celzas_sima(celpontok[0])
        else:
            self.boss.ellenfel.celpontotMegjelol(celpontok)
            self.boss.korOsszegzo.configure(text = self.master.szotar['celzas'])
            self.figyelo = self.boss.ellenfel.valasztottCsapat.trace('w',self.mukodes2)
            
    def mukodes2(self,x,y,z):
        csapat = self.boss.ellenfel.valasztottCsapat.get()
        self.boss.ellenfel.valasztottCsapat.trace_vdelete('w',self.figyelo)
        letszam = self.boss.ellenfel.skalaszotar[csapat].elo.get()
        if letszam < 2:
            pass
        else:
            for i in range(letszam-1):
                self.boss.ellenfel.skalaszotar[csapat].talalat()
        self.boss.csataIndulGomb.configure(state = NORMAL)

class Kartacs(Gombjektum):
    """Kartács objektum"""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "kartacs")
        self.maxCoolDown = -1
        self.hang = "Bu-bu-bu-bu-bu-bummmmmm!"
        
    def mukodes(self):
        "Egy szabad kört biztosít a játékosnak, azaz minden csapatával támadhat, anélkül, hogy az ellenfél visszatámadna."
        jatekosCsapatai = self.boss.jatekos.ertekkeszlet()
        jatekosDobasai = self.boss.dobas(len(jatekosCsapatai))
        for kocka in jatekosDobasai:
            talalt = self.boss.ellenfel.talalat(kocka)
        
class Gorogtuz(Gombjektum):
    """Görögtűz objektum"""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "gorogtuz")
        self.maxCoolDown = -1
        self.hang = "**Lobog.**"
        
    def mukodes(self):
        "Egy ellenséges csapat feloszlik, és tagjai másik, még létező csapatokba állnak át, vagy végük."
        self.boss.csataIndulGomb.configure(state = DISABLED)
        for elem in range(1,7):
            self.boss.ellenfel.skalaszotar[elem].radio.configure(command = self.boss.gombszotar['gorogtuz'].mukodes2, state = NORMAL)
            
    def mukodes2(self):
        "Folytatja a futást az adat megszerzése után."
        celpont = self.boss.ellenfel.valasztottCsapat.get() # Kiolvassuk a felhasználó választását.
        self.boss.ellenfel.valasztottCsapat.set(0)          # Alaphelyzetbe tesszük a változót.
        for elem in range(1,7):                             # Visszaállítjuk az eredeti működést.
            self.boss.ellenfel.skalaszotar[elem].radio.configure(command = self.boss.ellenfel.celzas, state = DISABLED)
        csapatmeret = self.boss.ellenfel.skalaszotar[celpont].elo.get()
        egyebCsapatok = []
        for egyebCsapat in range(1,7):
            if egyebCsapat != celpont:
                egyebCsapatLetszam = self.boss.ellenfel.skalaszotar[egyebCsapat].elo.get()
                if 1 < egyebCsapatLetszam < 6:
                    egyebCsapatok.append([egyebCsapat,egyebCsapatLetszam])
        szamlalo = 0
        szamlalo2 = csapatmeret
        while egyebCsapatok != [] and szamlalo2 > 0:
            aktCsap = egyebCsapatok[szamlalo%(len(egyebCsapatok))]
            self.boss.ellenfel.skalaszotar[aktCsap[0]].matrozszotar[aktCsap[1]+1].configure(image = self.boss.ellenfel.skalaszotar[aktCsap[0]].teli)
            self.boss.ellenfel.skalaszotar[aktCsap[0]].elo.set(aktCsap[1]+1)
            self.boss.ellenfel.skalaszotar[celpont].elo.set(szamlalo2-1)
            aktCsap[1] += 1
            szamlalo2 += -1
            if aktCsap[1] == 6:
                egyebCsapatok.remove(aktCsap)
            else:
                szamlalo += 1
        if szamlalo2 > 0:
            self.boss.ellenfel.skalaszotar[celpont].elo.set(0)
        for matroz in range(1+szamlalo2,csapatmeret+1):
            self.boss.ellenfel.skalaszotar[celpont].matrozszotar[matroz].configure(image = self.boss.ellenfel.skalaszotar[celpont].ures)
        for matroz in range(1,szamlalo2+1):
            self.boss.ellenfel.skalaszotar[celpont].matrozszotar[matroz].configure(image = self.boss.ellenfel.skalaszotar[celpont].serult)
        self.boss.ellenfel.csatafelirat()
        self.boss.csataIndulGomb.configure(state = NORMAL)

class Majom(Gombjektum):
    """Majom objektum"""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "majom")
        self.maxCoolDown = -1
        self.hang = "**Fut-fut-fut.**"
        
    def mukodes(self):
        "Megszerzi a kincset, ha az ellenséges hajó már süllyed."
        self.boss.kincsMegszerzese()
        
    def cooling(self):
        "Felülírja az alapértelmezett cooldownkezelést."
        if self.nev in self.master.jatekmenet.aktivjatekos.statuszlista:
            if self.boss.ellenfelSullyed.get() and not self.boss.kincsMegszerezve:
                self.gomb.configure(state = NORMAL)

class Szirenkurt(Gombjektum):
    """A szirének kürtje."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "szirenkurt")
        self.maxCoolDown = -1
        self.hang = "Phu-ú!"
    
    def mukodes(self):
        "Minden ellenséges csapatból egy fő átáll a játékoshoz, egy új csapatot alkotva."
        pluszmatrozok = 0
        for i in range(1,7):
            letszam = self.boss.ellenfel.skalaszotar[i].elo.get()
            if letszam:
                self.boss.ellenfel.skalaszotar[i].matrozszotar[letszam].configure(image = self.boss.ellenfel.skalaszotar[i].ures)
                self.boss.ellenfel.skalaszotar[i].elo.set(letszam-1)
                pluszmatrozok += 1
        for i in range(1,7):
            if pluszmatrozok and not self.boss.jatekos.skalaszotar[i].elo.get():
                for j in range(1,pluszmatrozok+1):
                    self.boss.jatekos.skalaszotar[i].matrozszotar[j].configure(image = self.boss.jatekos.skalaszotar[i].teli)
                self.boss.jatekos.skalaszotar[i].elo.set(pluszmatrozok)
                pluszmatrozok = 0
        self.boss.ellenfel.csatafelirat()
        self.boss.jatekos.csatafelirat()
        
    def cooling(self):
        if self.nev in self.master.jatekmenet.aktivjatekos.statuszlista and not self.cooldown:
            csapatletszamokListaja = []
            for i in range(1,7):
                csapatletszamokListaja.append(self.boss.jatekos.skalaszotar[i].elo.get())
            if 0 in csapatletszamokListaja:
                self.gomb.configure(state = NORMAL)
                
class Szirenek(Gombjektum):
    """Fogjul ejtett szirén."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "szirenek")
        self.maxCoolDown = -1
        self.hang = "Trillalá!"
        self.okozottVeszteseg = 3
        self.talon = self.master.jatekmenet.esemenytalon
        
    def mukodes(self):
        "A dobott számú csapatból három matrózt a tengerbe csábít."
        self.eldobas()
        dobas = randrange(1,7)
        csapat = self.boss.ellenfel.skalaszotar[dobas]
        letszam = csapat.elo.get()
        if letszam >= self.okozottVeszteseg:
            levonando = self.okozottVeszteseg
        else:
            levonando = letszam
        for i in range(levonando):
            csapat.matrozszotar[letszam-i].configure(image = csapat.serult)
        csapat.elo.set(letszam-levonando)

class Alvarez(Gombjektum):
    """Juan Alvarez"""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "alvarez")
        self.maxCoolDown = -1
        self.hang = "A helyetekre, fiúk!"
        
    def mukodes(self):
        "Lehetővé teszi, hogy a játékos átrendezze a csapatait egyszer egy csata folyamán."
        jatekos = self.boss.jatekos
        maxLegenyseg = 0
        for i in jatekos.skalaszotar.keys():
            if jatekos.skalaszotar[i].elo.get():
                maxLegenyseg += jatekos.skalaszotar[i].elo.get()
            jatekos.skalaszotar[i].value.set(jatekos.skalaszotar[i].elo.get())
        jatekos.maxLegenyseg_set(maxLegenyseg)
        jatekos.kiosztottLegenyseg.set(maxLegenyseg)
        jatekos.osszegzoFelirat.set(self.master.szotar['legenyseg']+': '+str(jatekos.kiosztottLegenyseg.get())+'/'+str(jatekos.maxLegenyseg))
        jatekos.mindentEngedelyez()
        self.boss.korOsszegzo.config(text = self.master.szotar["hajoalathataron_alvarez"])
                
if __name__ == '__main__':
    from tkinter import Tk
    from PIL import ImageTk
    from PIL.ImageTk import PhotoImage
    from PIL.Image import ANTIALIAS, open 
    class Tabla():
        def __init__(self):
            self.mezomeret = 216
            self.keptar = {}
            self.keptar['matroz1'] = open('img/matroz1.png')
            self.keptar['matroz0'] = PhotoImage((open('img/transparent.png')).resize((self.keptar['matroz1'].size[0], self.keptar['matroz1'].size[1]), ANTIALIAS))
            self.keptar['matroz1'] = PhotoImage(self.keptar['matroz1'])  
            self.keptar['matroz2'] = PhotoImage(open('img/matroz2.png'))
            for i in ['pisztoly', 'puska', 'labtovis', 'granat', 'kartacs', 'gorogtuz', 'majom', 'szirenkurt', 'szirenek', "alvarez"]:
                self.keptar['ikon_'+i] = PhotoImage(open('img/ikon_'+i+'.png'))
            self.keptar["szkuner"] = PhotoImage(open('img/szkuner.png'))
            self.hajotar = {}
            self.hajotar["Játékos"] = PhotoImage(open('img/fregatt.png'))
        def hajotathelyez(self, x = None, y = None, z = None):
            "Dummy"
            return
    class Player():
        def __init__(self):
            self.nev = "Játékos"
            self.hajo = None
            self.zaszlo = None
            self.legenyseg = IntVar()
            self.statuszlista = ["pisztoly", "puska", "labtovis", "granat", "kartacs", "gorogtuz", "papagaj", "majom", "szirenkurt", "szirenek", "alvarez"]
            self.kincs = IntVar()
            self.hajotar = {}
            self.hajotar['spanyol'] = IntVar()
    class Jatekmenet():
        def __init__(self):
            self.kincstalon = []
            self.esemenytalon = []
            self.aktivjatekos = Player()
            self.aktivjatekos.hajo = 'szkuner'
            self.aktivjatekos.zaszlo = 'angol'
            self.aktivjatekos.legenyseg.set(16)
        def kincsetHuz(self, x = None):
            print("Kincs kihúzva")
    def csataIndul():
        'Csataindító tesztfüggvény'
        b = Utkozet(a,a,('spanyol', 'szkuner', 'pirate1', ('underWaterHit', 2, 2, 2, 3, 'powderStore'), 16, True)) #'underWaterHit', 2, 2, 2, 3, 'powderStore' 
    class A(Tk):
        def __init__(self):
            Tk.__init__(self)
            self.height = 100
            self.width = 100
        def helymeghatarozas(self):
            'Visszaadja saját jelenlegi pozícióját.'
            info = self.winfo_geometry()
            xpos = info.index('+')+1
            ypos = info[(xpos):].index('+')+xpos
            x = int(info[(xpos):(ypos)])
            y = int(info[(ypos):])
            return (x,y)
        def szakasz_0(self):
            print("A játék megy tovább...")
    
    a = A()
    a.tabla = Tabla()
    a.kartyaszotar = dict([('pisztoly', ['Pisztoly','teszt']), ('puska', ['Puska','teszt']), ('labtovis', ['Lábtövis','teszt']),
                           ('granat', ['Gránát','teszt']), ('kartacs', ['Kartács','teszt']), ('gorogtuz', ['Görögtűz','teszt']),
                           ('majom', ['Majom','teszt']), ('szirenkurt', ['Szirénkürt','teszt']), ('szirenek', ['Szirének','teszt']),
                           ("alvarez", ["Juan Alvarez",'teszt'])])
    a.szotar = {}
    a.szotar['szkuner'] = 'szkúner'
    a.szotar['angol'] = 'angol'
    a.szotar['kaloz'] = 'kalóz'
    a.szotar['spanyol'] = 'spanyol'
    a.szotar['csata'] = 'Csata'
    a.szotar['autoElosztas'] = 'autoElosztas'
    a.szotar['legenyseg'] = 'Legénység'
    a.szotar['osszecsapas'] = 'Csata!'
    a.szotar['kesz'] = 'Kész'
    a.szotar['extra'] = 'Válaszd ki, melyik ellenséges csapat ellen indítasz extra támadást!'
    a.szotar['letszam'] = '%i matróz %i csapatban'
    a.szotar['celzas'] = 'Válaszd ki, melyik ellenséges csapatra lősz!'
    a.szotar["hajoalathataron"] = "Hajó a láthatáron! Mit tegyen a legénység?"
    a.szotar["hajoalathataron_kaloz"] = "Hajó a láthatáron! Egyenesen felénk tart!"
    a.szotar["hajoalathataron_menekules"] = "Menekülés"
    a.szotar["hajoalathataron_agyuzas"] = "Tűz!"
    a.szotar["hajoalathataron_megcsaklyazas"] = "Csáklyázzuk meg!"
    a.szotar["hajoalathataron_futnihagyas"] = "Hagyjuk futni"
    a.szotar["hajoalathataron_harc"] = "Kezdődik a harc. Oszd be csapatokba az embereidet."
    a.szotar["hajoalathataron_veszteseg_ellenfel"] = "Az ellenfél %i matrózt veszített az ágyúzás során."
    a.szotar["hajoalathataron_veszteseg_jatekos"] = "2 matrózt vesztettél az ágyúzás során."
    a.szotar["hajoalathataron_veszteseg_sullyed"] = "Az ellenfél hajója léket kapott. 3 körön belül elsüllyed!"
    a.szotar["hajoalathataron_csataindul"] = "Játssz ki egy kártyát, vagy kattints az alábbi gombra a harchoz."
    a.szotar["hajoalathataron_jutalom"] = "Zsákmányod %i arany%s."
    a.szotar["hajoalathataron_jutalom2"] = " és egy kincskártya"
    a.szotar["hajoalathataron_alvarez"] = "Most megváltoztathatod a csapatok felállását."
    a.szotar["tooltip"] = "Teszt."
    a.szotar["hajonev_pirate1"] = "Kalózhajó"
    a.szotar["hajonev_jatekos"] = "Hajó"
    a.szotar["hajoalathataron_loporraktar"] = "Az ellenfél elsüllyedt."
    a.szotar["csata_elhagyasa"] = "Csata elhagyása"
    a.szotar["csata_elhagyasa_szoveg"] = "Ha bezárod ezt a képernyőt, elveszíted a matrózaid, és a száműzöttek szigetére kerülsz. Biztosan ezt szeretnéd?"
    a.szotar["csata_elvesztese"] = "Veszítettél. Ellenfeleid fogságba ejtettek, és a Száműzöttek szigetén tettek partra."
    a.szotar["csata_elsullyed"] = "Az ellenséges hajó elsüllyedt."
    a.jatekmenet = Jatekmenet()
    Button(a, text = 'Csata!', command = csataIndul).pack()    
    a.mainloop()