from logging import debug
from tkinter import BooleanVar, BOTTOM, Button, DISABLED, FLAT, Frame, GROOVE, IntVar, Label, LEFT, NORMAL, \
    Radiobutton, RIGHT, StringVar, SUNKEN, TOP, Toplevel, X, Y
from tkinter.messagebox import askyesno
from random import randrange
from assets import Gallery
from settings import ApplicationSettings as s


class Utkozet(Toplevel):
    """Hajócsata függvény."""
    def __init__(self, boss, master, csatainfok, kovetkezoSzakasz=0):
        Toplevel.__init__(self, master=boss)
        self.boss = boss
        self.master = master
        self.grab_set()
        self.kovetkezoSzakasz = kovetkezoSzakasz
        self.title(s.language.battle)
        self.protocol("WM_DELETE_WINDOW", self.ablakBezarasa)
        self.resizable(width=0, height=0)
        self.ellensegesZaszlo, self.ellensegesHajoTipusa, self.ellensegesHajoNeve, self.ellensegesLegenyseg, \
            self.zsakmany, self.kincskartyaHuzas = csatainfok
        if self.ellensegesHajoNeve[0:6] == "pirate":
            self.ellensegesHajoNeve = s.language.get(self.ellensegesHajoNeve)
        self.gombok = ['gun', 'rifle', 'caltrop', 'grenade', 'grapeshot', 'greek_fire', 'monkey', 'sirenhorn',
                       'sirens']
        self.jatekosMatrozaiFenn = BooleanVar()
        self.jatekosMatrozaiFenn.set(False)
        self.jatekosMatrozaiFenn.trace('w', self.keszGombConf)
        self.ellenfelSullyed = BooleanVar()
        self.sullyedesigHatravan = -1
        self.kincsMegszerezve = False
        self.kartyaHuzando = False
        self.fokeret()
        self.szabadKockaLista = []
        self.update_idletasks()
        bx, by = self.master.get_window_position()
        self.geometry('+'+str(int(self.master.game_board.tile_size/2+bx))+'+'+str(self.master.game_board.tile_size+by))
        self.master.wait_window(self)

    def fokeret(self, dummy=0):
        'Leképezi az ablak tartalmát'
        if dummy == 1:
            debug('Victory')
            return True
        # játékos
        self.jatekos = Hajoablak(self, self.master, user=1)
        self.jatekos.pack(side=LEFT, fill=Y, padx=5, pady=5, ipadx=5, ipady=5)
        # csatatér
        self.csatater = Frame(self, bd=2, relief=GROOVE)
        gombsor = Frame(self.csatater)
        self.valosCelpontok = []
        self.valosCelpontKockak = []
        self.gombszotar = {}
        self.gombszotar['gun'] = Pisztoly(self, self.master, gombsor)
        self.gombszotar['rifle'] = Puska(self, self.master, gombsor)
        self.gombszotar['caltrop'] = Labtovis(self, self.master, gombsor)
        self.gombszotar['grenade'] = Granat(self, self.master, gombsor)
        self.gombszotar['grapeshot'] = Kartacs(self, self.master, gombsor)
        self.gombszotar['greek_fire'] = Gorogtuz(self, self.master, gombsor)
        self.gombszotar['monkey'] = Majom(self, self.master, gombsor)
        self.gombszotar['sirenhorn'] = Szirenkurt(self, self.master, gombsor)
        self.gombszotar['sirens'] = Szirenek(self, self.master, gombsor)
        self.gombszotar['alvarez'] = Alvarez(self, self.master, gombsor)
        gombsor.pack(side=TOP)
        self.tooltip = Frame(self.csatater)
        self.tooltip.label = Label(self.tooltip, relief=SUNKEN, bd=1)
        self.tooltip.label.pack(fill=X)
        self.tooltip.pack(side=TOP, fill=X, padx=5)
        self.interaktiv = Frame(self.csatater)
        self.textGombok = Frame(self.interaktiv)
        self.korOsszegzo = Label(self.interaktiv)
        self.csataIndulGomb = Button(self.textGombok, text=s.language.fight, command=self.harcikor,
                                     state=DISABLED)
        self.csataIndulGomb.pack(side=BOTTOM, pady=10)
        self.csataIndulGomb.pack_forget()
        self.csatakezdet()
        self.textGombok.pack(side=BOTTOM, pady=10)
        self.korOsszegzo.pack(side=BOTTOM, pady=20)
        self.interaktiv.pack(side=BOTTOM)
        self.csatater.pack(side=LEFT, fill=Y, pady=5, ipadx=5, ipady=5)
        # ellenfél
        self.ellenfel = Hajoablak(self, self.master)
        self.caltrop = 0
        self.ellenfel.pack(side=LEFT, fill=Y, padx=5, pady=5, ipadx=5, ipady=5)

    def csatakezdet(self):
        "Ellátja a játékost a kezdeti információkkal."
        if self.master.engine.aktivjatekos.empire == 'Pirate':
            tamad = randrange(2)
        elif self.ellensegesZaszlo == "Pirate":
            tamad = 1
        else:
            tamad = 0
        if tamad:
            self.korOsszegzo.config(text=s.language.ship_spotted_pirate)
        else:
            self.korOsszegzo.config(text=s.language.ship_spotted)
        self.csataGombLista = {}
        for id, command in (("ship_spotted_fire", self.agyuzas),
                            ("ship_spotted_boarding", self.megcsaklyazas),
                            ("ship_spotted_let_them_flee", self.futnihagy),
                            ("ship_spotted_fleeing", self.menekules)):
            self.csataGombLista[id] = Button(self.textGombok, text=s.language.get(id), command=command)
            self.csataGombLista[id].pack(side=LEFT, padx=3)
        if tamad:
            self.csataGombLista["ship_spotted_let_them_flee"].pack_forget()
        else:
            self.csataGombLista["ship_spotted_fleeing"].pack_forget()

    def futnihagy(self):
        "Elvonulás a csatából harc nélkül."
        if self.ellenfelSullyed.get() and "parrot" in self.master.aktivjatekos.states:
            for gomb in self.csataGombLista.keys():
                self.csataGombLista[gomb].pack_forget()
            self.korOsszegzo.config(text="")
            self.boss.kincsMegszerzese(papagaj=1)
        else:
            self.bezar()

    def menekules(self):
        "Menekülési függvény, ha a játékos hajója kisebb, sikeres a menekülés."
        if self.boss.hajotipustar[self.ellensegesHajoTipusa].price < \
                self.boss.hajotipustar[self.master.engine.aktivjatekos.ship].price:
            self.megcsaklyazas()
            self.korOsszegzo.config(text=(s.language.ship_spotted_fleeing_unsuccesful + "\n" +
                                          s.language.ship_spotted_battle))
        else:
            debug(self.master.engine.aktivjatekos.name + " elmenekült.")
            self.bezar()

    def megcsaklyazas(self):
        "A közelharcot indító függvény."
        self.korOsszegzo.config(text=s.language.ship_spotted_battle)
        for gomb in self.csataGombLista.keys():
            self.csataGombLista[gomb].pack_forget()
        self.csataIndulGomb.pack(side=BOTTOM, pady=10)
        self.jatekos.skalaablak.pack()
        self.ellenfel.skalaablak.pack()

    def agyuzas(self):
        "Az ágyúzás függvénye."
        eredmeny = ""
        # visszaloves = True
        # Játékos lő az ellenfélre
        dobas = 1  # randrange(1,7)
        minusz = 0
        if self.ellensegesLegenyseg[dobas-1] == 'underWaterHit':
            self.ellenfelSullyed.set(True)
            self.sullyedesigHatravan = 2
            eredmeny += (s.language.ship_spotted_enemy_sinking)
        elif self.ellensegesLegenyseg[dobas-1] == 'powderStore':
            self.ellenfelSullyed.set(True)
            self.sullyedesigHatravan = 0
            for gomb in self.csataGombLista.keys():
                self.csataGombLista[gomb].pack_forget()
            self.harcfeltetelek_vizsgalata()
            self.csataIndulGomb.configure(text=s.language.done, command=self.bezar, state=NORMAL)
            self.csataIndulGomb.pack()
            eredmeny += (s.language.ship_spotted_powder_storage)
        else:
            if self.ellenfel.skalaszotar[dobas].value.get() > 1:
                minusz = 2
            elif self.ellenfel.skalaszotar[dobas].value.get() == 1:
                minusz = 1
            self.ellenfel.skalaszotar[dobas].erteket_beallit(self.ellenfel.skalaszotar[dobas].value.get()-minusz)
            eredmeny += (s.language.ship_spotted_enemy_casualties % minusz)
        # Ellenfél lő a játékosra
        dobas2 = randrange(1, 7)
        lehetsegesCsapatok = self.master.engine.aktivjatekos.crew.get() / 6
        if lehetsegesCsapatok > dobas2:
            self.master.engine.aktivjatekos.crew.set(self.master.engine.aktivjatekos.crew.get()-2)
            self.jatekos.maxLegenyseg = self.master.engine.aktivjatekos.crew.get()
            if eredmeny != "":
                eredmeny += "\n"
            eredmeny += (s.language.ship_spotted_player_casualties)
        # Eredménykijelzés
        self.korOsszegzo.config(text=eredmeny)
        self.jatekos.osszegzoFelirat.vege = '/' + str(self.jatekos.maxLegenyseg)
        self.jatekos.osszegzoFelirat.set(self.jatekos.osszegzoFelirat.eleje +
                                         str(self.jatekos.kiosztottLegenyseg.get()) +
                                         self.jatekos.osszegzoFelirat.vege)
        self.ellenfel.osszegzoFelirat.set(self.ellenfel.osszegzoFelirat.eleje +
                                          str(self.ellenfel.kiosztottLegenyseg.get()) + '/' +
                                          str(self.ellenfel.maxLegenyseg))
        self.csataGombLista["ship_spotted_fire"].config(state=DISABLED)

    def csataIndul(self):
        'Letiltja a csatapok átrendezését.'
        self.jatekos.mindentLetilt()
        self.jatekos.eloszamol()
        self.ellenfel.eloszamol()
        for gomb in self.gombszotar.keys():
            if self.gombszotar[gomb].nev in self.master.engine.aktivjatekos.states:
                self.gombszotar[gomb].cooling()
        self.korOsszegzo.config(text=s.language.ship_spotted_battle_starts)
        self.csataIndulGomb.configure(state=NORMAL)

    def csataIndul2(self):
        'Letiltja a csatapok átrendezését.'
        self.jatekos.mindentLetilt()
        self.jatekos.eloszamol()
        self.ellenfel.eloszamol()
        self.korOsszegzo.config(text=s.language.ship_spotted_battle_starts)
        self.csataIndulGomb.configure(state=NORMAL)

    def harcikor(self):
        "Levezényel egy harci kört."
        debug('-----------------Új kör')
        self.csataIndulGomb.configure(state=DISABLED)
        for gomb in self.gombszotar.keys():
            self.gombszotar[gomb].gomb.configure(state=DISABLED)
        jatekosCsapatai, ellenfelCsapatai = self.jatekos.ertekkeszlet(), self.ellenfel.ertekkeszlet()
        jatekosDobasai = self.dobas(len(jatekosCsapatai))
        ellenfelDobasai = self.dobas(len(ellenfelCsapatai) - self.caltrop)
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
        celpontok, celpontKockak = self.szabadKockak(self.szabadKockaLista)
        debug("Lehetséges célpontok: {}; Ahogy a kockákból összeáll: {}".format(celpontok, celpontKockak))
        for celpont in celpontok:
            if self.ellenfel.skalaszotar[celpont].elo.get():
                debug('Célba vett csapat: ', celpont, 'Ennyi matróz van benne:',
                      self.ellenfel.skalaszotar[celpont].elo.get())
                self.valosCelpontok.append(celpont)
                self.valosCelpontKockak.append(celpontKockak[celpontok.index(celpont)])
            else:
                debug('Csapat üres, célpont kizárva.')
        debug("Valid targets: {}".format(self.valosCelpontok))
        debug("Valid target dies: {}".format(self.valosCelpontKockak))
        if self.valosCelpontok:
            if len(self.valosCelpontok) == 1:
                debug("AutoExtra")
                self.ellenfel.valasztottCsapat.set(self.valosCelpontok[0])
                self.ellenfel.celzas()
            else:
                self.ellenfel.celpontotMegjelol(self.valosCelpontok)
                self.korOsszegzo.configure(text=s.language.extra)
        else:
            self.harcikor_vege()

    def harcikor_vege(self):
        self.korOsszegzo.config(text=s.language.ship_spotted_battle_starts)
        vege_a_harcnak = self.harcfeltetelek_vizsgalata()
        if not vege_a_harcnak:
            for gomb in self.gombszotar.keys():
                self.gombszotar[gomb].cooling()
            if self.ellenfelSullyed.get():
                self.sullyedesigHatravan += -1
        self.valosCelpontok = []
        self.valosCelpontKockak = []
        self.csataIndulGomb.configure(state=NORMAL)

    def harcfeltetelek_vizsgalata(self):
        "Ellenőrzi, tart-e még a harc."
        if self.harc_vege():
            self.csataIndulGomb.configure(text=s.language.done, command=self.bezar)
            for gomb in self.gombszotar.keys():
                self.gombszotar[gomb].gomb.configure(state=DISABLED)
            return True
        else:
            return False

    def szabadKockak(self, szabadKockak):
        "Kiszámolja a lehetséges szabadkocka felhasználási módokat."
        debug('Szabad kockák:', szabadKockak)
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
                for eredmeny in [xo, xm, xsz, xh]:
                    if self.vizsgal(eredmeny) and eredmeny not in ertekkeszlet:
                        ertekkeszlet.append(int(eredmeny))
                        ertekkeszletKockak.append((dobas, dobas2))
        return ertekkeszlet, ertekkeszletKockak

    def vizsgal(self, x):
        if 0 < x < 7 and x == int(x):
            return True
        else:
            return False

    def harc_vege(self):
        "Ellenőrzi a felek harcképességét."
        if not self.jatekos.ertekkeszlet():
            debug('Vesztítettél.')
            self.korOsszegzo.configure(text=s.language.battle_lose)
            self.vereseg()
            return True
        elif (len(self.jatekos.ertekkeszlet()) == 1 and not len(self.ellenfel.ertekkeszlet())) or \
                (len(self.jatekos.ertekkeszlet()) > 1 and len(self.ellenfel.ertekkeszlet()) < 2):
            debug('Győztél.')
            self.matroztVisszair()  # mentjük a megmaradt matrózok számát a játékos profiljába
            # megnöveljük az elfogott hajók számát
            self.master.engine.aktivjatekos.scores[self.ellensegesZaszlo].set(
                self.master.engine.aktivjatekos.scores[self.ellensegesZaszlo].get() + 1)
            if not self.kincsMegszerezve:
                self.kincsMegszerzese()
            else:
                self.korOsszegzo.config(text="")
            return True
        elif self.ellenfelSullyed.get() and not self.sullyedesigHatravan:
            debug("Az ellenséges hajó elsüllyedt.")
            self.matroztVisszair()  # mentjük a megmaradt matrózok számát a játékos profiljába
            # megnöveljük az elfogott hajók számát
            self.master.engine.aktivjatekos.scores[self.ellensegesZaszlo].set(
                self.master.engine.aktivjatekos.scores[self.ellensegesZaszlo].get() + 1)
            self.korOsszegzo.config(text=s.language.battle_sink)
            return True
        else:
            return False

    def vereseg(self):
        "Ez történik, ha a játékost veszít vagy kilép."
        self.matroztVisszair()  # mentjük a megmaradt matrózok számát a játékos profiljába
        self.master.game_board.relocate_ship((5, 2))  # irány a hajótöröttek szigete
        if "landland" in self.master.engine.aktivjatekos.states:
            self.master.engine.aktivjatekos.remove_state("landland")
        self.master.engine.aktivjatekos.treasure_hunting_done = True

    def ablakBezarasa(self):
        if askyesno(s.language.leave_battle, s.language.leave_battle_text, parent=self):
            self.vereseg()
            self.bezar()
        else:
            self.focus_set()
            return

    def dobas(self, hany):
        'Elvégzi a dobást'
        x = []
        for i in range(hany):
            y = randrange(1, 7)
            x.append(y)
        return x

    def keszGombConf(self, x=None, y=None, z=None):
        'Tilja és engedélyezi a csataindító gombot.'
        if self.jatekosMatrozaiFenn.get():
            self.jatekos.kesz.configure(state=NORMAL)
        else:
            self.jatekos.kesz.configure(state=DISABLED)

    def szabadKockaListaCsokkent(self, ertek):
        "Eltávolítja a szabadKockaListából a már elhasznált szabad kockákat, majd újra támad, ha még lehet."
        idx = self.valosCelpontok.index(ertek)
        for elem in self.valosCelpontKockak[idx]:
            self.szabadKockaLista.remove(elem)
            debug("A szabad kockák közül törölve: {}".format(elem))
        debug("Megmaradt szabad kockák: {}".format(self.szabadKockaLista))
        if len(self.szabadKockaLista) > 1:
            debug('További extra lövésre van lehetőség.')
            self.extra_talalatok()
        else:
            debug('Nincs több extra lövésre lehetőség.')
            self.harcikor_vege()

    def kincsMegszerzese(self, papagaj=0):
        "Átadja a zsákmányt a játékosnak."
        if self.kincskartyaHuzas:
            szoveg2 = s.language.ship_spotted_reward2
            self.kartyaHuzando = True
        else:
            szoveg2 = ""
        szoveg = s.language.ship_spotted_reward % (self.zsakmany, szoveg2)
        if papagaj:
            szoveg = s.language.ship_spotted_parrot + szoveg
        self.master.engine.aktivjatekos.gold.set(self.master.engine.aktivjatekos.gold.get() + self.zsakmany)
        debug(self.master.engine.aktivjatekos.gold.get())
        self.korOsszegzo.config(text=szoveg)
        self.kincsMegszerezve = True

    def matroztVisszair(self):
        "Visszaadja a játékosadatnak a megmaradt matrózok számát."
        visszairando = 0
        for i in self.jatekos.skalaszotar.keys():
            visszairando += self.jatekos.skalaszotar[i].elo.get()
        debug("Életben maradt matrózok:" + str(visszairando))
        self.master.engine.aktivjatekos.crew.set(visszairando)

    def bezar(self):
        "Bezárja a csataképernyőt."
        self.destroy()
        if self.kartyaHuzando:
            self.master.engine.kincsetHuz()
        if self.kovetkezoSzakasz == 0:
            self.boss.szakasz_0()


