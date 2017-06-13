from random import uniform
from tkinter import *
import datetime

#glavna naloga okna je da dobimo višino, širino in štbomb, ki jih uporabnik vpiše v okna
#vpisavanje in branje highscore-a
class Zacetno_okno:
    def __init__(self, tk):
        self.highscore_file = 'highscore_file.txt'
        self.highscore = self.preberi_highscore_file()
        self.tk = tk
        self.okno = Frame(tk)
        self.vrednosti = (0,0,0)

        self.gumb1 = Button(self.okno, text="Nova igra", command=self.vnosi_okno)
        self.gumb1.grid(row=0)
        self.gumb2 = Button(self.okno, text="Highscore", command=self.preberi_highscore)
        self.gumb2.grid(row=1)
        self.gumb3 = Button(self.okno, text="Izhod", command=exit)
        self.gumb3.grid(row=2)
        self.okno.pack()

        self.tk.protocol("WM_DELETE_WINDOW", exit)
        self.tk.mainloop()

    def enable(self, tk):
        self.gumb1.configure(state=ACTIVE)
        self.gumb2.configure(state=ACTIVE)
        self.gumb3.configure(state=ACTIVE)
        tk.destroy()

    def disable(self):
        self.gumb1.configure(state='disable')
        self.gumb2.configure(state='disable')
        self.gumb3.configure(state='disable')

    def preberi_highscore_file(self):
        lista = []
        with open(self.highscore_file) as d:
            for vrstica in d:
                lista.append(vrstica)
        return lista

    def vpisi_highscore(self, ime, vis, sir, bomb):
        now = datetime.datetime.now()
        with open(self.highscore_file, 'w') as d:
            for vrstica in self.highscore:
                d.write(vrstica)
            print(ime + "\t\t" + now.strftime("%Y-%m-%d")+ "\t\t" + str(vis)+'×'+str(sir)+', '+str(bomb), file=d)

    def preberi_highscore(self):
        self.disable()

        self.tk4 = Tk()
        highscore_okno = Frame(self.tk4)
        naredi_vrstico = lambda vrsta, tekst: Label(highscore_okno, text=tekst).grid(row=vrsta, column=0)

        row_count = 0
        with open(self.highscore_file) as d:
            for vrstica in d:
                naredi_vrstico(row_count, vrstica[:len(vrstica)-2])
                row_count += 1

        highscore_okno.pack()
        self.tk4.protocol("WM_DELETE_WINDOW", lambda x=self.tk4: self.enable(x))
        self.tk4.mainloop()

    def vnosi_okno(self):
        self.disable()

        self.tk_vmesno_okno = Tk()
        vmesno_okno = Frame(self.tk_vmesno_okno)

        self.visina = Entry(vmesno_okno)
        self.sirina = Entry(vmesno_okno)
        self.stbomb = Entry(vmesno_okno)

        l_visina = Label(vmesno_okno, text='Vpiši višino: ')
        l_sirina = Label(vmesno_okno, text='Vpiši širino: ')
        l_stbomb = Label(vmesno_okno, text='Vpiši število bomb: ')

        gumb2 = Button(vmesno_okno, text = "Vnos", command=self.vpis)
        tip_of_the_day = Label(vmesno_okno, text='Priporočeno število bomb: visina*sirina/6')

        l_visina.grid(row=0, column=0)
        l_sirina.grid(row=1, column=0)
        l_stbomb.grid(row=2, column=0)

        self.visina.grid(row=0, column=1)
        self.sirina.grid(row=1, column=1)
        self.stbomb.grid(row=2, column=1)

        gumb2.grid(row=3, column=1)
        tip_of_the_day.grid(row=3, column=0)

        vmesno_okno.pack()
        self.tk_vmesno_okno.protocol("WM_DELETE_WINDOW", lambda x=self.tk_vmesno_okno: self.enable(x))
        self.tk_vmesno_okno.mainloop()

    def vpis(self):
        try:
            visina, sirina, stbomb = int(self.visina.get()), int(self.sirina.get()), int(self.stbomb.get())
            if (visina > 4 and visina <= 30) and (sirina > 4 and sirina <= 30) and (stbomb > 0 and stbomb < sirina * visina):
                minolovec = Minolovec(visina, sirina, stbomb)
                self.tk.destroy()
                self.tk_vmesno_okno.destroy()
                Glavno_okno(Tk(), minolovec, self)
        except:
            print('abc')

