# -*- coding: utf-8 -*-
from models import ShipType
from tkinter.messagebox import showerror
from xml.etree.ElementTree import parse

__author__ = 'Bárdos Dávid'


class DataReader(object):
    def __init__(self, master):
        self.master = master
        self.missing_files = []
        self.path_dictionary = self._load_path_dictionary('db/paths.xml')
        self.term_dictionary = dict(
            [('spanish', 'spanyol'), ('french', 'francia'), ('dutch', 'holland'), ('british', 'angol'),
             ('pirate', 'kaloz'),
             ('galleon', 'galleon'), ('schooner', 'szkuner'), ('brigantine', 'brigantin'), ('frigate', 'fregatt')])
        self.errors = self._load_errors()
        if self.missing_files:
            showerror('Error', (self.errors['configLocationMissingError'] % ', '.join(self.missing_files)))

    def _load_path_dictionary(self, path_file):
        path_xml_root = parse(path_file).getroot()
        path_dictionary = {}
        config_list = [item.tag for item in path_xml_root.find('xml')]
        for config in config_list:
            try:
                path_dictionary[config] = path_xml_root.find('xml').find(config).text
            except AttributeError:
                self.missing_files.append(config)
        return path_dictionary

    def _load_errors(self):
        error_xml_root = parse(self.path_dictionary['errors']).getroot()
        errors = {}
        for error in error_xml_root.findall('exception'):
            errors[error.get('id')] = error.text.replace('\\n', '\n')
        return errors

    def load_settings(self):
        config_root = parse(self.path_dictionary['config']).getroot()
        language = config_root.find('language').text
        resolution_code_text = config_root.find('resolution').text
        resolution_code = config_root.find(("./resolutionlist/res[@type='" + resolution_code_text + "']"))
        width = int(resolution_code.get('x'))
        height = int(resolution_code.get('y'))
        if int(config_root.find('fullscreen').text):
            full_screen = True
        else:
            full_screen = False
        screen_type = resolution_code.get('type')
        resolution_elements = config_root.find('resolutionlist').findall('res')
        resolution_tuple = ()
        for res in resolution_elements:
            resolution_tuple += (int(res.get('x')), int(res.get('y')), res.get('type')),
        return language, width, height, full_screen, screen_type, resolution_tuple

    def save_settings(self, new_resolution=None, new_full_screen=None, new_language=None):
        config_xml = parse(self.path_dictionary['config'])
        config = config_xml.getroot()
        if new_resolution and new_full_screen:
            config.find('resolution').text = new_resolution
            config.find('fullscreen').text = new_full_screen
        if new_language:
            config.find('language').text = new_language
        config_xml.write(self.path_dictionary['config'], xml_declaration=True, encoding='utf-8', method='xml')
        self._reformat_saved_xml()

    def _reformat_saved_xml(self):
        with open(self.path_dictionary['config'], 'r') as file_handler:
            text = file_handler.read()
        while '\n\n' in text or '\n ' in text:
            text = text.replace('\n\n', '\n')
            text = text.replace('\n ', '\n')
        with open(self.path_dictionary['config'], 'w') as file_handler:
            file_handler.write(text)

    def load_battle_data(self):
        battle_xml = parse(self.path_dictionary['battles']).getroot()
        battles = battle_xml.findall('encounter')
        battle_dictionary = {}
        for battle in battles:
            battle_id = battle.get('id')
            flag = self.term_dictionary[battle.find('flag').text]
            ship_type = self.term_dictionary[battle.find('shipType').text]
            ship_name = battle.find('shipName').text
            teams = self._load_teams(battle)
            loot = self._load_loot(battle)
            is_treasure_on_board = self._load_treasure(battle)
            battle_dictionary[battle_id] = (flag, ship_type, ship_name, teams, loot, is_treasure_on_board)
        return battle_dictionary

    def _load_teams(self, battle):
        teams = ()
        for i in range(1, 7):
            team = self._get_team_members(battle, i)
            teams += team,
        return teams

    def _get_team_members(self, battle, i):
        team = battle.find('parts').find('p' + str(i)).text
        if team not in ['powderStore', 'underWaterHit']:
            team = self._check_team_members(battle, team)
        return team

    def _check_team_members(self, battle, team):
        try:
            team = int(team)
        except ValueError:
            battle_id = battle.get('id')
            ship_name = battle.find('shipName').text
            showerror('Error', (self.errors['teamValueError'] % (ship_name, battle_id,
                                                                 self.path_dictionary['battles'])))
        else:
            team = min(team, 6)
        return team

    def _load_loot(self, battle):
        loot = battle.find('loot').text
        try:
            loot = int(loot)
        except ValueError:
            battle_id = battle.get('id')
            ship_name = battle.find('shipName').text
            showerror('Error', (self.errors['lootValueError'] % (ship_name, battle_id,
                                                                 self.path_dictionary['battles'])))
        return loot

    @staticmethod
    def _load_treasure(battle):
        is_treasure_on_board = battle.find('shipName').text
        if is_treasure_on_board == '0':
            is_treasure_on_board = False
        else:
            is_treasure_on_board = True
        return is_treasure_on_board

    def load_cards_data(self):
        all_cards, error_message, events, loot = self._load_common_card_data()
        event_dictionary = {}
        treasure_card_dictionary = {}
        money_dictionary = {}
        method_dictionary = {}
        for deck, xml_branch in ((event_dictionary, events), (treasure_card_dictionary, loot)):
            for card in xml_branch.findall('card'):
                try:
                    image_path = card.find('img').text
                except AttributeError:
                    image_path = self.errors['cardImgMissingAttributeError']
                deck[card.get('id')] = image_path
                try:
                    method = card.find("method").text
                except AttributeError:
                    method = "self.dummy"
                method_dictionary[card.get('id')] = method
                gold = all_cards.find('gold')
                for amount in gold.findall('sum'):
                    money_dictionary[amount.find('value').text] = int(amount.find('quantity').text)
        return event_dictionary, treasure_card_dictionary, money_dictionary, method_dictionary

    def load_cards_text(self):
        all_cards, error_message, events, loot = self._load_common_card_data()
        card_dictionary = {}
        for event_card in events.findall('card') + loot.findall('card'):
            try:
                title = event_card.find('title').find(self.master.nyelv).text
            except AttributeError:
                title = error_message
            else:
                if title is None:
                    title = ''
                else:
                    title = title.replace('\\n', '\n')
            try:
                text = event_card.find('text').find(self.master.nyelv).text
            except AttributeError:
                text = error_message
            else:
                if text is None:
                    text = ''
                else:
                    text = text.replace('\\n', '\n')
            card_dictionary[event_card.get('id')] = (title, text)
        return card_dictionary

    def _load_common_card_data(self):
        try:
            error_message = self.master.szotar['stringhiany']
        except AttributeError:
            error_message = self.errors['stringAttributeError']
        all_cards = parse(self.path_dictionary['cards']).getroot()
        events = all_cards.find('events')
        loot = all_cards.find('loot')
        return all_cards, error_message, events, loot

    def load_dictionary(self, language=None, entry_type=None, is_reverse_required=None):
        interface = parse(self.path_dictionary['interface']).getroot()
        if language:
            term_dictionary = []
            for item in interface:
                if item.get('type') == entry_type:
                    term_dictionary.append(item.tag)
            result = {original: interface.find(original).find(language).text for original in term_dictionary}
            return result
        elif is_reverse_required:
            language_list = {}
            language_list_reversed = {}
            for item in interface.find('nyelvek'):
                language_list[item.text] = item.tag
                language_list_reversed[item.tag] = item.text
            return language_list, language_list_reversed

    def get_ship_types(self):
        ship_types_root = parse(self.path_dictionary['shiptypes']).getroot()
        result = {}
        for ship in ship_types_root.findall('ship'):
            price = int(ship.get('cost'))
            max_crew = int(ship.get('maxCrew'))
            ship_type = ship.get('type')
            result[ship_type] = (ShipType(ship_type, price, max_crew))
        return result