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

        
if __name__ == '__main__':
    def test_load():
        a = Adatgazda()
        b = a.get_adatok_filebol()
        print(b[0]['player0'])