from logging import debug
from random import randrange
from tkinter import BooleanVar, Frame
from tkinter.messagebox import showinfo, askyesno
from assets import Empires
from card import Card
from csata import Utkozet
from port import Varos
from settings import ApplicationSettings as s


class Vezerlo(Frame):
    """Gondoskodik a játék folyamatáról."""
    def __init__(self, master=None, fogadoszotar=None):
        Frame.__init__(self, master)
        if fogadoszotar is None:
            fogadoszotar = {}
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
        self.teendotar = dict([('battle_french', lambda: self.csata("b0")),
                               ('battle_british', lambda: self.csata("b3")),
                               ('battle_dutch', lambda: self.csata("b1")),
                               ('battle_spanish', lambda: self.csata("b2")),
                               ('Port Royal', lambda: self.varos('Port Royal')),
                               ('Curacao', lambda: self.varos('Curacao')),
                               ('Tortuga', lambda: self.varos('Tortuga')),
                               ('Havanna', lambda: self.varos('Havanna')),
                               ('Martinique', lambda: self.varos('Martinique')),
                               ('windplus90', lambda: self.boss.game_board.change_wind_direction(90)),
                               ('windminus90', lambda: self.boss.game_board.change_wind_direction(-90)),
                               ('windplus45', lambda: self.boss.game_board.change_wind_direction(45)),
                               ('windminus45', lambda: self.boss.game_board.change_wind_direction(-45)),
                               ('bermuda', self.bermuda),
                               ('landland', self.landland),
                               ('storm', self.vihar),
                               ('driftwood', self.driftwood),
                               ('calm', self.calm),
                               ('taino', self.taino),
                               ('treasureisland', self.treasureisland),
                               ('stream', self.stream),
                               ("castaways", self.szamuzottekKozvetlen)
                               ])
        # A paklik előkészítése
        self.eventszotar = {}
        self.eventdeck = []
        self.eventstack = []
        self.kincsszotar = {}
        self.treasurestack = []
        eventtar, kincstar, penztar, fuggvenytar = self.boss.data_reader.load_cards_data()
        for lap in eventtar.keys():
            self.boss.game_board._render_card_image(eventtar[lap])  # betöltjük a képet
            self.eventszotar[lap] = Card(self, self.boss, lap, eventtar[lap], 'event', fuggvenytar[lap])
            self.eventdeck.append(lap)
        debug("Event cards in deck: {}/52".format(len(self.eventdeck)))
        self.csataszotar = self.boss.data_reader.load_battle_data()
        for csata in self.csataszotar.keys():
            if csata[0] != 'b':
                self.eventdeck.append(csata)
        for penz in penztar.keys():
            iPenz = 0
            for i in range(penztar[penz]):
                self.kincsszotar['treasure'+penz+'_'+str(iPenz)] = Card(self, self.boss, 'treasure',
                                                                        kincstar["treasure"], 'treasure',
                                                                        fuggvenytar["treasure"], int(penz))
                iPenz += 1
        for lap in kincstar.keys():
            self.boss.game_board._render_card_image(kincstar[lap])  # betöltjük a képet
            if lap != 'treasure':
                self.kincsszotar[lap] = Card(self, self.boss, lap, kincstar[lap], 'treasure', fuggvenytar[lap])
        self.kincspakli = list(self.kincsszotar.keys())
        # Hajók elkészítése
        self.hajotipustar = self.boss.data_reader.get_ship_types()
        for jatekos in self.boss.player_order:
            p = self.boss.players[jatekos]
            p.crew_limit.set(self.hajotipustar[p.ship].crew_limit)
        self.vehetoHajok = []
        hajoarak = []
        for hajo in self.hajotipustar.keys():
            if self.hajotipustar[hajo].price > 0:
                hajoarak.append(self.hajotipustar[hajo].price)
                hajoarak = sorted(hajoarak)
                arPozicio = hajoarak.index(self.hajotipustar[hajo].price)
                self.vehetoHajok.insert(arPozicio, hajo)
        debug('Ships to purchase:' + str(self.vehetoHajok))
        # Városablakok előkészítése
        self.varostar = {}
        if fogadoszotar == {}:
            for empire in Empires:
                self.varostar[empire.value.capital] = Varos(self, self.boss, empire.value)
        else:
            for empire in Empires:
                self.varostar[empire.value.capital] = Varos(self, self.boss, empire.value,
                                                            fogadoszotar[empire.value.capital])

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
        if self.kincsKiasva:
            debug('Vége a játéknak. A győztes:', self.aktivjatekos)
        if self.dobasMegtortent.get():
            # A legutóbb lépett játékost leghátra dobja, ha már lépett az aktív játékos
            self.boss.player_order.append(self.boss.player_order.pop(0))
        self.aktivjatekos = self.boss.players[self.boss.player_order[0]]
        debug("\n{0}\nIt's {1}'s turn.\n{0}\n".format('-' * 20, self.aktivjatekos.name))
        self.master.status_bar.log(s.language.new_turn % self.aktivjatekos.name)
        self.dobasMegtortent.set(False)
        self.boss.menu.reset_game_tab()
        if "scurvy" in self.aktivjatekos.states:
            self.aktivjatekos.update_crew(-1)
        self.boss.is_turn_in_progress.set(0)
        if not self.aktivjatekos.treasure_hunting_done:
            if askyesno(s.language.dig_for_treasure_label, s.language.dig_for_treasure_question):
                self.dig_on_treasureisland()
            else:
                self.aktivjatekos.treasure_hunting_done = True
        # debug("**MetódusID = " + str(id)+ " - szakasz_0 lezárva")
        self.unfinishedMethodes.remove(id)

    def szakasz_mezoevent(self):
        "A mező indukálta feladat elvégzése."
        id = self.methodeNo_get()
        # debug("**MetódusID = " + str(id) + " - szakasz_mezoevent")
        self.boss.status_bar.log('')
        if self.boss.exit_in_progress:
            return
        port_list = [empire.value.capital for empire in Empires]
        if 'grog_riot' in self.aktivjatekos.states:
            if self.boss.game_board.locationsR[self.aktivjatekos.coordinates] in port_list:
                self.aktivjatekos.remove_state("grog_riot")
                self.eventstack.append("grog_riot")
            else:
                self.eventszotar["grog_riot"].megjelenik()
        self.hivas = self.teendotar[self.boss.game_board.locationsR[self.aktivjatekos.coordinates]]()
        if self.hivas is False:
            self.szakasz_0()
        elif self.hivas is None:
            self.szakasz_kartyaevent()
        # debug("**MetódusID = " + str(id) + " - szakasz_mezoevent lezárva")
        self.unfinishedMethodes.remove(id)

    def szakasz_kartyaevent(self):
        "Egy kártya húzása, és az általa hordozott feladat elvégzése."
        id = self.methodeNo_get()
        # debug("**MetódusID = " + str(id) + " - szakasz_kartyaevent")
        if not self.eventdeck:
            for elem in self.eventstack:
                self.eventdeck.append(elem)
            self.eventstack = []
        kovetkezoLap = randrange(len(self.eventdeck))
        huz = self.eventdeck.pop(kovetkezoLap)
        if len(huz) < 4:  # 3
            # debug('A kihúzott lap:',huz,';',self.csataszotar[huz])
            self.eventstack.append(huz)  # eldobjuk a kártyát
            self.harc = Utkozet(self, self.boss, self.csataszotar[huz])  # lejátsszuk a csatát
        else:
            self.eventszotar[huz].megjelenik()
        # debug("**MetódusID = " + str(id) + " - szakasz_kartyaevent lezárva")
        self.unfinishedMethodes.remove(id)

    def kimaradas(self):
        "Vezérli a kimaradást."
        self.aktivjatekos.update_turns_to_miss()
        self.dobasMegtortent.set(True)
        self.szakasz_0()

    def set_paklik(self, pakli):
        "Visszatölti a mentésből származó paklieloszlásokat."
        ep, et, kp, kt = pakli
        self.eventdeck = ep
        self.eventstack = et
        self.kincspakli = kp
        self.treasurestack = kt
        debug("Loaded decks:")
        debug("Event deck: {}".format(self.eventdeck))
        debug("Event stack: {}".format(self.eventstack))
        debug("Treasure deck: {}".format(self.kincspakli))
        debug("Treasure stack: {}".format(self.treasurestack))

    def set_dobasMegtortent(self):
        "Híváskor érvényteleníti a kockát."
        self.dobasMegtortent.set(True)
        if self.unfinishedMethodes:
            debug("HIBA - Beragadt metódus:", self.unfinishedMethodes)

    def mozgas(self, roll, add_wind_modifier=True):
        target_tiles = self.boss.game_board.calculate_target_tiles(self.aktivjatekos.coordinates, roll, add_wind_modifier)
        self.boss.game_board.mark_target_tiles(target_tiles)

    def kincsetHuz(self):
        if not self.kincspakli:
            debug("Kincspakli keverése.")
            for elem in self.treasurestack:
                self.kincspakli.append(elem)
            self.treasurestack = []
        kovetkezoLap = randrange(len(self.kincspakli))
        huz = self.kincspakli.pop(kovetkezoLap)
        self.kincsszotar[huz].megjelenik()

    def varos(self, varosneve):
        "A várost működtető függvény."
        if "scurvy" in self.aktivjatekos.states:
            self.aktivjatekos.remove_state("scurvy")
        self.varostar[varosneve].aktival()
        return False

    def bermuda(self):
        "A Bermuda mező roppant izgalmas függvénye."
        showinfo(s.language.info, s.language.bermuda)

    def csata(self, csataId):
        "A csatát inicializáló függvény."
        Utkozet(self, self.boss, self.csataszotar[csataId])
        return True

    def landland(self):
        "A játékos újra dobhat a következő körben, ha az eredeti dobás kedvezőtlen."
        showinfo(s.language.info, s.language.land)
        self.aktivjatekos.add_state("fold_fold")
        if "scurvy" in self.aktivjatekos.states:
            self.aktivjatekos.remove_state("scurvy")
        return

    def vihar(self):
        "A vihar mező függvénye."
        viharEreje = self.boss.menu.game_tab.die.roll()  # Dobunk, ez adja meg a vihar erejét.
        self.aktivjatekos.last_roll = viharEreje  # Mentjük a kocka állapotát.
        # Ha a játékos hajóján ott utazik Jacques Levasseur, több esélye van sikeresen navigálni.
        if "levasseur" in self.aktivjatekos.states:
            maxSiker = 4
        else:
            maxSiker = 3
        if viharEreje > maxSiker:
            if "spare_sail" in self.aktivjatekos.states:  # Ha a játékosnak van pótvitorlája, megússza, hogy kimaradjon.
                self.aktivjatekos.remove_state("spare_sail")  # Eldobja a vitorlát.
                self.treasurestack.append("spare_sail")  # A vitorlakártya a talonba kerül.
                uzenet = s.language.storm_sail_damage
                return
            else:
                self.aktivjatekos.update_turns_to_miss(1)  # Beállítjuk, hogy turns_to_miss egy körből.
                uzenet = s.language.storm_miss_turn
            showinfo(s.language.info, uzenet)  # Kiírjuk, a történteket.
            return
        else:
            self.boss.status_bar.log(s.language.storm_success)
            self.mozgas(viharEreje)
            self.szakasz_mezoevent()
            return True

    def driftwood(self):
        "Vajon sikerül kincsre bukkanni?"
        dobas = self.boss.menu.game_tab.die.roll()  # Szerencsét próbálunk.
        self.aktivjatekos.last_roll = dobas  # Mentjük a kocka állapotát.
        if dobas == 6:
            self.aktivjatekos.update_gold(1)
            self.boss.status_bar.log(s.language.driftwood_success)
        else:
            self.boss.status_bar.log(s.language.driftwood)
        return

    def calm(self):
        "Egy körből turns_to_miss a játékos."
        self.aktivjatekos.update_turns_to_miss(1)  # Beállítjuk, hogy turns_to_miss egy körből.
        showinfo(s.language.info, s.language.calm)
        return

    def taino(self):
        "Bennszülöttek csatlakoznak a legénységhez."
        maxFelvehetoBennszulott = self.aktivjatekos.crew_limit.get() - self.aktivjatekos.crew.get()
        if maxFelvehetoBennszulott:
            dobas = self.boss.menu.game_tab.die.roll()  # Szerencsét próbálunk.
            self.aktivjatekos.last_roll = dobas  # Mentjük a kocka állapotát.
            if dobas >= maxFelvehetoBennszulott:
                self.aktivjatekos.update_crew(maxFelvehetoBennszulott)
                felveve = maxFelvehetoBennszulott
            else:
                self.aktivjatekos.update_crew(dobas)
                felveve = dobas
            if felveve < 2:
                self.boss.status_bar.log(s.language.taino_one)
            else:
                self.boss.status_bar.log(s.language.taino_some % felveve)
        else:
            self.boss.status_bar.log(s.language.taino_none)
        return

    def treasureisland(self):
        "Egy mező, ahol kincset lehet ásni."
        self.aktivjatekos.treasure_hunting_done = False
        self.boss.status_bar.log(s.language.dig_for_treasure)

    def dig_on_treasureisland(self):
        "A teendők, ha már kincses szigeten áll az ember."
        self.boss.is_turn_in_progress.set(1)
        self.dobasMegtortent.set(True)
        dobas = self.boss.menu.game_tab.die.roll()  # Szerencsét próbálunk.
        self.aktivjatekos.last_roll = dobas  # Mentjük a kocka állapotát.
        if dobas == 6:
            self.aktivjatekos.treasure_hunting_done = True
            self.kincsetHuz()
        else:
            showinfo(s.language.dig_for_treasure_label, s.language.dig_for_treasure_nothing)
        self.szakasz_0()

    def stream(self):
        "Az áramlat függvénye"
        dobas = self.boss.menu.game_tab.die.roll()
        self.aktivjatekos.last_roll = dobas
        self.mozgas(dobas, 0)
        return True

    def szamuzottek(self, esent=None):
        "Ez történik, ha valaki legénység nélkül van a száműzöttek szigetén."
        self.boss.is_turn_in_progress.set(1)
        self.dobasMegtortent.set(True)
        dobas = self.boss.menu.game_tab.die.roll()  # Szerencsét próbálunk.
        self.aktivjatekos.last_roll = dobas  # Mentjük a kocka állapotát.
        celokSzotar = dict([(1, "Martinique"),
                            (2, "Curacao"),
                            (3, "Havanna"),
                            (4, "Tortuga"),
                            (5, "Port Royal")])
        if dobas == 6:
            uzenet = s.language.castaway_no_hope
        else:
            varos = celokSzotar[dobas]
            uzenet = s.language.castaway_success % varos
            x, y = self.boss.game_board.locations[celokSzotar[dobas]][0]
            self.boss.game_board.relocate_ship(x, y)
            if self.aktivjatekos.gold.get() < 10:
                self.aktivjatekos.gold.set(0)
            else:
                self.aktivjatekos.gold.set(self.aktivjatekos.gold.get() - 10)
            self.aktivjatekos.update_crew(10)
        showinfo(s.language.info, uzenet)
        self.master.engine.szakasz_0()
        return False

    def szamuzottekKozvetlen(self):
        "Teendő belelépés esetén."

    def leviathan_kijatszasa(self):
        "A leviatán megmenti a játékost a kimaradástól."
        self.aktivjatekos.remove_state("leviathan")
        self.eventstack.append("leviathan")
        self.aktivjatekos.update_turns_to_miss()
        self.szakasz_0()
