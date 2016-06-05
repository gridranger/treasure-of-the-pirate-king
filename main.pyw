from tabla import *
from naplo import *
from game import *
from adatgazda import *
from tkinter import DISABLED, NORMAL, StringVar, Tk, ttk
from tkinter.messagebox import askokcancel
from tkinter.ttk import Notebook,LabelFrame,Combobox,Separator
import tkinter.colorchooser as tkColorChooser
from PIL.ImageTk import PhotoImage
from colorize import *
from time import sleep
from gc import get_count

class Alkalmazas(Tk):
    """A játék grafikus felülete."""
    def __init__(self, debugmode = 0):
        Tk.__init__(self)
        self.debugmode = debugmode
        self.adatolvaso = Adatolvaso(self)
        self.config_olvasas()
        self.szotar2 = self.szovegezov2(False)
        self.adatgazda = Adatgazda()
        # Panelek megjelenítése
        self.jatekinditasFolyamatban = IntVar()
        self.jatekinditasFolyamatban.set(0)
        self.jatekFolyamatban = IntVar()
        self.jatekFolyamatban.set(0)
        self.jatekforduloFolyamatban = IntVar()
        self.jatekforduloFolyamatban.set(1)
        self.korfolyamatban = 0
        self.panelek()
        self.jatekFolyamatban.trace('w',self.jatekFolyamatbanValtozasa)
        self.jatekforduloFolyamatban.trace('w',self.jatekforduloFolyamatbanValtozasa)
        # Alapszótár
        self.birodalomszotar = dict([('angol',   Birodalom('angol',   'portroyal',  '', (0,0))),
                                     ('francia', Birodalom('francia', 'martinique', '', (0,0))),
                                     ('holland', Birodalom('holland', 'curacao',    '', (0,0))),
                                     ('spanyol', Birodalom('spanyol', 'havanna',    '', (0,0))),
                                     ('kaloz',   Birodalom('kaloz',   'tortuga',    '', (0,0)))])
        # Feliratok előkészítése
        self.szovegezo()
        self.protocol("WM_DELETE_WINDOW", self.shutdown_ttk_repeat)
        self.kilepesFolyamatban = False

    def config_olvasas(self):
        "A config file beolvasása."
        self.nyelv,self.width,self.height,fullscreen,self.felbontaskod,self.felbontaslista = self.adatolvaso.beallitasok_betoltese()
        self.keparany = self.felbontaskod[:4]
        self.screen = IntVar()
        self.screen.set(fullscreen)
        self.minsize(self.width,self.height) # átméretezhetetlenné tesszük
        self.maxsize(self.width,self.height) # átméretezhetetlenné tesszük
        if self.screen.get():
            self.overrideredirect(1)
            self.geometry("%dx%d+0+0" % (self.width, self.height))
        else:
            self.overrideredirect(0)
            self.geometry("%dx%d+%d+%d" % (self.width, self.height, 100, 100))
        
    def panelek(self):
        "Betölti a paneleket"
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        menuszelesseg = int(self.height*0.33-10)
        self.naplo = Naplo(self, menuszelesseg)
        self.naplo.grid(row = 1, column = 0, sticky = S+W, padx = 5, pady = 5)
        self.tablaszelesseg = self.height-10
        if self.jatekFolyamatban.get():
            self.tabla = Tabla(self,self.tablaszelesseg) # játéktér inicializálása
            self.tabla.lekepez()
            self.tabla.grid(row = 0, column = 1, rowspan = 2, sticky = N+W, padx = 5, pady = 5)
        else:
            self.tabla = Frame(self, width = self.tablaszelesseg, height = self.tablaszelesseg)
            self.tabla.grid(row = 0, column = 1, rowspan = 2, sticky = N+W, padx = 5, pady = 5)
        self.menu = Fulek(self,menuszelesseg)   # oldalsó menü inicializálása
        self.menu.grid(row = 0, column = 0, sticky = N+W, padx = 5, pady = 5)
        if self.keparany == 'wide':             # ha kell, akkor a hajópanelt is meghívjuk
            hajoszelesseg = self.width-menuszelesseg-self.tablaszelesseg-30
            self.ship = Frame(self,width=hajoszelesseg) # helyőrző
            self.ship.grid(row = 0, column = 2, rowspan = 2, sticky = W+N+E, padx = 5, pady = 5)
    
    def szovegezov2(self, valtozokFeltoltve = True):
        "Kiváltja a szovegezo függvény egy részét, karbantartja a felület nyelvi elemeit."
        szotar = self.adatolvaso.szotar_betoltese(self.nyelv, tipus = 'textvariable')
        if valtozokFeltoltve:
            for szo in szotar.keys():
                self.szotar2[szo].set(szotar[szo])
        else:
            szotar2 = {}
            for szo in szotar.keys():
                szotar2[szo] = StringVar()
                szotar2[szo].set(szotar[szo])
            return szotar2
    
    def szovegezo(self):
        "Újragenerálja a felület állandó szövegelemeit."
        self.szovegezov2()
        self.szotar = self.adatolvaso.szotar_betoltese(self.nyelv, tipus = 'text')
        self.title(self.szotar['cim'])
        self.menu.tab(0, text=self.szotar['fomenu'])
        self.menu.tab(1, text=self.szotar['jatek'])
        self.menu.tab(2, text=self.szotar['beallitasok'])
        #self.menu.felbontasmezo.config(text=self.szotar['felbontas'])
        #self.menu.nyelvMezo.config(text=self.szotar['nyelv'])
        #self.menu.felbontasvalto.config(text=self.szotar['alkalmaz'])
        #self.menu.teljeskepernyo.config(text=self.szotar['teljeskepernyo'])
        #self.menu.ujjatekgomb.config(text=self.szotar['ujjatek'])
        #self.menu.betoltgomb.config(text=self.szotar['betolt'])
        #self.menu.mentgomb.config(text=self.szotar['ment'])
        #self.menu.mentEsKilepgomb.config(text=self.szotar['mentEsKilep'])
        #self.menu.kilepgomb.config(text=self.szotar['kilep'])
        if self.jatekinditasFolyamatban.get():
            valasztottZaszlok = []
            for i in range(6):
                if self.tabla.jatekosopciok[i].zaszlovalaszto.get() != '':
                    valasztottZaszlok.append(self.zaszloszotar[self.tabla.jatekosopciok[i].zaszlovalaszto.get()])
                else:
                    valasztottZaszlok.append(0)
        for rowid,row in self.birodalomszotar.items():
            row.set_nev(self.szotar[row.birodalom])
        #------------------------------------------------#
        # Nézetek a birodalomDB létrehozásakor már létezett szótárak helyettesítésére.
        self.zaszloszotar2 = {row.birodalom:row.varos for (rowid,row) in self.birodalomszotar.items()}
        self.zaszloszotar2R = {row.varos:row.birodalom for (rowid,row) in self.birodalomszotar.items()}
        self.varosszotar = {row.varos:row.nev for (rowid,row) in self.birodalomszotar.items()}
        self.zaszloszotar = {row.nev:row.varos for (rowid,row) in self.birodalomszotar.items()}
        #------------------------------------------------#
        if self.jatekinditasFolyamatban.get():
            for i in range(6):
                #self.tabla.jatekosopciok[i].nevfelirat.config(text=self.szotar['nevfelirat'])
                #self.tabla.jatekosopciok[i].szinfelirat.config(text=self.szotar['szinfelirat'])
                #self.tabla.jatekosopciok[i].zaszlofelirat.config(text=self.szotar['zaszlofelirat'])
                self.tabla.jatekosopciok[i].zaszlok = list(self.zaszloszotar.keys())
                self.tabla.jatekosopciok[i].zaszlovalaszto.config(value=self.tabla.jatekosopciok[i].zaszlok)
                if valasztottZaszlok[i] != 0:
                    self.tabla.jatekosopciok[i].zaszlovalaszto.set(self.varosszotar[valasztottZaszlok[i]])
                #self.tabla.startgomb.config(text=self.szotar['startgomb'])
        if self.jatekFolyamatban.get():
            self.menu.ful1feltolt()
            
    def birodalomszotar_query(self, keresettMezo, ismertMezo, ismertMezoErteke):
        "Lekérdez egy értéket a birodalomszótárból. Pontosan egy értéket ad válaszul."
        for rowid,rekord in self.birodalomszotar.items():
            a = rekord.select(keresettMezo, ismertMezo, ismertMezoErteke)
            if a:
                return a

    def nyelvvaltas(self, ujnyelv):
        "Beállítja az új nyelvet."
        if self.nyelv == ujnyelv:
            return
        self.nyelv = ujnyelv # beállítja az új nyelvet
        self.szovegezo() # megjeleníti a kiválasztott nyelven a felület elemeit
        self.kartyaszotar = self.adatolvaso.kartyak_betoltese("text") # cseréli az esemény- és kincskártyák szövegét
        self.naplo.ir(self.szotar['ujnyelv'])
        mentesSikeres = self.adatolvaso.beallitasok_irasa(ujnyelv = ujnyelv)
        
    def meretez(self, ujfelbontas, ujteljeskepernyo):
        "Újraméretezi az ablakot."
        if (self.width,self.height) == (ujfelbontas[0],ujfelbontas[1]) and self.screen.get() == ujteljeskepernyo:
            return
        configMentesSikeres = self.adatolvaso.beallitasok_irasa(ujfelbontas[2],str(ujteljeskepernyo))
        jatekosadatok = []
        if self.jatekinditasFolyamatban.get():
            for i in range(6):
                if self.tabla.jatekosopciok[i].aktiv.get():
                    jatekosadatok.append([self.tabla.jatekosopciok[i].nev.get(), self.tabla.jatekosopciok[i].valasztottSzin.get(), self.tabla.jatekosopciok[i].zaszlovalaszto.get()])
                else:
                    pass
        self.config_olvasas()
        self.torolMindent()
        self.panelek()
        if self.jatekinditasFolyamatban.get():
            self.jatekBeallit(0)
            if len(jatekosadatok) > 0:
                for i in range(len(jatekosadatok)): 
                    self.tabla.jatekosopciok[i].visszatolt(jatekosadatok[i][0],jatekosadatok[i][1],jatekosadatok[i][2])
        self.szovegezo()
        self.menu.select(self.menu.lap2)
        self.naplo.ir('%s %i×%i' % (self.szotar['ujmeret'], self.width, self.height))

    def torolMindent(self):
        "Törli a létrehozott paneleket."
        self.menu.destroy()
        self.tabla.destroy()
        self.naplo.destroy()
        try:
            self.ship.destroy()
        except:
            pass           
    
    def jatekBeallit(self, turnoff = 1):
        "Bekéri a játékosok adatait egy panel megjelenítésével. Kikapcsoláshoz újra meg kell hívni, újrageneráláshoz 0 paraméterrel hívandó."
        if self.jatekFolyamatban.get() and not askokcancel(self.szotar2['ujjatek'].get(), self.szotar['jatekfelbeszakitas']):
            return
        else:
            self.jatekFolyamatban.set(0)
        if self.jatekinditasFolyamatban.get() and turnoff: # Új kattintásra a gomb visszaáll alapheyzetbe, és töri a bevitt adatokat.s
            self.jatekinditasFolyamatban.set(0)
            self.tabla.destroy()
            self.tabla = Frame(self, width = self.tablaszelesseg, height = self.tablaszelesseg)
            self.tabla.grid(row = 0, column = 1, rowspan = 2, sticky = N+W, padx = 5, pady = 5)
            self.menu.ujjatekgomb.config(overrelief = RAISED, relief = FLAT)
            return
        self.jatekinditasFolyamatban.set(1)
        self.menu.ujjatekgomb.config(relief = SUNKEN, overrelief = SUNKEN)
        self.tabla.destroy()
        self.tabla = Frame(self, width = self.tablaszelesseg, height = self.tablaszelesseg)
        self.tabla.grid(row = 0, column = 1, rowspan = 2, sticky = N+W, padx = 5, pady = 5)
        self.tabla = UjJatekAdatok(self, self.tablaszelesseg)
        self.tabla.columnconfigure('all', weight=1)
        self.tabla.rowconfigure('all', weight=1)
        self.tabla.grid(row = 0, column = 1, rowspan = 2, sticky = N+E+W+S, padx = 5, pady = 5)
        
    def jatekIndit(self, adathalmaz, uj = 1, kezd = 'player0', szelindex = 6, fogadoszotar = {}, paklik = [], hadnagyElokerult = False, grogbaroLegyozve = False):
        "Elindítja a játékot."
        if uj or self.jatekinditasFolyamatban.get():
            self.jatekinditasFolyamatban.set(0) 
        self.menu.ujjatekgomb.config(overrelief = RAISED, relief = FLAT)
        self.update_idletasks()
        self.jatekFolyamatban.set(1)
        self.jatekostar = {}
        self.tabla.destroy()
        self.tabla = Tabla(self,self.tablaszelesseg, szelindex) # játéktér inicializálása
        self.tabla.grid(row = 0, column = 1, rowspan = 2, sticky = N+W, padx = 5, pady = 5)
        self.kartyaszotar = self.adatolvaso.kartyak_betoltese("text")
        if uj:
            for adat in adathalmaz:
                kikoto = self.zaszloszotar[adat[2]]
                self.jatekostar['player'+str(adathalmaz.index(adat))] = Jatekos(self, self.tabla, adat[0], adat[1], adat[2])
        else:
            for adat in adathalmaz:
                self.jatekostar[adat] = Jatekos(self, self.tabla, adathalmaz[adat][0], adathalmaz[adat][1],
                                                adathalmaz[adat][2], adathalmaz[adat][3], adathalmaz[adat][4],
                                                adathalmaz[adat][5], adathalmaz[adat][6], adathalmaz[adat][7],
                                                adathalmaz[adat][8], adathalmaz[adat][9], adathalmaz[adat][10],
                                                adathalmaz[adat][11])
        self.jatekossor = sorted(self.jatekostar.keys())
        self.tabla.lekepez()
        self.menu.select(self.menu.lap1)
        while self.jatekossor[0] != kezd:                   # amíg nem a megfelelő játékos következik
            self.jatekossor.append(self.jatekossor.pop(0))  # a legelső játékost leghátra tesszük
        for jatekos in self.jatekostar.keys():
            self.jatekostar[jatekos].set_birodalom()
        self.jatekmenet = Vezerlo(self,self.jatekossor[0],fogadoszotar)
        if hadnagyElokerult:
            self.jatekmenet.set_hadnagyElokerult()
        if grogbaroLegyozve:
            self.jatekmenet.set_set_grogbaroLegyozve()
        self.menu.ful3_var()
        if not uj:
            self.jatekmenet.set_paklik(paklik)
            self.naplo.ir(self.szotar["jatekbetoltes_kesz"])
        else:
            self.naplo.ir(self.szotar["jatekinditas_kesz"])
        self.jatekmenet.szakasz_0()
    
    def jatekFolyamatbanValtozasa(self, a = None, b = None, c = None):
        "A figyelt változónak megfelelően engedélyezi vagy letiltja a Játék fület."
        if self.jatekFolyamatban.get():
            self.menu.tab(1, state = NORMAL)
        else:
            self.menu.tab(1, state = DISABLED)
            
    def set_jatekforduloFolyamatban(self, ertek = 1):
        "Lehetővé teszi a változó manipulálását kívülről"
        self.jatekforduloFolyamatban.set(ertek)
        #if ertek == 1:
        #    print(str(self.jatekmenet.get_korokSzama())+". kör eleje.")
        #if ertek == 0:
        #    print(str(self.jatekmenet.korokSzama)+". kör vége.")
            
    def jatekforduloFolyamatbanValtozasa(self, a = None, b = None, c = None):
        "Ki és be kapcsolja azokat a funkciókat, amelyeket egy körön belül nem használhatnak a játékosok."
        if not self.jatekforduloFolyamatban.get():
            self.menu.mentgomb.config(state = NORMAL)
            self.menu.mentEsKilepgomb.config(state = NORMAL)
            self.menu.tab(0, state = NORMAL)
            self.menu.tab(2, state = NORMAL)
        else:
            self.menu.mentgomb.config(state = DISABLED)
            self.menu.mentEsKilepgomb.config(state = DISABLED)
            self.menu.tab(0, state = DISABLED)
            self.menu.tab(2, state = DISABLED)
            
    def shutdown_ttk_repeat(self):
        'Javítja a ttk modul egy hibáját, és leállítja a gyermekszálakat.'
        self.eval('::ttk::CancelRepeat')
        self.kilepesFolyamatban = True
        self.menu.kilep()
        
    def helymeghatarozas(self):
        'Visszaadja saját jelenlegi pozícióját.'
        info = self.winfo_geometry()
        xpos = info.index('+')+1
        ypos = info[(xpos):].index('+')+xpos
        x = int(info[(xpos):(ypos)])
        y = int(info[(ypos):])
        return (x,y)
    
