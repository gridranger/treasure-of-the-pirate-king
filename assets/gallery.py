from PIL.ImageTk import PhotoImage
from PIL.Image import ANTIALIAS, BICUBIC, open as pillow_open
from assets.constants import Empires
from settings import Settings


class Gallery:
    _raw_images = {}
    _pictures = {}

    @classmethod
    def get(cls, item):
        try:
            result = cls._pictures.__getitem__(item)
        except KeyError:
            cls._load_picture(item)
            result = cls._pictures.__getitem__(item)
        return result

    @classmethod
    def _get_raw_image(cls, item):
        try:
            result = cls._raw_images[item]
        except KeyError:
            result = cls._raw_images[item] = pillow_open(f"{Settings.image_folder_path}/{item}.png")
        return result

    @classmethod
    def _load_picture(cls, name):
        if "crewman" in name:
            cls._generate_crewman()
            return
        elif "flag_" in name:
            cls._generate_flags()
            return
        name = "wind_direction" if "wind_direction" in name else name
        image = cls._get_raw_image(name)
        edge_ratio = image.size[0] / image.size[1]
        size = {"compass": (Settings.tile_size * 3 - 10, Settings.tile_size * 3 - 10),
                "map": (Settings.board_size, Settings.board_size),
                "penz-1": (Settings.board_size // 40, Settings.board_size / 40 // edge_ratio),
                "penz-8": (Settings.icon_size, Settings.icon_size),
                "penz-d": (Settings.icon_size, Settings.icon_size),
                "penz-d2": (Settings.icon_size, Settings.icon_size),
                "crew": (Settings.icon_size, Settings.icon_size),
                "wind_direction": (int(Settings.tile_size * 2 * edge_ratio), int(Settings.tile_size * 2)),
                "brigantine": (Settings.tile_size, Settings.tile_size // edge_ratio),
                "frigate": (Settings.tile_size, Settings.tile_size // edge_ratio),
                "schooner": (Settings.tile_size, Settings.tile_size // edge_ratio),
                "galleon": (Settings.tile_size, Settings.tile_size // edge_ratio)}
        size_required = size.get(name, (Settings.tile_size, Settings.tile_size))
        resized_raw_image = image.resize(size_required, ANTIALIAS)
        if name == "wind_direction":
            cls._generate_wind_direction_images(resized_raw_image)
        else:
            cls._pictures[name] = PhotoImage(resized_raw_image.convert("RGBA"))

    @classmethod
    def _generate_wind_direction_images(cls, resized_raw_image):
        for i in range(8):
            rotated_image = resized_raw_image.rotate(i * -45, resample=BICUBIC, expand=1)
            cls._pictures[f"wind_direction{i}"] = PhotoImage(rotated_image.convert("RGBA"))

    @classmethod
    def _generate_flags(cls):
        for empire in Empires:
            flag_name = f"flag_{empire.value}"
            flag = cls._get_raw_image(flag_name)
            side_ratio = flag.size[0] / flag.size[1]
            resized_image = flag.resize((Settings.icon_size * side_ratio, Settings.icon_size), ANTIALIAS)
            cls._pictures[flag_name] = PhotoImage(resized_image)

    @classmethod
    def _generate_crewman(cls):
        for i in [1, 2]:
            cls._pictures[f"crewman{i}"] = PhotoImage(cls._get_raw_image(f"crewman{i}"))
        crewman_size = cls._get_raw_image("crewman1").size
        cls._pictures["crewman0"] = PhotoImage(cls._get_raw_image("transparent").resize(crewman_size, ANTIALIAS))

    @classmethod
    def _generate_battle_screen_button_images(cls):
        buttons = ['gun', 'rifle', 'caltrop', 'grenade', 'grapeshot', 'greek_fire', 'monkey', 'sirenhorn', 'sirens',
                   "alvarez"]
        for button_name in buttons:
            name = f"icon_{button_name}"
            cls._pictures[name] = PhotoImage(cls._get_raw_image(name))

    @classmethod
    def _generate_card_image(cls, name):
        raw_image = cls._get_raw_image(name)
        cls._pictures[f"{name}_i"] = PhotoImage(raw_image.resize((Settings.icon_size, Settings.icon_size), ANTIALIAS))
        cls._pictures[name] = PhotoImage(raw_image)

    @classmethod
    def tint_image(cls, src, color_hex_code=""):
        binary_data = cls._get_raw_image(src)
        if not color_hex_code:
            return binary_data
        width, height = binary_data.size
        pixel_map = binary_data.load()
        r, g, b = cls._convert_color_hex_to_rgb(color_hex_code)
        for y in range(0, height):
            for x in range(0, width):
                tint = pixel_map[x, y][1] / 255
                transparency_bit = pixel_map[x, y][3]
                pixel_is_colored = bool(transparency_bit)
                if pixel_is_colored:
                    pixel_map[x, y] = (int(r * tint), int(g * tint), int(b * tint), transparency_bit)
        return binary_data

    @staticmethod
    def _convert_color_hex_to_rgb(hex_code):
        r = int(hex_code[1:3], 16)
        g = int(hex_code[3:5], 16)
        b = int(hex_code[5:], 16)
        return r, g, b
