from tkinter import *

class Naplo_legacy(Text):
    "A játék naplóosztálya."
    def __init__(self, boss=None, meret=200, sorszam = 0):
        Text.__init__(self, state = DISABLED, background = '#DEDEDE', relief = SUNKEN, borderwidth=2, wrap = WORD)
        self.boss = boss
        # Beállítjuk a betűtípust.
        try:
            self.config(font=('Helvetica', 8, 'normal'))
        except:
            self.config(font=' -*-Helvetica-R-*--*-80-*-*-*-*-UTF-8') # Hogy MacOSX-en is fusson.
        # Beállítjuk a méretet:
        #self.config(width = 2)
        #self.config(height = 2)
        #print(self.winfo_reqwidth(),self.winfo_reqheight())
        self.config(width = int((meret - 4)/6))
        self.config(height = int((meret - 4)/14))
        # Beállítjuk az írást:
        self.sorszam = sorszam
        self.string = ''

    def ir(self, string):
        "Ezt a függvényt kell hívni, ha írni szeretnénk a mezőbe."
        self.string = string
        self.ujelem()
        
    def ujelem(self):
        "Saját írófüggvény"
        self.config(state=NORMAL)
        self.insert(0.0,('%i: %s\n' % (self.sorszam,self.string)))
        self.config(state=DISABLED)
        self.sorszam+=1

class Naplo(Frame):
    "A játék állapotsora."
    def __init__(self,parent=None,meret=0):
        Frame.__init__(self,parent)
        self.grid_columnconfigure(0, minsize=meret)
        self.status = Label(self, text='', anchor=W, relief = SUNKEN, bd=1, width = 20)
        self.status.grid(row = 0, column = 0, sticky = W+E)
        
    def ir(self,string):
        "Saját írófüggvény"
        self.status.config(text=string)

if __name__ == '__main__':
    def ir():
        "Ezt a függvényt kell hívni, ha írni szeretnénk a mezőbe."
        a.ujelem("Szöveg")
    
    b = Tk()
    b.title('Napló')
    b.minsize(200,200)
    b.maxsize(200,200)
    Button(b, text="Semmi").grid(row=0,column = 0)
    a = Naplo(b,200)
    a.grid(row = 1, column = 0, sticky = S)
    a.status.config(text="Árvíztűrő tükörfúrógép")
    b.mainloop()