class Fulek(Notebook):
    def __init__(self,boss=None,width=0):
        ttk.Notebook.__init__(self,master=boss,width=width)
        self.boss = boss
        self.width = width
        self.fold_fold_dobas = False
        # Leképezzük a füleket
        self.lap0 = Frame(self)
        self.lap1 = Frame(self)
        self.lap2 = Frame(self)
        self.lap3 = Frame(self)
        for lap in (self.lap0,self.lap1,self.lap2,self.lap3):
            lap.columnconfigure(0, weight=1)
            lap.grid(row=0, column=0)
            self.add(lap, text='', underline=0, sticky=N+E+W) # ezzek rögzítjük a lapkat a notebookba
        self.enable_traversal() # engedélyezzük a gyorsbillentyűket
        self.grid(row=0, column=0)
        # Betöltjük a füleket
        self.ful0()
        self.ful1()
        self.ful2()
        self.ful3()
    
    def ful0(self):
        "A főmenü elemeinek betöltése."
        keret = Frame(self.lap0)
        keret.grid(row = 0, column = 0, pady = 10)
        self.ujjatekgomb = Button(keret, textvariable=self.boss.szotar2['ujjatek'], command=self.ujjatek, width = 20, overrelief = RAISED, relief = FLAT)
        self.ujjatekgomb.grid(row = 0, column = 0)
        self.betoltgomb = Button(keret, textvariable=self.boss.szotar2['betolt'], command=self.betolt, width = 20, overrelief = RAISED, relief = FLAT)
        self.betoltgomb.grid(row = 1, column = 0)
        self.mentgomb = Button(keret, textvariable=self.boss.szotar2['ment'], command=self.ment, width = 20, overrelief = RAISED, relief = FLAT, state = DISABLED)
        self.mentgomb.grid(row = 2, column = 0)
        self.mentEsKilepgomb = Button(keret, textvariable=self.boss.szotar2['mentEsKilep'], command=self.mentEsKilep, width = 20, overrelief = RAISED, relief = FLAT, state = DISABLED)
        self.mentEsKilepgomb.grid(row = 3, column = 0)
        self.kilepgomb = Button(keret, textvariable=self.boss.szotar2['kilep'], command=self.kilep, width = 20, overrelief = RAISED, relief = FLAT)
        self.kilepgomb.grid(row = 4, column = 0)

    def ful1(self):
        "A játék menü elemeinek betöltése."
        self.ful1tartalom = Frame()
        if self.boss.jatekFolyamatban.get():
            self.ful1feltolt()
        else:
            self.tab(1, state = DISABLED)
       
    def ful2(self):
        self.felbontasmezo = LabelFrame(self.lap2, text='')
        self.nyelvMezo = LabelFrame(self.lap2, text='')
        self.newscreen = IntVar()
        self.newscreen.set(self.boss.screen.get())
        sorszam = 0
        for mezo in (self.felbontasmezo,self.nyelvMezo):
            mezo.columnconfigure(0, weight=1)
            mezo.grid(row=sorszam, column=0, sticky = E+W, padx = 5 , pady = 5)
            sorszam +=1
        # Felbontás
        self.felbontaslista = sorted(self.boss.felbontaslista) # rendezzük a listát arra az esetre, ha felhasználó beleírt volna egy új értéket
        self.felbontasskala = Scale(self.felbontasmezo, from_ = 0, to = len(self.felbontaslista)-1,
                                    orient = HORIZONTAL, resolution = 1,
                                    takefocus = 0, showvalue = 0,
                                    length = self.width, command = self.felbontassav)
        self.felbontasskala.set(self.felbontaslista.index([item for item in self.felbontaslista if item[2] == self.boss.felbontaskod][0]))
        self.felbontasskala.grid(row=0, column=0, columnspan = 2, sticky = E+W)
        self.felbontaskijelzo = Label(self.felbontasmezo, text=(self.boss.width,'×',self.boss.height))
        self.felbontaskijelzo.grid(row=1, column=0, padx = 5, pady = 5, sticky = W)
        self.felbontasvalto = Button(self.felbontasmezo, textvariable=self.boss.szotar2['alkalmaz'], command= lambda : self.boss.meretez(self.felbontaslista[self.felbontasskala.get()], self.newscreen.get()), state = DISABLED)
        self.felbontasvalto.grid(row=1, column=1, padx = 5, pady = 5, sticky = E)
        self.teljeskepernyo = Label(self.felbontasmezo, textvariable=self.boss.szotar2['teljeskepernyo'])
        self.teljeskepernyo.grid(row=2, column=0, padx = 5, pady = 5, sticky = W)
        self.teljeskepernyoPipa = Checkbutton(self.felbontasmezo, takefocus = 0, variable=self.newscreen, command = lambda : self.felbontasvalto.config(state = NORMAL))
        self.teljeskepernyoPipa.grid(row=2, column=1, padx = 5, pady = 5, sticky = E)
        # Nyelv
        self.nyelvmodul()

    def ful3(self):
        if not self.boss.debugmode:
            self.hide(3)
        self.tab(3, text='D')
        gombsor = Frame(self.lap3)
        Button(gombsor, text = 'Kincskártya húzása', command = lambda : self.boss.jatekmenet.kincsetHuz()).grid()
        gombsor.grid(row = 0)
        aranybeallit = Frame(self.lap3)
        Label(aranybeallit, text = 'Arany növelése:').grid(column = 0, row = 0)
        aranyMezo = Entry(aranybeallit, width = 3)
        aranyMezo.grid(column = 1, row = 0)
        Button(aranybeallit, text = 'Beállít', command = lambda : self.boss.jatekmenet.aktivjatekos.set_kincs(int(aranyMezo.get()))).grid(column = 2, row = 0)
        aranybeallit.grid(row = 1)
        
    def ful3_var(self):
        valtozok = Frame(self.lap3)
        Label(valtozok, text = 'hadnagyElokerult:').grid(column = 0, row = 0)            
        Label(valtozok, text = 'grogbaroLegyozve:').grid(column = 0, row = 1)
        Label(valtozok, textvar = self.boss.jatekmenet.hadnagyElokerult).grid(column = 1, row = 0)
        Label(valtozok, textvar = self.boss.jatekmenet.grogbaroLegyozve).grid(column = 1, row = 1)
        valtozok.grid(row = 2)
        
    def ful1feltolt(self, aktivjatekos=None):
        self.ful1tartalom.destroy()
        self.ful1tartalom = JatekFul(self, self.lap1)
        self.ful1tartalom.grid(pady = 5)
        
    def dobas(self, event):
        "Dob a kockával."
        if self.fold_fold_dobas:
            self.boss.tabla.villogaski()
            self.boss.jatekmenet.dobasMegtortent.set(False)
        if not self.boss.jatekmenet.dobasMegtortent.get():
            dobas = self.ful1tartalom.kocka.dob()
            if "fold_fold" in self.boss.jatekmenet.aktivjatekos.statuszlista:
                print("Újra dobhatna.")
                self.boss.naplo.ir(self.boss.szotar['foldfold_naplo'])
                self.boss.jatekmenet.aktivjatekos.set_statusz("fold_fold", 0)
                self.fold_fold_dobas = True
            else:
                self.boss.naplo.ir('')
                self.ful1tartalom.kockamezo.config(relief = SUNKEN)
            self.boss.jatekmenet.set_dobasMegtortent()
            self.boss.set_jatekforduloFolyamatban(1)
            self.boss.jatekmenet.aktivjatekos.set_utolsodobas(dobas)
            self.boss.jatekmenet.mozgas(dobas, 1)
            
    def fold_fold_dobas_null(self):
        "Amennyiben elfogadta az első dobást, itt kerül kikapcsolásra az isméltlés lehetősége."
        self.fold_fold_dobas = False
    
    def felbontassav(self,ertek):
        "A felbontáscsúszka betöltése"
        self.felbontaskijelzo.config(text=(str(self.felbontaslista[int(ertek)][0]),'×',str(self.felbontaslista[int(ertek)][1])))
        if (self.boss.width,self.boss.height) == (self.felbontaslista[int(ertek)][0],self.felbontaslista[int(ertek)][1]):
            self.felbontasvalto.config(state = DISABLED)
        else:
            self.felbontasvalto.config(state = NORMAL)
        
    def nyelvmodul(self):
        "Leképezi a nyelvi modult"
        self.nyelvlista,self.nyelvlistaR = self.boss.adatolvaso.szotar_betoltese(listaz = True)
        self.nyelvvalaszto = Combobox(self.nyelvMezo, value=sorted(list(self.nyelvlista)), takefocus=0)
        self.nyelvvalaszto.set(self.nyelvlistaR[self.boss.nyelv])
        self.nyelvvalaszto.bind("<<ComboboxSelected>>", self.ujnyelv)
        self.nyelvvalaszto.grid(row=0, column=0, padx = 5, pady = 5)

    def ujnyelv(self,event):
        "Meghívja főfolyamat nyelvváltó eseményét."
        ujnyelv = self.nyelvlista[self.nyelvvalaszto.get()] # kinyerjük a választott nyelvet
        self.boss.nyelvvaltas(ujnyelv)
    
    def ujjatek(self):
        "Új játékot kezd"
        self.boss.jatekBeallit()
    
    def ment(self):
        "Kimenti az aktuális adatokat"
        soronkovetkezoJatekos = self.boss.jatekossor[0]
        szelindex = self.boss.tabla.szelirany.index(0)
        fogadoszotar = {}
        exportszotar = {}
        for jatekos in sorted(list(self.boss.jatekostar.keys())):
            exportszotar[jatekos] = self.boss.jatekostar[jatekos].export()
            exportszotar[jatekos][2] = self.boss.tabla.kikototarR[exportszotar[jatekos][2]]
        for fogado in self.boss.tabla.kikotolista:
            fogadoszotar[fogado] = self.boss.jatekmenet.varostar[fogado].export_matroz()
        esemenypakli = self.boss.jatekmenet.esemenypakli
        esemenytalon = self.boss.jatekmenet.esemenytalon
        kincspakli = self.boss.jatekmenet.kincspakli
        kincstalon = self.boss.jatekmenet.kincstalon
        kartyak = [esemenypakli, esemenytalon, kincspakli, kincstalon]
        mentesSikerult = self.boss.adatgazda.set_adatok_fileba(exportszotar, soronkovetkezoJatekos, szelindex, fogadoszotar, kartyak)
        return mentesSikerult
           
    def betolt(self):
        "Betölt egy mentett állást."
        if self.boss.jatekFolyamatban.get():
            if not askokcancel(self.boss.szotar2['ujjatek'].get(), self.boss.szotar['jatekfelbeszakitas-b']):
                return
            else:
                # Memóriafelszabadítás
                print("GC_COUNT =",get_count())
                # Eddig tartott a memória felszabadítása
        adatok = self.boss.adatgazda.get_adatok_filebol()
        if not adatok:
            return
        helyzetszotar, kovetkezoJatekos, szelindex, fogadoszotar, paklik = adatok
        self.boss.naplo.ir(self.boss.szotar['jatekbetoltes'])
        self.update_idletasks()
        self.boss.jatekIndit(helyzetszotar, 0, kovetkezoJatekos, szelindex, fogadoszotar, paklik)
        
    def kilep(self):
        "Kilép a játékból."
        if self.boss.jatekFolyamatban.get():
            if self.boss.tabla.villogasaktiv:
                self.boss.tabla.villogasaktiv = -1
        self.boss.destroy()

    def mentEsKilep(self):
        "Menti a játékot, és kilép."
        mentesSikerult = self.ment()
        if mentesSikerult:
            self.boss.shutdown_ttk_repeat()        