class Hajoablak(Frame):
    """A játékosok és ellenfeleik megjelenítésére szolgál."""
    def __init__(self, boss, master, user=0):
        Frame.__init__(self, master=boss, bd=2, relief=GROOVE)
        cimStilus = 'helvetica 14 bold'
        self.boss = boss
        self.master = master
        self.maxLegenyseg = self.master.engine.aktivjatekos.crew.get()
        self.kiosztottLegenyseg = IntVar()
        self.kiosztottLegenyseg.set(0)
        self.osszegzoFelirat = StringVar()
        self.osszegzoFelirat.eleje = s.language.crew+': '
        self.osszegzoFelirat.vege = '/'+str(self.maxLegenyseg)
        self.osszegzoFelirat.set(self.osszegzoFelirat.eleje+str(self.kiosztottLegenyseg.get())+self.osszegzoFelirat.vege)
        self.full = BooleanVar()
        self.full.set(False)
        self.full.trace('w', self.csataIndulConf)
        self.skalaszotar = {}
        self.aktivCsapatok = IntVar()
        if user:
            self.kiosztottLegenyseg.trace('w', self.matrozValtozas)
            self.hossz = 6
        else:
            self.valasztottCsapat = IntVar()
            csapatok = []
            for i in boss.ellensegesLegenyseg:
                if isinstance(i, int):
                    csapatok.append(i)
            self.hossz = 6  # max(csapatok)
        # Adatgenerálás
        if user:
            nev = s.language.ship_name_player
            # TODO empire and ship translations should be received more elegant better than this
            reszletek = '%s %s' % (s.language.get(master.engine.aktivjatekos.empire.adjective),
                                   s.language.get(master.engine.aktivjatekos.ship))
        else:
            # TODO also this
            nev = boss.ellensegesHajoNeve
            reszletek = '%s %s' % (s.language.get(boss.ellensegesZaszlo), s.language.get(boss.ellensegesHajoTipusa))
        # Képablak
        kepkeret = Frame(self, height=self.master.game_board.tile_size, width=self.master.game_board.tile_size)
        kepkeret.pack_propagate(0)
        if user:
            kep = self.master.game_board.ship_figure_images[self.master.engine.aktivjatekos.name]
        else:
            kep = Gallery.get(self.boss.ellensegesHajoTipusa)
        Label(kepkeret, image=kep).pack(side=BOTTOM)
        kepkeret.pack()
        # Hajó neve
        Label(self, text=nev, font=cimStilus).pack()
        Label(self, text=reszletek).pack()
        # Skálák
        self.skalaablak = Frame(self)
        for i in range(1, 7):
            self.skalaszotar[i] = MatrozSkala(self.skalaablak, self, self.master, user,
                                              boss.ellensegesLegenyseg[i - 1], radioValue=i, hossz=self.hossz)
            self.skalaszotar[i].pack()
        elosztas = Frame(self.skalaablak)
        Label(elosztas, textvariable=self.osszegzoFelirat).pack()
        pult = Frame(elosztas)
        if user:
            self.auto = Button(pult, text=s.language.balance_teams, command=self.autoElosztas)
            self.auto.pack(side=LEFT, padx=3)
            self.kesz = Button(pult, text=s.language.done, command=self.boss.csataIndul, state=DISABLED)
            self.kesz.pack(side=LEFT, padx=3)
        pult.pack()
        elosztas.pack(fill=X)
        # Utókozmetikázás az ellenfél mutatóján
        if not user:
            self.maxLegenyseg = 0
            for i in range(1, 7):
                self.maxLegenyseg += self.skalaszotar[i].value.get()
            self.kiosztottLegenyseg.set(self.maxLegenyseg)
            self.osszegzoFelirat.set(self.osszegzoFelirat.eleje + str(self.kiosztottLegenyseg.get()) + '/' +
                                     str(self.maxLegenyseg))

    def autoElosztas(self):
        "Működteti az automatikus elosztást végző gombot"
        autoLista = [5, 3, 4, 2, 6]  # statisztikailag ez kedvez legjobban a játékosnak
        crew = self.maxLegenyseg
        alapletszam = int(crew/6)
        maradek = crew % 6
        skalaAlapok = [alapletszam] * 6
        if maradek > 0:
            for i in range(maradek):
                skalaAlapok[autoLista[i] - 1] += 1
        for i in range(1, 7):
            self.skalaszotar[i].erteket_beallit(skalaAlapok[i - 1])

    def matrozValtozas(self, x=0, y=0, z=0):
        "Ha minden matrózt kiosztott a játékos, megakadályozza, hogy többet osszon ki."
        if self.kiosztottLegenyseg.get() == self.maxLegenyseg:
            for i in range(1, 7):
                self.skalaszotar[i].pluszgomb.configure(state=DISABLED)
            self.full.set(True)
        elif self.full.get() and self.kiosztottLegenyseg.get() < self.maxLegenyseg:
            for i in range(1, 7):
                self.skalaszotar[i].letilto()
            self.full.set(False)
        self.osszegzoFelirat.set(self.osszegzoFelirat.eleje + str(self.kiosztottLegenyseg.get()) + '/' +
                                 str(self.maxLegenyseg))

    def mindentLetilt(self):
        "Minden változtatást letilt a táblán."
        for i in range(1, 7):
            self.skalaszotar[i].letilto(all=1)
        self.auto.configure(state=DISABLED)
        self.kesz.configure(state=DISABLED)

    def mindentEngedelyez(self):
        "Minden változtatást engedélyez a táblán, Alvarez parancsára."
        self.boss.csataIndulGomb.config(state=DISABLED)
        for i in range(1, 7):
            self.skalaszotar[i].minuszgomb.config(state=NORMAL)
            self.skalaszotar[i].pluszgomb.config(state=NORMAL)
        self.matrozValtozas()
        self.auto.configure(state=NORMAL)
        self.kesz.configure(state=NORMAL, command=self.boss.csataIndul2)

    def csataIndulConf(self, x=None, y=None, z=None):
        "Állítja a szülőkeret azonos paraméterét"
        self.boss.jatekosMatrozaiFenn.set(self.full.get())

    def ertekkeszlet(self):
        """
            Visszaadja az aktív csapatok méretét egy listaként. Amennyiben a csapat inaktív, azaz nem tartalmaz
            matrózt, nem kerül nulla a listába.
        """
        ertekek = []
        for i in range(1, 7):
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
            self.skalaszotar[i].radio.configure(state=NORMAL)

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
        self.boss.korOsszegzo.configure(text='')
        self.valasztottCsapat.set(0)
        for i in self.skalaszotar.keys():
            self.skalaszotar[i].radio.configure(state=DISABLED)

    def csatafelirat(self):
        "Figyelemmel kíséri a létszámváltozásokat, és frissíti a felületet."
        x = 0
        y = 0
        for i in self.skalaszotar.keys():
            if self.skalaszotar[i].elo.get():
                x += self.skalaszotar[i].elo.get()
                y += 1
        self.osszegzoFelirat.set(s.language.men_count % (x, y))

    def maxLegenyseg_set(self, ertek):
        "Állítja a maxLegenyseg változót."
        self.maxLegenyseg = ertek


