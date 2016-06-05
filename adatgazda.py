from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename,asksaveasfilename,StringVar
from xml.etree.ElementTree import Element,ElementTree,fromstring,parse,SubElement

class Adatgazda():
    """Mentő és betöltő modul."""
    def __init__(self):
        self.kiterjesztes = '.savx'
        self.tipus = [('XML mentés', '.savx')]
        
    def get_adatok_filebol(self):
        "Betölti az adatokat egy fájlból"
        helyzetek = {}
        empires = dict([('British', 'angol'),
                        ('French',  'francia'),
                        ('Dutch',   'holland'),
                        ('pirate',  'kaloz'),
                        ('Spanish', 'spanyol')])
        allomany = askopenfilename(defaultextension = self.kiterjesztes, filetypes = self.tipus, initialdir='saved')
        if allomany == '':
            return False
        parameterek = ['name', 'color', 'home', 'ship', 'sailors', 'money', 'lastRoll', 'turnsToMiss', 'treasureHuntFinished']
        file = parse(allomany)
        save = file.getroot()
        aktivjatekosok = []
        fogadoszotar = {}
        for player in save.findall('player'):
            id = player.get('id')
            helyzetlista = []
            # betöltjük az alapadatokat
            for p in parameterek:
                helyzetlista.append(player.find(p).text)
            # betöltjük az összetettebb adatokat
            koordinatak = (int(player.find('coordinates').get('x')),int(player.find('coordinates').get('y')))
            helyzetlista.insert(5, koordinatak)
            statusz = player.find('status').text
            if statusz == None:
                helyzetlista.insert(7, [])
            else:
                statusz = [str(x) for x in statusz.split(',')]
                helyzetlista.insert(7, statusz)
            # a három számot számmá alakítjuk
            for i in [4,6,8,9]:
                helyzetlista[i] = int(helyzetlista[i])
            # a booleant visszaalakítjuk:
            if helyzetlista[10] == 'True':
                helyzetlista[10] = True
            else:
                helyzetlista[10] = False
            # betöltjük a zsákmányolt hajókat
            kiraboltHajok = {}
            kiraboltHajokTag = player.find('shipsLooted')
            for kiraboltHajo in kiraboltHajokTag.findall('score'):
                kiraboltHajok[empires[kiraboltHajo.get('empire')]] = int(kiraboltHajo.get('ships'))
            helyzetlista.append(kiraboltHajok)
            helyzetek[id] = helyzetlista
        kovetkezo = save.find('currentPlayer').text
        szelindex = int(save.find('windDirection').text)
        hadnagyElokerult = bool(save.find('firstMateFound').text)
        grogbaroLegyozve = bool(save.find('grogLordDefeated').text)
        fogadok = save.find('taverns')
        for fogado in fogadok.findall('tavern'):
            fogadoszotar[fogado.get('port')] = int(fogado.get('sailors'))
        # A kártyák betöltése
        kartyak = save.find('cards')
        cardsEp = kartyak.find('eventDeck').text
        cardsEt = kartyak.find('eventStack').text
        cardsKp = kartyak.find('trasureDeck').text
        cardsKt = kartyak.find('trasureStack').text
        paklik = [cardsEp, cardsEt, cardsKp, cardsKt]
        for pakli in paklik:
            if pakli:
                paklik[paklik.index(pakli)] = pakli.replace(' ','').split(',')
            else:
                paklik[paklik.index(pakli)] = []
        return (helyzetek, kovetkezo, szelindex, fogadoszotar, paklik)
        
    def set_adatok_fileba(self, jatekosAdatok = {}, kovetkezoJatekos = '', szelindex = 6, varosadatok = {}, kartyak = [], grogbaroLegyozve = False, hadnagyElokerult = False):
        "Kimenti az aktuális adatokat egy fájlba."
        helyzetek = jatekosAdatok
        kovetkezoJatekos = kovetkezoJatekos
        szelindex = szelindex
        varosadatok = varosadatok
        empire = ['British', 'French', 'Dutch', 'pirate', 'Spanish']
        esemenypakli, esemenytalon, kincspakli, kincstalon = kartyak
        grogbaroLegyozve = grogbaroLegyozve
        hadnagyElokerult = hadnagyElokerult
        # A paklik stringgé alakítása
        paklik = [esemenypakli, esemenytalon, kincspakli, kincstalon]
        for pakli in paklik:
            a = ''
            for i in pakli:
                a = a + ', ' + i
            paklik[paklik.index(pakli)] = a[2:]
        # Elkészítjük az XML-struktúra gyökerét
        allomany = asksaveasfilename(defaultextension = self.kiterjesztes, filetypes = self.tipus, initialdir='saved')
        if allomany == '':
            return False
        save = Element('save')
        file = ElementTree(save)
        # Tényleges mentés
        jatekosok = sorted(list(helyzetek.keys()))
        parameterek = ['name', 'color', 'home', 'ship', 'sailors', 'money', 'status', 'lastRoll', 'turnsToMiss', 'treasureHuntFinished']
        for jatekos in jatekosok:
            player = SubElement(save, 'player')
            player.set('id',jatekos)
            # Kivesszük a paraméterlistából a speciális paramétereket.
            statusz = helyzetek[jatekos][7]
            statusz = str(statusz).strip("[]'") # A statuszt vissza is tesszük.
            helyzetek[jatekos][7] = statusz
            kiraboltHajok = helyzetek[jatekos].pop(10)
            koordinatak = helyzetek[jatekos].pop(5)
            for i in range(len(parameterek)):
                tag = SubElement(player, parameterek[i])
                tag.text = str(helyzetek[jatekos][i])
            # Mentjük a kirabolt hajók mennyiségét.
            kiraboltHajokTag = SubElement(player, 'shipsLooted')
            for kiraboltHajo in kiraboltHajok:
                pontok = SubElement(kiraboltHajokTag, 'score')
                pontok.set('empire', empire[kiraboltHajok.index(kiraboltHajo)])
                pontok.set('ships', str(kiraboltHajo[1]))
            # Lementjük a koordinátákat is.
            coords = SubElement(player, 'coordinates')
            coords.set('x', str(koordinatak[0]))
            coords.set('y', str(koordinatak[1]))
        kovetkezo = SubElement(save, 'currentPlayer')
        kovetkezo.text = kovetkezoJatekos
        szel = SubElement(save, 'windDirection')
        szel.text = str(szelindex)
        hadnagy = SubElement(save, 'firstMateFound')
        hadnagy.text = str(hadnagyElokerult)
        grogbaro = SubElement(save, 'grogLordDefeated')
        grogbaro.text = str(grogbaroLegyozve)
        fogadok = SubElement(save, 'taverns')
        for aktualisFogado in list(varosadatok.keys()):
            fogado = SubElement(fogadok, 'tavern')
            fogado.set('port', aktualisFogado)
            fogado.set('sailors', str(varosadatok[aktualisFogado]))
        # Kártyák mentése
        kartyak = SubElement(save, 'cards')
        cardsEp = SubElement(kartyak, 'eventDeck')
        cardsEp.text = paklik[0]
        cardsEt = SubElement(kartyak, 'eventStack')
        cardsEt.text = paklik[1]
        cardsKp = SubElement(kartyak, 'trasureDeck')
        cardsKp.text = paklik[2]
        cardsKt = SubElement(kartyak, 'trasureStack')
        cardsKt.text = paklik[3]
        file.write(allomany, xml_declaration = True, encoding = 'utf-8', method = 'xml')
        return True
        
