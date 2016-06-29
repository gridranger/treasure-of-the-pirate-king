# -*- coding: utf-8 -*-
from tkinter import Frame, DISABLED, Label, N, E, W, S, ALL, HORIZONTAL, Button, RAISED
from tkinter.ttk import LabelFrame, Separator
from game import Dobokocka

__author__ = 'Bárdos Dávid'


class GameTab(Frame):
    """A játékos menü osztálya."""

    def __init__(self, boss, notepad):
        Frame.__init__(self, notepad)
        self.boss = boss
        self.master = self.boss.boss
        self.aktivjatekos = None
        if self.master.is_game_in_progress.get():
            self.aktivjatekos = self.master.engine.aktivjatekos
            self.feltolt()
        else:
            self.boss.tab(1, state=DISABLED)
            self.fejlec = Frame()
            self.kincseslada = Frame(self)
            self.kockamezo = Frame(self)
            self.pontmezo = Frame(self)
            self.jateksor = Frame(self)

    def feltolt(self):
        "Megjeleníti a fül tényleges tartalmát."
        self.fejlec_epito(0)
        self.kincseslada_epito(1)
        # self.vonal(2)
        self.pontszamok_epito(2)
        self.statusz_epito(3)
        self.vonal(4)
        self.kockamezo_epito(5)
        self.vonal(6)
        self.sorrend_epito(7)

    def fejlec_epito(self, pozicio):
        "A fejléc."
        self.fejlec = Frame(self)
        Label(self.fejlec, text=self.aktivjatekos.nev).grid(row=0, column=0)
        Label(self.fejlec, image=self.master.game_board.gallery['flag_' + self.aktivjatekos.empire]).grid(row=1, column=0)
        self.fejlec.grid(row=pozicio, column=0, pady=5)

    def kincseslada_epito(self, pozicio):
        "Pénz- és legénységkijelző."
        self.kincseslada = Frame(self)
        rekesz0 = LabelFrame(self.kincseslada, text=self.master.ui_texts['treasure'])
        Label(rekesz0, image=self.master.game_board.gallery['penz-d2']).grid(row=0, column=0)
        Label(rekesz0, textvariable=self.aktivjatekos.kincs).grid(row=0, column=1)
        rekesz0.grid(row=0, column=0, sticky=N + E + W + S, padx=5)
        rekesz1 = LabelFrame(self.kincseslada, text=self.master.ui_texts['crew'])
        Label(rekesz1, image=self.master.game_board.gallery['matrozok']).grid(row=0, column=0)
        Label(rekesz1, textvariable=self.aktivjatekos.legenyseg).grid(row=0, column=1)
        rekesz1.grid(row=0, column=1, sticky=N + E + W + S, padx=5)
        self.kincseslada.grid(row=pozicio, column=0)
        self.kincseslada.columnconfigure(ALL, minsize=(self.boss.width - 20) / 2)

    def vonal(self, pozicio):
        "Vonal."
        Separator(self, orient=HORIZONTAL).grid(row=pozicio, column=0, sticky=E + W, padx=5, pady=5)

    def pontszamok_epito(self, pozicio):
        "Pontozótábla."
        pontmezo = LabelFrame(self, text=self.master.ui_texts['scores'])
        ponthelyszamlalo = 0
        pontkeretszotar = {}
        for birodalom in sorted(self.master.empires.keys()):
            if birodalom != self.aktivjatekos.empire:
                pontkeretszotar[birodalom] = Frame(pontmezo)
                Label(pontkeretszotar[birodalom], image=self.master.game_board.gallery['flag_' + birodalom]).grid(row=0,
                                                                                                              column=0)
                Label(pontkeretszotar[birodalom], text=':').grid(row=0, column=1)
                Label(pontkeretszotar[birodalom], textvariable=self.aktivjatekos.hajotar[birodalom]).grid(row=0,
                                                                                                          column=2)
                pontkeretszotar[birodalom].grid(row=int((ponthelyszamlalo / 2) % 2), column=ponthelyszamlalo % 2,
                                                sticky=E + W)
                ponthelyszamlalo += 1
        pontmezo.grid(row=pozicio, column=0)
        pontmezo.columnconfigure(ALL, minsize=(self.boss.width - 34) / 2)

    def kockamezo_epito(self, pozicio):
        "A dobókocka megjelenítőfelülete."
        self.kockamezo = Frame(self)
        self.kockamezo.columnconfigure(0, weight=1)
        self.kockamezo.rowconfigure(0, weight=1)
        self.kockamezo.grid(row=pozicio, column=0, ipady=5, ipadx=5)
        kimaradas = self.aktivjatekos.kimarad.get()
        if kimaradas > 0:
            if kimaradas > 1:
                uzenet = self.master.ui_texts["miss_turn"] % kimaradas
            else:
                uzenet = self.master.ui_texts["miss_turn_last_time"]
            Button(self.kockamezo, text=uzenet, command=self.master.engine.kimaradas).pack()
            if "leviathan" in self.master.engine.aktivjatekos.statuszlista:
                Button(self.kockamezo, text=self.master.ui_texts["play_leviathan"],
                       command=self.master.engine.leviathan_kijatszasa).pack()
        else:
            self.kockamezo.config(relief=RAISED, bd=2)
            self.kocka = Dobokocka(self.kockamezo, self.boss.width / 4, self.aktivjatekos.szin,
                                   self.aktivjatekos.masodikszin, self.aktivjatekos.utolsodobas)
            if self.master.engine.aktivjatekos.pozicio in self.master.game_board.locations[
                "szamuzottek"] and not self.master.engine.aktivjatekos.legenyseg.get():
                self.kocka.bind('<Button-1>', self.master.engine.szamuzottek)
            else:
                self.kocka.bind('<Button-1>', self.boss.dobas)
            self.kocka.grid(row=0, column=0)

    def sorrend_epito(self, pozicio):
        "A sorrend megjelenítője."
        self.jateksor = Frame(self)
        self.jateksorszotar = {}
        sor = self.master.player_order
        self.jateksorCimke = Label(self.jateksor, text=self.master.ui_texts['turn_order'])
        self.jateksorCimke.grid(row=0, column=0, sticky=W)
        for sorszam in range(len(self.master.player_order)):
            self.jateksorszotar['label' + str(sorszam)] = Label(self.jateksor,
                                                                text=str(sorszam + 1) + '. ' + self.master.players[
                                                                    sor[sorszam]].nev,
                                                                bg=self.master.players[sor[sorszam]].szin,
                                                                fg=self.master.players[sor[sorszam]].masodikszin)
            self.jateksorszotar['label' + str(sorszam)].grid(row=sorszam + 1, column=0, sticky=W, padx=10)
        self.jateksor.grid(row=pozicio, column=0, sticky=W, padx=5)

    def statusz_epito(self, pozicio):
        "A játékos státuszainak megjelenítője."
        statuszmezo = LabelFrame(self, text=self.master.ui_texts['cards'], relief=RAISED, width=self.boss.width - 31)
        maxStatuszEgySorban = int((self.boss.width - 31) / 32)
        if len(self.master.engine.aktivjatekos.statuszlista):
            i = 0
            for statusz in self.master.engine.aktivjatekos.statuszlista:
                if statusz in self.master.engine.nemKartyaStatusz:
                    pass
                else:
                    if statusz in self.master.engine.eventszotar.keys():
                        hely = self.master.engine.eventszotar
                    else:
                        hely = self.master.engine.kincsszotar
                    leendoKep = self.master.engine.eventszotar[statusz].kep + '_i'
                    leendoKep = leendoKep[(leendoKep.find('_') + 1):]
                    Button(statuszmezo, image=self.master.game_board.gallery[leendoKep],
                           command=lambda statusz=statusz: hely[statusz].megjelenik(1)).grid(
                        row=int(i / maxStatuszEgySorban), column=i % maxStatuszEgySorban)
                    i += 1
            statuszmezo.config(height=24 + ((int(i / maxStatuszEgySorban) + 1) * 32))
            if statuszmezo.winfo_children():
                statuszmezo.grid(row=pozicio, column=0)
            statuszmezo.grid_propagate(False)