class MatrozSkala(Frame):
    """Matrózok elrendezésére szolgál"""
    def __init__(self, boss2, boss, master, user=0, ellensegesLegenyseg=0, radioValue=0, hossz=6):
        Frame.__init__(self, master=boss2)
        if isinstance(ellensegesLegenyseg, str):
            ellensegesLegenyseg = 0
        self.boss = boss
        self.root = master
        self.ures = Gallery.get("crewman0")
        self.teli = Gallery.get("crewman1")
        self.serult = Gallery.get("crewman2")
        self.value = IntVar()
        self.elo = IntVar()
        if user:
            self.minuszgomb = Button(self, text='-', command=self.minusz, state=DISABLED)
            self.minuszgomb.pack(side=LEFT)
        self.matrozszotar = {}
        for i in range(1, hossz + 1):
            self.matrozszotar[i] = Label(self, image=self.ures)
            if user:
                self.matrozszotar[i].pack(side=LEFT)
            else:
                self.matrozszotar[i].pack(side=RIGHT)
        if user:
            self.pluszgomb = Button(self, text='+', command=self.plusz)
            self.pluszgomb.pack(side=LEFT)
            self.value.trace('w', self.letilto)
            self.value.set(0)
        else:
            self.radio = Radiobutton(self, var=self.boss.valasztottCsapat, value=radioValue, state=DISABLED,
                                     command=self.boss.celzas)
            self.radio.pack(side=RIGHT)
            self.value.set(0)
            self.erteket_beallit(ellensegesLegenyseg)

    def letilto(self, x=0, y=0, z=0, all=0):
        if all:
            self.pluszgomb.configure(state=DISABLED)
            self.minuszgomb.configure(state=DISABLED)
        elif self.value.get() == 6:
            self.pluszgomb.configure(state=DISABLED)
            self.minuszgomb.configure(state=NORMAL)
        elif 0 < self.value.get() < 6 and self.boss.kiosztottLegenyseg.get() < self.boss.maxLegenyseg:
            self.pluszgomb.configure(state=NORMAL)
            self.minuszgomb.configure(state=NORMAL)
        elif self.value.get() == 0:
            self.minuszgomb.configure(state=DISABLED)
            self.pluszgomb.configure(state=NORMAL)

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
        self.matrozszotar[self.value.get()].configure(image=self.teli)
        self.boss.kiosztottLegenyseg.set(self.boss.kiosztottLegenyseg.get() + 1)

    def minusz(self):
        'Kijelzi a matrózok létszámának változását.'
        self.matrozszotar[self.value.get()].configure(image=self.ures)
        self.value.set(self.value.get() - 1)
        self.boss.kiosztottLegenyseg.set(self.boss.kiosztottLegenyseg.get() - 1)

    def eloszamol(self):
        self.elo.set(self.value.get())

    def talalat(self):
        "A csapat veszít egy matrózt."
        self.matrozszotar[self.elo.get()].configure(image=self.serult)
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
        self.gomb = Button(keret, image=Gallery.get(f"icon_{nev}"), relief=FLAT, command=self.hasznalat,
                           state=DISABLED)
        self.gomb.pack(side=TOP)
        Label(keret, text=master.card_texts[nev][0], wraplength=55).pack(side=TOP)
        keret.pack(side=LEFT, fill=Y)
        self.talon = self.master.engine.treasurestack
        self.tooltipSzoveg = self.master.card_texts[self.nev][1]
        self.gomb.bind("<Enter>", self.tooltipMutat)
        self.gomb.bind("<Leave>", self.tooltipRejt)

    def tooltipMutat(self, event):
        "Mutatja a súgómezőben a súgószöveget."
        self.boss.tooltip.label.config(text=self.tooltipSzoveg)

    def tooltipRejt(self, event):
        "Törli a súgómezőből a súgószöveget."
        self.boss.tooltip.label.config(text="")

    def cooling(self):
        "Megvalósítja a cooldown-kezelést."
        if self.nev in self.master.engine.aktivjatekos.states:
            if self.cooldown > 1:
                self.cooldown += -1
            elif self.cooldown in [0, 1]:
                self.cooldown = 0
                self.gomb.configure(state=NORMAL)

    def mukodes(self):
        "A gomb fő működésfüggvénye. Minden egyes származtatott osztálynak felül kell írnia ezt a függvényt!"
        pass

    def hasznalat(self):
        "Meghívja a működést, majd futtat egy feltételvizsgálatot."
        debug(self.hang)
        for i in self.boss.gombszotar.keys():
            self.boss.gombszotar[i].gomb.config(state=DISABLED)
        self.mukodes()
        self.cooldown = self.maxCoolDown
        self.gomb.configure(state=DISABLED)
        self.boss.harcfeltetelek_vizsgalata()

    def eldobas(self):
        "Eldobja a játék kártyáját."
        self.master.engine.aktivjatekos.states.remove(self.nev)
        self.talon.append(self.nev)