class Adatolvaso():
    """Beolvassa a játék adatait a beállításokat hordozó XML-állományokból."""
    def __init__(self, master):
        self.master = master
        pathFile = 'db/paths.xml'
        self.eleres = parse(pathFile).getroot()   # megnyitjuk az egyetlen beégetett XML-t
        self.eleresSzotar = {} # létrehozzuk az üres szótárat, amelyben le fogjuk tárolni az egyes db-k helyét
        configLista = [item.tag for item in self.eleres.find('xml')] # betöltendő configok listája
        confighelyHianyzik = []
        for config in configLista:
            try:
                self.eleresSzotar[config] = self.eleres.find('xml').find(config).text # betöltjük a kulcsok értékét
            except AttributeError:
                confighelyHianyzik.append(config)
        self.angolSzotar = dict([('spanish','spanyol'),('french','francia'),('dutch','holland'),('british','angol'),('pirate','kaloz'),
                            ('galleon','galleon'),('schooner','szkuner'),('brigantine','brigantin'),('frigate','fregatt')])
        self.errorlista = self.hibauzenetek_betoltese()
        if confighelyHianyzik:
            showerror('Error', (self.errorlista['confighelyHianyzikAttributeError'] % ', '.join(confighelyHianyzik)))
        
    def hibauzenetek_betoltese(self):
        "Betölti a hibaüzeneteket, amelyeket a játék során visszaad."
        file = parse(self.eleresSzotar['errors'])
        errors = file.getroot()
        errorlista = {}
        for error in errors.findall('exception'):
            errorlista[error.get('id')] = error.text.replace('\\n','\n')
        return errorlista
        
    def beallitasok_betoltese(self):
        "Betölti az alkalmazás alapbeállításait."
        file = parse(self.eleresSzotar['config'])
        config = file.getroot()
        nyelv = config.find('language').text # beolvassuk a nyelvet
        felbontaskod = config.find(("./resolutionlist/res[@type='"+config.find('resolution').text+"']")) # visszakeressük a beállított felbontást
        width = int(felbontaskod.get('x'))
        height = int(felbontaskod.get('y')) # kinyerjük a magasságot
        if int(config.find('fullscreen').text):
            fullscreen = True
        else:
            fullscreen = False
        screen = felbontaskod.get('type')
        resElementList = config.find('resolutionlist').findall('res')
        reslist = ()
        for res in resElementList:
            reslist += (int(res.get('x')),int(res.get('y')),res.get('type')),
        return nyelv,width,height,fullscreen,screen,reslist
        
    def beallitasok_irasa(self, ujfelbontas = None, ujteljeskepernyo = None, ujnyelv = None):
        "Menti az új megjelenítési beállításokat."
        file = parse(self.eleresSzotar['config'])
        config = file.getroot()
        if ujfelbontas and ujteljeskepernyo:
            config.find('resolution').text = ujfelbontas
            config.find('fullscreen').text = ujteljeskepernyo
        if ujnyelv:
            config.find('language').text = ujnyelv
        file.write(self.eleresSzotar['config'], xml_declaration = True, encoding = 'utf-8', method = 'xml')
        # Hibaszűrés (plusz enterek eltávolítása)
        file = open(self.eleresSzotar['config'],'r')
        text = file.read()
        file.close()
        while '\n\n' in text or '\n ' in text:
            text = text.replace('\n\n','\n')
            text = text.replace('\n ','\n')
        file = open(self.eleresSzotar['config'],'w')
        file.write(text)
        file.close()
        return True
    
    def csatak_betoltese(self):
        "Betolti a csaták adatait."
        file = parse(self.eleresSzotar['battles'])
        battles = file.getroot()
        csatalista = battles.findall('encounter')
        csataszotar = {}
        for csata in csatalista:
            id = csata.get('id')
            zaszlo = self.angolSzotar[csata.find('flag').text]
            hajotipus = self.angolSzotar[csata.find('shipType').text]
            hajonev = csata.find('shipName').text
            csapatok = ()
            for i in range(1,7):
                csapat = csata.find('parts').find('p'+str(i)).text
                if csapat not in ['powderStore', 'underWaterHit']:
                    try:
                        csapat = int(csapat)
                    except ValueError:
                        showerror('Error',(self.errorlista['csapatValueError'] % (hajonev,id,self.eleresSzotar['battles'])))
                    else:
                        if csapat > 6:
                            csapat = 6
                csapatok += csapat,
            zsakmany = csata.find('loot').text
            try:
                zsakmany = int(zsakmany)
            except ValueError:
                showerror('Error',(self.errorlista['zsakmanyValueError']% (hajonev,id,self.eleresSzotar['battles'])))
            kincshuzas = csata.find('shipName').text
            if kincshuzas == '0':
                kincshuzas = False
            else:
                kincshuzas = True
            csataszotar[id] = (zaszlo, hajotipus, hajonev, csapatok, zsakmany, kincshuzas)
        return csataszotar
        
    def kartyak_betoltese(self, type = "data"):
        "Betölti a kártyák tartalmát."
        try:
            hibauzenet = self.master.szotar['stringhiany']
        except AttributeError:
            hibauzenet = self.errorlista['stringAttributeError']
        file = parse(self.eleresSzotar['cards'])
        allCards = file.getroot()
        events = allCards.find('events')
        loot = allCards.find('loot')
        if type == "data":
            esemenykartyaszotar = {}
            kincskartyaszotar = {}
            penzszotar = {}
            fuggvenyszotar = {}
            for pakli,ag in ((esemenykartyaszotar,events), (kincskartyaszotar,loot)):
                for lap in ag.findall('card'):
                    try:
                        kep = lap.find('img').text
                    except AttributeError:
                        kep = self.errorlista['cardImgMissingAttributeError']
                    pakli[lap.get('id')] = kep
                    try:
                        fuggveny = lap.find("method").text
                    except AttributeError:
                        fuggveny = "self.dummy"
                    fuggvenyszotar[lap.get('id')] = fuggveny
                    gold = allCards.find('gold')
                    for sum in gold.findall('sum'):
                        penzszotar[sum.find('value').text] = int(sum.find('quantity').text)
            return esemenykartyaszotar,kincskartyaszotar,penzszotar,fuggvenyszotar
        elif type == "text":
            kartyaszotar = {}
            for esemenykartya in events.findall('card')+loot.findall('card'):
                try:
                    cim = esemenykartya.find('title').find(self.master.nyelv).text
                except AttributeError:
                    cim = hibauzenet
                else:
                    if cim == None:
                        cim = ''
                    else:
                        cim = cim.replace('\\n','\n')
                try:
                    szoveg = esemenykartya.find('text').find(self.master.nyelv).text
                except AttributeError:
                    szoveg = hibauzenet
                else:
                    if szoveg == None:
                        szoveg = ''
                    else:
                        szoveg = szoveg.replace('\\n','\n')
                kartyaszotar[esemenykartya.get('id')] = (cim, szoveg)
            return kartyaszotar

    def szotar_betoltese(self, nyelv = None, tipus = None, listaz = None):
        'Betölti a játék szótárát.'
        file = parse(self.eleresSzotar['interface'])
        interface = file.getroot()
        if nyelv:
            #szokincslista = [item.tag for item in interface]
            szokincslista = []
            for item in interface:
                if item.get('type') == tipus:
                    szokincslista.append(item.tag)
            szotar = {eredeti:interface.find(eredeti).find(nyelv).text for eredeti in szokincslista}
            return szotar
        elif listaz:
            nyelvlista = {}
            nyelvlistaR = {}
            for item in interface.find('nyelvek'):
                nyelvlista[item.text] = item.tag
                nyelvlistaR[item.tag] = item.text
            return nyelvlista,nyelvlistaR
            
    def get_hajotipusok(self):
        "Betölti a hajótípusokat."
        file = parse(self.eleresSzotar['shiptypes'])
        tipusok = file.getroot()
        eredmenylista = []
        for hajo in tipusok.findall('ship'):
            ar = int(hajo.get('cost'))
            maxlegenyseg = int(hajo.get('maxCrew'))
            tipus = hajo.get('type')
            eredmenylista.append((tipus, ar, maxlegenyseg))
        return eredmenylista
        
if __name__ == '__main__':
    def test_load():
        a = Adatgazda()
        b = a.get_adatok_filebol()
        print(b[0]['player0'])