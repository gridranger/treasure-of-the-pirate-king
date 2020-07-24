from sys import modules
from unittest import TestCase
from unittest.mock import Mock, patch
from board import Board


create_image = "board.Canvas.create_image"


class TestGalleryToBoard(TestCase):
    def setUp(self):
        self._board = Board(None)

    def tearDown(self):
        modules.get("assets").Gallery._raw_images = {}
        modules.get("assets").Gallery._raw_images = {}

    @patch(create_image)
    def test__render_background(self, create_image):
        self._board._render_background()
        self.assertIn("_PhotoImage__photo", create_image.call_args.kwargs["image"].__dict__)

    @patch(create_image)
    def test__render_semi_transparent_tile_backgrounds(self, create_image):
        self._board._render_semi_transparent_tile_backgrounds()
        self.assertIn("_PhotoImage__photo", create_image.call_args.kwargs["image"].__dict__)

    @patch(create_image)
    def test__render_tiles(self, create_image):
        self._board._render_tiles()
        self.assertIn("_PhotoImage__photo", create_image.call_args.kwargs["image"].__dict__)

    def test_render_ship_figure(self):
        mock_player = Mock(ship="frigate", color="#00FF00", name="dummy", coordinates=(1, 2))
        self._board.render_ship_figure(mock_player)
        self.assertIn("frigate_#00FF00", modules.get("assets").Gallery._pictures)