class Pisztoly(Gombjektum):
    """A gun objektum."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, 'gun')
        self.maxCoolDown = 2
        self.hang = "Piff!"

    def mukodes(self):
        dobas = randrange(1, 7)
        if self.boss.ellenfel.skalaszotar[dobas].elo.get():  # Ha a dobás talált (van a dobott számú csapatban matróz),
            self.boss.ellenfel.celzas_sima(dobas)            # törlünk belőle egyet.


class Puska(Gombjektum):
    """Pisztoly módosulat."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, 'rifle')
        self.maxCoolDown = 3
        self.hang = "Puff!"

    def mukodes(self):
        self.boss.csataIndulGomb.configure(state=DISABLED)
        # dobunk
        dobas = randrange(1, 7)
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
                debug('Célpont', celpont, 'eltávolítva.')
        if not celpontok2:
            debug("Mellé.")
        elif len(celpontok2) == 1:
            debug("AutoCélzás.")
            self.boss.ellenfel.celzas_sima(celpontok2[0])
            self.boss.csataIndulGomb.configure(state=NORMAL)
        else:
            self.boss.ellenfel.celpontotMegjelol(celpontok2)
            self.boss.korOsszegzo.configure(text=s.language.amining)
            self.figyelo = self.boss.ellenfel.valasztottCsapat.trace('w', self.mukodes2)

    def mukodes2(self, x, y, z):
        self.boss.ellenfel.valasztottCsapat.trace_vdelete('w', self.figyelo)
        self.boss.csataIndulGomb.configure(state=NORMAL)


