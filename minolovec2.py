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

        self.gumb1 = Button(self.okno, text="Nova igra", fg="green", command=self.vnosi_okno)
        self.gumb1.grid(row=0)
        self.gumb2 = Button(self.okno, text="Highscore", fg="blue", command=self.preberi_highscore)
        self.gumb2.grid(row=1)
        self.gumb3 = Button(self.okno, text="Izhod", fg="red", command=exit)
        self.gumb3.grid(row=2)
        self.okno.pack()

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
                print(vrstica)
                d.write(vrstica)
            print(ime + "\t\t" + now.strftime("%Y-%m-%d")+ "\t\t" + str(vis)+'×'+str(sir)+', '+str(bomb), file=d)

    def preberi_highscore(self):
        tk4 = Tk()
        wkno = Frame(tk4)
        naredi_vrstico = lambda vrsta, tekst: Label(wkno, text=tekst).grid(row=vrsta, column=0)
        row_count = 0
        with open(self.highscore_file) as d:
            for vrstica in d:
                naredi_vrstico(row_count, vrstica[:len(vrstica)-2])
                row_count += 1
        wkno.pack()
        tk4.mainloop()

    def vnosi_okno(self):
        self.tk_v_okno = Tk()

        vmesno_okno = Frame(self.tk_v_okno)

        self.v_visina = Entry(vmesno_okno)
        self.v_sirina = Entry(vmesno_okno)
        self.v_stbomb = Entry(vmesno_okno)

        l_visina = Label(vmesno_okno, text='Vpiši višino: ')
        l_sirina = Label(vmesno_okno, text='Vpiši širino: ')
        l_stbomb = Label(vmesno_okno, text='Vpiši število bomb: ')

        gumb2 = Button(vmesno_okno, text = "Vnos", command=self.vpis)
        tip_of_the_day = Label(vmesno_okno, text='Priporočeno število bomb: visina*sirina/6')

        l_visina.grid(row=0, column=0)
        l_sirina.grid(row=1, column=0)
        l_stbomb.grid(row=2, column=0)

        self.v_visina.grid(row=0, column=1)
        self.v_sirina.grid(row=1, column=1)
        self.v_stbomb.grid(row=2, column=1)

        gumb2.grid(row=3, column=1)
        tip_of_the_day.grid(row=3, column=0)

        vmesno_okno.pack()
        self.tk_v_okno.mainloop()


    def vpis(self):
        self.visina, self.sirina, self.stbomb = int(self.v_visina.get()), int(self.v_sirina.get()), int(self.v_stbomb.get())
        minolovec = Minolovec(self.visina, self.sirina, self.stbomb)
        self.tk.destroy()
        self.tk_v_okno.destroy()

        tk_glavno_okno = Tk()
        glavno_okno = Glavno_okno(tk_glavno_okno, self.visina, self.sirina, self.stbomb, minolovec, self)

class Glavno_okno:
    def __init__(self, tk, visina, sirina, stbomb, minolovec, zac_okno):
        self.odprto = []
        self.tk = tk
        self.minolovec = minolovec
        self.zac_okno = zac_okno
        self.visina = visina
        self.sirina = sirina
        self.stbomb = stbomb
        self.ime_highscore = ''

        self.okno_zgori = Frame(tk)
        self.okno_spodi = Frame(tk)

        self.slika_bomb = PhotoImage(file='bomb.png')
        self.slika_smiley1 = PhotoImage(file='smiley1.png')
        self.slika_smiley2 = PhotoImage(file='smiley2.png')
        self.slika_smiley3 = PhotoImage(file='smiley3.png')
        self.slika_zastavica = PhotoImage(file='zastavica.png')

        self.smiley = Button(self.okno_zgori, image=self.slika_smiley1, text='aaa', command=self.try_again_okno)
        self.smiley.grid(row=0)

        self.fun_gumbi = lambda x, y: Button(self.okno_spodi, height=1, width=2, command=lambda: self.callback(x, y))
        self.fun_label = lambda x, y, polje, barva='green': Label(self.okno_spodi, height=1, width=2, padx=3, pady=3, text=str(polje), fg=barva).grid(row=x, column=y)

        self.knofi = [[0] * sirina for _ in range(visina)]

        for i in range(visina):
            for j in range(sirina):
               self.knofi[i][j] = self.fun_gumbi(i, j)
               #self.knofi[i][j].bind("<Button-3>", lambda gumb=self.knofi[i][j]:self.zastavica(gumb))
               self.knofi[i][j].grid(row=i, column=j)

        self.okno_zgori.grid(row=0)
        self.okno_spodi.grid(row=1)
        self.tk.mainloop()

    def callback(self, x, y):
        polje = self.minolovec.odkrij(x, y)

        if int(polje) == -1:
            self.knofi[x][y].grid_remove()
            self.smiley.configure(image=self.slika_smiley3)
            Label(self.okno_spodi, image = self.slika_bomb).grid(row=x, column=y)
            self.mina()

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

    def mina(self):
        for child in self.okno_spodi.winfo_children():
            child.configure(state='disable')

    def try_again_okno(self):
        self.tk_t_a_okno= Tk()
        self.t_a_okno = Frame(self.tk_t_a_okno)

        self.restart = Button(self.t_a_okno, text='Restart', command=self.restart)
        self.menu = Button(self.t_a_okno, text='Menu', command=self.na_zacetno_okno)
        self.resume = Button(self.t_a_okno, text='Resume', command=self.tk_t_a_okno.destroy)

        self.restart.grid(row=0, column=0)
        self.menu.grid(row=0, column=1)
        self.resume.grid(row=0, column=2)

        self.t_a_okno.pack()
        self.tk_t_a_okno.mainloop()

    def na_zacetno_okno(self, sklopka = 0):
        self.tk_z_okno = Tk()
        self.zacetno_okno = Zacetno_okno(self.tk_z_okno)

        if sklopka == 0:
            self.tk_t_a_okno.destroy()
        elif sklopka == 2:
            self.tk_mina.destroy()
        self.tk.destroy()
        self.zac_okno.tk.mainloop()

    def za_konec_igre(self):
        self.smiley.configure(image=self.slika_smiley2)
        self.smiley.configure(command=self.za_konec_igre)
        for child in self.okno_spodi.winfo_children():
            child.configure(state='disable')
        self.tk3 = Tk()
        self.highscore_okno = Frame(self.tk3)
        self.poziv = Label(self.highscore_okno, text='Vpiši ime: ')
        self.vpis_imena = Entry(self.highscore_okno)
        self.imeknof = Button(self.highscore_okno, text='Potrdi', command=self.vzemi_ime)

        self.poziv.grid(row=0, column=0)
        self.vpis_imena.grid(row=0, column=1)
        self.imeknof.grid(row=0, column=2)
        self.highscore_okno.pack()
        self.tk3.mainloop()

    def vzemi_ime(self):
        self.zac_okno.vpisi_highscore(self.vpis_imena.get(), self.visina, self.sirina, self.stbomb)
        self.tk3.destroy()
        self.na_zacetno_okno(1)

    def restart(self):
        minolovec = Minolovec(self.visina, self.sirina, self.stbomb)
        self.tk.destroy()
        self.tk_t_a_okno.destroy()

        tk_glavno_okno = Tk()
        glavno_okno = Glavno_okno(tk_glavno_okno, self.visina, self.sirina, self.stbomb, minolovec, self.zac_okno)
        tk_glavno_okno.mainloop()

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

tk_zacetno_okno = Tk()
zacetno_okno = Zacetno_okno(tk_zacetno_okno)
tk_zacetno_okno.mainloop()


