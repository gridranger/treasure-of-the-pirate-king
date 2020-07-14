from unittest import TestCase
from unittest.mock import Mock, patch
from board import Board, Canvas


assets_gallery_get = "assets.Gallery.get"


class TestBoard(TestCase):

    def setUp(self):
        self._board = Board(None)
        self._original_canvas_create_image = Canvas.create_image
        Canvas.create_image = Mock(return_value="dummy_picture")

    def tearDown(self):
        Canvas.create_image = self._original_canvas_create_image

    def test__collect_ports(self):
        result = self._board._collect_ports()
        self.assertEqual(5, len(result))
        test_key = list(result.keys())[0]
        self.assertEqual(result[test_key], self._board.locations[test_key][0])

    @patch(assets_gallery_get, return_value="dummy_picture")
    def test__render_background(self, get):
        self._board._render_background()
        Canvas.create_image.assert_called_once_with(0, 0, image="dummy_picture", anchor="nw")

    def test__render_semi_transparent_tile_backgrounds(self):
        self._board._render_semi_transparent_tile_backgrounds()
        self.assertEqual(len(self._board.tiles), Canvas.create_image.call_count)

    def test__render_tiles(self):
        self._board._render_tiles()
        self.assertEqual(45, Canvas.create_image.call_count)
