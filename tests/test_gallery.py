from sys import modules
from unittest import TestCase
from unittest.mock import Mock, patch
import assets


def add_dummy_picture(*args):
    assets.Gallery._pictures["foo"] = "bar"


class TestGallery(TestCase):
    def setUp(self):
        if modules.get("assets"):
            del modules["assets"]
        assets.Gallery._pictures = {}
        self.mock_image = Mock()
        self.mock_image.resize = Mock()
        self.mock_image.size = 2, 1

    def test_get_item_existing(self):
        assets.Gallery._pictures["foo"] = "bar"
        self.assertEqual("bar", assets.Gallery.get("foo"))

    @patch("assets.Gallery._load_picture", side_effect=add_dummy_picture)
    def test_get_item_nonexisting(self, _load_picture):
        self.assertEqual("bar", assets.Gallery.get("foo"))
        _load_picture.assert_called_once_with("foo")

    def test__load_picture(self):
        assets.gallery.pillow_open = Mock(return_value=self.mock_image)
        assets.gallery.PhotoImage = Mock(return_value="photo_data")
        assets.Gallery._load_picture("map")
        self.assertEqual("photo_data", assets.Gallery._pictures["map"])
        assets.gallery.pillow_open.assert_called_with("img/map.png")
        self.mock_image.resize.assert_called_once()

    def test__load_picture_wind_direction(self):
        assets.gallery.pillow_open = Mock(return_value=self.mock_image)
        assets.gallery.PhotoImage = Mock(return_value="photo_data")
        assets.Gallery._load_picture("wind_direction6")
        self.assertEqual("photo_data", assets.Gallery._pictures["wind_direction2"])

    @patch("assets.Gallery._generate_crewman")
    def test__load_picture_crewman(self, _generate_crewman):
        assets.Gallery._load_picture("crewman1")
        _generate_crewman.assert_called_once()

    def test_generate_crewman(self):
        assets.gallery.pillow_open = Mock(return_value=self.mock_image)
        assets.gallery.PhotoImage = Mock(return_value="photo_data")
        assets.Gallery._generate_crewman()
        self.assertEqual(3, len(assets.Gallery._pictures))
