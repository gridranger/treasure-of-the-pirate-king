from assets import classproperty


class Settings:
    application_height = 1024
    application_width = 768
    image_folder_path = "img"

    @classproperty
    def board_size(cls):
        return cls.application_width - cls.application_width % 9

    @classproperty
    def icon_size(cls):
        return cls.board_size // 20

    @classproperty
    def tile_size(cls):
        return cls.application_width // 9
