import tkinter
import time

class App:
    def __init__(self):
        self._nb_disques = 5 # Nombre de disques
        
        self._disques = [None] * self._nb_disques # Liste des disques

        # Listes des couleurs des disques
        self._COLORS = ['blue', 'red', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'grey']

        # Dictionnaire des tours
        self._tours = dict()
        self._tours['départ'] = [ j for j in range(self._nb_disques,0,-1) ] # Liste des disques sur la tour de départ
        self._tours['intermédiaire'] = [] # Liste des disques sur la tour intermédiaire
        self._tours['arrivée'] = [] # Liste des disques sur la tour d'arrivée

    # Initialisation de la fenetre et lancement de la boucle principale
    def main(self): 
        self._create_window()
        self._draw_grid()
        
        self._root.update()
        self.calcul_hanoi(self._nb_disques)
        
        self._root.mainloop()
        

    
    # Creation de la fenetre et du canvas
    def _create_window(self):
        self._root = tkinter.Tk() # Creation de la fenetre tkinter
        self._root.title("Tour hanoi Flaceliere Matthieu") # Titre de la fenetre

        self._canvas = tkinter.Canvas(self._root, width=530, height=500) # Creation du canvas avec les bonnes dimensions
        self._canvas.pack() # Organisation du canvas en pack

    # Affichage de l'état initial des tours sur le canvas
    def _draw_grid(self):
        self._canvas.create_rectangle(0, 470, 530, 500, fill='black')  # Base des tours
        # Création des tours
        for x in range(100,550,150):
            x0 = x
            y0 = 500
            x1 = x0 + 10
            y1 = 170
            self._canvas.create_rectangle(x0, y0, x1, y1, fill='black')
        
        # Création des disques
        taille = 50
        x = 0
        for y in range(440,(440 - 30 * self._nb_disques), -30):
            self._disques[x] = self._canvas.create_rectangle(taille, y, taille + (110 - 20 * x), y + 30, fill=self._COLORS[x])
            taille += 10
            x += 1


    # Calcul des déplacements
    # Algo d'hanoi récursif
    # procédure Hanoï(n, D, A, I)
    # si n ≠ 0
    #     Hanoï(n-1, D, I, A)
    #     Déplacer le disque de D vers A
    #     Hanoï(n-1, I, A, D)
    # fin-si
    # fin-procédure
    def calcul_hanoi(self,n,dep='départ',inter='intermédiaire',arr='arrivée'):
        if n==0:
            return        
        else:
            self.calcul_hanoi(n-1,dep,arr,inter)        
            disque_deplace = self._tours[dep].pop()
            self._tours[arr].append(disque_deplace)
            self.deplacement_disques(disque_deplace, self._tours[arr],dep, arr)
            self.calcul_hanoi(n-1,inter,dep,arr)

    # Update affichage des disques
    def deplacement_disques(self, x, tour,nom_tour_dep, nom_tour_arr):
        disque = self._disques[self._nb_disques - x] # Récupération du disque à déplacer
        self._canvas.move(disque,self.move_calculate_x(nom_tour_dep, nom_tour_arr), 0) # Déplacement du disque sur l'axe des x

        # Déplacement du disque sur l'axe des y
        x0, y0, x1, y1 = self._canvas.coords(disque)
        if len(tour) > 1:
            tlen = len(tour) - 1
            self._canvas.coords(disque, x0, 440 - tlen * 30, x1, 470 - tlen * 30)
        else:
            self._canvas.coords(disque, x0, 440, x1, 470)

        time.sleep(1)
        self._root.update()

    # Calcul du déplacement sur l'axe des x
    def move_calculate_x(self,nom_tour_dep, nom_tour_arr):
        if nom_tour_dep == 'départ' and nom_tour_arr == 'intermédiaire':
            return 150
        elif nom_tour_dep == 'départ' and nom_tour_arr == 'arrivée':
            return 300
        elif nom_tour_dep == 'intermédiaire' and nom_tour_arr == 'départ':
            return -150
        elif nom_tour_dep == 'intermédiaire' and nom_tour_arr == 'arrivée':
            return 150
        elif nom_tour_dep == 'arrivée' and nom_tour_arr == 'départ':
            return -300
        elif nom_tour_dep == 'arrivée' and nom_tour_arr == 'intermédiaire':
            return -150


#Lancement du programme
App().main()