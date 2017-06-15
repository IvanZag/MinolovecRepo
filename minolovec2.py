from random import uniform
from tkinter import *
import datetime

#glavna naloga okna je da dobimo višino, širino in štbomb, ki jih uporabnik vpiše v okna
#vpisavanje in branje highscore-a
class Zacetno_okno:
    def __init__(self, tk):
        #random spremenljivke za zacet
        self.highscore_file = 'highscore_file.txt'
        self.highscore_lista = self.preberi_highscore_file()

        #gumbi in zacetno okno
        self.tk_zacetno_okno = tk
        self.tk_zacetno_okno.title('Minolovec')
        self.tk_zacetno_okno.geometry("250x75")
        self.okno_zacetno = Frame(self.tk_zacetno_okno)
        self.vrednosti = (0,0,0)

        self.g_nova_igra = Button(self.okno_zacetno, text="Nova igra", command=self.vnosi)
        self.g_nova_igra.pack(fill=X)
        self.g_highscore = Button(self.okno_zacetno, text="Highscore", command=self.highscore)
        self.g_highscore.pack(fill=X)
        self.g_izhod = Button(self.okno_zacetno, text="Izhod", command=self.zapri)
        self.g_izhod.pack(fill=X)
        self.okno_zacetno.pack(fill=BOTH)

        self.tk_zacetno_okno.protocol("WM_DELETE_WINDOW", self.zapri)
        self.tk_zacetno_okno.mainloop()

    def vkljuci_gumbe(self, x):
        self.g_nova_igra.configure(state=ACTIVE)
        self.g_highscore.configure(state=ACTIVE)
        self.g_izhod.configure(state=ACTIVE)
        if x == 0:
            self.tk_vmesno_okno.destroy()
        elif x == 1:
            self.tk_okno_hs.destroy()

    def izkljuci_gumbe(self):
        self.g_nova_igra.configure(state=DISABLED)
        self.g_highscore.configure(state=DISABLED)
        self.g_izhod.configure(state=DISABLED)

    #prebere highscore_file ua nadaljnje pisanje
    def preberi_highscore_file(self):
        lista = []
        with open(self.highscore_file) as d:
            for vrstica in d:
                ta_vrstica = vrstica.split('&')
                print(ta_vrstica)
                if ta_vrstica != '':
                    if '\n' in ta_vrstica[2]:
                        ta_vrstica[2] = ta_vrstica[2][:-1]
                lista.append(ta_vrstica)
                print(ta_vrstica)
        return lista

    #po uspešni igri vpise na datoteko
    def vpisi_highscore(self, ime, vis, sir, bomb):
        now = datetime.datetime.now()
        with open(self.highscore_file, 'w') as d:
            for vrstica in self.highscore_lista:
                print('&'.join(vrstica), file=d)
            d.write(ime + "&" + now.strftime("%Y-%m-%d")+ "&" + str(vis)+'×'+str(sir)+', '+str(bomb))

    #naredi highscore okno
    def highscore(self):
        self.izkljuci_gumbe()
        self.tk_okno_hs = Tk()
        self.tk_okno_hs.title('highscore')
        okno_hs_oknoR = Frame(self.tk_okno_hs)
        okno_hs_oknoC = Frame(self.tk_okno_hs)
        okno_hs_oknoL = Frame(self.tk_okno_hs)

        for i in range(len(self.highscore_lista)):
            for j in range(len(self.highscore_lista[i])):
                if j == 0:
                    Label(okno_hs_oknoL, text=' '+self.highscore_lista[i][j]+' ', borderwidth=3, relief="ridge").pack(fill=X)
                elif j == 1:
                    Label(okno_hs_oknoC, text=' '+self.highscore_lista[i][j]+' ', borderwidth=3, relief="ridge").pack(fill=X)
                else:
                    Label(okno_hs_oknoR, text=' '+self.highscore_lista[i][j]+' ', borderwidth=3, relief="ridge").pack(fill=X)

        okno_hs_oknoL.pack(fill=X, side = LEFT)
        okno_hs_oknoR.pack(fill=X, side = RIGHT)
        okno_hs_oknoC.pack(fill=X, side = RIGHT)
        self.tk_okno_hs.protocol("WM_DELETE_WINDOW", lambda x=1: self.vkljuci_gumbe(x))
        self.tk_okno_hs.mainloop()

    def vnosi(self):
        self.izkljuci_gumbe()

        #gumbi in vmesno okno
        self.tk_vmesno_okno = Tk()
        self.tk_vmesno_okno.title('')
        vmesno_oknoL = Frame(self.tk_vmesno_okno)
        vmesno_oknoD = Frame(self.tk_vmesno_okno)

        self.e_visina = Entry(vmesno_oknoD)
        self.e_sirina = Entry(vmesno_oknoD)
        self.e_stbomb = Entry(vmesno_oknoD)
        self.e_visina.pack(fill=X)
        self.e_sirina.pack(fill=X)
        self.e_stbomb.pack(fill=X)

        Label(vmesno_oknoL, text='Vpiši višino: ', fg='blue', relief="groove", pady=2).pack(fill=BOTH)
        Label(vmesno_oknoL, text='Vpiši širino: ', fg='blue', relief="groove", pady=2).pack(fill=BOTH)
        Label(vmesno_oknoL, text='Vpiši število bomb: ', fg='blue', relief="groove", pady=2).pack(fill=BOTH)

        self.gumb_vnos = Button(vmesno_oknoD, text = "Vnos", command=self.vpis)
        self.gumb_vnos.bind('<Return>', lambda x: self.vpis(x))
        self.gumb_vnos.pack(fill=X)
        Label(vmesno_oknoL, text='Priporočeno št bomb: viš*šir/6', padx=20).pack(fill=X)

        vmesno_oknoD.pack(fill=X, side=RIGHT)
        vmesno_oknoL.pack(fill=X, side=LEFT)
        self.tk_vmesno_okno.protocol("WM_DELETE_WINDOW", lambda x=0: self.vkljuci_gumbe(x))
        self.tk_vmesno_okno.mainloop()

    def vpis(self, event=''):
        try:
            visina, sirina, stbomb = int(self.e_visina.get()), int(self.e_sirina.get()), int(self.e_stbomb.get())
            if (visina > 6 and visina <= 30) and (sirina > 6 and sirina <= 45) and (stbomb > 0 and stbomb < sirina * visina):
                minolovec = Minolovec(visina, sirina, stbomb)
                self.tk_zacetno_okno.destroy()
                self.tk_vmesno_okno.destroy()
                Glavno_okno(Tk(), minolovec, self)
        except:
            pass

    def zapri(self, event = ''):
        self.tk_zacetno_okno.destroy()
        try:
            self.tk_vmesno_okno.destroy()
        except:
            pass
        exit()