class Labtovis(Gombjektum):
    """Az ellefél eggyel kevesebb kockával játszhat. Egyszeri használat után eldobandó."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, 'caltrop')
        self.maxCoolDown = -1
        self.hang = "**Szétgurul.**"

    def mukodes(self):
        self.eldobas()
        self.boss.caltrop = 1
        self.gomb.configure(relief=SUNKEN, command=self.mukodes2)

    def mukodes2(self):
        pass


class Granat(Gombjektum):
    """Elsöpör egy tetszőleges ellenséges csapatot. Egyszeri használat után eldobandó."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, 'grenade')
        self.maxCoolDown = -1
        self.hang = "Durrrrr!"

    def mukodes(self):
        self.boss.csataIndulGomb.configure(state=DISABLED)
        self.eldobas()
        celpontok = []  # Ahova lőhet a játékos
        for celpont in range(1, 7):
            if self.boss.ellenfel.skalaszotar[celpont].elo.get():
                celpontok.append(celpont)
        if len(celpontok) == 1:
            debug("AutoCélzás.")
            for i in self.boss.ellenfel.skalaszotar[celpontok[0]].elo.get():
                self.boss.ellenfel.celzas_sima(celpontok[0])
        else:
            self.boss.ellenfel.celpontotMegjelol(celpontok)
            self.boss.korOsszegzo.configure(text=s.language.aiming)
            self.figyelo = self.boss.ellenfel.valasztottCsapat.trace('w', self.mukodes2)

    def mukodes2(self, x, y, z):
        csapat = self.boss.ellenfel.valasztottCsapat.get()
        self.boss.ellenfel.valasztottCsapat.trace_vdelete('w', self.figyelo)
        letszam = self.boss.ellenfel.skalaszotar[csapat].elo.get()
        if letszam < 2:
            pass
        else:
            for i in range(letszam-1):
                self.boss.ellenfel.skalaszotar[csapat].talalat()
        self.boss.csataIndulGomb.configure(state=NORMAL)