class Glavno_okno:
    def __init__(self, tk, minolovec, zac_okno):
        self.odprto = []
        self.je_konec_igre = False
        self.tk_glavno_okno = tk
        self.minolovec = minolovec
        self.zac_okno = zac_okno

        self.visina = self.minolovec.visina
        self.sirina = self.minolovec.sirina
        self.stbomb = self.minolovec.stbomb
        self.ime_highscore = ''

        self.okno_zgori = Frame(self.tk_glavno_okno)
        self.okno_spodi = Frame(self.tk_glavno_okno)

        self.slika_bomb = PhotoImage(file='bomb.png')
        self.slika_smiley1 = PhotoImage(file='smiley1.png')
        self.slika_smiley2 = PhotoImage(file='smiley2.png')
        self.slika_smiley3 = PhotoImage(file='smiley3.png')
        self.slika_zastavica = PhotoImage(file='zastavica.png')

        self.smiley = Button(self.okno_zgori, image=self.slika_smiley1, text='aaa', command=self.try_again)
        self.smiley.grid(row=0)

        self.fun_gumbi = lambda x, y: Button(self.okno_spodi, height=1, width=2, command=lambda: self.callback(x, y))
        self.fun_label = lambda x, y, polje, barva='green': Label(self.okno_spodi, height=1, width=2, padx=3, pady=3, text=str(polje), fg=barva).grid(row=x, column=y)

        self.knofi = [[0] * self.sirina for _ in range(self.visina)]

        for i in range(self.visina):
            for j in range(self.sirina):
               self.knofi[i][j] = self.fun_gumbi(i, j)
               #self.knofi[i][j].bind("<Button-3>", lambda gumb=self.knofi[i][j]:self.zastavica(gumb))
               self.knofi[i][j].grid(row=i, column=j)

        self.okno_zgori.grid(row=0)
        self.okno_spodi.grid(row=1)

        self.tk_glavno_okno.protocol("WM_DELETE_WINDOW", exit)
        self.tk_glavno_okno.mainloop()

    def callback(self, x, y):
        polje = self.minolovec.odkrij(x, y)

        if int(polje) == -1:
            self.knofi[x][y].grid_remove()
            Label(self.okno_spodi, image = self.slika_bomb).grid(row=x, column=y)
            self.smiley.configure(image=self.slika_smiley3)
            self.je_konec_igre = True
            self.disable()

        elif int(polje) == 0:
            otocec = self.minolovec.vrni_otocec((x, y))

            for i in otocec:
                n = i[0]
                m = i[1]
                self.knofi[n][m].grid_remove()
                self.fun_label(n, m, 0, 'black')

                self.odprto.append((n, m))

                if n-1 >= 0 and not((n-1, m) in otocec) and not((n-1, m) in self.odprto):
                    polje = self.minolovec.odkrij(n - 1, m)
                    self.knofi[n-1][m].grid_remove()
                    self.fun_label(n-1, m, polje)
                    self.odprto.append((n-1, m))

                if n+1 < self.visina and not((n+1, m) in otocec) and not((n+1, m) in self.odprto):
                    polje = self.minolovec.odkrij(n + 1, m)
                    self.knofi[n + 1][m].grid_remove()
                    self.fun_label(n + 1, m, polje)
                    self.odprto.append((n+1, m))

                if m-1 >= 0 and not((n, m-1) in otocec) and not((n, m-1) in self.odprto):
                    polje = self.minolovec.odkrij(n, m - 1)
                    self.knofi[n][m-1].grid_remove()
                    self.fun_label(n, m-1, polje)
                    self.odprto.append((n, m-1))

                if m+1 < self.sirina and not((n, m+1) in otocec) and not((n, m+1) in self.odprto):
                    polje = self.minolovec.odkrij(n, m + 1)
                    self.knofi[n][m+1].grid_remove()
                    self.fun_label(n, m+1, polje)
                    self.odprto.append((n, m+1))

                if (n-1 >= 0 and m-1 >= 0) and not((n-1, m-1) in otocec) and not((n-1, m-1) in self.odprto):
                    polje = self.minolovec.odkrij(n - 1, m - 1)
                    if polje != 0:
                        self.knofi[n-1][m-1].grid_remove()
                        self.fun_label(n-1, m-1, polje)
                        self.odprto.append((n-1, m-1))

                if (n-1 >= 0 and m+1 < self.sirina) and not((n-1, m+1) in otocec) and not((n-1, m+1) in self.odprto):
                    polje = self.minolovec.odkrij(n - 1, m + 1)
                    if polje != 0:
                        self.knofi[n-1][m+1].grid_remove()
                        self.fun_label(n-1, m+1, polje)
                        self.odprto.append((n-1, m+1))


                if (n+1 < self.visina and m-1 >= 0) and not((n+1, m-1) in otocec) and not((n+1, m-1) in self.odprto):
                    polje = self.minolovec.odkrij(n + 1, m - 1)
                    if polje != 0:
                        self.knofi[n+1][m-1].grid_remove()
                        self.fun_label(n+1, m-1, polje)
                        self.odprto.append((n+1, m-1))

                if (n+1 < self.visina and m+1 < self.sirina) and not((n+1, m+1) in otocec) and not((n+1, m+1) in self.odprto):
                    polje = self.minolovec.odkrij(n + 1, m + 1)
                    if polje != 0:
                        self.knofi[n+1][m+1].grid_remove()
                        self.fun_label(n+1, m+1, polje)
                        self.odprto.append((n+1, m+1))
        else:
            self.knofi[x][y].grid_remove()
            self.fun_label(x, y, polje)
            self.odprto.append((x,y))

        if  self.visina * self.sirina - len(self.odprto) == self.minolovec.stbomb:
            self.za_konec_igre()

    def disable(self):
        for child in self.okno_spodi.winfo_children():
            child.configure(state='disable')

    def enable(self, tk):
        if self.je_konec_igre == False:
            for child in self.okno_spodi.winfo_children():
                child.configure(state='normal')
        if tk == self.tk_try_again_okno:
            self.smiley.configure(state='normal')
        tk.destroy()

    def try_again(self):
        self.disable()
        self.smiley.configure(state='disabled')

        self.tk_try_again_okno= Tk()
        self.try_again_okno = Frame(self.tk_try_again_okno)

        self.restart = Button(self.try_again_okno, text='Restart', command=self.restarti_igro)
        self.menu = Button(self.try_again_okno, text='Menu', command= self.na_zacetno_okno)
        self.resume = Button(self.try_again_okno, text='Resume', command= lambda x=self.tk_try_again_okno: self.enable(x))

        self.restart.grid(row=0, column=0)
        self.menu.grid(row=0, column=1)
        self.resume.grid(row=0, column=2)

        self.try_again_okno.pack()
        self.tk_try_again_okno.protocol("WM_DELETE_WINDOW", lambda x=self.tk_try_again_okno: self.enable(x))
        self.tk_try_again_okno.mainloop()

    def na_zacetno_okno(self, sklopka = 0):
        self.tk_glavno_okno.destroy()
        if sklopka == 0:
            self.tk_try_again_okno.destroy()
        elif sklopka == 1:
            self.tk_konec_igre.destroy()
        Zacetno_okno(Tk())

    def za_konec_igre(self):
        self.disable()
        self.smiley.configure(image=self.slika_smiley2, command=self.za_konec_igre, state='disabled')
        self.tk_konec_igre = Tk()
        self.highscore_okno = Frame(self.tk_konec_igre)
        self.poziv = Label(self.highscore_okno, text='Vpiši ime: ')
        self.vpis_imena = Entry(self.highscore_okno)
        self.imeknof = Button(self.highscore_okno, text='Potrdi', command=self.vzemi_ime)

        self.poziv.grid(row=0, column=0)
        self.vpis_imena.grid(row=0, column=1)
        self.imeknof.grid(row=0, column=2)
        self.highscore_okno.pack()

        self.tk_konec_igre.protocol("WM_DELETE_WINDOW", lambda x=self.tk_try_again_okno: self.enable(x))


        self.tk_konec_igre.mainloop()

    def vzemi_ime(self):
        vzdevek = self.vpis_imena.get()
        if len(vzdevek) > 0 and len(vzdevek) < 10:
            self.zac_okno.vpisi_highscore(vzdevek, self.visina, self.sirina, self.stbomb)
            self.na_zacetno_okno(1)

    def restarti_igro(self):
        self.tk_glavno_okno.destroy()
        self.tk_try_again_okno.destroy()
        minolovec = Minolovec(self.visina, self.sirina, self.stbomb)
        Glavno_okno(Tk(), minolovec, self.zac_okno)

    #def zastavica(self, gumb):
    #    gumb.configure(image = self.slika_zastavica)


