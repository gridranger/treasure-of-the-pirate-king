from PIL.ImageTk import PhotoImage
from PIL.Image import ANTIALIAS, BICUBIC, open as pillow_open
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
    def _load_picture(cls, name):
        if "crewman" in name:
            cls._generate_crewman()
            return
        name = "wind_direction" if "wind_direction" in name else name
        cls._raw_images[name] = pillow_open(f'{Settings.image_folder_path}/{name}.png')
        edge_ratio = cls._raw_images[name].size[0] / cls._raw_images[name].size[1]
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
        resized_raw_image = cls._raw_images[name].resize(size_required, ANTIALIAS)
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
    def _generate_crewman(cls):
        for i in [1, 2]:
            cls._raw_images[f"crewman{i}"] = pillow_open(f"{Settings.image_folder_path}/crewman{i}.png")
            cls._pictures[f"crewman{i}"] = PhotoImage(cls._raw_images[f"crewman{i}"])
        crewman_size = cls._raw_images["crewman1"].size
        cls._pictures["crewman0"] = PhotoImage((pillow_open('img/transparent.png')).resize(crewman_size, ANTIALIAS))