class Kartacs(Gombjektum):
    """Kartács objektum"""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "grapeshot")
        self.maxCoolDown = -1
        self.hang = "Bu-bu-bu-bu-bu-bummmmmm!"

    def mukodes(self):
        "Egy szabad kört biztosít a játékosnak, azaz minden csapatával támadhat, anélkül, hogy az ellenfél visszatámadna."
        jatekosCsapatai = self.boss.jatekos.ertekkeszlet()
        jatekosDobasai = self.boss.dobas(len(jatekosCsapatai))
        for kocka in jatekosDobasai:
            self.boss.ellenfel.talalat(kocka)


class Gorogtuz(Gombjektum):
    """Görögtűz objektum"""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "greek_fire")
        self.maxCoolDown = -1
        self.hang = "**Lobog.**"

    def mukodes(self):
        "Egy ellenséges csapat feloszlik, és tagjai másik, még létező csapatokba állnak át, vagy végük."
        self.boss.csataIndulGomb.configure(state=DISABLED)
        for elem in range(1, 7):
            self.boss.ellenfel.skalaszotar[elem].radio.configure(command=self.boss.gombszotar['greek_fire'].mukodes2,
                                                                 state=NORMAL)

    def mukodes2(self):
        "Folytatja a futást az adat megszerzése után."
        celpont = self.boss.ellenfel.valasztottCsapat.get()  # Kiolvassuk a felhasználó választását.
        self.boss.ellenfel.valasztottCsapat.set(0)           # Alaphelyzetbe tesszük a változót.
        for elem in range(1, 7):                             # Visszaállítjuk az eredeti működést.
            self.boss.ellenfel.skalaszotar[elem].radio.configure(command=self.boss.ellenfel.celzas, state=DISABLED)
        csapatmeret = self.boss.ellenfel.skalaszotar[celpont].elo.get()
        egyebCsapatok = []
        for egyebCsapat in range(1, 7):
            if egyebCsapat != celpont:
                egyebCsapatLetszam = self.boss.ellenfel.skalaszotar[egyebCsapat].elo.get()
                if 1 < egyebCsapatLetszam < 6:
                    egyebCsapatok.append([egyebCsapat, egyebCsapatLetszam])
        szamlalo = 0
        szamlalo2 = csapatmeret
        while egyebCsapatok != [] and szamlalo2 > 0:
            aktCsap = egyebCsapatok[szamlalo % (len(egyebCsapatok))]
            self.boss.ellenfel.skalaszotar[aktCsap[0]].matrozszotar[aktCsap[1] + 1].configure(
                image=self.boss.ellenfel.skalaszotar[aktCsap[0]].teli)
            self.boss.ellenfel.skalaszotar[aktCsap[0]].elo.set(aktCsap[1] + 1)
            self.boss.ellenfel.skalaszotar[celpont].elo.set(szamlalo2 - 1)
            aktCsap[1] += 1
            szamlalo2 += -1
            if aktCsap[1] == 6:
                egyebCsapatok.remove(aktCsap)
            else:
                szamlalo += 1
        if szamlalo2 > 0:
            self.boss.ellenfel.skalaszotar[celpont].elo.set(0)
        for matroz in range(1 + szamlalo2, csapatmeret + 1):
            self.boss.ellenfel.skalaszotar[celpont].matrozszotar[matroz].configure(
                image=self.boss.ellenfel.skalaszotar[celpont].ures)
        for matroz in range(1, szamlalo2 + 1):
            self.boss.ellenfel.skalaszotar[celpont].matrozszotar[matroz].configure(
                image=self.boss.ellenfel.skalaszotar[celpont].serult)
        self.boss.ellenfel.csatafelirat()
        self.boss.csataIndulGomb.configure(state=NORMAL)


