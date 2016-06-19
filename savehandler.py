from tkinter.filedialog import askopenfilename, asksaveasfilename
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, ElementTree, parse, SubElement, tostring


class SaveHandler(object):
    def __init__(self, master):
        self._master = master
        self.extension = '.savx'
        self.type = [('XML mentés', '.savx')]
        
    def load_saved_state(self):
        states = {}
        file_name = askopenfilename(defaultextension=self.extension, filetypes=self.type, initialdir='saved')
        if file_name == '':
            return False
        xml_content = parse(file_name)
        save = xml_content.getroot()
        taverns = {}
        for player in save.findall('player'):
            player_id = player.get('id')
            states[player_id] = self._load_player(player)
        next_player = save.find('currentPlayer').text
        wind_index = int(save.find('windDirection').text)
        lieutenant_found = bool(save.find('firstMateFound').text)
        captain_defeated = bool(save.find('grogLordDefeated').text)
        tavern_tag = save.find('taverns')
        for tavern in tavern_tag.findall('tavern'):
            taverns[tavern.get('port')] = int(tavern.get('sailors'))
        decks = self._load_cards(save)
        return states, next_player, wind_index, taverns, decks, lieutenant_found, captain_defeated

    @staticmethod
    def _load_player(player):
        parameters = ['name', 'color', 'empire', 'ship', 'sailors', 'money', 'lastRoll', 'turnsToMiss',
                      'treasureHuntFinished']
        state = []
        for parameter in parameters:
            state.append(player.find(parameter).text)
        coordinates = (int(player.find('coordinates').get('x')), int(player.find('coordinates').get('y')))
        state.insert(5, coordinates)
        modifiers = player.find('status').text
        if modifiers is None:
            state.insert(7, [])
        else:
            modifiers = [str(x) for x in modifiers.split(',')]
            state.insert(7, modifiers)
        for i in [4, 6, 8, 9]:
            state[i] = int(state[i])
        if state[10] == 'True':
            state[10] = True
        else:
            state[10] = False
        looted_ships = {}
        looted_ships_tag = player.find('shipsLooted')
        for looted_ship in looted_ships_tag.findall('score'):
            looted_ships[looted_ship.get('empire')] = int(looted_ship.get('ships'))
        state.append(looted_ships)
        return state

    @staticmethod
    def _load_cards(save):
        cards = save.find('cards')
        event_deck = cards.find('eventDeck').text
        event_stack = cards.find('eventStack').text
        treasure_deck = cards.find('treasureDeck').text
        treasure_stack = cards.find('treasureStack').text
        decks = [event_deck, event_stack, treasure_deck, treasure_stack]
        for deck in decks:
            if deck:
                decks[decks.index(deck)] = deck.replace(' ', '').split(',')
            else:
                decks[decks.index(deck)] = []
        return decks

    def set_adatok_fileba(self, jatekosAdatok = {}, kovetkezoJatekos = '', szelindex = 6, varosadatok = {}, kartyak = [], grogbaroLegyozve = False, hadnagyElokerult = False):
        "Kimenti az aktuális adatokat egy fájlba."
        helyzetek = jatekosAdatok
        kovetkezoJatekos = kovetkezoJatekos
        szelindex = szelindex
        varosadatok = varosadatok
        empire = [self._master.empires.keys()]
        eventdeck, eventstack, kincspakli, treasurestack = kartyak
        grogbaroLegyozve = grogbaroLegyozve
        hadnagyElokerult = hadnagyElokerult
        # A paklik stringgé alakítása
        paklik = [eventdeck, eventstack, kincspakli, treasurestack]
        for pakli in paklik:
            a = ''
            for i in pakli:
                a = a + ', ' + i
            paklik[paklik.index(pakli)] = a[2:]
        # Elkészítjük az XML-struktúra gyökerét
        allomany = asksaveasfilename(defaultextension=self.extension, filetypes=self.type, initialdir='saved')
        if allomany == '':
            return False
        save = Element('save')
        file = ElementTree(save)
        # Tényleges mentés
        jatekosok = sorted(list(helyzetek.keys()))
        parameterek = ['name', 'color', 'empire', 'ship', 'sailors', 'money', 'status', 'lastRoll', 'turnsToMiss', 'treasureHuntFinished']
        for jatekos in jatekosok:
            player = SubElement(save, 'player')
            player.set('id', jatekos)
            # Kivesszük a paraméterlistából a speciális paramétereket.
            statusz = helyzetek[jatekos][7]
            statusz = str(statusz).strip("[]'") # A statuszt vissza is tesszük.
            helyzetek[jatekos][7] = statusz
            kiraboltHajok = helyzetek[jatekos].pop(10)
            koordinatak = helyzetek[jatekos].pop(5)
            for i in range(len(parameterek)):
                tag = SubElement(player, parameterek[i])
                tag.text = str(helyzetek[jatekos][i])
            # Mentjük a kirabolt hajók mennyiségét.
            kiraboltHajokTag = SubElement(player, 'shipsLooted')
            for kiraboltHajo in kiraboltHajok:
                pontok = SubElement(kiraboltHajokTag, 'score')
                pontok.set('empire', kiraboltHajo[0])
                pontok.set('ships', str(kiraboltHajo[1]))
            # Lementjük a koordinátákat is.
            coords = SubElement(player, 'coordinates')
            coords.set('x', str(koordinatak[0]))
            coords.set('y', str(koordinatak[1]))
        kovetkezo = SubElement(save, 'currentPlayer')
        kovetkezo.text = kovetkezoJatekos
        szel = SubElement(save, 'windDirection')
        szel.text = str(szelindex)
        hadnagy = SubElement(save, 'firstMateFound')
        hadnagy.text = str(hadnagyElokerult)
        grogbaro = SubElement(save, 'grogLordDefeated')
        grogbaro.text = str(grogbaroLegyozve)
        fogadok = SubElement(save, 'taverns')
        for aktualisFogado in list(varosadatok.keys()):
            fogado = SubElement(fogadok, 'tavern')
            fogado.set('port', aktualisFogado)
            fogado.set('sailors', str(varosadatok[aktualisFogado]))
        # Kártyák mentése
        kartyak = SubElement(save, 'cards')
        cardsEp = SubElement(kartyak, 'eventDeck')
        cardsEp.text = paklik[0]
        cardsEt = SubElement(kartyak, 'eventStack')
        cardsEt.text = paklik[1]
        cardsKp = SubElement(kartyak, 'treasureDeck')
        cardsKp.text = paklik[2]
        cardsKt = SubElement(kartyak, 'treasureStack')
        cardsKt.text = paklik[3]
        rough_xml = tostring(save, encoding='utf-8', method='xml')
        minidom_xml = parseString(rough_xml)
        pretty_xml = minidom_xml.toprettyxml('    ')
        with open(allomany, 'w') as xml_file:
            xml_file.write(pretty_xml)
        return True
