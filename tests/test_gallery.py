from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock
from assets import Gallery


def add_dummy_picture(*args):
    Gallery._pictures["foo"] = "bar"


class TestGallery(TestCase):
    def setUp(self):
        Gallery._pictures = {}
        Gallery._raw_images = {}
        self.mock_image = Mock()
        self.mock_image.resize = Mock()
        self.mock_image.size = 2, 1

    def test_get_item_existing(self):
        Gallery._pictures["foo"] = "bar"
        self.assertEqual("bar", Gallery.get("foo"))

    @patch("assets.Gallery._load_picture", side_effect=add_dummy_picture)
    def test_get_item_nonexisting(self, _load_picture):
        self.assertEqual("bar", Gallery.get("foo"))
        _load_picture.assert_called_once_with("foo")

    @patch("assets.gallery.Settings.board_size", new_callable=PropertyMock)
    @patch("assets.Gallery._get_raw_image")
    @patch("assets.gallery.PhotoImage", return_value="photo_data")
    def test__load_picture(self, PhotoImage, _ger_raw_image, board_size):
        board_size.return_value = 100
        _ger_raw_image.return_value = self.mock_image
        Gallery._load_picture("map")
        _ger_raw_image.assert_called_with("map")
        board_size.assert_called()
        self.mock_image.resize.assert_called_once_with((100, 100), 1)
        self.assertEqual("photo_data", Gallery._pictures["map"])

    @patch("assets.Gallery._get_raw_image")
    @patch("assets.gallery.PhotoImage", return_value="photo_data")
    def test__load_picture_wind_direction(self, PhotoImage, _get_raw_image):
        _get_raw_image.return_value = self.mock_image
        Gallery._load_picture("wind_direction5")
        self.assertEqual("photo_data", Gallery._pictures["wind_direction2"])

    @patch("assets.Gallery._get_raw_image")
    @patch("assets.gallery.PhotoImage", return_value="photo_data")
    def test__load_picture_flag(self, PhotoImage, _get_raw_image):
        _get_raw_image.return_value = self.mock_image
        Gallery._load_picture("flag_british")
        self.assertEqual("photo_data", Gallery._pictures["flag_pirate"])

    @patch("assets.Gallery._generate_crewman")
    def test__load_picture_crewman(self, _generate_crewman):
        Gallery._load_picture("crewman1")
        _generate_crewman.assert_called_once()

    @patch("assets.Gallery._get_raw_image")
    @patch("assets.gallery.PhotoImage", return_value="photo_data")
    def test_generate_crewman(self, PhotoImage, _get_raw_image):
        _get_raw_image.return_value = self.mock_image
        Gallery._generate_crewman()
        self.assertEqual("photo_data", Gallery._pictures["crewman2"])
        self.assertEqual("photo_data", Gallery._pictures["crewman0"])
        self.mock_image.resize.assert_called_once_with((2, 1), 1)
        self.assertEqual(3, len(Gallery._pictures))

    @patch("assets.gallery.pillow_open", return_value="data")
    def test__get_raw_image_non_existing_key(self, pillow_open):
        self.assertEqual("data", Gallery._get_raw_image("non_existing_key"))
        pillow_open.assert_called_once_with("img/non_existing_key.png")

    def test__get_raw_image(self):
        Gallery._raw_images["existing_key"] = "data"
        self.assertEqual("data", Gallery._get_raw_image("existing_key"))

    @patch("assets.gallery.pillow_open")
    @patch("assets.gallery.PhotoImage", return_value="photo_data")
    def test__generate_flags_raw_loaded(self, PhotoImage, pillow_open):
        Gallery._raw_images = {"flag_british": self.mock_image, "flag_spanish": self.mock_image,
                               "flag_pirate": self.mock_image, "flag_dutch": self.mock_image,
                               "flag_french": self.mock_image}
        Gallery._generate_flags()
        pillow_open.assert_not_called()
        self.assertEqual(5, self.mock_image.resize.call_count)
        self.assertEqual(set(Gallery._raw_images.keys()), set(Gallery._pictures.keys()))
        self.assertTrue("photo_data" in Gallery._pictures.values())

    @patch("assets.gallery.PhotoImage", return_value="photo_data")
    @patch("assets.Gallery._get_raw_image")
    def test__generate_battle_screen_button_images(self, _get_raw_image, PhotoImage):
        Gallery._generate_battle_screen_button_images()
        self.assertEqual(10, _get_raw_image.call_count)
        self.assertIn("icon_grenade", Gallery._pictures)

    @patch("assets.gallery.PhotoImage", return_value="photo_data")
    @patch("assets.Gallery._get_raw_image")
    def test__generate_card_image(self, _get_raw_image, PhtotoImage):
        _get_raw_image.return_value = self.mock_image
        Gallery._generate_card_image("my_card")
        _get_raw_image.assert_called_once_with("my_card")
        self.mock_image.resize.assert_called_once()
        self.assertEqual("photo_data", Gallery._pictures["my_card_i"])
        self.assertEqual("photo_data", Gallery._pictures["my_card"])


class TestTinting(TestCase):
    def setUp(self):
        self.pixel_map = dict([((0, 0), (25, 25, 25, 0)),
                               ((0, 1), (44, 44, 44, 255)),
                               ((0, 2), (128, 128, 128, 128)),
                               ((0, 3), (255, 255, 255, 255))])
        self.mock_image = Mock()
        self.mock_image.size = 1, 4
        self.mock_image.load = Mock(return_value=self.pixel_map)

    @patch("assets.Gallery._get_raw_image", return_value="binary_image_data")
    def test_tint_image_to_white(self, _get_raw_image):
        self.assertEqual("binary_image_data", Gallery.tint_image("img/map.png"))

    @patch("assets.Gallery._get_raw_image")
    @patch("assets.Gallery._convert_color_hex_to_rgb", return_value=(0, 127, 127))
    def test_tint_image_to_dark_cyan(self, _convert_color_hex_to_rgb, _get_raw_image):
        _get_raw_image.return_value = self.mock_image
        self.assertEqual(self.mock_image, Gallery.tint_image("img/map.png", "#007F7F"))
        _get_raw_image.assert_called_once()
        self.mock_image.load.assert_called_once()
        _convert_color_hex_to_rgb.assert_called_once()
        self.assertEqual(self.pixel_map[0, 0], (25, 25, 25, 0))
        self.assertEqual(self.pixel_map[0, 1], (0, 21, 21, 255))
        self.assertEqual(self.pixel_map[0, 2], (0, 63, 63, 128))
        self.assertEqual(self.pixel_map[0, 3], (0, 127, 127, 255))

    def test__convert_color_hex_to_rgb(self):
        self.assertEqual((0, 127, 127), Gallery._convert_color_hex_to_rgb("#007F7F"))
