from models import GameState
from tkinter.filedialog import askopenfilename, asksaveasfilename
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, parse, SubElement, tostring


class SaveHandler(object):
    def __init__(self, master):
        self._master = master
        self.extension = '.savx'
        self.type = [('XML save', '.savx')]
        
    def load_saved_state(self):
        current_state = GameState()
        file_name = askopenfilename(defaultextension=self.extension, filetypes=self.type, initialdir='saved')
        if file_name == '':
            return None
        xml_content = parse(file_name)
        save = xml_content.getroot()
        for player in save.findall('player'):
            player_id = player.get('id')
            current_state.player_data[player_id] = self._load_player(player)
        current_state.next_player = save.find('currentPlayer').text
        current_state.wind_index = int(save.find('windDirection').text)
        current_state.is_lieutenant_found = True if save.find('firstMateFound').text == 'True' else False
        current_state.is_grog_lord_defeated = True if save.find('firstMateFound').text == 'True' else False
        tavern_tag = save.find('taverns')
        for tavern in tavern_tag.findall('tavern'):
            current_state.taverns[tavern.get('port')] = int(tavern.get('sailors'))
        current_state.card_decks = self._load_cards(save)
        return current_state

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

    def set_adatok_fileba(self, game_state):
        assert isinstance(game_state, GameState)
        file_name = asksaveasfilename(defaultextension=self.extension, filetypes=self.type, initialdir='saved')
        if not file_name:
            return
        save_root = Element('save')
        serialized_decks = []
        for deck in game_state.card_decks:
            serialized_decks.append(", ".join(deck))
        parameters = ['name', 'color', 'empire', 'ship', 'sailors', 'money', 'status', 'lastRoll', 'turnsToMiss',
                      'treasureHuntFinished']
        for player in sorted(game_state.player_data):
            player_tag = SubElement(save_root, 'player')
            player_tag.set('id', player)
            game_state.player_data[player][7] = ", ".join(game_state.player_data[player][7])
            looted_ships = game_state.player_data[player].pop(10)
            coordinates = game_state.player_data[player].pop(5)
            for index, parameter in enumerate(parameters):  # TODO let's structure player state!
                tag = SubElement(player_tag, parameter)
                tag.text = str(game_state.player_data[player][index])
            looted_ships_tag = SubElement(player_tag, 'shipsLooted')
            for looted_ship in looted_ships:
                scores_tag = SubElement(looted_ships_tag, 'score')
                scores_tag.set('empire', looted_ship[0])
                scores_tag.set('ships', str(looted_ship[1]))
            coordinates_tag = SubElement(player_tag, 'coordinates')
            coordinates_tag.set('x', str(coordinates[0]))
            coordinates_tag.set('y', str(coordinates[1]))
        current_player_tag = SubElement(save_root, 'currentPlayer')
        current_player_tag.text = game_state.next_player
        wind_direction_tag = SubElement(save_root, 'windDirection')
        wind_direction_tag.text = str(game_state.wind_index)
        lieutenant_tag = SubElement(save_root, 'firstMateFound')
        lieutenant_tag.text = str(game_state.is_lieutenant_found)
        grog_lord_defeated_tag = SubElement(save_root, 'grogLordDefeated')
        grog_lord_defeated_tag.text = str(game_state.is_grog_lord_defeated)
        taverns_tag = SubElement(save_root, 'taverns')
        for tavern_name, men_count in sorted(game_state.taverns.items()):
            fogado = SubElement(taverns_tag, 'tavern')
            fogado.set('port', tavern_name)
            fogado.set('sailors', str(men_count))
        card_tag = SubElement(save_root, 'cards')
        event_deck_tag = SubElement(card_tag, 'eventDeck')
        event_deck_tag.text = serialized_decks[0]
        event_stack_tag = SubElement(card_tag, 'eventStack')
        event_stack_tag.text = serialized_decks[1]
        treasure_deck_tag = SubElement(card_tag, 'treasureDeck')
        treasure_deck_tag.text = serialized_decks[2]
        treasure_stack_tag = SubElement(card_tag, 'treasureStack')
        treasure_stack_tag.text = serialized_decks[3]
        rough_xml = tostring(save_root, encoding='utf-8', method='xml')
        minidom_xml = parseString(rough_xml)
        pretty_xml = minidom_xml.toprettyxml('    ', encoding='utf-8')
        with open(file_name, 'wb') as xml_file:
            xml_file.write(pretty_xml)
        return True