#glavno okno in interakcija
class Glavno_okno:
    def __init__(self, tk, minolovec, zac_okno):
        self.odprto = []
        self.je_konec_igre = False

        self.minolovec = minolovec
        self.zac_okno = zac_okno

        self.visina = self.minolovec.visina
        self.sirina = self.minolovec.sirina
        self.stbomb = self.minolovec.stbomb
        self.ime_highscore = ''
        self.zastavice = [[0] * self.sirina for _ in range(self.visina)]
        self.preostale_bombe = self.stbomb

        self.tk_glavno_okno = tk
        self.tk_glavno_okno.title('Minolovec')
        self.okno_zgori = Frame(self.tk_glavno_okno)
        self.okno_spodi = Frame(self.tk_glavno_okno)

        self.slika_bomb = PhotoImage(file='bomb.png')
        self.slika_smiley_default = PhotoImage(file='smiley1.png')
        self.slika_smiley_win = PhotoImage(file='smiley2.png')
        self.slika_smiley_lose = PhotoImage(file='smiley3.png')
        self.slika_zastavica = PhotoImage(file='zastavica.png')

        self.l_stbomb = Label(self.okno_zgori, text=self.preostale_bombe, anchor="w")
        self.l_stbomb.pack(side=LEFT, fill=X)
        self.l_cas = Label(self.okno_zgori, text='tuki bo čas', anchor="e")
        self.l_cas.pack(side = RIGHT, fill=X)

        self.smiley = Button(self.okno_zgori, image=self.slika_smiley_default, command=self.try_again)
        self.smiley.pack(side=RIGHT)

        self.fun_gumbi = lambda x, y: Button(self.okno_spodi, height=1, width=2, command=lambda: self.odpri_polje(x, y))
        self.fun_label = lambda x, y, polje, barva='green': Label(self.okno_spodi, height=1, width=2, padx=3, pady=3, text=str(polje), fg=barva, relief="sunken").grid(row=x, column=y)

        self.gumbi = [[0] * self.sirina for _ in range(self.visina)]

        for i in range(self.visina):
            for j in range(self.sirina):
               self.gumbi[i][j] = self.fun_gumbi(i, j)
               self.gumbi[i][j].grid(row=i, column=j)
               self.gumbi[i][j].bind('<Button-3>', lambda event, x=i, y=j: self.zamenjaj_slikco(event, x, y))


        self.okno_zgori.pack(side = TOP)
        self.okno_spodi.pack(side = BOTTOM)
        self.tk_glavno_okno.protocol("WM_DELETE_WINDOW", self.zapri)
        self.tk_glavno_okno.mainloop()

    def zapri(self):
        self.tk_glavno_okno.destroy()
        exit()

    def odpri_polje(self, x, y):
        polje = int(self.minolovec.odkrij(x, y))

        if polje == -1:
            self.gumbi[x][y].grid_remove()
            Label(self.okno_spodi, image = self.slika_bomb, relief="sunken").grid(row=x, column=y)
            self.smiley.configure(image=self.slika_smiley_lose)
            self.je_konec_igre = True
            self.disable()
        elif polje == 0:
            otocec = self.minolovec.vrni_otocec((x, y))

            for nicla in otocec:
                n = nicla[0]
                m = nicla[1]
                self.gumbi[n][m].grid_remove()
                self.fun_label(n, m, 0)
                self.odprto.append(nicla)

                for i in range(n-1, n+2):
                    if i >= 0 and i < len(self.minolovec.tabela):
                        for j in range(m-1, m+2):
                            if j >=0 and j < len(self.minolovec.tabela[i]) and not(i == n and j == m):
                                if not((i,j) in otocec) and not((i,j) in self.odprto):
                                    if self.minolovec.tabela[i][j] == 0:
                                        otocec.append(self.minolovec.vrni_otocec((n, m)))
                                    else:
                                        self.gumbi[i][j].grid_remove()
                                        self.fun_label(i, j, self.minolovec.tabela[i][j])
                                        self.odprto.append((i,j))
        else:
            self.gumbi[x][y].grid_remove()
            self.fun_label(x, y, polje)
            self.odprto.append((x,y))

        self.preveri_zastavice()

        if  self.visina * self.sirina - len(self.odprto) == self.minolovec.stbomb:
            self.za_konec_igre()

    def disable(self):
        for child in self.okno_spodi.winfo_children():
            child.configure(state='disable')

    def enable(self, tk):
        if self.je_konec_igre == False:
            for child in self.okno_spodi.winfo_children():
                child.configure(state='normal')
        self.smiley.configure(state='normal')
        tk.destroy()

    def try_again(self):
        self.disable()
        self.smiley.configure(state='disabled')

        self.tk_try_again_okno= Tk()
        self.tk_try_again_okno.title('Pavza')
        self.tk_try_again_okno.geometry()
        self.try_again_okno = Frame(self.tk_try_again_okno)

        Button(self.try_again_okno, text='Menu', command=self.na_zacetno_okno, padx=30).pack(side=LEFT, fill=X)
        Button(self.try_again_okno, text='Restart', command=self.restarti_igro, padx=30).pack(side=LEFT, fill=X)
        Button(self.try_again_okno, text='Resume', command= lambda x=self.tk_try_again_okno: self.enable(x), padx=30).pack(side=LEFT, fill=X)

        self.try_again_okno.pack(fill=X)
        self.tk_try_again_okno.protocol("WM_DELETE_WINDOW", lambda x=self.tk_try_again_okno: self.enable(x))
        self.tk_try_again_okno.mainloop()

    def za_konec_igre(self):
        self.disable()
        self.smiley.configure(image=self.slika_smiley_win, command=self.za_konec_igre, state='disabled')
        self.tk_konec_igre = Tk()
        self.highscore_okno = Frame(self.tk_konec_igre)
        Label(self.highscore_okno, text='Vpiši ime: ').pack(fill=X, side=LEFT)
        self.vpis_imena = Entry(self.highscore_okno)
        self.imeknof = Button(self.highscore_okno, text='Potrdi', command=self.vzemi_ime)
        self.imeknof.bind('<Return>', self.vzemi_ime)
        self.imeknof.pack(fill=X, side=RIGHT)
        self.vpis_imena.pack(fill=X, side=RIGHT)
        self.highscore_okno.pack(fill=X)

        self.tk_konec_igre.protocol("WM_DELETE_WINDOW", lambda x=self.tk_konec_igre: self.enable(x))
        self.tk_konec_igre.mainloop()

    def vzemi_ime(self, event=''):
        vzdevek = self.vpis_imena.get()
        if len(vzdevek) > 0 and len(vzdevek) < 10:
            self.zac_okno.vpisi_highscore(vzdevek, self.visina, self.sirina, self.stbomb)
            self.na_zacetno_okno(1)

    def na_zacetno_okno(self, sklopka = 0):
        self.tk_glavno_okno.destroy()
        if sklopka == 0:
            self.tk_try_again_okno.destroy()
        elif sklopka == 1:
            self.tk_konec_igre.destroy()
        Zacetno_okno(Tk())

    def restarti_igro(self):
        self.tk_glavno_okno.destroy()
        self.tk_try_again_okno.destroy()
        minolovec = Minolovec(self.visina, self.sirina, self.stbomb)
        Glavno_okno(Tk(), minolovec, self.zac_okno)

    def zamenjaj_slikco(self, event, i, j):
        self.gumbi[i][j].grid_remove()
        if self.zastavice[i][j] == 1:
            self.gumbi[i][j] = Button(self.okno_spodi, height=1, width=2, command=lambda x=i, y=j: self.odpri_polje(x, y))
            self.preostale_bombe += 1
            self.zastavice[i][j] = 0
            self.gumbi[i][j].grid(row=i, column=j)
            self.gumbi[i][j].bind('<Button-3>', lambda event, x=i, y=j: self.zamenjaj_slikco(event, x, y))
        elif self.zastavice[i][j] == 0:
            self.gumbi[i][j] = Button(self.okno_spodi, image=self.slika_zastavica, command=lambda x=i, y=j: self.odpri_polje(x, y))
            self.preostale_bombe -= 1
            self.zastavice[i][j] = 1
            self.gumbi[i][j].grid(row=i, column=j)
            self.gumbi[i][j].bind('<Button-3>', lambda event, x=i, y=j: self.zamenjaj_slikco(event, x, y))

        self.l_stbomb.config(text = str(self.preostale_bombe))

    def preveri_zastavice(self):
        for i in self.odprto:
            self.zastavice[i[0]][i[1]] = 0
        self.preostale_bombe = 0
        for i in self.zastavice:
            for j in i:
                if j == 1:
                    self.preostale_bombe += 1
        self.preostale_bombe = self.stbomb - self.preostale_bombe
        self.l_stbomb.config(text=str(self.preostale_bombe))

