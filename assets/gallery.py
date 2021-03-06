from PIL.ImageTk import PhotoImage
from PIL.Image import ANTIALIAS, BICUBIC, open as pillow_open
from assets.empires import Empires
from settings import ApplicationSettings as app, Paths


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
            file_name = item.replace(" ", "").lower()
            result = cls._raw_images[item] = pillow_open(f"{Paths.image_folder}/{file_name}.png")
        return result

    @classmethod
    def _load_picture(cls, name):
        if "crewman" in name:
            cls._generate_crewman()
            return
        elif "flag_" in name:
            cls._generate_flags()
            return
        elif "icon_" in name:
            cls._generate_battle_screen_button_images()
            return
        elif any(prefix in name for prefix in ["event_", "treasure_"]):
            cls._generate_card_image(name)
            return
        name = "wind_direction" if "wind_direction" in name else name
        image = cls._get_raw_image(name)
        edge_ratio = image.size[0] / image.size[1]
        size = {"compass": (app.tile_size * 3 - 10, app.tile_size * 3 - 10),
                "map": (app.board_size, app.board_size),
                "penz-1": (int(app.board_size / 40), int(app.board_size / 40 / edge_ratio)),
                "penz-8": (app.icon_size, app.icon_size),
                "penz-d": (app.icon_size, app.icon_size),
                "penz-d2": (app.icon_size, app.icon_size),
                "crew": (app.icon_size, app.icon_size),
                "wind_direction": (int(app.tile_size * 2 * edge_ratio), int(app.tile_size * 2)),
                "brigantine": (app.tile_size, int(app.tile_size / edge_ratio)),
                "frigate": (app.tile_size, int(app.tile_size / edge_ratio)),
                "schooner": (app.tile_size, int(app.tile_size / edge_ratio)),
                "galleon": (app.tile_size, int(app.tile_size / edge_ratio)),
                "tile": (app.tile_size, app.tile_size)}
        size_required = size.get(name, (int(app.tile_size * 0.9), int(app.tile_size * 0.9)))
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
            flag_name = f"flag_{empire.value.adjective.lower()}"
            flag = cls._get_raw_image(flag_name)
            side_ratio = flag.size[0] / flag.size[1]
            resized_image = flag.resize((int(app.icon_size * side_ratio), app.icon_size), ANTIALIAS)
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
        name = name[:-2] if name.endswith("_i") else name
        raw_image = cls._get_raw_image(name)
        cls._pictures[f"{name}_i"] = PhotoImage(raw_image.resize((app.icon_size, app.icon_size), ANTIALIAS))
        cls._pictures[name] = PhotoImage(raw_image)

    @classmethod
    def _generate_assembled_ship_image(cls, ship_type, color):
        ship_image = cls._get_raw_image(f"{ship_type}-h")
        edge_ratio = ship_image.size[1] / ship_image.size[0]
        target_size = app.tile_size, int(app.tile_size * edge_ratio)
        resized_ship_image = ship_image.resize(target_size, ANTIALIAS)
        sail_image = cls.tint_image(f"{ship_type}-v", color)
        resized_sail_image = sail_image.resize(target_size, ANTIALIAS)
        resized_ship_image.paste(resized_sail_image, (0, 0), resized_sail_image)
        cls._pictures[f"{ship_type}_{color}"] = PhotoImage(resized_ship_image)

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

    @classmethod
    def discard_cache(cls):
        cls._pictures = {}
