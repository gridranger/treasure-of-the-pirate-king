class Localization:
    _all_terms = ["this_language", "British", "price", "gold", "balance_teams", "settings", "bermuda",
                  "brigantine", "aiming", "whalevsoctopus", "title", "battle", "leave_battle",
                  "leave_battle_text", "battle_sink", "battle_lose", "event_card", "extra", "resolution",
                  "land", "land_log", "tavern", "French", "frigate", "main_main", "galleon", "shipwright",
                  "ship_spotted", "ship_spotted_fire", "ship_spotted_alvarez", "ship_spotted_battle_starts",
                  "ship_spotted_let_them_flee", "ship_spotted_battle", "ship_spotted_reward",
                  "ship_spotted_reward2", "ship_spotted_pirate", "ship_spotted_powder_storage",
                  "ship_spotted_boarding", "ship_spotted_fleeing", "ship_spotted_fleeing_unsuccesful",
                  "ship_spotted_parrot", "ship_spotted_enemy_casualties", "ship_spotted_player_casualties",
                  "ship_spotted_enemy_sinking", "ship_name_player", "ship_name_pirate0",
                  "ship_name_pirate1", "ship_name_pirate2", "ship_name_pirate3", "to_battle", "Dutch",
                  "info", "game", "loading_game", "loading_done", "discard_game", "discard_game_b",
                  "start_game", "start_game_done", "turn_order", "Pirate", "card_discard", "card_keep",
                  "cards", "done", "port", "miss_turn", "miss_turn_last_time", "treasure", "treasure_card",
                  "dig_for_treasure", "dig_for_treasure_label", "dig_for_treasure_question",
                  "dig_for_treasure_nothing", "governor", "governor_punish", "governor_reward", "crew",
                  "crew_new", "crew_ship_full", "crew_port_empty", "crew_no_money", "crew_hire",
                  "men_count", "play_leviathan", "already_bought", "name_missing", "fight", "language",
                  "scores", "Spanish", "translation_missing", "sailors_to_hire", "castaway_no_hope",
                  "castaway_success", "calm", "color_missing", "sirens", "sirens_skipped", "schooner",
                  "taino_one", "taino_none", "taino_some", "new_turn", "new_resolution", "new_language",
                  "driftwood", "driftwood_success", "defeated_by_kraken", "casualties_of_kraken",
                  "storm_miss_turn", "storm_success", "storm_sail_damage", "flag_invalid", "flag_missing",
                  "mutiny_succeeded", "mutiny_suppressed", "apply", "load_saved_game", "exit", "save", "save_and_exit",
                  "name_label", "start_button", "color_label", "full_screen", "new_game", "flag_label"]
    _var_terms = ["apply", "load_saved_game", "exit", "save", "save_and_exit", "name_label", "start_button",
                  "color_label", "full_screen", "new_game", "flag_label"]
    # overload only the following lines to make the translation
    name = ""
    _terms = dict([(term, None) for term in _all_terms])
    # overload only the lines above to make the translation

    def __init__(self):  # don't call it and don't overload it!
        for term in self._all_terms:
            self.__dict__[term] = self._fetch_term(term)
        self.var_terms = dict([(term, self.__dict__[term]) for term in self._var_terms])

    def _fetch_term(self, term):
        translation = self._terms[term]
        if translation is None:
            raise NotImplementedError(f"Translataion of term '{term}' is missing from the {self._language} language.")
        else:
            return translation

    def get(self, term):
        return self._terms[term]
