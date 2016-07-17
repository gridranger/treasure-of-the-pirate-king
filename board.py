from PIL.ImageTk import PhotoImage
from PIL.Image import ANTIALIAS, BICUBIC, open as pillow_open
from colorize import image_tint
from logging import debug
from time import sleep
from tkinter import BooleanVar, Canvas, CENTER, Frame, NW

_RGBA = "RGBA"


class Board(Frame):
    def __init__(self, master, width=768):
        Frame.__init__(self, master=master)
        self.player_setups = []
        self.size = width - width % 9
        self.board_canvas = self._add_board_canvas()
        self.tile_size = int(width / 9)
        self.tiles = self._generate_tiles()
        self.gallery = {}
        self.locations = {"battle_french": [(5, 9)],
                          "battle_british": [(9, 5)],
                          "battle_dutch": [(1, 5)],
                          "battle_spanish": [(5, 1)],
                          "portroyal": [(5, 5)],
                          "curacao": [(1, 9)],
                          "tortuga": [(9, 1)],
                          "havanna": [(1, 1)],
                          "martinique": [(9, 9)],
                          "windplus90": [(7, 1), (9, 7)],
                          "windminus90": [(1, 7), (3, 5)],
                          "windplus45": [(1, 3), (5, 7), (7, 9), (9, 3)],
                          "windminus45": [(3, 1), (5, 3), (7, 5), (3, 9)],
                          "bermuda": [(9, 4)],
                          "landland": [(1, 6), (2, 9), (5, 4), (9, 2)],
                          "storm": [(2, 5), (5, 6), (9, 6)],
                          "driftwood": [(1, 8), (2, 1), (6, 5), (9, 8)],
                          "calm": [(4, 5), (8, 9)],
                          "taino": [(4, 1), (6, 9)],
                          "treasureisland": [(1, 2), (4, 9), (8, 1), (8, 5)],
                          "stream": [(1, 4), (5, 8), (6, 1)],
                          "castaways": [(5, 2)]}
        self.locationsR = self._reverse_locations()
        self.ports = self._collect_ports()
        self.ship_figure_images = {}
        self.figures = {}
        self.is_field_select_blinking = False
        self.is_field_select_visible = BooleanVar(value=False)
        #                      N, NE, E, SE,S, SW,W, NW
        self.wind_direction = [2, 1, -3, 1, 2, 1, 0, 1]

    @property
    def port_coordinates(self):
        return list(self.ports.values())

    def _add_board_canvas(self):
        canvas = Canvas(self, width=self.size, height=self.size, bd=0, highlightthickness=0, relief='ridge')
        canvas.grid()
        canvas.bind("<Button-1>", self.klikk)
        return canvas

    def _generate_tiles(self):
        tiles = []
        tiles += self._generate_whole_lines()
        tiles += self._generate_other_lines()
        tiles.sort()
        return tiles

    def _reverse_locations(self):
        result = {}
        for location, tiles in self.locations.items():
            for coordinates in tiles:
                result[coordinates] = location
        return result

    def _collect_ports(self):
        ports = {}
        capitals = [empire.capital for empire in self.master.empires.values()]
        for capital in capitals:
            ports[capital] = self.locations[capital][0]
        return ports

    def change_wind_direction(self, wind_index):
        while self.wind_direction[wind_index] != 0:
            self.wind_direction.append(self.wind_direction.pop(0))

    def _generate_whole_lines(self):
        return self._generate_lines((1, 5, 9), tuple(range(1, 10)))

    def _generate_other_lines(self):
        return self._generate_lines((2, 3, 4, 6, 7, 8), (1, 5, 9))

    @staticmethod
    def _generate_lines(rows, fields):
        tiles = []
        for row in rows:
            for field in fields:
                tiles.append((row, field))
        return tiles

    def render_board(self):
        debug('Board rendering started.')
        icon_size = int(self.size / 20)
        self._render_background()
        self._render_semi_transparent_tile_backgrounds()
        self._render_tiles()
        self._render_player_ship_figures()
        self._load_tile_picker()
        self._render_compass()
        self._display_wind()
        self._render_money(icon_size)
        self._render_ports()
        self._render_crew(icon_size)
        self._render_ships()
        self._render_flags()
        self._render_crewman()
        self._render_battle_screen_button_images()
        debug('Board rendering finished.')

    def _render_background(self):
        self.gallery['map_background'] = PhotoImage(pillow_open('img/map.png').resize((self.size, self.size),
                                                                                      ANTIALIAS))
        self.board_canvas.create_image(0, 0, image=self.gallery['map_background'], anchor=NW)

    def _render_semi_transparent_tile_backgrounds(self):
        i = 'img/tile.png'
        s = (self.tile_size, self.tile_size)
        self.gallery['tile_background'] = PhotoImage((pillow_open(i).resize(s, ANTIALIAS)).convert(_RGBA))
        for (field_x, field_y) in self.tiles:
            self.board_canvas.create_image(int((field_x - 0.5) * self.tile_size),
                                           int((field_y - 0.5) * self.tile_size),
                                           image=self.gallery['tile_background'], anchor=CENTER)

    def _render_tiles(self):
        for location in self.locations:
            current = pillow_open('img/' + location + '.png')
            current = current.resize((int(self.tile_size * 0.9), int(self.tile_size * 0.9)), ANTIALIAS)
            current = PhotoImage(image=current)
            self.gallery[location] = current
            for x, y in self.locations[location]:
                self.board_canvas.create_image(int((x - 0.5) * self.tile_size), int((y - 0.5) * self.tile_size),
                                               image=self.gallery[location], anchor=CENTER)

    def _render_player_ship_figures(self):
        for player_object in self.master.players.values():
            self._render_ship_figure(player_object)

    def _render_ship_figure(self, player):
        ship_image = self._render_assembled_ship_image_for_player(player)
        self.ship_figure_images[player.nev] = PhotoImage(ship_image)
        if player.nev in self.figures:
            self.board_canvas.delete(self.figures[player.nev])
        x, y = player.pozicio
        self.figures[player.nev] = self.board_canvas.create_image((x - 0.5) * self.tile_size,
                                                                  (y - 0.5) * self.tile_size,
                                                                  image=self.ship_figure_images[player.nev],
                                                                  anchor=CENTER)

    def _render_assembled_ship_image_for_player(self, player):
        ship_image = pillow_open('img/{}-h.png'.format(player.hajo))
        height_multiplier = ship_image.size[1] / ship_image.size[0]
        ship_image = self._scale_ship_part(ship_image, height_multiplier)
        sail_image = image_tint('img/{}-v.png'.format(player.hajo), player.szin)
        sail_image = self._scale_ship_part(sail_image, height_multiplier)
        ship_image.paste(sail_image, (0, 0), sail_image)
        return ship_image

    def _scale_ship_part(self, ship_part, height_multiplier):
        return ship_part.resize((self.tile_size, int(self.tile_size * height_multiplier)), ANTIALIAS)

    def _load_tile_picker(self):
        picker = pillow_open('img/X.png')
        height_multiplier = picker.size[1] / picker.size[0]
        self.gallery['x'] = PhotoImage(image=picker.resize((self.tile_size, int(self.tile_size * height_multiplier)),
                                                           ANTIALIAS))

    def _render_compass(self):
        self.gallery['compass'] = PhotoImage((pillow_open('img/compass.png').resize(
            (self.tile_size * 3 - 10, self.tile_size * 3 - 10), ANTIALIAS)).convert(_RGBA))
        self.board_canvas.create_image(int(6.5 * self.tile_size), int(2.5 * self.tile_size),
                                       image=self.gallery['compass'], anchor=CENTER)
        wind_direction_arrow_image = pillow_open('img/wind_direction.png')
        wind_width_multiplier = wind_direction_arrow_image.size[0] / wind_direction_arrow_image.size[1]
        wind_direction_arrow_image = wind_direction_arrow_image.resize(
            (int(self.tile_size * 2 * wind_width_multiplier), int(self.tile_size * 2)), ANTIALIAS).convert(_RGBA)
        for i in range(8):
            self.gallery['wind_direction' + str(i)] = PhotoImage(
                wind_direction_arrow_image.rotate(i * -45, resample=BICUBIC, expand=1))
        self.wind_direction_arrow = self.board_canvas.create_image(0, 0, image=None)

    def _display_wind(self):
        current_direction = str(self.wind_direction.index(0))
        image_key = 'wind_direction' + current_direction
        self.board_canvas.delete(self.wind_direction_arrow)
        self.wind_direction_arrow = self.board_canvas.create_image(int(6.5 * self.tile_size),
                                                                   int(2.5 * self.tile_size),
                                                                   image=self.gallery[image_key], anchor=CENTER)

    def _render_money(self, icon_size):
        money = pillow_open('img/penz-1.png')
        size_rate = money.size[1] / money.size[0]
        money = money.resize((int(self.size / 40), int(self.size / 40 * size_rate)), ANTIALIAS)
        self.gallery['penz-1'] = PhotoImage(money.convert(_RGBA))
        for money_type in ['8', 'd', 'd2']:
            i = 'img/penz-' + money_type + '.png'
            loaded_image = (pillow_open(i).resize((icon_size, icon_size), ANTIALIAS)).convert(_RGBA)
            self.gallery['penz-' + money_type] = PhotoImage(loaded_image)

    def _render_ports(self):
        for empire in self.master.empires.values():
            capital = empire.capital
            self.gallery[capital + 'full'] = PhotoImage(pillow_open('img/' + capital + '.png').convert(_RGBA))

    def _render_crew(self, icon_size):
        self.gallery['crew'] = PhotoImage(
            (pillow_open('img/crew.png').resize((icon_size, icon_size), ANTIALIAS)).convert(_RGBA))

    def _render_ships(self):
        for ship_type in ['brigantine', 'frigate', 'schooner', 'galleon']:
            ship_image = pillow_open('img/' + ship_type + '.png')
            side_ratio = ship_image.size[1] / ship_image.size[0]
            ship_image = ship_image.resize((self.tile_size, int(self.tile_size * side_ratio)), ANTIALIAS)
            self.gallery[ship_type] = PhotoImage(ship_image)

    def _render_flags(self):
        for empire in self.master.empires:
            flag_name = 'flag_' + empire
            flag_image = pillow_open(('img/' + flag_name + '.png'))
            side_ratio = flag_image.size[0] / flag_image.size[1]
            self.gallery[flag_name] = PhotoImage(
                flag_image.resize((int(self.size / 20 * side_ratio), int(self.size / 20)), ANTIALIAS))

    def _render_crewman(self):
        crewman = pillow_open('img/crewman1.png')
        self.gallery['crewman0'] = PhotoImage((pillow_open('img/transparent.png')).resize(crewman.size, ANTIALIAS))
        self.gallery['crewman1'] = PhotoImage(crewman)
        self.gallery['crewman2'] = PhotoImage(pillow_open('img/crewman2.png'))

    def _render_battle_screen_button_images(self):
        buttons = ['gun', 'rifle', 'caltrop', 'grenade', 'grapeshot', 'greek_fire', 'monkey', 'sirenhorn', 'sirens',
                   "alvarez"]
        for button in buttons:
            self.gallery['icon_' + button] = PhotoImage(pillow_open('img/icon_' + button + '.png'))

    def kartyakep(self, pakli, prefix):
        "Leképezi a kártyákhoz szükséges képeket."
        for elem in pakli:
            self.gallery[elem] = PhotoImage(pillow_open('img/'+prefix+elem+'.png'))

    def kartyakep2(self, kep):
        "Leképezi a kártyákhoz szükséges képeket. A Kartya3-mal kompatibilis."
        self.gallery[kep] = pillow_open('img/'+kep+'.png')
        self.gallery[kep[kep.rfind('_')+1:]+'_i'] = PhotoImage(self.gallery[kep].resize((30,30),ANTIALIAS))
        self.gallery[kep] = PhotoImage(self.gallery[kep])

    def kormanyos(self,mostanioszlop,mostanisor,dobas,szellel = 1):
        "Meghatározza a lépések lehetséges kimenetelét."
        iranyok = {"e":(0,-1),
                   "d":(0,1),
                   "k":(1,0),
                   "ny":(-1,0)} # az irányok rácson való értelmezése
        szelirany = self.szel()
        celok = [] # ide írjuk majd az eredményeket (x,y) formában
        # leképezzük a lehetséges lépéseket
        utak = [] # az utak során meglátogatott mezők listája
        lepes = 1
        for (irany,(oszlop,sor)) in iranyok.items(): # leképezzük az első szomszédos mezőket, és beírjuk a kiindulási irányt, így a további mezőkből meg lehet tudni, hogy merről értük el őket
            elsomezo = (mostanioszlop+oszlop,mostanisor+sor,lepes,irany)
            if self.hajozhato(elsomezo[0],elsomezo[1]):
                utak.append(elsomezo)
        lepes = 2 # a további mezők következnek
        while lepes <= dobas+2:
            for elem in utak:
                lehetsegesUtak = [] # a vizsgálat alatt álló szomszédos mezők listája
                if elem[2] == lepes-1: # csak azokat a mezőket vizsgáljuk, amelyeket még nem néztünk meg (CPU takarékos)
                    for (irany,(oszlop,sor)) in iranyok.items(): # leképezzük a szomszédos mezőket, és felvesszük őket a vizsgálólistára 
                        lehetsegesUtak.append((elem[0]+oszlop,elem[1]+sor,lepes,elem[3]),)
                    for lehetsegesUt in lehetsegesUtak: # elvégzünk mindegyik lehetséges úton egy ellenőrzést
                        if self.hajozhato(lehetsegesUt[0],lehetsegesUt[1]) == False:
                            lehetsegesUtak[lehetsegesUtak.index(lehetsegesUt)] = 0 # ha a mező nincs rajta a táblán, megjelöljük
                        else: # megnézzük, a maradék mező nincs-e már rajta az útlistán
                            for ut in utak:
                                if (lehetsegesUt[0],lehetsegesUt[1]) == (ut[0],ut[1]) and lehetsegesUt[2] >= ut[2] and (lehetsegesUt[0],lehetsegesUt[1]) not in self.port_coordinates:
                                    lehetsegesUtak[lehetsegesUtak.index(lehetsegesUt)] = 0 # ha a mező már szerepel a listán, megjelöljük             
                    # ezzel kinyertük a utak listában tárolt mezők használható szomszédos mezőit
                for lehetsegesUt in lehetsegesUtak:
                    if lehetsegesUt:
                        utak.append(lehetsegesUt)
            lepes += 1
        if szellel:
            for ut in utak:
                if ut[2] == (dobas + self.szel(ut[3])):
                    celok.append((ut[0],ut[1]))
                elif ((ut[0],ut[1]) in self.port_coordinates) and ut[2] < (dobas + self.szel(ut[3])):
                    celok.append((ut[0],ut[1]))
        else:
            for ut in utak:
                if ut[2] == dobas:
                    celok.append((ut[0],ut[1]))
                elif ((ut[0],ut[1]) in self.port_coordinates) and ut[2] < dobas:
                    celok.append((ut[0],ut[1]))
        if (mostanioszlop,mostanisor) in celok: # Ha kiindulómező cél lenne, töröljük.
            celok.remove((mostanioszlop,mostanisor))
        if (mostanioszlop,mostanisor) in self.port_coordinates and szellel: # Ha kikötőből indulunk, visszatesszük / hozzáadjuk.
            celok.append((mostanioszlop,mostanisor))
        for cel in celok:
            if celok.count(cel) > 1:
                celok.remove(cel)
        self.celok = celok
        return celok

    def hajozhato(self,x,y):
        "Ellenőrzi, hogy az adott mező része-e a táblának"
        if (x,y) in self.tiles:
            return 1
        else:
            return 0

    def szel(self,irany="x"):
        "A szél erejét visszaadó függvény"
        szeliranyszotar = {"e":   self.wind_direction[0],
                           "ek":  self.wind_direction[1],
                           "k":   self.wind_direction[2],
                           "dk":  self.wind_direction[3],
                           "d":   self.wind_direction[4],
                           "dny": self.wind_direction[5],
                           "ny":  self.wind_direction[6],
                           "eny": self.wind_direction[7],
                           "x":   0}
        return szeliranyszotar[irany]
        
    def szel_valtoztat(self, szog = 0):
        "Megváltoztatja a szél irányát."
        ujszeliranyindex = (self.wind_direction.index(0) + int(szog / 45)) % 8
        self.change_wind_direction(ujszeliranyindex)
        self._display_wind()
    
    def celkereso(self, tiles):
        "Megmutatja a játékosnak azokat a négyzeteket, ahová majd lépni lehet."
        self.xlista = []
        for mezox,mezoy in tiles:
            self.xlista.append(self.board_canvas.create_image((mezox - 0.5) * self.tile_size, (mezoy - 0.5) * self.tile_size, image = self.gallery['x'], anchor = CENTER))
            self.is_field_select_visible.set(True)
        self.is_field_select_blinking = True
        self.villogas = None
        self.villogas = Mutatrejt(self)
        self.villogas.start()
          
    def klikk(self,event):
        "A mezőválasztást kezelő függvény."
        if not self.master.engine.dobasMegtortent.get():
            return
        self.master.menu.disable_additional_roll()
        klikkx,klikky = int(event.x / self.tile_size) + 1, int(event.y / self.tile_size) + 1
        if (klikkx,klikky) not in self.celok:
            return
        else:
            self.villogaski()
            self.hajotathelyez(klikkx,klikky)
            self.master.engine.szakasz_mezoevent()
            
    def villogaski(self):
        "Kikapcsolja a célnégyzetek villogását."
        self.master.game_board.is_field_select_blinking = False
        if self.is_field_select_visible.get():
            for x in self.xlista:
                self.board_canvas.itemconfigure(x, state='hidden')
            self.is_field_select_visible.set(False)
            self.xlista = []
            
    def hajotathelyez(self, celx, cely):
        "Végrehajtja a kijelölt lépést."
        self.board_canvas.coords(self.figures[self.master.engine.aktivjatekos.nev], (celx - 0.5) * self.tile_size, (cely - 0.5) * self.tile_size)
        self.master.engine.aktivjatekos.pozicio = (celx, cely)
        
