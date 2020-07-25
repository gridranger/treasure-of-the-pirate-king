from .localization import Localization


class Pirate(Localization):
    name = "Kalóz"
    _terms = {
        "this_language": name,
        "British": "könyörtelen angol",
        "price": "Ár",
        "gold": "arany",
        "balance_teams": "Mindenki a heléyre!",
        "settings": "Fedélköz",
        "bermuda": "A Bermuda-háromszög szélén a tenger csendes. Arr... Sehol egy hajó!",
        "brigantine": "brigantin",
        "aiming": "Célozz!",
        "whalevsoctopus": "megküzd vele",
        "title": "A kalózkirály kincse - Vedd el, ami kell, és vissza ne add!",
        "battle": "Harc",
        "leave_battle": "Gyáva megfutamodás",
        "leave_battle_text": "Ha bezárod ezt a képernyőt, elveszíted a matrózaid, és a száműzöttek szigetére kerülsz. "
                             "Biztosan ezt szeretnéd?",
        "battle_sink": "Az ellenséges hajót a fenékre küldtük.",
        "battle_lose": "Veszítettél. Ellenfeleid fogságba ejtettek, és a Száműzöttek szigetén tettek partra.",
        "event_card": "Eseménykártya",
        "extra": "Válaszd ki, melyik ellenséges csapat ellen indítasz extra támadást!",
        "resolution": "Mérrret",
        "land": "Amíg a többiek vannak soron, matrózaid gyümölcsöket és szárnyasokat gyűjtenek be az érintetlen "
                "szigetről. A friss koszt fellelkesíti őket, ezért, ha a következő körben hajózáshoz dobott érték "
                "kedvezőtlen, egyszer újra dobhatsz helyette.",
        "land_log": "Újra dobhat, uram, ehelyett.",
        "tavern": "Csapszék",
        "French": "puhány francia",
        "frigate": "fregatt",
        "main_main": "Árboc",
        "galleon": "galleon",
        "shipwright": "Hajóács",
        "ship_spotted": "Hajó a láthatáron! Mit tegyünk, kapitány?",
        "ship_spotted_fire": "Pörköljünk oda!",
        "ship_spotted_alvarez": "Rendezze újra az embereit, uram!",
        "ship_spotted_battle_starts": "Játssz ki egy lapot, vagy harcolj.",
        "ship_spotted_let_them_flee": "Ne törődjetek vele",
        "ship_spotted_battle": "Kapitány, állítsa össze a csapatokat a harc előtt.",
        "ship_spotted_reward": "Megkaparintottunk %i aranyat%s.",
        "ship_spotted_reward2": " és egy kincskártyát",
        "ship_spotted_pirate": "Hajó a láthatáron! Felénk tart, kapitány.",
        "ship_spotted_powder_storage": "Az ellenséges hajó lőporraktára felrobbant.",
        "ship_spotted_boarding": "Csáklyákat készenlétbe!",
        "ship_spotted_fleeing": "Menküljünk!",
        "ship_spotted_fleeing_unsuccesful": "Nem tudjuk lehagyni őekt, készüljünk a közelharcra!",
        "ship_spotted_parrot": "Papagájod megszerezte az ellenséges hajó kincsét!\\n",
        "ship_spotted_enemy_casualties": "Az ellenfél %i matrózt veszített az ágyúzás során.",
        "ship_spotted_player_casualties": "2 matrózt vesztettünk az ágyúzás során, uram.",
        "ship_spotted_enemy_sinking": "Léket ütöttünk az ellenséges hajó, uram. 3 kör és elsüllyed.",
        "ship_name_player": "Saját hajód",
        "ship_name_pirate0": "Fekete Sikoly",
        "ship_name_pirate1": "Vérszínű Bárka",
        "ship_name_pirate2": "Végzet",
        "ship_name_pirate3": "Grogbáró",
        "to_battle": "Harcra!",
        "Dutch": "pohos holland",
        "info": "Palackposta",
        "game": "Főfedélzet",
        "loading_game": "Kötélzet kibogozása...",
        "loading_done": "Kötélzet kibogozása... Kész!",
        "discard_game": "Teringettét, már kihajóztunk egyszer! Ha újra megtesszük, a korábbi út lejegyzetlen "
                        "eredményei elvesznek. Hótbiztos kihajózzunk, kapitány?",
        "discard_game_b": "Teringettét, ha hajót váltunk, a jelenlegi zsákmány elmentetlen része odavész. Hótbiztos "
                          "átszállunk, kapitány?",
        "start_game": "Mindenki a fedélzetre, kihajózunk!",
        "start_game_done": "Kihajóztunk!",
        "turn_order": "Csak sorjában, matrózok:",
        "Pirate": "kalóz",
        "card_discard": "Eldobom",
        "card_keep": "Megtartom",
        "cards": "Kártyák",
        "done": "Ennyit erről",
        "port": "Kikötő",
        "miss_turn": "Kimaradunk (még %i kör)",
        "miss_turn_last_time": "Kimaradunk",
        "treasure": "Zsákmány",
        "treasure_card": "Kincskártya",
        "dig_for_treasure": "Ez egy kincses sziget, kapitány!",
        "dig_for_treasure_label": "A kincses szigeten",
        "dig_for_treasure_question": "Tovább is mehetünk. Maradjunk kincsetkeresni, uram?",
        "dig_for_treasure_nothing": "Semmit sem találtunk, uram.",
        "governor": "Kormányzó",
        "governor_punish": "Kalózkodás vétkéért %i kör börtönbüntetést kapsz. Legközelebb ne számíts irgalmora, ha a "
                           "birodalmunk hajóit fosztogatod!",
        "governor_reward": "Áldásos tevékenyégedért %i aranytallér üti a markodat.",
        "crew": "Matrózok",
        "crew_new": "Hány fő kell még, kapitány?",
        "crew_ship_full": "Tele a hajó, kapitány!",
        "crew_port_empty": "A csapszék üres.",
        "crew_no_money": "Nincs pénzünk újakra, kapitány.",
        "crew_hire": "Johó!",
        "men_count": "%i matróz %i csapatban",
        "play_leviathan": "Majd a szörny segít!",
        "already_bought": "Már megszereztük",
        "name_missing": "{}. matróz, mi a neved?",
        "fight": "Harcra!",
        "language": "Nyelv...arr...",
        "scores": "Davy Jones ládája",
        "Spanish": "gaz spanyol",
        "translation_missing": "[Kapitány, ezen a nyelven ezt nem tudom elmondani.]",
        "sailors_to_hire": "Tettrekész legények",
        "castaway_no_hope": "Ebben a körben nem tudsz megszabadulni a szigetről.",
        "castaway_success": "Egy hajó felvett a szigetről, és %s kikötőjébe vitt.",
        "calm": "A szélcsend miatt egy körből kimaradunk, uram.",
        "color_missing": "{}, válassz színt, de még ma!",
        "sirens": "%i matróz a vízbe vetette magát, uram.",
        "sirens_skipped": "Egy szirént befogtunk, uram!",
        "schooner": "szkúner",
        "taino_one": "Egy benszülött csatlakozott hozzánk, uram.",
        "taino_none": "Benszülötteket láttunk, uram.",
        "taino_some": "%i benszülött csatlakozott hozzánk, uram.",
        "new_turn": "%s köre jön.",
        "new_resolution": "Zsákmányod egy új felbontás:",
        "new_language": "A legénység kalózok módjára beszél, johó!",
        "driftwood": "Az uszadékban semmi hasznos nem volt, uram!",
        "driftwood_success": "Egy arany értékű kincset találtunk, uram.",
        "defeated_by_kraken": "A kraken legyőzött minket, uram.",
        "casualties_of_kraken": "A kraken elragadott %i matrózt, mielőtt legyőztük, uram.",
        "storm_miss_turn": "A vihar tönkretette a vitorlázatot. Kimaradsz egy körből, amíg a legénység megfoltozza.",
        "storm_success": "A viharos szél tovább röpíti hajódat.",
        "storm_sail_damage": "A vihar tönkretette a vitorlázatot. Még szerencse, hogy a raktérben volt "
                             "tartalékvitorla.",
        "flag_invalid": "{}, válassz zászlót, de érvényeset!",
        "flag_missing": "{}, válassz zászlót, de még ma!",
        "mutiny_succeeded": "A matrózaid egy isten háta mögötti szigeten hagynak.",
        "mutiny_suppressed": "Miután rendre utasítottad a kutyákat, a pallóra tereled a vezérüket.",
        "apply": "Hajrá",
        "load_saved_game": "Folytassuk, kalózok!",
        "exit": "Takarodó",
        "save": "Jegyezzük föl",
        "save_and_exit": "Jegyezd meg és tünés",
        "name_label": "Neved:",
        "start_button": "Hajrá!",
        "color_label": "Vitorla:",
        "full_screen": "Vitorlát bonts!",
        "new_game": "Tengerre, semmirekellők!",
        "flag_label": "Lobogó:"
    }
