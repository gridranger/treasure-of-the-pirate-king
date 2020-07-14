from assets import classproperty


class Settings:
    application_height = 1024
    application_width = 768
    image_folder_path = "img"
    preload_images = True

    @classproperty
    def board_size(cls):
        return cls.application_height - cls.application_height % 9

    @classproperty
    def icon_size(cls):
        return cls.board_size // 20

    @classproperty
    def tile_size(cls):
        return cls.application_height // 9
