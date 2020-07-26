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
                  "name_label", "start_button", "color_label", "full_screen", "new_game", "flag_label",
                  "leviathan_title", "sirens_title", "bobbydick_title", "scurvy_title", "mutiny_title", "reefs_title",
                  "deserters_title", "treacherous_mate_title", "kraken_title", "grog_riot_title", "carousal_title",
                  "monkey3_title", "castaways_title", "ghost_ship_title", "sail_title", "freed_slaves_title",
                  "set_sail_to_portroyal_title", "set_sail_to_havanna_title", "set_sail_to_martinique_title",
                  "set_sail_to_curacao_title", "set_sail_to_tortuga_title", "shipwreck_title", "voodoo_curse_title",
                  "voodoo_wind_spell_title", "tavern_brawl_title", "found_port_title", "competition_title",
                  "compass_title", "luck_title", "breath_title", "pirate_map_0_title", "pirate_map_1_title",
                  "leviathan_text", "sirens_text", "bobbydick_text", "scurvy_text", "mutiny_text", "reefs_text",
                  "deserters_text", "treacherous_mate_text", "kraken_text", "grog_riot_text", "carousal_text",
                  "monkey3_text", "castaways_text", "ghost_ship_text", "sail_text", "freed_slaves_text",
                  "set_sail_to_portroyal_text", "set_sail_to_havanna_text", "set_sail_to_martinique_text",
                  "set_sail_to_curacao_text", "set_sail_to_tortuga_text", "shipwreck_text", "voodoo_curse_text",
                  "voodoo_wind_spell_text", "tavern_brawl_text", "found_port_text", "competition_text", "compass_text",
                  "luck_text", "breath_text", "pirate_map_0_text", "pirate_map_1_text", "treasure_title",
                  "greek_fire_title", "grenade_title", "grapeshot_title", "dog_title", "caltrop_title", "monkey_title",
                  "parrot_title", "gun_title", "rifle_title", "sirenhorn_title", "map_title", "spare_sail_title",
                  "hawke_title", "fuil_title", "lopez_title", "alvarez_title", "vandenbergh_title", "molenaar_title",
                  "therese_title", "levasseur_title", "lizzy_title", "billy_title", "treasure_text", "greek_fire_text",
                  "grenade_text", "grapeshot_text", "dog_text", "caltrop_text", "monkey_text", "parrot_text",
                  "gun_text", "rifle_text", "sirenhorn_text", "map_text", "spare_sail_text", "hawke_text", "fuil_text",
                  "lopez_text", "alvarez_text", "vandenbergh_text", "molenaar_text", "therese_text", "levasseur_text",
                  "lizzy_text", "billy_text"]
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
            raise NotImplementedError(f"Translataion of term '{term}' is missing from the {self.name} language.")
        else:
            return translation

    def get(self, term):
        return self._terms[term]