class JatekFul(Frame):
    """A játékos menü osztálya."""
    def __init__(self, boss, notepad):
        Frame.__init__(self, notepad)
        self.boss = boss
        self.master = self.boss.boss
        self.aktivjatekos = None
        if self.master.jatekFolyamatban.get():
            self.aktivjatekos = self.master.jatekmenet.aktivjatekos
            self.feltolt()
        else:
            self.boss.tab(1, state = DISABLED)
            self.fejlec = Frame()
            self.kincseslada = Frame(self)
            self.kockamezo = Frame(self)
            self.pontmezo = Frame(self)
            self.jateksor = Frame(self)
            
    def feltolt(self):
        "Megjeleníti a fül tényleges tartalmát."
        self.fejlec_epito(0)
        self.kincseslada_epito(1)
        #self.vonal(2)
        self.pontszamok_epito(2)
        self.statusz_epito(3)
        self.vonal(4)
        self.kockamezo_epito(5)
        self.vonal(6)
        self.sorrend_epito(7)
        
    def fejlec_epito(self, pozicio):
        "A fejléc."
        self.fejlec = Frame(self)
        Label(self.fejlec, text = self.aktivjatekos.nev).grid(row = 0, column = 0)
        Label(self.fejlec, image = self.master.tabla.keptar['zaszlo_'+self.aktivjatekos.birodalom]).grid(row = 1, column = 0)
        self.fejlec.grid(row = pozicio, column = 0, pady = 5)
        
    def kincseslada_epito(self, pozicio):
        "Pénz- és legénységkijelző."
        self.kincseslada = Frame(self)
        rekesz0 = LabelFrame(self.kincseslada, text = self.master.szotar['kincs'])
        Label(rekesz0, image = self.master.tabla.keptar['penz-d2']).grid(row = 0, column = 0)
        Label(rekesz0, textvariable = self.aktivjatekos.kincs).grid(row = 0, column = 1)
        rekesz0.grid(row = 0, column = 0, sticky = N+E+W+S, padx = 5)
        rekesz1 = LabelFrame(self.kincseslada, text = self.master.szotar['legenyseg'])
        Label(rekesz1, image = self.master.tabla.keptar['matrozok']).grid(row = 0, column = 0)
        Label(rekesz1, textvariable = self.aktivjatekos.legenyseg).grid(row = 0, column = 1)
        rekesz1.grid(row = 0, column = 1, sticky = N+E+W+S, padx = 5)
        self.kincseslada.grid(row = pozicio, column = 0)
        self.kincseslada.columnconfigure(ALL, minsize = (self.boss.width-20)/2)
        
    def vonal(self, pozicio):
        "Vonal."
        Separator(self, orient = HORIZONTAL).grid(row = pozicio, column = 0, sticky = E+W, padx = 5, pady = 5)
    
    def pontszamok_epito(self, pozicio):
        "Pontozótábla."
        pontmezo = LabelFrame(self, text = self.master.szotar['pontszamok'])
        ponthelyszamlalo = 0
        pontkeretszotar = {}
        for birodalom in sorted(self.master.birodalomszotar.keys()):
            if birodalom != self.aktivjatekos.birodalom:
                pontkeretszotar[birodalom] = Frame(pontmezo)
                Label(pontkeretszotar[birodalom], image = self.master.tabla.keptar['zaszlo_'+birodalom]).grid(row = 0, column = 0)
                Label(pontkeretszotar[birodalom], text = ':').grid(row = 0, column = 1)
                Label(pontkeretszotar[birodalom], textvariable = self.aktivjatekos.hajotar[birodalom]).grid(row = 0, column = 2)
                pontkeretszotar[birodalom].grid(row = int((ponthelyszamlalo/2)%2), column = ponthelyszamlalo%2, sticky = E+W)
                ponthelyszamlalo += 1
        pontmezo.grid(row = pozicio, column = 0)
        pontmezo.columnconfigure(ALL, minsize = (self.boss.width-34)/2)
        
    def kockamezo_epito(self,pozicio):
        "A dobókocka megjelenítőfelülete."
        self.kockamezo = Frame(self)
        self.kockamezo.columnconfigure(0, weight=1)
        self.kockamezo.rowconfigure(0, weight=1)
        self.kockamezo.grid(row = pozicio, column = 0, ipady = 5, ipadx = 5)
        kimaradas = self.aktivjatekos.kimarad.get()
        if kimaradas > 0:
            if kimaradas > 1:
                uzenet = self.master.szotar["kimaradok"] % kimaradas
            else:
                uzenet = self.master.szotar["kimaradok_utoljara"]
            Button(self.kockamezo, text = uzenet, command = self.master.jatekmenet.kimaradas).pack()
            if "leviatan" in self.master.jatekmenet.aktivjatekos.statuszlista:
                Button(self.kockamezo, text = self.master.szotar["leviatan_kijatszasa"], command = self.master.jatekmenet.leviatan_kijatszasa).pack()
        else:
            self.kockamezo.config(relief = RAISED, bd = 2)
            self.kocka = Dobokocka(self.kockamezo, self.boss.width/4, self.aktivjatekos.szin, self.aktivjatekos.masodikszin, self.aktivjatekos.utolsodobas)
            if self.master.jatekmenet.aktivjatekos.pozicio in self.master.tabla.helyszotar["szamuzottek"] and not self.master.jatekmenet.aktivjatekos.legenyseg.get():
                self.kocka.bind('<Button-1>', self.master.jatekmenet.szamuzottek)
            else:
                self.kocka.bind('<Button-1>', self.boss.dobas)
            self.kocka.grid(row = 0, column = 0)
    
    def sorrend_epito(self, pozicio):
        "A sorrend megjelenítője."
        self.jateksor = Frame(self)
        self.jateksorszotar = {}
        sor = self.master.jatekossor
        self.jateksorCimke = Label(self.jateksor, text = self.master.szotar['jateksorCimke'])
        self.jateksorCimke.grid(row = 0, column = 0, sticky = W)
        for sorszam in range(len(self.master.jatekossor)):
            self.jateksorszotar['label'+str(sorszam)] = Label(self.jateksor, text = str(sorszam+1) + '. ' + self.master.jatekostar[sor[sorszam]].nev, bg = self.master.jatekostar[sor[sorszam]].szin, fg = self.master.jatekostar[sor[sorszam]].masodikszin)
            self.jateksorszotar['label'+str(sorszam)].grid(row = sorszam+1, column = 0, sticky = W, padx = 10)
        self.jateksor.grid(row = pozicio, column = 0, sticky = W, padx = 5)
        
    def statusz_epito(self,pozicio):
        "A játékos státuszainak megjelenítője."
        statuszmezo = LabelFrame(self, text = self.master.szotar['kartyak'], relief = RAISED, width = self.boss.width - 31)
        maxStatuszEgySorban = int((self.boss.width - 31) / 32)
        if len(self.master.jatekmenet.aktivjatekos.statuszlista):
            i = 0
            for statusz in self.master.jatekmenet.aktivjatekos.statuszlista:
                if statusz in self.master.jatekmenet.nemKartyaStatusz:
                    pass
                else:
                    if statusz in self.master.jatekmenet.esemenyszotar.keys():
                        hely = self.master.jatekmenet.esemenyszotar
                    else:
                        hely = self.master.jatekmenet.kincsszotar
                    leendoKep = self.master.jatekmenet.esemenyszotar[statusz].kep + '_i'
                    leendoKep = leendoKep[(leendoKep.find('_')+1):]
                    Button(statuszmezo, image = self.master.tabla.keptar[leendoKep], command = lambda statusz = statusz: hely[statusz].megjelenik(1)).grid(row = int(i/maxStatuszEgySorban), column = i%maxStatuszEgySorban)
                    i += 1
            statuszmezo.config(height = 24 + ((int(i/maxStatuszEgySorban) + 1) * 32))
            if statuszmezo.winfo_children():
                statuszmezo.grid(row = pozicio, column = 0)
            statuszmezo.grid_propagate(False)
    