class Minolovec:
    def __init__(self, visina, sirina, stbomb):
        self.visina = visina
        self.sirina = sirina
        self.stbomb = stbomb
        self.tabela, self.nicle = self.gen_tabelo()
        self.izpis_tabele()

    # prešteje število bomb okoli točke (x,y)
    def okolica(self, podlaga, x, y):
        stevec = 0
        for i in range(x - 1, x + 2):
            if i >= 0 and i < len(podlaga):
                for j in range(y - 1, y + 2):
                    if j >= 0 and j < len(podlaga[i]) and not (i == x and j == y):
                        if podlaga[i][j] == -1:
                            stevec += 1
        return stevec

    #odkrije polje ko uporabnik pritisne na gumb
    def odkrij(self, x, y):
        return str(self.tabela[x][y])

    #vrne nicle skupne z niclo pri (x,y)
    def vrni_otocec(self, nicla):
        for i in self.nicle:
            if nicla in i:
                return i

    # ZGENERIRA TABELO ZA IGRO
    def gen_tabelo(self):
        podlaga = [[0]*self.sirina for _ in range(self.visina)]
        listabomb = []

        # vstavi bombe v tabelo
        x = 0
        while x < self.stbomb:
            i = int(uniform(0, self.visina))
            j = int(uniform(0, self.sirina))

            if podlaga[i][j] == 0 and not((i, j) in listabomb):
                podlaga[i][j] = -1
                listabomb.append((i,j))
                x += 1

        # vstavi stevilke v tabelo
        for t in range(len(podlaga)):
            for u in range(len(podlaga[t])):
                stsosednjihbomb = self.okolica(podlaga, t, u)
                if stsosednjihbomb > 0 and podlaga[t][u] == 0:
                    podlaga[t][u] = stsosednjihbomb

        # naredi seznam seznamov točk skupnih ničel
        nicle = []
        stnicl = 0

        # najprej iz podlage dobi koordinate nicel v obliki (x, y) shranjeni v listi
        for i in range(len(podlaga)):
            for j in range(len(podlaga[i])):
                if podlaga[i][j] == 0:
                    nicle.append((i, j))
                    stnicl += 1

        # zdruzi nicle v skupne liste z lastnostjo, da se nicle držijo skupi v podlagi
        lista_nicel = []
        while not (nicle == []):
            otocec = []
            a = True
            dolzina1 = 0
            dolzina2 = 1
            while a:
                if len(otocec) == 0:
                    otocec.append(nicle.pop(0))
                    dolzina1 += 1
                for n in nicle:
                    x, y = n[0], n[1]
                    if (x + 1, y) in otocec:
                        otocec.append(nicle.pop(nicle.index((x, y))))
                        dolzina1 += 1
                    elif (x - 1, y) in otocec:
                        otocec.append(nicle.pop(nicle.index((x, y))))
                        dolzina1 += 1
                    elif (x, y + 1) in otocec:
                        otocec.append(nicle.pop(nicle.index((x, y))))
                        dolzina1 += 1
                    elif (x, y - 1) in otocec:
                        otocec.append(nicle.pop(nicle.index((x, y))))
                        dolzina1 += 1

                if dolzina1 == dolzina2:
                    a = False
                else:
                    dolzina2 = dolzina1

            lista_nicel.append(otocec)
        return (podlaga, lista_nicel)

    # lepši izpis tabele
    def izpis_tabele(self):
        for i in self.tabela:
            a = ''
            for j in i:
                a += str(j) + '\t'
            print(a)

# ZAČETEK KLICANJA ====================================================================================000000001

Zacetno_okno(Tk())


