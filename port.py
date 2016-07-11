# -*- coding: utf-8 -*-
from tkinter import IntVar, Scale, StringVar, Y
from card import *
from tkinter.ttk import LabelFrame, Separator


__author__ = 'Bárdos Dávid'


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
        return self.empire.empire_id

    def aktival(self):
        "Működteti a kikötőt."
        self.letrehoz()

    def letrehoz(self):
        self.ablak = Toplevel()
        if self.nev == 'portroyal':
            self.ablak.title((self.master.ui_texts['port'] + ' - Port Royal'))
        else:
            self.ablak.title((self.master.ui_texts['port'], '-', self.nev.capitalize()))
        self.ablak.transient(self.master)
        self.ablak.grab_set()
        self.ujMatrozok()  # A játékos belépésekor a kocka által mutatott számot hozzáadjuk a helyi matrózok létszámához.
        self.tevekenysegek = Frame(self.ablak)  # Főkeret: tartalma panelek és gombok
        self.tevekenysegek.pack(side=TOP, ipadx=5)
        # A kép panel
        self.kep = Label(self.tevekenysegek, image=self.master.game_board.gallery[self.nev])
        self.kep.pack(side=LEFT, pady=5, padx=5, fill=Y)
        # A fogadó panel
        self.fogado = LabelFrame(self.tevekenysegek, text=self.master.ui_texts['tavern'])
        line1 = Frame(self.fogado)  # a bérelhető létszám
        Label(line1, text=(self.master.ui_texts['sailors_to_hire'] + ':')).pack(side=LEFT)
        self.matrozokszama_kiirva = Label(line1, textvariable=self.matrozokszama).pack(side=RIGHT)
        line1.pack(side=TOP, fill=X)
        line2 = Frame(self.fogado)  # legénység / hajó max. kapacitás
        Label(line2, text=(self.master.ui_texts['crew'] + ':')).pack(side=LEFT)
        Label(line2, textvariable=self.boss.aktivjatekos.legenyseg_max).pack(side=RIGHT)
        Label(line2, text='/').pack(side=RIGHT)
        Label(line2, textvariable=self.boss.aktivjatekos.legenyseg).pack(side=RIGHT)
        line2.pack(side=TOP, fill=X)
        berskalahossz = min(self.boss.aktivjatekos.legenyseg_max.get(), self.matrozokszama.get(),
                            self.boss.aktivjatekos.kincs.get())
        Separator(self.fogado, orient=HORIZONTAL).pack(side=TOP, fill=X, pady=5, padx=5)
        line3 = Frame(self.fogado)  # a skála címe
        szoveg = self.master.ui_texts['crew_new']
        szoveg = szoveg + ' ' * (33 - len(szoveg))
        Label(line3, text=szoveg).pack(side=LEFT)
        line3.pack(side=TOP, fill=X)
        self.line4 = Frame(self.fogado)  # a skála
        self.berskala = Scale(self.line4)
        self.line4.pack(side=TOP, fill=X)
        self.line5 = Frame(self.fogado)  # a skálán beállított értéket érvényesítő gomb
        self.skalaCimke = Label(self.line5)
        self.felberel = Button(self.line5, text=self.master.ui_texts['crew_hire'], command=self.matrozFelberelese)
        self.felberel.pack(side=RIGHT, padx=5, pady=5)
        self.line5.pack(side=TOP, fill=X)
        self.fogado.pack(side=LEFT, pady=5, padx=5, fill=Y)
        # A hajóács panel
        self.hajoacs = LabelFrame(self.tevekenysegek, text=self.master.ui_texts['shipwright'])
        self.hajoacs_lekepez()
        self.hajoacs.pack(side=LEFT, fill=Y, pady=5)
        # A kormányzó panel
        pontok = 0
        kormanyzo_mondja = StringVar()
        for pontforras in self.boss.aktivjatekos.hajotar.keys():
            pontok += self.boss.aktivjatekos.hajotar[pontforras].get()
        self.kormanyzo = LabelFrame(self.tevekenysegek, text=self.master.ui_texts['governor'])
        if self.zaszlo == 'pirate':
            elsullyesztettHelyiHajok = 0  # A kalózok nem birodalom, nem büntetnek az elsüllyedt kalózhajókért
        else:
            elsullyesztettHelyiHajok = self.boss.aktivjatekos.hajotar[self.zaszlo].get()
        if elsullyesztettHelyiHajok > 0:
            kormanyzo_mondja.set(self.master.ui_texts['governor_punish'] % elsullyesztettHelyiHajok)
            self.boss.aktivjatekos.set_kimarad(elsullyesztettHelyiHajok)
            self.boss.aktivjatekos.set_hajoszam(self.zaszlo, -elsullyesztettHelyiHajok)
        else:
            maxJutalom = self.jutalomszamolo() * 8
            kormanyzo_mondja.set(self.master.ui_texts['governor_reward'] % maxJutalom)
            self.boss.aktivjatekos.set_kincs(maxJutalom)
            self.penzszamolo()
            for birodalom in self.boss.aktivjatekos.hajotar.keys():
                fizetve = self.boss.aktivjatekos.hajotar[birodalom].get()
                self.boss.aktivjatekos.set_hajoszam(birodalom, -fizetve)
        Label(self.kormanyzo, wraplength=125, textvariable=kormanyzo_mondja).pack(side=LEFT)
        if self.zaszlo != 'pirate' and pontok > 0:
            self.kormanyzo.pack(side=LEFT, pady=5, padx=5, fill=Y)
        # Gombok
        Button(self.ablak, text=self.master.ui_texts['done'], command=self.ablak.destroy).pack(side=BOTTOM, pady=5)
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
            self.hajogombok[hajo] = Button(self.hajoframek[hajo], image=self.master.game_board.gallery[hajo],
                                           command=lambda hajo=hajo: self.ujHajo(hajo))
            self.hajogombok[hajo].pack(side=LEFT)
            if self.boss.aktivjatekos.hajo in self.boss.vehetoHajok:
                if self.boss.vehetoHajok.index(self.boss.aktivjatekos.hajo) < self.boss.vehetoHajok.index(hajo):
                    ar = self.boss.hajotipustar[hajo].price - self.boss.hajotipustar[self.boss.aktivjatekos.hajo].price
                    Label(self.hajoframek[hajo],
                          text='%s: %i %s' % (self.master.ui_texts['price'], ar, self.master.ui_texts['gold'])).pack(
                        side=LEFT, fill=X)
                else:
                    Label(self.hajoframek[hajo], text=self.master.ui_texts['already_bought']).pack(side=LEFT, fill=X)
            else:
                Label(self.hajoframek[hajo], text='%s: %i %s' % (
                self.master.ui_texts['price'], self.boss.hajotipustar[hajo].price, self.master.ui_texts['gold'])).pack(
                    side=LEFT, fill=X)
            self.hajoframek[hajo].pack(side=TOP, pady=5, padx=5, fill=X)
        self.penzszamolo()
        self.hajoacs.pack(fill=Y, pady=5)

    def jutalomszamolo(self):
        "Megmutatja, mennyi jutalmat vehet át a játékos legfeljebb."
        hajotar = self.boss.aktivjatekos.hajotar
        pontszam = 0
        for birodalom in hajotar.keys():
            helyiPontszam = hajotar[birodalom].get()
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
        if self.boss.aktivjatekos.hajo in self.boss.vehetoHajok:
            for hajo in self.boss.vehetoHajok:
                if hajo == self.boss.aktivjatekos.hajo:
                    self.hajogombok[hajo].config(state=DISABLED)
                elif self.boss.hajotipustar[hajo].price < self.boss.hajotipustar[self.boss.aktivjatekos.hajo].price:
                    self.hajogombok[hajo].config(state=DISABLED)
                elif self.boss.hajotipustar[hajo].price - self.boss.hajotipustar[
                    self.boss.aktivjatekos.hajo].price > self.boss.aktivjatekos.kincs.get():
                    self.hajogombok[hajo].config(state=DISABLED)
                else:
                    self.hajogombok[hajo].config(state=NORMAL)
        else:
            for hajo in self.boss.vehetoHajok:
                if self.boss.hajotipustar[hajo].price > self.boss.aktivjatekos.kincs.get():
                    self.hajogombok[hajo].config(state=DISABLED)
                else:
                    self.hajogombok[hajo].config(state=NORMAL)
        self.berskalat_letrehoz()

    def berskalat_letrehoz(self):
        "Létrehozza a skálát, a felbérelendő matrózok számának kijelöléséhez."
        berskalahossz = min(
            (self.boss.hajotipustar[self.boss.aktivjatekos.hajo].crew_limit - self.boss.aktivjatekos.legenyseg.get()),
            self.matrozokszama.get(), self.boss.aktivjatekos.kincs.get())
        self.berskala.destroy()
        self.skalaCimke.destroy()
        if not berskalahossz:
            if self.boss.hajotipustar[
                self.boss.aktivjatekos.hajo].crew_limit - self.boss.aktivjatekos.legenyseg.get() == 0:
                visszajelzes = self.master.ui_texts['crew_ship_full']
            elif self.matrozokszama.get() == 0:
                visszajelzes = self.master.ui_texts['crew_port_empty']
            else:
                visszajelzes = self.master.ui_texts['crew_no_money']
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
        "A mezőre lépéskor módosítja a helyben elérhető matrózok számát."
        self.matrozokszama.set(self.matrozokszama.get() + self.boss.boss.menu.game_tab.die.export_ertek())

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

    def ujHajo(self, tipus=''):
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
