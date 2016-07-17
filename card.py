from logging import debug
from random import randrange
from tkinter import BOTTOM, Button, DISABLED, Frame, GROOVE, HORIZONTAL, Label, LEFT, NORMAL, RIGHT, TOP, Toplevel, X
from tkinter.ttk import Separator


class Card(object):
    """Egy kártyalap leírója."""
    def __init__(self, boss, master, nev, kep, pakli, fuggveny, ertek=0):
        self.boss = boss
        self.master = self.boss.boss
        # --- A kártya tulajdonságai. --- #
        self.nev = nev  # A kártyalap neve
        self.kep = kep   # A kártyalap képe
        self.pakli = pakli   # A szülőpakli.
        self.ertek = ertek   # Ha kincs, értéke
        self.fuggveny = fuggveny
        # --- Eddig tartottak a kártya tulajdonságai. --- #
        
    def megjelenik(self, megtekint=0):
        "Megjelenítő-függvény."
        self.ablak = KartyaAblak(self.master, self.pakli, self.kep, self.nev, self.ertek, self.fuggveny, megtekint)
        self.ablak.grab_set()
        self.ablak.update_idletasks()
        w, h = self.ablak.winfo_width(),self.ablak.winfo_height()
        bx, by = self.master.get_window_position()
        bh, bw = self.master.height,self.master.width
        self.ablak.geometry('+'+str(int(bx+(bw+(bh/3)-w)/2))+'+'+str(int(by+(bh-h)/2)))
        self.master.wait_window(self.ablak)