#naredi tabela za minolovca in naredi seznam seznamov skupnih ničel
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

    #odkrije polje ko uporabnik pritisne na gumb // klice Glavno_okno
    def odkrij(self, x, y):
        return str(self.tabela[x][y])

    #vrne nicle skupne z niclo pri (x,y) // klice Glavno_okno
    def vrni_otocec(self, nicla):
        for i in self.nicle:
            if nicla in i:
                return i

    # ZGENERIRA TABELO ZA IGRO
    def gen_tabelo(self):
        tabela1 = [[0]*self.sirina for _ in range(self.visina)]


        # vstavi bombe v tabelo
        listabomb = []
        st_vstavljenih_bomb = 0
        while st_vstavljenih_bomb < self.stbomb:
            i = int(uniform(0, self.visina))
            j = int(uniform(0, self.sirina))
            if tabela1[i][j] == 0 and not((i, j) in listabomb):
                tabela1[i][j] = -1
                listabomb.append((i,j))
                st_vstavljenih_bomb += 1

        # vstavi stevilke v tabelo
        for t in range(len(tabela1)):
            for u in range(len(tabela1[t])):
                stsosednjihbomb = self.okolica(tabela1, t, u)
                if stsosednjihbomb > 0 and tabela1[t][u] == 0:
                    tabela1[t][u] = stsosednjihbomb

        # naredi seznam seznamov točk skupnih ničel
        # najprej iz tabele dobi koordinate nicel v obliki (x, y) shranjeni v listi
        nicle = []
        for i in range(len(tabela1)):
            for j in range(len(tabela1[i])):
                if tabela1[i][j] == 0:
                    nicle.append((i, j))

        # zdruzi nicle v skupne liste z lastnostjo, da se nicle držijo skupi v tabeli
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
        return (tabela1, lista_nicel)

    # lepši izpis tabele // za konzolo
    def izpis_tabele(self):
        for i in self.tabela:
            a = ''
            for j in i:
                a += str(j) + '\t'
            print(a)

# ZAČETEK KLICANJA ====================================================================================000000001

Zacetno_okno(Tk())


