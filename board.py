from PIL.ImageTk import PhotoImage
from PIL.Image import ANTIALIAS, BICUBIC, open as pillow_open
from colorize import image_tint
from logging import debug
from time import sleep
from tkinter import BooleanVar, Canvas, CENTER, Frame, NW


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
                          "szelcsend": [(4, 5), (8, 9)],
                          "taino": [(4, 1), (6, 9)],
                          "treasureisland": [(1, 2), (4, 9), (8, 1), (8, 5)],
                          "stream": [(1, 4), (5, 8), (6, 1)],
                          "castaways": [(5, 2)]}
        self.locationsR = self._reverse_locations()
        # TODO Purge the newt two lines
        self.kikototarR = {}  # A városok koordináta alapú meghatározására szolgál.
        self.kikotok = self._collect_ports()
        self.hajotar = {}
        self.figuraszotar = {}
        self.villogasaktiv = 0
        self.xlatszik = BooleanVar()
        self.xlatszik.set(0)
        #                 e  ek   k  dk  d  dny  ny  eny
        self.szelirany = [2,  1, -3,  1, 2,   1,  0,   1]

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
        ports = []
        for empire in self.master.empires.values():
            ports.append(self.locations[empire.capital][0])
            self.kikototarR[self.locations[empire.capital][0]] = empire.capital
        return sorted(ports)

    def change_wind_direction(self, wind_index):
        while self.szelirany[wind_index] != 0:
            self.szelirany.append(self.szelirany.pop(0))

    def _generate_whole_lines(self):
        return self._generate_lines((1, 5, 9), tuple(range(1, 10)))

    def _generate_other_lines(self):
        return self._generate_lines((2, 3, 4, 6, 7, 8), (1, 5, 9))

    def _generate_lines(self, rows, fields):
        tiles = []
        for row in rows:
            for field in fields:
                tiles.append((row, field))
        return tiles

    def render_board(self):
        debug('Board rendering started.')
        # A háttér betöltése
        self.gallery['hatter'] = PhotoImage(pillow_open('img/map.png').resize((self.size, self.size), ANTIALIAS))
        self.board_canvas.create_image(0, 0, image = self.gallery['hatter'], anchor = NW)
        # A félig áttetsző mezőhátterek leképezése
        self.gallery['mezohatter'] = PhotoImage((pillow_open('img/mezo.png').resize((self.tile_size, self.tile_size), ANTIALIAS)).convert("RGBA"))
        for (mezox,mezoy) in self.tiles:
            self.board_canvas.create_image(int((mezox - 0.5) * self.tile_size), int((mezoy - 0.5) * self.tile_size), image = self.gallery['mezohatter'], anchor = CENTER)
        # A mezőiconok betöltése
        for elem in self.locations:
            aktualis = pillow_open('img/'+elem+'.png')
            aktualis = aktualis.resize((int(self.tile_size * 0.9), int(self.tile_size * 0.9)), ANTIALIAS)
            aktualis = PhotoImage(image=aktualis)
            self.gallery[elem]=aktualis
        self.mezoszotar = {} # ebben tároljuk a mezőket
        for elem in self.locations.keys():
            self.mezoszotar[elem] = Mezo(self, self.locations[elem], elem)
        for jatekos in self.master.players.keys():
            self.figuratLetrehoz(self.master.players[jatekos].nev,
                                 self.master.players[jatekos].pozicio[0],
                                 self.master.players[jatekos].pozicio[1],
                                 self.master.players[jatekos].hajo,
                                 self.master.players[jatekos].szin)
        # Az úticéljelölő betöltése
        self.xkep = pillow_open('img/X.png')
        magassagszorzo = self.xkep.size[1]/self.xkep.size[0]
        self.gallery['x'] = PhotoImage(image=self.xkep.resize((self.tile_size, int(self.tile_size * magassagszorzo)), ANTIALIAS))
        # A szélrózsa betöltése
        self.gallery['compass'] = PhotoImage((pillow_open('img/compass.png').resize((self.tile_size * 3 - 10, self.tile_size * 3 - 10), ANTIALIAS)).convert("RGBA"))
        self.board_canvas.create_image(int(6.5 * self.tile_size), int(2.5 * self.tile_size), image = self.gallery['compass'], anchor = CENTER)
        self.szeliranykep = pillow_open('img/szelirany.png')
        szeliranySzelessegszorzo = self.szeliranykep.size[0]/self.szeliranykep.size[1]
        self.szeliranykep = self.szeliranykep.resize((int(self.tile_size * 2 * szeliranySzelessegszorzo), int(self.tile_size * 2)), ANTIALIAS).convert("RGBA")
        for i in range(8):
            self.gallery['szelirany'+str(i)] = PhotoImage(self.szeliranykep.rotate(i*-45, resample = BICUBIC, expand = 1))
        self.szelmutato = self.board_canvas.create_image(0, 0, image = None)
        self.szel_megjelenit()
        # A pénzek betöltése
        a = pillow_open('img/penz-1.png')
        penzszorzo = a.size[1]/a.size[0]
        self.gallery['penz-1'] = PhotoImage((a.resize((int(self.size / 40), int(self.size / 40 * penzszorzo)), ANTIALIAS)).convert("RGBA"))
        a = int(self.size / 20)
        for penzfajta in ['8','d','d2']:
            self.gallery['penz-'+penzfajta] = PhotoImage((pillow_open('img/penz-'+penzfajta+'.png').resize((a,a), ANTIALIAS)).convert("RGBA"))
        # A kikötőképek betöltése
        for empire in self.master.empires:
            capital = self.master.empires[empire].capital
            self.gallery[capital + 'full'] = PhotoImage(pillow_open('img/' + capital + '.png').convert("RGBA"))
        # A matrózok betöltése
        self.gallery['matrozok'] = PhotoImage((pillow_open('img/matrozok.png').resize((a,a), ANTIALIAS)).convert("RGBA"))
        # Hajók betöltése a hajóács gombjaihoz, és az ellenfelekhez.
        for hajotipus in ['brigantine', 'frigate', 'schooner', 'galleon']:
            hajokep = pillow_open('img/'+hajotipus+'.png')
            magassagszorzo = hajokep.size[1]/hajokep.size[0]
            hajokep = hajokep.resize((self.tile_size, int(self.tile_size * magassagszorzo)), ANTIALIAS)
            self.gallery[hajotipus] = PhotoImage(hajokep)
        # A zászlók betöltése.
        for birodalom in self.master.empires.keys():
            zNev = 'flag_'+birodalom
            zKep = pillow_open(('img/'+zNev+'.png'))
            magassagszorzo = zKep.size[0]/zKep.size[1]
            self.gallery[zNev] = PhotoImage(zKep.resize((int(self.size / 20 * magassagszorzo), int(self.size / 20)), ANTIALIAS))
        # Matrózok betöltése.
        self.gallery['matroz1'] = pillow_open('img/matroz1.png')
        self.gallery['matroz0'] = PhotoImage((pillow_open('img/transparent.png')).resize((self.gallery['matroz1'].size[0], self.gallery['matroz1'].size[1]), ANTIALIAS))
        self.gallery['matroz1'] = PhotoImage(self.gallery['matroz1'])
        self.gallery['matroz2'] = PhotoImage(pillow_open('img/matroz2.png'))
        # Csatagombok betöltése.
        for i in ['gun', 'rifle', 'caltrop', 'grenade', 'grapeshot', 'greek_fire', 'monkey', 'sirenhorn', 'sirens', "alvarez"]:
            self.gallery['icon_'+i] = PhotoImage(pillow_open('img/icon_'+i+'.png'))
        debug('Board rendering finished.')
    
    def kartyakep(self, pakli, prefix):
        "Leképezi a kártyákhoz szükséges képeket."
        for elem in pakli:
            self.gallery[elem] = PhotoImage(pillow_open('img/'+prefix+elem+'.png'))

    def kartyakep2(self, kep):
        "Leképezi a kártyákhoz szükséges képeket. A Kartya3-mal kompatibilis."
        self.gallery[kep] = pillow_open('img/'+kep+'.png')
        self.gallery[kep[kep.rfind('_')+1:]+'_i'] = PhotoImage(self.gallery[kep].resize((30,30),ANTIALIAS))
        self.gallery[kep] = PhotoImage(self.gallery[kep])
        
    def figuratLetrehoz(self, username, x, y, hajotipus, szin, korabbiTorlese = 0):
        "Leképezi a felhasználó figuráját a táblán."
        hajokep = pillow_open('img/'+hajotipus+'-h.png')
        magassagszorzo = hajokep.size[1]/hajokep.size[0]
        hajokep = hajokep.resize((self.tile_size, int(self.tile_size * magassagszorzo)), ANTIALIAS)
        vitorlakep = (image_tint('img/'+hajotipus+'-v.png',szin).resize((self.tile_size, int(self.tile_size * magassagszorzo)), ANTIALIAS))
        hajokep.paste(vitorlakep, (0,0), vitorlakep)
        self.hajotar[username] = PhotoImage(hajokep)
        if korabbiTorlese == 1:
            self.board_canvas.delete(self.figuraszotar[username])
        self.figuraszotar[username] = self.board_canvas.create_image((x - 0.5) * self.tile_size, (y - 0.5) * self.tile_size, image = self.hajotar[username], anchor = CENTER)

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
                                if (lehetsegesUt[0],lehetsegesUt[1]) == (ut[0],ut[1]) and lehetsegesUt[2] >= ut[2] and (lehetsegesUt[0],lehetsegesUt[1]) not in self.kikotok:
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
                elif ((ut[0],ut[1]) in self.kikotok) and ut[2] < (dobas + self.szel(ut[3])):
                    celok.append((ut[0],ut[1]))
        else:
            for ut in utak:
                if ut[2] == dobas:
                    celok.append((ut[0],ut[1]))
                elif ((ut[0],ut[1]) in self.kikotok) and ut[2] < dobas:
                    celok.append((ut[0],ut[1]))
        if (mostanioszlop,mostanisor) in celok: # Ha kiindulómező cél lenne, töröljük.
            celok.remove((mostanioszlop,mostanisor))
        if (mostanioszlop,mostanisor) in self.kikotok and szellel: # Ha kikötőből indulunk, visszatesszük / hozzáadjuk.
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
        szeliranyszotar = {"e":   self.szelirany[0],
                           "ek":  self.szelirany[1],
                           "k":   self.szelirany[2],
                           "dk":  self.szelirany[3],
                           "d":   self.szelirany[4],
                           "dny": self.szelirany[5],
                           "ny":  self.szelirany[6],
                           "eny": self.szelirany[7],
                           "x":   0}
        return szeliranyszotar[irany]
        
    def szel_megjelenit(self):
        "Megjeleníti a szélirányt jelző mutatót."
        mutatoirany = str(self.szelirany.index(0))
        self.board_canvas.delete(self.szelmutato)
        self.szelmutato = self.board_canvas.create_image(int(6.5 * self.tile_size), int(2.5 * self.tile_size), image = self.gallery['szelirany' + mutatoirany], anchor = CENTER)
        
    def szel_valtoztat(self, szog = 0):
        "Megváltoztatja a szél irányát."
        ujszeliranyindex = (self.szelirany.index(0) + int(szog/45))%8
        self.change_wind_direction(ujszeliranyindex)
        self.szel_megjelenit()
    
    def celkereso(self, tiles):
        "Megmutatja a játékosnak azokat a négyzeteket, ahová majd lépni lehet."
        self.xlista = []
        for mezox,mezoy in tiles:
            self.xlista.append(self.board_canvas.create_image((mezox - 0.5) * self.tile_size, (mezoy - 0.5) * self.tile_size, image = self.gallery['x'], anchor = CENTER))
            self.xlatszik.set(True)
        self.villogasaktiv = 1
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
        self.master.game_board.villogasaktiv = 0
        if self.xlatszik.get():
            for x in self.xlista:
                self.board_canvas.itemconfigure(x, state='hidden')
            self.xlatszik.set(False)
            self.xlista = []
            
    def hajotathelyez(self, celx, cely):
        "Végrehajtja a kijelölt lépést."
        self.board_canvas.coords(self.figuraszotar[self.master.engine.aktivjatekos.nev], (celx - 0.5) * self.tile_size, (cely - 0.5) * self.tile_size)
        self.master.engine.aktivjatekos.pozicio = (celx, cely)
        
