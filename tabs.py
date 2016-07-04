# -*- coding: utf-8 -*-
from logging import debug
from gametab import GameTab
from tkinter import DISABLED, E, FLAT, HORIZONTAL, NORMAL, RAISED, SUNKEN, N, W
from tkinter import Checkbutton, Button, Entry, Frame, IntVar, Label, Scale
from tkinter.messagebox import askokcancel
from tkinter.ttk import Combobox, LabelFrame, Notebook

__author__ = 'Bárdos Dávid'


class Tabs(Notebook):
    def __init__(self, boss=None, width=0):
        Notebook.__init__(self, master=boss, width=width)
        self.boss = boss
        self.width = width
        self.may_use_land_land_roll = False
        self.tabs = [MainTab(self, boss), Frame(self), Frame(self), Frame(self)]
        for tab in self.tabs:
            self._position_tab(tab)
        self._enable_hotkeys()
        self.grid(row=0, column=0)
        self.ful1()
        self.ful2()
        self.ful3()

    def _position_tab(self, tab):
        tab.columnconfigure(0, weight=1)
        tab.grid(row=0, column=0)
        self.add(tab, text='', underline=0, sticky=N + E + W)

    def _enable_hotkeys(self):
        self.enable_traversal()

    def push_new_game_button(self):
        self.tabs[0].push_new_game_button()

    def release_new_game_button(self):
        self.tabs[0].release_new_game_button()

    def enable_save_buttons(self):
        self.tabs[0].enable_save_buttons()

    def disable_save_buttons(self):
        self.tabs[0].disable_save_buttons()

    def ful1(self):
        "A játék menü elemeinek betöltése."
        self.ful1tartalom = Frame()
        if self.boss.is_game_in_progress.get():
            self.ful1feltolt()
        else:
            self.tab(1, state=DISABLED)

    def ful2(self):
        self.felbontasmezo = LabelFrame(self.tabs[2], text='')
        self.nyelvMezo = LabelFrame(self.tabs[2], text='')
        self.newscreen = IntVar()
        self.newscreen.set(self.boss.is_full_screen.get())
        sorszam = 0
        for mezo in (self.felbontasmezo, self.nyelvMezo):
            mezo.columnconfigure(0, weight=1)
            mezo.grid(row=sorszam, column=0, sticky=E + W, padx=5, pady=5)
            sorszam += 1
        # Felbontás
        self.felbontaslista = sorted(
            self.boss.resolution_list)  # rendezzük a listát arra az esetre, ha felhasználó beleírt volna egy új értéket
        self.felbontasskala = Scale(self.felbontasmezo, from_=0, to=len(self.felbontaslista) - 1,
                                    orient=HORIZONTAL, resolution=1,
                                    takefocus=0, showvalue=0,
                                    length=self.width, command=self.felbontassav)
        self.felbontasskala.set(
            self.felbontaslista.index([item for item in self.felbontaslista if item[2] == self.boss.resolution_code][0]))
        self.felbontasskala.grid(row=0, column=0, columnspan=2, sticky=E + W)
        self.felbontaskijelzo = Label(self.felbontasmezo, text=(self.boss.width, '×', self.boss.height))
        self.felbontaskijelzo.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.felbontasvalto = Button(self.felbontasmezo, textvariable=self.boss.ui_text_variables['apply'],
                                     command=lambda: self.boss.resize(self.felbontaslista[self.felbontasskala.get()],
                                                                      self.newscreen.get()), state=DISABLED)
        self.felbontasvalto.grid(row=1, column=1, padx=5, pady=5, sticky=E)
        self.teljeskepernyo = Label(self.felbontasmezo, textvariable=self.boss.ui_text_variables['full_screen'])
        self.teljeskepernyo.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.teljeskepernyoPipa = Checkbutton(self.felbontasmezo, takefocus=0, variable=self.newscreen,
                                              command=lambda: self.felbontasvalto.config(state=NORMAL))
        self.teljeskepernyoPipa.grid(row=2, column=1, padx=5, pady=5, sticky=E)
        # Nyelv
        self.nyelvmodul()

    def ful3(self):
        if not self.boss.debug_mode:
            self.hide(3)
        self.tab(3, text='D')
        gombsor = Frame(self.tabs[3])
        Button(gombsor, text='Kincskártya húzása', command=lambda: self.boss.engine.kincsetHuz()).grid()
        gombsor.grid(row=0)
        aranybeallit = Frame(self.tabs[3])
        Label(aranybeallit, text='Arany növelése:').grid(column=0, row=0)
        aranyMezo = Entry(aranybeallit, width=3)
        aranyMezo.grid(column=1, row=0)
        Button(aranybeallit, text='Beállít',
               command=lambda: self.boss.engine.aktivjatekos.set_kincs(int(aranyMezo.get()))).grid(column=2, row=0)
        aranybeallit.grid(row=1)

    def ful3_var(self):
        valtozok = Frame(self.tabs[3])
        Label(valtozok, text='hadnagyElokerult:').grid(column=0, row=0)
        Label(valtozok, text='grogbaroLegyozve:').grid(column=0, row=1)
        Label(valtozok, textvar=self.boss.engine.hadnagyElokerult).grid(column=1, row=0)
        Label(valtozok, textvar=self.boss.engine.grogbaroLegyozve).grid(column=1, row=1)
        valtozok.grid(row=2)

    def ful1feltolt(self, aktivjatekos=None):
        self.ful1tartalom.destroy()
        self.ful1tartalom = GameTab(self, self.tabs[1])
        self.ful1tartalom.grid(pady=5)

    def dobas(self, event):
        "Dob a kockával."
        if self.may_use_land_land_roll:
            self.boss.game_board.villogaski()
            self.boss.engine.dobasMegtortent.set(False)
        if not self.boss.engine.dobasMegtortent.get():
            dobas = self.ful1tartalom.kocka.dob()
            if "fold_fold" in self.boss.engine.aktivjatekos.statuszlista:
                debug("New roll is possible because of Land, land! bonus.")
                self.boss.status_bar.log(self.boss.ui_texts['land_log'])
                self.boss.engine.aktivjatekos.set_statusz("fold_fold", 0)
                self.may_use_land_land_roll = True
            else:
                self.boss.status_bar.log('')
                self.ful1tartalom.kockamezo.config(relief=SUNKEN)
            self.boss.engine.set_dobasMegtortent()
            self.boss.is_turn_in_progress.set(1)
            self.boss.engine.aktivjatekos.set_utolsodobas(dobas)
            self.boss.engine.mozgas(dobas, 1)

    def felbontassav(self, ertek):
        "A felbontáscsúszka betöltése"
        self.felbontaskijelzo.config(
            text=(str(self.felbontaslista[int(ertek)][0]), '×', str(self.felbontaslista[int(ertek)][1])))
        if (self.boss.width, self.boss.height) == (
        self.felbontaslista[int(ertek)][0], self.felbontaslista[int(ertek)][1]):
            self.felbontasvalto.config(state=DISABLED)
        else:
            self.felbontasvalto.config(state=NORMAL)

    def nyelvmodul(self):
        "Leképezi a nyelvi modult"
        self.nyelvlista = self.boss.data_reader.load_language_list()
        self.nyelvlistaR = {v: k for k, v in self.nyelvlista.items()}
        self.nyelvvalaszto = Combobox(self.nyelvMezo, value=sorted(list(self.nyelvlista)), takefocus=0)
        self.nyelvvalaszto.set(self.nyelvlistaR[self.boss.language])
        self.nyelvvalaszto.bind("<<ComboboxSelected>>", self.ujnyelv)
        self.nyelvvalaszto.grid(row=0, column=0, padx=5, pady=5)

    def ujnyelv(self, event):
        "Meghívja főfolyamat nyelvváltó eseményét."
        ujnyelv = self.nyelvlista[self.nyelvvalaszto.get()]  # kinyerjük a választott nyelvet
        self.boss.set_new_language(ujnyelv)