class KartyaAblak(Toplevel):
    """A kártya megjelenítése a felületen."""
    def __init__(self, master, pakli, kep, nev, ertek, fuggveny, megtekint):
        Toplevel.__init__(self)
        self.master = master
        self.pakli = pakli
        self.nev = nev
        self.ertek = ertek
        self.fuggveny = fuggveny
        self.bezar = self.destroy
        cim = self.master.card_texts[self.nev][0]
        if self.nev == 'treasure':
            szoveg = self.master.card_texts[self.nev][1] % ertek
        else:
            szoveg = self.master.card_texts[self.nev][1]
        self.title(self.master.ui_texts[pakli+'_card'])
        cimStilus = 'helvetica 14 bold'
        self.kartyalap = Frame(self, relief = GROOVE, bd = 2, bg = 'ivory')
        Label(self.kartyalap, image = self.master.game_board.gallery[kep]).pack()
        Separator(self.kartyalap, orient = HORIZONTAL).pack(fill = X)
        Label(self.kartyalap, wraplength = 216, text = cim, font = cimStilus).pack(fill = X)
        Separator(self.kartyalap, orient = HORIZONTAL).pack(fill = X)
        self.szovegfelirat = Label(self.kartyalap, wraplength = 216, text = szoveg)
        self.szovegfelirat.pack(fill = X)
        self.kartyalap.pack(pady = 5, padx = 5)
        if megtekint:
            pass
        else:
            exec(self.fuggveny)
            self.protocol("WM_DELETE_WINDOW", self.bezar)
        self.transient(self.master)
        self.resizable(False,False)
        
    def noEscape(self):
        debug("There is no escape.")
        
    def dummy(self):
        debug("Card method is yet to be developed.")
        self.bezar = self.lapotEldob
        return
    
    def csakMegtart(self):
        "Függvény a lap kötelező megtartásához."
        self.bezar = self.lapotMegtart
        Button(self, text = self.master.ui_texts['card_keep'], command = self.lapotMegtart).pack(pady = 5)
    
    def lapotMegtart(self, event = None):
        "A lap megtartásának függvénye."
        self.master.engine.aktivjatekos.set_statusz(self.nev)
        self.destroy()
        self.master.engine.szakasz_0()
        
    def lapotEldob(self, event = None):
        debug("Card discarded.")
        if self.pakli == "event":
            self.master.engine.eventstack.append(self.nev)
            self.destroy()
            self.master.engine.szakasz_0()
        elif self.pakli == "treasure":
            self.master.engine.treasurestack.append(self.nev)
            self.destroy()
    
    def eltunik(self):
        "Az ablak bezárása."
        self.destroy()
        return False
        
    def treasure(self):
        "A pénzt adó kincskártyák függvénye."
        self.master.engine.aktivjatekos.set_kincs(self.ertek)
        Button(self, text = self.master.ui_texts['done'], command=self.destroy).pack(pady = 5, side = BOTTOM)
        return
        
    def sirens(self):
        "A sziréneket működtető függvény."
        enekEreje = randrange(1, 7)
        if enekEreje == 6:
            uzenet = self.master.ui_texts["sirens_skipped"]
            parancs = self.lapotMegtart
        else:
            if self.master.engine.aktivjatekos.legenyseg.get() > 3:
                self.master.engine.aktivjatekos.set_legenyseg(-3)
                uzenet = self.master.ui_texts["sirens"] % 3
            else:
                self.master.engine.aktivjatekos.set_legenyseg(-self.master.engine.aktivjatekos.get())
                uzenet = self.master.ui_texts["sirens"] % self.master.engine.aktivjatekos.legenyseg.get()
                self.master.game_board.hajotathelyez(5,2)
            parancs = self.lapotEldob
        self.bezar = parancs
        Label(self, text = uzenet, wraplength = 216).pack()
        Button(self, text = self.master.ui_texts['done'], command = parancs).pack(pady = 5, side = BOTTOM)
        
    def bobbyDick(self):
        "A cetet vezérlő függvény."
        self.bezar = self.lapotMegtart
        Button(self, text = self.master.ui_texts['card_keep'], command = self.lapotMegtart).pack(side = LEFT, pady = 5, padx = 5)
        Button(self, text = self.master.ui_texts['card_discard'], command = self.bobbyDick_eldob).pack(side = RIGHT, pady = 5, padx = 5)
        
    def bobbyDick_eldob(self):
        "A cet eldobását vezérlő függvény."
        self.master.engine.eventstack.append(self.nev)
        self.destroy()
        self.master.engine.kincsetHuz()
        self.master.engine.szakasz_0()
        
    def mutiny(self):
        self.bezar = self.lapotEldob
        husegetNovel = ["sirens", "bobbydick", "hawke", "fuil", "lopez", "alvarez", "vandenbergh", "molenaar", "therese", "levasseur", "lizzy", "billy"]
        husegetCsokkent = ["scurvy"]
        matrozokHusege = randrange(1, 7)
        for statusz in self.master.engine.aktivjatekos.statuszlista:
            if statusz in husegetNovel:
                matrozokHusege += 1
            elif statusz in husegetCsokkent:
                matrozokHusege -= 2
        if matrozokHusege < 6:
            if self.master.engine.aktivjatekos.kincs.get() < 6 - matrozokHusege:
                self.master.engine.aktivjatekos.legenyseg.set(0)
                if "landland" in self.master.engine.aktivjatekos.statuszlista:
                    self.master.engine.aktivjatekos.set_statusz("landland", 0)
                self.master.engine.aktivjatekos.set_kincskereses(True)
                self.master.game_board.hajotathelyez(5,2)
                uzenet = self.master.ui_texts["mutiny_succeeded"]
            else:
                self.master.engine.aktivjatekos.set_kincs(self.master.engine.aktivjatekos.kincs.get() - (6 - matrozokHusege))
                self.master.engine.aktivjatekos.set_legenyseg(-1)
                uzenet = self.master.ui_texts["mutiny_suppressed"]
        else:
            self.master.engine.aktivjatekos.set_legenyseg(-1)
            uzenet = self.master.ui_texts["mutiny_suppressed"]
        Label(self, text=uzenet, wraplength=216).pack()
        self.btn_mutiny = Button(self, text=self.master.ui_texts['done'], command=self.lapotEldob)
        self.btn_mutiny.pack(pady=5, side=BOTTOM)
        
    def reefs(self):
        "A zátonyok függvénye."
        self.bezar = self.lapotEldob
        siker = randrange(1,7)
        uzenet = self.master.card_texts[self.nev][1]
        cezura = uzenet.find('|')
        if siker < 4:
            uzenet = uzenet[cezura + 1:]
            self.master.engine.aktivjatekos.set_kimarad(1)
        else:
            uzenet = uzenet[:cezura]
        self.szovegfelirat.config(text = uzenet)
        Button(self, text = self.master.ui_texts['done'], command = self.lapotEldob).pack(pady = 5, side = BOTTOM)
        
    def deserters(self):
        "A dezertőrök függvénye."
        self.bezar = self.lapotEldob
        self.csatlakozikVagyElmegy(False)
        Button(self, text = self.master.ui_texts['done'], command = self.lapotEldob).pack(pady = 5, side = BOTTOM)
        
    def treacherous_mate(self):
        self.bezar = self.eltunik # A lap kikerül a pakliból X-eléskor, csak egyszer húzható ki egy játék folyamán, így sehová nem kell tennünk, csak bezárni.
        self.master.engine.set_hadnagyElokerult() # A játékszintű változót átírjuk.
        Button(self, text = self.master.ui_texts['done'], command = self.eltunik).pack(pady = 5, side = BOTTOM) # Kilépésgomb. Ld. 2 sorral fejjebb.
        
    def kraken(self):
        "A kraken kártyája."
        if 'bobbydick' in self.master.engine.aktivjatekos.statuszlista: # Megvizsgáljuk, hogy játékos kezében van-e a Bobby Dick-kártya.
            self.bezar = self.kraken_bobbydick # Az ablaki X-gomb függvénye
            Button(self, text = (self.master.card_texts['bobbydick'][0] + ' ' + self.master.ui_texts['whalevsoctopus']), command = self.kraken_bobbydick).pack(pady = 5, side = BOTTOM) # Gomb azoknak, akik rendelkeznek a Bobby Dick kártyával.
        else:
            self.bezar = self.noEscape
            self.btn_kraken_dob = Button(self, text = self.master.ui_texts['to_battle'], command = self.kraken_dob)
            self.btn_kraken_dob.pack(pady = 5, side = BOTTOM)
        
    def kraken_bobbydick(self):
        "Csak a kraken-kártya hívhatja, amennyiben a játékos rendelkezik a Bobby Dick kártyával."
        self.master.engine.aktivjatekos.statuszlista.remove('bobbydick')
        self.master.engine.eventstack.append('bobbydick')
        self.lapotEldob()
        
    def kraken_dob(self):
        "A játékos küzdelme a krakennel."
        self.btn_kraken_dob.config(state = DISABLED) # Megakadályozzuk, hogy többször megnyomják a gombot.
        i = 0
        while 1: # Ciklus, amely addig dob, amíg a játékos nem győzi le a krakent.
            dobas = randrange(2,13) # Dobunk.
            if dobas == 8:
                break # Ha 8-at dobott, legyőzte.
            else:
                i += 1 # Egyébként felírjuk, hogy veszített egy matrózt.
        self.btn_kraken_dob.pack_forget() # Eltüntetjük a ciklust indító gombot.
        frame_kraken = Frame(self)
        if i < self.master.engine.aktivjatekos.legenyseg.get(): # Ha nem fogyott el az összes matróz...
            self.master.engine.aktivjatekos.set_legenyseg(-i) # ...akkor levonjuk az elesetteket,
            Label(frame_kraken, text = (self.master.ui_texts['casualties_of_kraken'] % i), wraplength = 216).pack(pady = 5, side = TOP) # és kiírjuk, mennyit vesztett.
        else: # Ha elfogyott az összes matróz...
            self.master.engine.aktivjatekos.set_legenyseg(self.master.engine.aktivjatekos.legenyseg.get() * -1) # ... elvesszük az összeset,
            self.master.game_board.hajotathelyez(5,2) # irány a hajótöröttek szigete,
            if "landland" in self.master.engine.aktivjatekos.statuszlista: # elvesszük a föld, föld bónuszt is, ha volt,
                self.master.engine.aktivjatekos.set_statusz("landland", 0)
            self.master.engine.aktivjatekos.set_kincskereses(True) # és persze leállítjuk a kincskeresést, ha épp aktív volt.
            Label(frame_kraken, text = self.master.ui_texts['defeated_by_kraken'], wraplength = 216).pack(pady = 5, side = TOP) # Kiírjuk, hogy vesztett.
        self.protocol("WM_DELETE_WINDOW", self.lapotEldob) # Most már bezárható a lap, és talonba kerül.
        Button(frame_kraken, text = self.master.ui_texts['done'], command = self.lapotEldob).pack(pady = 5, side = TOP) # Kilépésgomb. A lap a talonba kerül.
        frame_kraken.pack(side = BOTTOM)
        
    def grogLazadas(self):
        "A groglázadás kártyájának megszerzése."
        if 'grog_riot' in self.master.engine.aktivjatekos.statuszlista:
            self.mutiny()
            self.protocol("WM_DELETE_WINDOW", self.grogLazadastEldob)
            self.btn_mutiny.config(command=self.grogLazadastEldob)
        else:
            self.bezar = self.lapotMegtart
            Button(self, text=self.master.ui_texts['done'], command = self.lapotMegtart).pack(pady = 5, side = BOTTOM)
            
    def grogLazadastEldob(self):
        self.master.engine.aktivjatekos.set_statusz("grog_riot", 0)
        self.lapotEldob()
    
    def carousal(self):
        self.bezar = self.lapotEldob
        self.master.engine.aktivjatekos.set_statusz("fold_fold")
        Button(self, text = self.master.ui_texts['done'], command = self.lapotEldob).pack(pady = 5, side = BOTTOM)
        
    def three_headed_monkey(self):
        self.bezar = self.lapotEldob
        Button(self, text = self.master.ui_texts['done'], command = self.lapotEldob).pack(pady = 5, side = BOTTOM)
        
    def castaways(self):
        self.bezar = self.lapotEldob
        self.csatlakozikVagyElmegy()
        Button(self, text = self.master.ui_texts['done'], command = self.lapotEldob).pack(pady = 5, side = BOTTOM)
        
    def ghost_ship(self):
        self.bezar = self.ghost_ship2
        self.csatlakozikVagyElmegy(False)
        Button(self, text = self.master.ui_texts['done'], command = self.ghost_ship2).pack(pady = 5, side = BOTTOM)
        
    def ghost_ship2(self):
        "A kísértethajó nevű kártya eldobásának metódusa."
        self.master.engine.eventstack.append(self.nev)
        self.destroy()
        self.master.engine.kincsetHuz()
        self.master.engine.szakasz_0()
        
    def parts_of_the_sail(self):
        "A sorold fel a vitorla részeit kezdetű kártya metódusa."
        self.bezar = self.lapotEldob
        self.master.engine.dobasMegtortent.set(0)
        Button(self, text = self.master.ui_texts['done'], command = self.lapotEldob).pack(pady = 5, side = BOTTOM)
    
    def csatlakozikVagyElmegy(self, csatlakozik = True):
        "A csatlakozó matrózok függvénye. False esetén a legénység létszáma csökken, és nem nő."
        delta = randrange(1,7) # A létszámváltozás megállapításához dobunk egy kockával.
        delta_str = str(delta)
        if csatlakozik: # Ha csatlakoznak a matrózok, 
            delta_max = self.master.engine.aktivjatekos.legenyseg_max.get() - self.master.engine.aktivjatekos.legenyseg.get() # ...megnézzük, mennyien férnek el még a hajón.
            if delta > delta_max: # Ha többen jönnének,
                delta = delta_max # ...akkor csak annyian jönnek, amennyien elférnek.
        else: # Ha a játékos matrózokat veszít,
            if delta > self.master.engine.aktivjatekos.legenyseg.get(): # Ha több matróz tűnne el, mint amennyi van,
                delta = self.master.engine.aktivjatekos.legenyseg.get() # ...akkor csak annyi fog eltűnni, amennyi van.
                self.master.game_board.hajotathelyez(5,2) # A játékos a hajótöröttek szigetére kerül,
                if "landland" in self.master.engine.aktivjatekos.statuszlista: # ...ha volt föld, föld bónusz,
                    self.master.engine.aktivjatekos.set_statusz("landland", 0) # ...elvesszük,
                self.master.engine.aktivjatekos.set_kincskereses(True) # ...és persze leállítjuk a kincskeresést, ha épp aktív volt.
            delta = - delta # Hogy kivonjuk a matrózokat, deltát negatívvá alakítjuk.
        self.master.engine.aktivjatekos.set_legenyseg(delta) # Lekönyveljük a változást.
        uzenet = self.master.card_texts[self.nev][1]
        cezura = uzenet.find('|')
        uzenet = uzenet[:cezura] + str(delta_str) + uzenet[cezura + 1:]
        self.szovegfelirat.config(text = uzenet) # Feltüntetjük a változást a kártya szövegében.
    
    def slaver(self):
        "A felszabadított rabszolgák nevű kártya metódusa."
        self.bezar = self.lapotEldob
        self.csatlakozikVagyElmegy()        
        Button(self, text = self.master.ui_texts['done'], command=self.lapotEldob).pack(pady = 5, side = BOTTOM)

    def set_sail_to(self, celKikoto):
        self.bezar = self.irany_bezar
        celkocka = self.master.game_board.locations[celKikoto][0] # Kiolvassuk, hol van az adott város.
        debug("Set sail target city is at {}".format(celkocka))
        self.master.game_board.hajotathelyez(celkocka[0], celkocka[1]) # Áttesszük oda a játékost.
        Button(self, text = self.master.ui_texts['done'], command = self.irany_bezar).pack(pady = 5, side = BOTTOM)
        
    def irany_bezar(self):
        self.master.engine.eventstack.append(self.nev)
        self.destroy()
        debug("Arrived at: {}".format(self.master.engine.aktivjatekos.pozicio))
        self.master.engine.teendotar[self.master.game_board.locationsR[self.master.engine.aktivjatekos.pozicio]]()
        self.master.engine.szakasz_0()
