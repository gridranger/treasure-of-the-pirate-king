from models import GameState, PlayerState
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
        name = player.find("name").text
        color = player.find("color").text
        empire = player.find("empire").text
        player_state = PlayerState(name, color, empire)
        player_state.ship = player.find("ship").text
        player_state.crew = int(player.find("sailors").text)
        player_state.gold = int(player.find("money").text)
        player_state.last_roll = int(player.find("lastRoll").text)
        player_state.turns_to_miss = int(player.find("turnsToMiss").text)
        player_state.treasure_hunting_done = True if player.find("treasureHuntFinished").text == "True" else False
        player_state.coordinates = (int(player.find('coordinates').get('x')), int(player.find('coordinates').get('y')))
        bulk_states = player.find('status').text
        player_state.states = [] if bulk_states is None else [str(x) for x in bulk_states.split(',')]
        looted_ships_tag = player.find('shipsLooted')
        for looted_ship in looted_ships_tag.findall('score'):
            player_state.looted_ships[looted_ship.get('empire')] = int(looted_ship.get('ships'))
        return player_state

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

    def write_save(self, game_state):
        assert isinstance(game_state, GameState)
        file_name = asksaveasfilename(defaultextension=self.extension, filetypes=self.type, initialdir='saved')
        if not file_name:
            return
        save_root = Element('save')
        serialized_decks = []
        for deck in game_state.card_decks:
            serialized_decks.append(", ".join(deck))
        for player_id, player in sorted(game_state.player_data.items()):
            player_tag = SubElement(save_root, 'player')
            player_tag.set('id', player_id)
            self._save_player(player, player_tag)
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
            tavern_tag = SubElement(taverns_tag, 'tavern')
            tavern_tag.set('port', tavern_name)
            tavern_tag.set('sailors', str(men_count))
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

    @staticmethod
    def _save_player(player, player_tag):
        name = SubElement(player_tag, 'name')
        name.text = player.name
        color = SubElement(player_tag, 'color')
        color.text = player.color
        empire = SubElement(player_tag, 'empire')
        empire.text = player.empire
        ship = SubElement(player_tag, 'ship')
        ship.text = player.ship
        sailors = SubElement(player_tag, 'sailors')
        sailors.text = str(player.crew)
        money = SubElement(player_tag, 'money')
        money.text = str(player.gold)
        status = SubElement(player_tag, 'status')
        status.text = ', '.join(player.states)
        last_roll = SubElement(player_tag, 'lastRoll')
        last_roll.text = str(player.last_roll)
        turns_to_miss = SubElement(player_tag, 'turnsToMiss')
        turns_to_miss.text = str(player.turns_to_miss)
        treasure_hunt_finished = SubElement(player_tag, 'treasureHuntFinished')
        treasure_hunt_finished.text = str(player.treasure_hunting_done)
        ships_looted = SubElement(player_tag, 'shipsLooted')
        for empire, value in sorted(player.looted_ships.items()):
            empire_tag = SubElement(ships_looted, "score")
            empire_tag.set("empire", empire)
            empire_tag.set("ships", str(value))
        coordinates = SubElement(player_tag, "coordinates")
        coordinates.set("x", str(player.coordinates[0]))
        coordinates.set("y", str(player.coordinates[1]))