class Mutatrejt():
    """A villogást irányító osztály."""
    def __init__(self, parent):
        self.boss = parent
    def start(self):
        while self.boss.is_field_select_blinking:
            self.fut()
            self.boss.master.update()
            sleep(0.25)
    
    def fut(self):
        if self.boss.is_field_select_visible.get():
            for x in self.boss.xlista:
                self.boss.board_canvas.itemconfigure(x,state='hidden')
            self.boss.is_field_select_visible.set(False)
        else:
            for x in self.boss.xlista:
                self.boss.board_canvas.itemconfigure(x,state='normal')
            self.boss.is_field_select_visible.set(True)
    
    def start0(self):
        if self.boss.is_field_select_visible.get():
            for x in self.boss.xlista:
                self.boss.board_canvas.itemconfigure(x,state='hidden')
            self.boss.is_field_select_visible.set(False)
            self.boss.boss.update()
            if not self.boss.is_field_select_blinking:
                self.boss.xlista = []
                return
        else:
            if not self.boss.is_field_select_blinking:
                self.boss.xlista = []
                return
            for x in self.boss.xlista:
                self.boss.board_canvas.itemconfigure(x,state='normal')
            self.boss.is_field_select_visible.set(True)
            self.boss.boss.update()
        sleep(0.25)
        self.start()