class Majom(Gombjektum):
    """Majom objektum"""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "monkey")
        self.maxCoolDown = -1
        self.hang = "**Fut-fut-fut.**"

    def mukodes(self):
        "Megszerzi a kincset, ha az ellenséges hajó már süllyed."
        self.boss.kincsMegszerzese()

    def cooling(self):
        "Felülírja az alapértelmezett cooldownkezelést."
        if self.nev in self.master.engine.aktivjatekos.states:
            if self.boss.ellenfelSullyed.get() and not self.boss.kincsMegszerezve:
                self.gomb.configure(state=NORMAL)


class Szirenkurt(Gombjektum):
    """A szirének kürtje."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "sirenhorn")
        self.maxCoolDown = -1
        self.hang = "Phu-ú!"

    def mukodes(self):
        "Minden ellenséges csapatból egy fő átáll a játékoshoz, egy új csapatot alkotva."
        pluszmatrozok = 0
        for i in range(1, 7):
            letszam = self.boss.ellenfel.skalaszotar[i].elo.get()
            if letszam:
                self.boss.ellenfel.skalaszotar[i].matrozszotar[letszam].configure(
                    image=self.boss.ellenfel.skalaszotar[i].ures)
                self.boss.ellenfel.skalaszotar[i].elo.set(letszam - 1)
                pluszmatrozok += 1
        for i in range(1, 7):
            if pluszmatrozok and not self.boss.jatekos.skalaszotar[i].elo.get():
                for j in range(1, pluszmatrozok + 1):
                    self.boss.jatekos.skalaszotar[i].matrozszotar[j].configure(
                        image=self.boss.jatekos.skalaszotar[i].teli)
                self.boss.jatekos.skalaszotar[i].elo.set(pluszmatrozok)
                pluszmatrozok = 0
        self.boss.ellenfel.csatafelirat()
        self.boss.jatekos.csatafelirat()

    def cooling(self):
        if self.nev in self.master.engine.aktivjatekos.states and not self.cooldown:
            csapatletszamokListaja = []
            for i in range(1, 7):
                csapatletszamokListaja.append(self.boss.jatekos.skalaszotar[i].elo.get())
            if 0 in csapatletszamokListaja:
                self.gomb.configure(state=NORMAL)


class Szirenek(Gombjektum):
    """Fogjul ejtett szirén."""
    def __init__(self, boss, master, hely):
        Gombjektum.__init__(self, boss, master, hely, "sirens")
        self.maxCoolDown = -1
        self.hang = "Trillalá!"
        self.okozottVeszteseg = 3
        self.talon = self.master.engine.eventstack

    def mukodes(self):
        "A dobott számú csapatból három matrózt a tengerbe csábít."
        self.eldobas()
        dobas = randrange(1, 7)
        csapat = self.boss.ellenfel.skalaszotar[dobas]
        letszam = csapat.elo.get()
        if letszam >= self.okozottVeszteseg:
            levonando = self.okozottVeszteseg
        else:
            levonando = letszam
        for i in range(levonando):
            csapat.matrozszotar[letszam-i].configure(image=csapat.serult)
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
        jatekos.osszegzoFelirat.set(s.language.crew + ': ' + str(jatekos.kiosztottLegenyseg.get()) + '/'
                                    + str(jatekos.maxLegenyseg))
        jatekos.mindentEngedelyez()
        self.boss.korOsszegzo.config(text=s.language.ship_spotted_alvarez)