class UjJatekos(Frame):
    """Az új játékost beállító panel."""
    def __init__(self, boss):
        Frame.__init__(self, master = boss, relief = RAISED, bd = 2)
        self.boss = boss
        self.aktiv = IntVar()
        self.aktiv.set(0)
        self.aktiv.trace('w',self.aktival)
        self.valasztottSzin = StringVar()
        self.valasztottSzin.trace('w',self.hajoepito)
        self.valasztottSzin.set('')
        self.zaszlok = list(self.boss.boss.zaszloszotar.keys())
        self.hajoepito()
        self.aktiv.trace('w',self.aktival)
        self.config(height = self.boss.meret/5, width = (self.boss.meret-(3*self.boss.meret/10))/2)
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        self.nevfelirat = Label(self, textvariable=self.boss.boss.szotar2['nevfelirat'])
        self.nevfelirat.grid(row = 0, column = 0, sticky = E)
        self.nev = Entry(self, width = 15)
        self.nev.grid(row = 0, column = 1, sticky = E)
        self.szinfelirat = Label(self, textvariable=self.boss.boss.szotar2['szinfelirat'])
        self.szinfelirat.grid(row = 1, column = 0, sticky = E)
        self.szin = Button(self, width=12, bd = 2, relief = SUNKEN, command=self.szinvalaszto)
        self.szin.grid(row = 1, column = 1)
        self.zaszlofelirat = Label(self, textvariable=self.boss.boss.szotar2['zaszlofelirat'])
        self.zaszlofelirat.grid(row = 2, column = 0, sticky = E)
        self.zaszlovalaszto = Combobox(self, value=self.zaszlok, takefocus=0, width=12, state='readonly')
        self.zaszlovalaszto.bind("<<ComboboxSelected>>", self.zaszlovalasztas)
        self.zaszlovalaszto.grid(row=2, column=1)
        for elem in [self.nev,self.szin,self.zaszlovalaszto]:
            elem.config(state = DISABLED)
        self.hajo = Label(self, image = self.boss.hajokepszurke)
        self.hajo.grid(row = 0, column = 2, rowspan = 3)
            
    def szinvalaszto(self):
        "Megnyit egy színválasztóablakot, és kiválasztja a hajó színét."
        (rgb, hex) = tkColorChooser.askcolor()
        if hex == None:
            return
        self.valasztottSzin.set(hex)
        self.szin.config(bg = self.valasztottSzin.get())
    
    def hajoepito(self,a=None,b=None,c=None):
        "Kiszínezi a hajó vitorlázatát."
        self.hajokep = open('img/szkuner-h.png')
        szelesseg,magassag = self.hajokep.size
        self.hajokep = self.hajokep.resize((int(self.boss.meret/5),int(self.boss.meret/5*magassag/szelesseg)), ANTIALIAS)
        self.vitorlakep = (image_tint('img/szkuner-v.png',self.valasztottSzin.get()).resize((int(self.boss.meret/5),int(self.boss.meret/5*magassag/szelesseg)), ANTIALIAS))
        self.hajokep.paste(self.vitorlakep, (0,0), self.vitorlakep)
        self.hajokep = PhotoImage(self.hajokep)
        self.hajo = Label(self, image = self.hajokep)
        self.hajo.grid(row = 0, column = 2, rowspan = 3)
    
    def aktival(self,a=None,b=None,c=None):
        "Hozzáadható vagy kikapcsolható vele egy játékos."
        if self.aktiv.get():
            for elem in [self.nev,self.szin,self.zaszlovalaszto]:
                elem.config(state = NORMAL)
            self.hajo.config(image = self.hajokep)
        else:
            for elem in [self.nev,self.szin,self.zaszlovalaszto]:
                elem.config(state = DISABLED)
            self.hajo.config(image = self.boss.hajokepszurke)
    
    def zaszlovalasztas(self, event):
        "A legkördülőmenüre kattintáskor végrehajtandó függvény."
        self.zaszlo=self.zaszlovalaszto.get()
        
    def visszatolt(self, nev='', szin='', zaszlo=''):
        'Fogadja a felbontásváltás után visszatöltendő adatokat.'
        if not self.aktiv.get():
            self.aktiv.set(1)
        if nev != '':
            self.nev.insert(0, nev)
        if szin != '':
            self.valasztottSzin.set(szin)
            self.szin.config(bg = self.valasztottSzin.get())
        if zaszlo != '':
            self.zaszlovalaszto.set(zaszlo)