class MainTab(Frame):
    def __init__(self, parent, master):
        Frame.__init__(self, parent)
        self._new_game_button = Button(self, textvariable=master.ui_text_variables['new_game'],
                                       command=master.start_game_setup, width=20, overrelief=RAISED, relief=FLAT)
        self._load_button = Button(self, textvariable=master.ui_text_variables['load_saved_game'],
                                   command=master.select_file_to_load, width=20, overrelief=RAISED, relief=FLAT)
        self._save_button = Button(self, textvariable=master.ui_text_variables['save'], command=master.save_game,
                                   width=20, overrelief=RAISED, relief=FLAT, state=DISABLED)
        self._save_and_exit_button = Button(self, textvariable=master.ui_text_variables['save_and_exit'],
                                            command=master.save_and_exit, width=20, overrelief=RAISED, relief=FLAT,
                                            state=DISABLED)
        self._exit_button = Button(self, textvariable=master.ui_text_variables['exit'], command=master.exit, width=20,
                                   overrelief=RAISED, relief=FLAT)
        self._position_elements()

    def _position_elements(self):
        self.grid(row=0, column=0, pady=10)
        self._new_game_button.grid(row=0, column=0)
        self._load_button.grid(row=1, column=0)
        self._save_button.grid(row=2, column=0)
        self._save_and_exit_button.grid(row=3, column=0)
        self._exit_button.grid(row=4, column=0)

    def push_new_game_button(self):
        self._new_game_button.config(relief=SUNKEN, overrelief=SUNKEN)

    def release_new_game_button(self):
        self._new_game_button.config(overrelief=RAISED, relief=FLAT)

    def enable_save_buttons(self):
        self._save_button.config(state=NORMAL)
        self._save_and_exit_button.config(state=NORMAL)

    def disable_save_buttons(self):
        self._save_button.config(state=DISABLED)
        self._save_and_exit_button.config(state=DISABLED)
