from .localization import Localization


class English(Localization):
    name = "English"
    _terms = {"this_language": name,
              "British": "British",
              "price": "Cost",
              "gold": "gold",
              "balance_teams": "Balance teams",
              "settings": "Settings",
              "bermuda": "You sail through the edge of the Bermuda triangle, but nothing happens.",
              "brigantine": "brigantine",
              "aiming": "Take aim!",
              "whalevsoctopus": "fights it",
              "title": "The Treasure of the Pirate King",
              "battle": "Battle",
              "leave_battle": "Leaving battlefield",
              "leave_battle_text": "Leaving the battlefield now makes you lose your entire crew and you will be "
                                   "stranded on the Forgotten Island. Are you sure that you leave now?",
              "battle_sink": "The enemy ship sunk.",
              "battle_lose": "You lost. The enemy captain put you ashore at the Forgotten Island.",
              "event_card": "Event card",
              "extra": "Pick an enemy team to target bonus attack.",
              "resolution": "Resolution",
              "land": "The sailors collect fruits and fowl on the island. If the value you rolled is unfavourable you "
                      "may roll again at the next turn.",
              "land_log": "You may roll again.",
              "tavern": "Tavern",
              "French": "French",
              "frigate": "frigate",
              "main_main": "Main menu",
              "galleon": "galleon",
              "shipwright": "Shipwright",
              "ship_spotted": "Ship spotted. What is your order?",
              "ship_spotted_fire": "Fire!",
              "ship_spotted_alvarez": "You can rearrange your man.",
              "ship_spotted_battle_starts": "Use a card or push the Battle button to fight.",
              "ship_spotted_let_them_flee": "Let them sail away",
              "ship_spotted_battle": "The battle begun. Form teams.",
              "ship_spotted_reward": "Your loot %i gold pieces%s.",
              "ship_spotted_reward2": " and a loot card.",
              "ship_spotted_pirate": "Ship spotted. She is on intercept course.",
              "ship_spotted_powder_storage": "The enemy ship got a hit to the powder store and exploded.",
              "ship_spotted_boarding": "Board her!",
              "ship_spotted_fleeing": "Run for it",
              "ship_spotted_fleeing_unsuccesful": "The hostile ship were faster than you and the enemy sailors are "
                                                  "boarding your ship.",
              "ship_spotted_parrot": "Your parrot brings you the treasure from the enemy ship.\\n",
              "ship_spotted_enemy_casualties": "The enemy lost %i sailor(s) due the cannonfire.",
              "ship_spotted_player_casualties": "You lost 2 sailors due the cannonfire.",
              "ship_spotted_enemy_sinking": "The enemy ship got a leak! It will sink in 3 turns.",
              "ship_name_player": "Your own ship",
              "ship_name_pirate0": "Black Scream",
              "ship_name_pirate1": "Black Freighter",
              "ship_name_pirate2": "Destiny",
              "ship_name_pirate3": "Groglord",
              "to_battle": "Pick up the fight",
              "Dutch": "Dutch",
              "info": "Message",
              "game": "Game",
              "loading_game": "Loadig game...",
              "loading_done": "Loadig game... Done!",
              "discard_game": "Game is already in progress. If you start a new one, all unsaved changes will be lost. "
                              "Are you sure you want to start a new game?",
              "discard_game_b": "Game is already in progress. If you load a saved one, all unsaved changes will be "
                                "lost. Are you sure you want to load a saved game?",
              "start_game": "Starting game...",
              "start_game_done": "Starting game... Done!",
              "turn_order": "Turn order:",
              "Pirate": "Pirate",
              "card_discard": "Discard it",
              "card_keep": "Keep card",
              "cards": "Cards",
              "done": "Done",
              "port": "Port",
              "miss_turn": "I miss a turn (%i turns left)",
              "miss_turn_last_time": "I miss a turn",
              "treasure": "Treasure",
              "treasure_card": "Treasure card",
              "dig_for_treasure": "You can dig for treasuere next turn.",
              "dig_for_treasure_label": "You can dig for treasuere next turn.",
              "dig_for_treasure_question": "You can sail away or stay to look for treasure. Do you want to stay?",
              "dig_for_treasure_nothing": "Bad luck: you found nothing.",
              "governor": "Governor",
              "governor_punish": "As a pirate you are senteced to inprisonment for %i turn(s). Don't hope such mercy "
                                 "if you are caught plundering our ships again.",
              "governor_reward": "The govenor gives you %i gold(s) as a reward for sinking enemy ships.",
              "crew": "Crew",
              "crew_new": "Hire new members:",
              "crew_ship_full": "Ship is fully manned.",
              "crew_port_empty": "No one to hire.",
              "crew_no_money": "You have not enough treasure.",
              "crew_hire": "Hire",
              "men_count": "%i sailor(s) in %i team(s)",
              "play_leviathan": "Play leviathan",
              "already_bought": "Already bought",
              "name_missing": "Player {} has no name.",
              "fight": "Fight!",
              "language": "Language",
              "scores": "Scores",
              "Spanish": "Spanish",
              "translation_missing": "[Translation is missing.]",
              "sailors_to_hire": "Sailors to hire",
              "castaway_no_hope": "You could not get away from the island in this round.",
              "castaway_success": "A ship picked you up from the island and brought you to %s.",
              "calm": "You miss a turn because of the dead calm.",
              "color_missing": "{} has picked no color.",
              "sirens": "You lost %i sailors.",
              "sirens_skipped": "You have the card.",
              "schooner": "schooner",
              "taino_one": "A friendly native man joined your crew.",
              "taino_none": "Some natives wave you from the shores.",
              "taino_some": "%i friendly native men joined your crew.",
              "new_turn": "'%s's turn.",
              "new_resolution": "Resolution is set to",
              "new_language": "English is set as display language.",
              "driftwood": "Nothing useful could be found among the driftwood.",
              "driftwood_success": "Treasure worth of one gold found among the driftwood.",
              "defeated_by_kraken": "The kraken defeated you.",
              "casualties_of_kraken": "The Kraken killed %i of your sailors before you could fight it off.",
              "storm_miss_turn": "The storm shred the sails. Miss a turn while your crew patch it.",
              "storm_success": "Your ship sails further because of the storm's wind.",
              "storm_sail_damage": "The storm shred the sails. Fortunately you had some spare sails at the cargo "
                                   "hold.",
              "flag_invalid": "{} has picked no valid flag.",
              "flag_missing": "{} has picked no flag.",
              "mutiny_succeeded": "You are put ashore on the Forgotten Island.",
              "mutiny_suppressed": "You manage to calm you crew down. The crewman who plotted the mutiny is put "
                                   "ashore on an island.",
              'apply': 'Apply',
              'load_saved_game': 'Load saved game',
              'exit': 'Exit',
              'save': 'Save game',
              'save_and_exit': 'Save & exit',
              'name_label': 'Name:',
              'start_button': 'Start',
              'color_label': 'Color:',
              'full_screen': 'Full screen',
              'new_game': 'New Game',
              'flag_label': 'Flag:',
              "leviathan_title": "Leviathan",
              "sirens_title": "Sirens",
              "bobbydick_title": "Bobby Dick",
              "scurvy_title": "Scurvy",
              "mutiny_title": "Mutiny",
              "reefs_title": "Reefs",
              "deserters_title": "Deserters",
              "treacherous_mate_title": "The treacherous mate",
              "kraken_title": "Kraken attack",
              "grog_riot_title": "Grogriot",
              "carousal_title": "Carousal",
              "monkey3_title": "Three-headed monkey",
              "castaways_title": "Castaways",
              "ghost_ship_title": "Ghost ship",
              "sail_title": "List all parts of a sail",
              "freed_slaves_title": "Freed slaves",
              "set_sail_to_portroyal_title": "Set sail for Port Royal!",
              "set_sail_to_havanna_title": "Set sail for Havana!",
              "set_sail_to_martinique_title": "Set sail for Martinique!",
              "set_sail_to_curacao_title": "Set sail for Curacao!",
              "set_sail_to_tortuga_title": "Set sail for Tortuga!",
              "shipwreck_title": "Shipwreck",
              "voodoo_curse_title": "Voodoo Curse",
              "voodoo_wind_spell_title": "Voodoo Wind Spell",
              "tavern_brawl_title": "Tavern brawl",
              "found_port_title": "Establish a pirate anchorage",
              "competition_title": "Knotting competition",
              "compass_title": "Useless compass",
              "luck_title": "Fishermen's luck",
              "breath_title": "Hold breath competition",
              "pirate_map_0_title": "Treasure map",
              "pirate_map_1_title": "Treasure map",
              "leviathan_text": "If you have to miss a turn discard the leviathan instead.",
              "sirens_text": "Your crew hear strange melody from the direction of a nearby reef.",
              "bobbydick_text": "You encounter a harpooned  great sperm whale. You can either help it or finish it.",
              "scurvy_text": "Your crew suffer from scurvy. You will lose a sailor in every turn until you get to a "
                             "port or a fertile island.",
              "mutiny_text": "One of your sailors organized a mutiny.",
              "reefs_text": "You navigate through reefs.|The ship run aground on a reef. You miss a turn.",
              "deserters_text": "One of the longboats is missing. | crewmans deserted.",
              "treacherous_mate_text": "You found a delirious castaway who was first mate on Groglord. Before he died "
                                       "he told you how to find the pirate king's treasure once you are on the island "
                                       "that's coordinates are known only to Captain Harrison himself.",
              "kraken_text": "This high seas monster decided to consume your ship.",
              "grog_riot_text": "The grog you purchased at the last port is so weak so the sailors begin to sober. "
                                "Try to get to a port until your next turn is finished or the crew will mutiny.",
              "carousal_text": "The crew celebrate Davy Jones' birthday. The extra dose of grog makes them spirited. "
                               "You can roll again in the next turn if your first roll is not satisfying.",
              "monkey3_text": "A sailor at top spotted a three-headed monkey on a nearby island. You disembark but "
                              "find nothing.",
              "castaways_text": "You found some castaway on an island. | crewmen added.",
              "ghost_ship_text": "You gaff an abandoned ship. | of your crewmen mysteriously disappear however you "
                                 "find a treasure chest.",
              "sail_text": "We believe you can. It's your turn again.",
              "freed_slaves_text": "You intercepted a drifting slaver. The crew is missing mysteriously but some of "
                                   "the slaves are still alive. | crewmen joined.",
              "set_sail_to_portroyal_text": "None",
              "set_sail_to_havanna_text": "None",
              "set_sail_to_martinique_text": "None",
              "set_sail_to_curacao_text": "None",
              "set_sail_to_tortuga_text": "None",
              "shipwreck_text": "You can choose either to miss three turns or to lose your entire crew and get to the "
                                "Forgotten Island.",
              "voodoo_curse_text": "A vodou priest cursed your ship. Next time you would get some treasure you will "
                                   "find and empty chest.",
              "voodoo_wind_spell_text": "A vodou priest asks the loas for blessed wind. You can use this card once to "
                                        "turn the wind to any direciton.",
              "tavern_brawl_text": "Your men started to brawl at the tavern.",
              "found_port_text": "You fame has grown. Your favourite anchorage is more and more popular.",
              "competition_text": "You and the quatermaster bet tieing blowline faster.",
              "compass_text": "Islands are where they should be it is your compass that became useless. You miss one "
                              "turn as you calcualte your location according to the stars.",
              "luck_text": "None",
              "breath_text": "The breath holding record was beaten. You lost a sailor.",
              "pirate_map_0_text": "You found a treasure map. If you are at the southern treasure island you "
                                   "instantly find some tresure.",
              "pirate_map_1_text": "You found a treasure map. If you are at the northwestern treasure island you "
                                   "instantly find some tresure.",
              "treasure_title": "Loot",
              "treasure_text": "You get {} gold coins.",
              "greek_fire_title": "Greek fire",
              "greek_fire_text": "Scatters the selected enemy team. It can be used once in each battle.",
              "grenade_title": "Grenade",
              "grenade_text": "Vanishes a whole enemy team. Consumable.",
              "grapeshot_title": "Grapeshot",
              "grapeshot_text": "You can attack once without counterattack.",
              "dog_title": "Dog",
              "dog_text": "None",
              "caltrop_title": "Caltrop",
              "caltrop_text": "It reduces the enemy's attack strength when used in battle. Consumable.",
              "monkey_title": "Monkey",
              "monkey_text": "Recovers treasure from sinking enemy ships.",
              "parrot_title": "Parrot",
              "parrot_text": "None",
              "gun_title": "Pistol",
              "gun_text": "This will come in handy in battles.",
              "rifle_title": "Rifle",
              "rifle_text": "Reloading a rifle is longer than realoading a gun, but it is more accurate.",
              "sirenhorn_title": "Sirenhorn",
              "sirenhorn_text": "Makes some enemy sailors join you.",
              "map_title": "Map",
              "map_text": "None",
              "spare_sail_title": "Spare sail",
              "spare_sail_text": "None",
              "hawke_title": "Jane Hawke",
              "hawke_text": "The crew will not mutiny as long as she is aboard.",
              "fuil_title": "Peter Fuil",
              "fuil_text": "He can save some sailors after battle.",
              "lopez_title": "Maria Lopez",
              "lopez_text": "The player may always choose between two treasure cards as long as she is aboard.",
              "alvarez_title": "Juan Alvarez",
              "alvarez_text": "Teams can be rearranged once in every battle as long as he is aboard.",
              "vandenbergh_title": "Anna van den Bergh",
              "vandenbergh_text": "Two more sailors can be hired in every inn as long as she is aboard.",
              "molenaar_title": "Thomas Molenaar",
              "molenaar_text": "Sailors can be hired cheaper as long as he is aboard.",
              "therese_title": "Thérése",
              "therese_text": "Scurvy will not affect the crew as long as she is aboard.",
              "levasseur_title": "Jacques Levasseur",
              "levasseur_text": "The crew has higher chance to navigate through storms as long as he is aboard.",
              "lizzy_title": "Lizzy",
              "lizzy_text": "The only daughter of the pirate king.",
              "billy_title": "Billy",
              "billy_text": "Improved targeting with cannons."
              }