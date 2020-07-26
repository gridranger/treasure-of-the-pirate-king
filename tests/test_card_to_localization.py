from unittest import TestCase
from assets.cards.card import Leviathan, TreasureCard
from assets.cards.cardactions import CardActions
from settings import ApplicationSettings as s
from localization import Languages


class TestCardToLocalization(TestCase):
    def setUp(self):
        s.language = Languages.ENGLISH.value

    def test_treasure_card(self):
        c = TreasureCard(50)
        self.assertEqual("Loot", c.title)
        self.assertEqual("You get 50 gold coins.", c.text)

    def test_event_card(self):
        l = Leviathan()
        self.assertEqual("If you have to miss a turn discard the leviathan instead.", l.text)
        self.assertEqual((CardActions.ADD_PLAYER_STATUS, ["leviathan"]), l.action())