class Mutatrejt():
    """A villogást irányító osztály."""
    def __init__(self, parent):
        self.boss = parent
    def start(self):
        while self.boss.villogasaktiv == 1:
            self.fut()
            self.boss.boss.update()
            sleep(0.25)
        if self.boss.villogasaktiv == -1:
            return
        #elif self.boss.xlatszik.get():
        #    for x in self.boss.xlista:
        #        self.boss.board_canvas.itemconfigure(x,state='hidden')
        #    self.boss.xlatszik.set(False)
        #self.boss.xlista = []
    
    def fut(self):
        if self.boss.xlatszik.get():
            for x in self.boss.xlista:
                self.boss.board_canvas.itemconfigure(x,state='hidden')
            self.boss.xlatszik.set(False)
        else:
            for x in self.boss.xlista:
                self.boss.board_canvas.itemconfigure(x,state='normal')
            self.boss.xlatszik.set(True)
    
    def start0(self):
        if self.boss.xlatszik.get():
            for x in self.boss.xlista:
                self.boss.board_canvas.itemconfigure(x,state='hidden')
            self.boss.xlatszik.set(False)
            self.boss.boss.update()
            if self.boss.villogasaktiv != 1:
                self.boss.xlista = []
                return
        else:
            if self.boss.villogasaktiv != 1:
                self.boss.xlista = []
                return
            for x in self.boss.xlista:
                self.boss.board_canvas.itemconfigure(x,state='normal')
            self.boss.xlatszik.set(True)
            self.boss.boss.update()
        sleep(0.25)
        self.start()
            
class Mezo():
    """Egy játékmező logikai megjelenése."""
    def __init__(self, boss, koordinatlista, mezotipus):
        self.boss = boss
        self.koordinatlista = koordinatlista
        self.mezotipus = mezotipus
        self.lekepez()
        
    def lekepez(self):
        for x,y in self.koordinatlista:
            self.boss.board_canvas.create_image(int((x-0.5)*self.boss.tile_size),int((y-0.5)*self.boss.tile_size), image = self.boss.gallery[self.mezotipus], anchor = CENTER)
