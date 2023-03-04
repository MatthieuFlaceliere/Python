import tkinter
from copy import deepcopy

# Classe représentant la grille
class Grid:
    # Création de la grille avec des cellules,  True == VIVANTE, False == MORT
    def __init__(self, n):
        self._lenght_grille = n # nombre de cellules par ligne/colonne
        self._cells = [] # liste représentant la grille

        # Remplissant la grille avec des cellules mortes
        for x in range(self._lenght_grille):
            self._cells.append([])
            for _ in range(self._lenght_grille):
                self._cells[x].append(False)
        
        # Remplissage de la grille avec des cellules vivantes
        self._cells[5][6] = True
        self._cells[6][6] = True
        self._cells[7][6] = True
        self._cells[6][8] = True
        self._cells[6][9] = True

    # Retourne l'état de la cellule à la position (x, y)
    def cell_etat(self, x, y):
        return self._cells[x][y]

    # Met à jour l'état de la grille
    def update(self):
        self._new_cells = deepcopy(self._cells) # copie de la grille actuelle
        self._cell_chnagees = [] # list (x,y) des cellules qui ont changé d'état

        self._update_cells() # Simulation du jeu de la vie

        self._cells = self._new_cells # Remplacement de la grille actuelle par la nouvelle grille
        return self._cell_chnagees

    # Met à jour l'état de chaque cellule basé sur les règles du jeu de la vie
    def _update_cells(self):
        for x in range(self._lenght_grille):
            for y in range(self._lenght_grille):
                nbVoisin = self._nombre_voisin(x, y)
                if self.cell_etat(x, y):
                    # Si la cellule est vivante et qu'elle a moins de 2 voisins ou plus de 3 voisins, elle meurt
                    if nbVoisin < 2 or nbVoisin > 3:
                        self._switch_cell_etat(x, y) 
                elif nbVoisin == 3:
                    # Si la cellule est morte et qu'elle a 3 voisins, elle devient vivante
                    self._switch_cell_etat(x, y)
    
    # Change l'état d'une cellule True -> False, False -> True
    def _switch_cell_etat(self, x, y):
        self._new_cells[x][y] = not self.cell_etat(x, y)
        self._cell_chnagees.append((x, y))

    # Conte le nombre de cellules vivantes autour d'une cellule
    def _nombre_voisin(self, x, y):
        top = (x - 1) % self._lenght_grille
        gauche = (y - 1) % self._lenght_grille
        droite = (y + 1) % self._lenght_grille
        bas = (x + 1) % self._lenght_grille

        nbVoisin = 0
        nbVoisin += int(self.cell_etat(top, gauche))
        nbVoisin += int(self.cell_etat(top, y))
        nbVoisin += int(self.cell_etat(top, droite))
        nbVoisin += int(self.cell_etat(x, gauche))
        nbVoisin += int(self.cell_etat(x, droite))
        nbVoisin += int(self.cell_etat(bas, gauche))
        nbVoisin += int(self.cell_etat(bas, y))
        nbVoisin += int(self.cell_etat(bas, droite))

        return nbVoisin

# Classe principale
class App:
    def __init__(self):
        # Definition des couleurs
        self._COLOR_VIE = 'black'
        self._COLOR_MORT = 'white'

        self._n = 20 # nombre de cellules par ligne/colonne
        self._cell_taille = 24 # taille d'une cellule en pixels

        self._grid = Grid(self._n)

    # Initialisation de la fenetre et lancement de la boucle principale
    def main(self):
        self._create_window()
        self._draw_grid()
        self._play()

        self._root.mainloop()
    
    # Creation de la fenetre et du canvas
    def _create_window(self):
        self._root = tkinter.Tk() # Creation de la fenetre tkinter
        self._root.title("Jeu de la vie Flaceliere Matthieu") # Titre de la fenetre

        canvasTaille = self._n * self._cell_taille # Calcul de la taille du canvas par rapport au nombre de cellules et a la taille d'une cellule
        self._canvas = tkinter.Canvas(self._root, width=canvasTaille, height=canvasTaille) # Creation du canvas avec les bonnes dimensions
        self._canvas.pack() # Organisation du canvas en pack
        

    # Affichage de l'état initial de la grille sur le canvas
    def _draw_grid(self):
        for x in range(self._n):
            for y in range(self._n):
                x0 = x * self._cell_taille
                y0 = y * self._cell_taille
                x1 = x0 + self._cell_taille
                y1 = y0 + self._cell_taille
                if self._grid.cell_etat(x, y):
                    color = self._COLOR_VIE
                else:
                    color = self._COLOR_MORT
                self._canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    # Fonction pour débuter la boucle de jeu
    def _play(self):
        self._root.after(500, self._play) # Appel de la fonction _play dans 500ms pour créer une boucle

        pos_cells_change = self._grid.update() # Récupération de la position des cellules qui ont changé d'état
        # Changement de la couleur des cellules qui ont changé d'état
        for cell in pos_cells_change:
            x, y = cell
            id = (x * self._n) + y + 1
            if self._grid.cell_etat(x, y):
                self._canvas.itemconfig(id, fill=self._COLOR_VIE)
            else:
                self._canvas.itemconfig(id, fill=self._COLOR_MORT)


#Lancement du programme
App().main()