class UjJatekAdatok(Frame):
    """Az új játék beállításai."""
    def __init__(self, boss, meret):
        Frame.__init__(self, master = boss, height = meret, width = meret)
        self.boss = boss
        self.meret = meret
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        self.jatekosopciok = {}
        self.hajokepszurke = image_tint('img/szkuner.png', '#ffffff')
        hajokepszurkew,hajokepszurkeh = self.hajokepszurke.size
        self.hajokepszurke = PhotoImage(self.hajokepszurke.resize((int(self.meret/5),int(self.meret/5*hajokepszurkeh/hajokepszurkew)), ANTIALIAS))
        for i in range(6):
            self.jatekosopciok[i] = UjJatekos(self)
            self.jatekosAktiv = Checkbutton(self, takefocus = 0, variable = self.jatekosopciok[i].aktiv)
            if i == 0:
                self.jatekosopciok[i].aktiv.set(1)
                self.jatekosAktiv.config(state = DISABLED)               
            self.jatekosAktiv.grid(row=i%6, column=0, padx = 5, pady = 5, sticky = E)
            self.jatekosopciok[i].grid(row = i%6, column = 1, sticky = W)
        self.startgomb = Button(self, textvariable=self.boss.szotar2['startgomb'], command=self.jatekosokBeallitasaKesz)
        self.startgomb.grid(row = 0, column = 2, rowspan = 6, sticky = W)
        
    def jatekosokBeallitasaKesz(self):
        "Létrehozza a játékosokat a megadott paraméterekkel, és elindítja a játékot."
        jatekosadatok = []
        for i in range(6):
            if self.jatekosopciok[i].aktiv.get():
                if self.jatekosopciok[i].nev.get() == '':
                    self.boss.naplo.ir(self.boss.szotar['nevhiany'] % (i+1))
                    return
                elif self.jatekosopciok[i].valasztottSzin.get() == '':
                    self.boss.naplo.ir(self.boss.szotar['szinhiany'] % (self.jatekosopciok[i].nev.get()))
                    return
                elif self.jatekosopciok[i].zaszlovalaszto.get() == '':
                    self.boss.naplo.ir(self.boss.szotar['zaszlohiany'] % (self.jatekosopciok[i].nev.get()))
                    return
                elif self.jatekosopciok[i].zaszlovalaszto.get() not in list(self.boss.zaszloszotar.keys()):
                    self.boss.naplo.ir(self.boss.szotar['zaszloervenytelen'] % (self.jatekosopciok[i].nev.get()))
                    return
                self.boss.naplo.ir(self.boss.szotar['jatekinditas'])
                self.update_idletasks()
                jatekosadatok.append([self.jatekosopciok[i].nev.get(), self.jatekosopciok[i].valasztottSzin.get(), self.jatekosopciok[i].zaszlovalaszto.get()])
        self.boss.jatekIndit(jatekosadatok)
        
class Birodalom():
    def __init__(self, birodalom, varos, nev, koordinatak):
        self.birodalom = birodalom
        self.varos = varos
        self.nev = nev
        self.koordinatak = koordinatak
                            
    def select(self, keresettMezo, ismertMezo, ismertMezoErteke):
        "SELECT keresettMezo FROM self WHERE ismertMezo = ismertMezoErteke"
        self.szotar = dict([('birodalom',   self.birodalom),
                            ('varos',       self.varos),
                            ('nev',         self.nev),
                            ('koordinatak', self.koordinatak)])
        if self.szotar[ismertMezo] == ismertMezoErteke:
            return self.szotar[keresettMezo]
            
    def set_nev(self, ujnev):
        "Az új nyelv választásakor társítja az adott nyelv szavát a megfelelő birodalomhoz."
        self.nev = ujnev
        
    def set_koordinatak(self, ujkoordinatak):
        "A tábla felépítésekor társítja az adott koordinátákat (tuple) a megfelelő birodalomhoz. Előre beépített kompatibilitás véletlenszerű térképekhez."
        self.koordinatak = ujkoordinatak
            
if __name__ == '__main__':
    a = Alkalmazas(1)
    a.mainloop()