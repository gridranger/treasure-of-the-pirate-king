from tkinter import BOTTOM, Button, DISABLED, Frame, HORIZONTAL, IntVar, Label, LEFT, NORMAL, RIGHT, Scale, \
    StringVar, TOP, Toplevel, X, Y
from tkinter.ttk import LabelFrame, Separator
from assets import Gallery
from settings import ApplicationSettings as s


class Varos(object):
    def __init__(self, parent, master, empire, matrozokszama=5):
        self.matrozokszama = IntVar()
        self.matrozokszama.set(matrozokszama)
        self.boss = parent
        self.master = master
        self.empire = empire

    @property
    def nev(self):
        return self.empire.capital

    @property
    def zaszlo(self):
        return self.empire.adjective

    def aktival(self):
        "Működteti a kikötőt."
        self.letrehoz()

    def letrehoz(self):
        self.ablak = Toplevel()
        if self.nev == 'portroyal':
            self.ablak.title((s.language.port + ' - Port Royal'))
        else:
            self.ablak.title((s.language.port, '-', self.nev.capitalize()))
        self.ablak.transient(self.master)
        self.ablak.grab_set()
        self.ujMatrozok()  # A játékos belépésekor a kocka által mutatott számot hozzáadjuk a helyi matrózok létszámához.
        self.tevekenysegek = Frame(self.ablak)  # Főkeret: tartalma panelek és gombok
        self.tevekenysegek.pack(side=TOP, ipadx=5)
        # A kép panel
        self.kep = Label(self.tevekenysegek, image=Gallery.get(self.nev))
        self.kep.pack(side=LEFT, pady=5, padx=5, fill=Y)
        # A fogadó panel
        self.fogado = LabelFrame(self.tevekenysegek, text=s.language.tavern)
        line1 = Frame(self.fogado)  # a bérelhető létszám
        Label(line1, text=(s.language.sailors_to_hire + ':')).pack(side=LEFT)
        self.matrozokszama_kiirva = Label(line1, textvariable=self.matrozokszama).pack(side=RIGHT)
        line1.pack(side=TOP, fill=X)
        line2 = Frame(self.fogado)  # legénység / hajó max. kapacitás
        Label(line2, text=(s.language.crew + ':')).pack(side=LEFT)
        Label(line2, textvariable=self.boss.aktivjatekos.crew_limit).pack(side=RIGHT)
        Label(line2, text='/').pack(side=RIGHT)
        Label(line2, textvariable=self.boss.aktivjatekos.crew).pack(side=RIGHT)
        line2.pack(side=TOP, fill=X)
        Separator(self.fogado, orient=HORIZONTAL).pack(side=TOP, fill=X, pady=5, padx=5)
        line3 = Frame(self.fogado)  # a skála címe
        szoveg = s.language.crew_new
        szoveg = szoveg + ' ' * (33 - len(szoveg))
        Label(line3, text=szoveg).pack(side=LEFT)
        line3.pack(side=TOP, fill=X)
        self.line4 = Frame(self.fogado)  # a skála
        self.berskala = Scale(self.line4)
        self.line4.pack(side=TOP, fill=X)
        self.line5 = Frame(self.fogado)  # a skálán beállított értéket érvényesítő gomb
        self.skalaCimke = Label(self.line5)
        self.felberel = Button(self.line5, text=s.language.crew_hire, command=self.matrozFelberelese)
        self.felberel.pack(side=RIGHT, padx=5, pady=5)
        self.line5.pack(side=TOP, fill=X)
        self.fogado.pack(side=LEFT, pady=5, padx=5, fill=Y)
        # A hajóács panel
        self.hajoacs = LabelFrame(self.tevekenysegek, text=s.language.shipwright)
        self.hajoacs_lekepez()
        self.hajoacs.pack(side=LEFT, fill=Y, pady=5)
        # A kormányzó panel
        pontok = 0
        kormanyzo_mondja = StringVar()
        for pontforras in self.boss.aktivjatekos.scores.keys():
            pontok += self.boss.aktivjatekos.scores[pontforras].get()
        self.kormanyzo = LabelFrame(self.tevekenysegek, text=s.language.governor)
        if self.empire == 'pirate':
            elsullyesztettHelyiHajok = 0  # A kalózok nem birodalom, nem büntetnek az elsüllyedt kalózhajókért
        else:
            elsullyesztettHelyiHajok = self.boss.aktivjatekos.scores[self.empire.adjective].get()
        if elsullyesztettHelyiHajok > 0:
            kormanyzo_mondja.set(s.language.governor_punish % elsullyesztettHelyiHajok)
            self.boss.aktivjatekos.update_turns_to_miss(elsullyesztettHelyiHajok)
            self.boss.aktivjatekos.scores[self.empire.adjective].set(0)
        else:
            maxJutalom = self.jutalomszamolo() * 8
            kormanyzo_mondja.set(s.language.governor_reward % maxJutalom)
            self.boss.aktivjatekos.update_gold(maxJutalom)
            self.penzszamolo()
            for birodalom in self.boss.aktivjatekos.scores.keys():
                self.boss.aktivjatekos.scores[birodalom].set(0)
        Label(self.kormanyzo, wraplength=125, textvariable=kormanyzo_mondja).pack(side=LEFT)
        if self.empire != 'pirate' and pontok > 0:
            self.kormanyzo.pack(side=LEFT, pady=5, padx=5, fill=Y)
        # Gombok
        Button(self.ablak, text=s.language.done, command=self.ablak.destroy).pack(side=BOTTOM, pady=5)
        self.ablak.update_idletasks()
        w, h = self.ablak.winfo_width(), self.ablak.winfo_height()
        bx, by = self.master.get_window_position()
        bh, bw = self.master.height, self.master.width
        self.ablak.geometry('+' + str(int(bx + (bw + (bh / 3) - w) / 2)) + '+' + str(int(by + (bh - h) / 2)))
        self.master.wait_window(self.ablak)

    def hajoacs_lekepez(self):
        "A hajóácspanel."
        self.hajoframek = {}
        self.hajogombok = {}
        for hajo in self.boss.vehetoHajok:
            self.hajoframek[hajo] = Frame(self.hajoacs)
            self.hajogombok[hajo] = Button(self.hajoframek[hajo], image=Gallery.get(hajo),
                                           command=lambda hajo=hajo: self.ujHajo(hajo))
            self.hajogombok[hajo].pack(side=LEFT)
            if self.boss.aktivjatekos.ship in self.boss.vehetoHajok:
                if self.boss.vehetoHajok.index(self.boss.aktivjatekos.ship) < self.boss.vehetoHajok.index(hajo):
                    ar = self.boss.hajotipustar[hajo].price - self.boss.hajotipustar[self.boss.aktivjatekos.ship].price
                    Label(self.hajoframek[hajo],
                          text='%s: %i %s' % (s.language.price, ar, s.language.gold)).pack(
                        side=LEFT, fill=X)
                else:
                    Label(self.hajoframek[hajo], text=s.language.already_bought).pack(side=LEFT, fill=X)
            else:
                Label(self.hajoframek[hajo], text='%s: %i %s' % (
                    s.language.price, self.boss.hajotipustar[hajo].price,
                    s.language.gold)).pack(side=LEFT, fill=X)
            self.hajoframek[hajo].pack(side=TOP, pady=5, padx=5, fill=X)
        self.penzszamolo()
        self.hajoacs.pack(fill=Y, pady=5)

    def jutalomszamolo(self):
        "Megmutatja, mennyi jutalmat vehet át a játékos legfeljebb."
        scores = self.boss.aktivjatekos.scores
        pontszam = 0
        for birodalom in scores.keys():
            helyiPontszam = scores[birodalom].get()
            if helyiPontszam / 5 > 0:
                pontszam += int(helyiPontszam / 5) * 7
                helyiPontszam = helyiPontszam % 5
            if helyiPontszam / 3 > 0:
                pontszam += int(helyiPontszam / 3) * 4
                helyiPontszam = helyiPontszam % 3
            pontszam += helyiPontszam
        return pontszam

    def penzszamolo(self):
        "A játékos anyagi lehetőségeinek fényében engedélyezi a hajók vásárlását."
        current_ship = self.boss.aktivjatekos.ship
        if current_ship in self.boss.vehetoHajok:
            for hajo in self.boss.vehetoHajok:
                price = self.boss.hajotipustar[hajo].price
                if hajo == current_ship:
                    self.hajogombok[hajo].config(state=DISABLED)
                elif price < self.boss.hajotipustar[current_ship].price:
                    self.hajogombok[hajo].config(state=DISABLED)
                elif price - self.boss.hajotipustar[current_ship].price > self.boss.aktivjatekos.gold.get():
                    self.hajogombok[hajo].config(state=DISABLED)
                else:
                    self.hajogombok[hajo].config(state=NORMAL)
        else:
            for hajo in self.boss.vehetoHajok:
                if self.boss.hajotipustar[hajo].price > self.boss.aktivjatekos.gold.get():
                    self.hajogombok[hajo].config(state=DISABLED)
                else:
                    self.hajogombok[hajo].config(state=NORMAL)
        self.berskalat_letrehoz()

    def berskalat_letrehoz(self):
        "Létrehozza a skálát, a felbérelendő matrózok számának kijelöléséhez."
        crew_limit = self.boss.hajotipustar[self.boss.aktivjatekos.ship].crew_limit - self.boss.aktivjatekos.crew.get()
        locally_available_sailors = self.matrozokszama.get()
        berskalahossz = min(crew_limit, locally_available_sailors, self.boss.aktivjatekos.gold.get())
        self.berskala.destroy()
        self.skalaCimke.destroy()
        if not berskalahossz:
            if self.boss.hajotipustar[self.boss.aktivjatekos.ship].crew_limit - self.boss.aktivjatekos.crew.get() == 0:
                visszajelzes = s.language.crew_ship_full
            elif self.matrozokszama.get() == 0:
                visszajelzes = s.language.crew_port_empty
            else:
                visszajelzes = s.language.crew_no_money
            self.berskala = Label(self.line4, text=visszajelzes)
            self.felberel.config(state=DISABLED)
        else:
            self.berskala = Scale(self.line4, from_=0, to=berskalahossz,
                                  orient=HORIZONTAL, resolution=1, takefocus=0,
                                  showvalue=0, command=self.berskalaErtek)
            self.skalaCimke = Label(self.line5)
            self.skalaCimke.pack()
            self.felberel.config(state=NORMAL)
        self.berskala.pack(side=TOP, fill=X)

    def berskalaErtek(self, event):
        self.skalaCimke.config(text=str(self.berskala.get()))

    def ujMatrozok(self):
        self.matrozokszama.set(self.matrozokszama.get() + self.boss.boss.menu.game_tab.die._current_value)

    def matrozFelberelese(self):
        "Lebonyolítja a metrózok felbérelésével járó tranzakciót"
        delta = self.berskala.get()
        if not delta:
            return
        else:
            self.boss.aktivjatekos.update_crew(delta)
            self.boss.aktivjatekos.update_gold(-delta)
            self.matrozokszama.set(self.matrozokszama.get() - delta)
            self.berskalat_letrehoz()
        self.penzszamolo()

    def ujHajo(self, tipus=''):
        "Lebonyolítja az új hajó vásárlásával járó tranzakciót"
        ar = self.boss.hajotipustar[tipus].price - self.boss.hajotipustar[self.boss.aktivjatekos.ship].price
        self.boss.aktivjatekos.update_ship(tipus)
        self.boss.aktivjatekos.update_gold(-ar)
        self.boss.aktivjatekos.crew_limit.set(self.boss.hajotipustar[tipus].crew_limit)
        for hajo in self.boss.vehetoHajok:
            self.hajoframek[hajo].destroy()
            self.hajogombok[hajo].destroy()
        self.hajoacs_lekepez()

    def export_matroz(self):
        "Átadja saját adatait a mentéshez."
        return self.matrozokszama.get()
