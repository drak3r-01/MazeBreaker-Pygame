from random import *
import random

class Maze:
    """
    Classe `Maze` (Labyrinthe) :
    Représentation d'un labyrithe sous forme d'un graphe non-orienté
    dont chaque sommet est une cellule (sous forme d'un tuple (l,c))
    et dont la structure est représentée par un dictionnaire :
    clefs = sommets, valeurs = ensemble des sommets voisins accessibles.
    """

    def __init__(self, height: int, width: int, empty: bool):
        """
        Le constructeur de cette classe créer un labyrinthe de `height` cellules de haut
        et de `width` cellules de large.
        Les voisinages sont initialisés par des ensembles vides.
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée.
        Paramètres:
            `height` (int)

            `width` (int)

            `empty` (bool).
        """
        self.height = height
        self.width = width

        # Si empty vaut True alors le constructeur initialise l'objet sans murs internes sinon il construit tous les murs

        if empty:
            self.neighbors = {
                (i, j): set() for i in range(height) for j in range(width)
            }
            for h in range(height):
                for w in range(width):
                    if h - 1 >= 0:
                        self.neighbors[(h, w)].add((h - 1, w))
                    if h + 1 <= height - 1:
                        self.neighbors[(h, w)].add((h + 1, w))
                    if w - 1 >= 0:
                        self.neighbors[(h, w)].add((h, w - 1))
                    if w + 1 <= width - 1:
                        self.neighbors[(h, w)].add((h, w + 1))
        else:
            self.neighbors = {
                (i, j): set() for i in range(height) for j in range(width)
            }

    def info(self) -> str:
        """
        Affichage des attributs d'un objet `Maze` (fonction utile pour deboguer).
        Retour:
            Chaîne de caractères (str) contenant une description textuelle des attributs de l'intance.
        """
        txt = f'{self.height} x {self.width}\n'
        txt += str(self.neighbors)
        return txt

    def __str__(self) -> str:
        """
        Représentation textuelle d'une intance de l'objet `Maze` (en utilisant des caractères ASCII).
        Retour:
             Chaîne de caractères (str) : chaîne de caractères représentant le labyrinthe
        :return:
        """
        txt = ''
        # Première ligne
        txt += '┏'
        for j in range(self.width - 1):
            txt += '━━━┳'
        txt += '━━━┓\n'
        txt += '┃'
        for j in range(self.width - 1):
            txt += (
                '   ┃' if (0, j + 1) not in self.neighbors[(0, j)] else '    '
            )
        txt += '   ┃\n'
        # Lignes normales
        for i in range(self.height - 1):
            txt += '┣'
            for j in range(self.width - 1):
                txt += (
                    '━━━╋'
                    if (i + 1, j) not in self.neighbors[(i, j)]
                    else '   ╋'
                )
            txt += (
                '━━━┫\n'
                if (i + 1, self.width - 1)
                not in self.neighbors[(i, self.width - 1)]
                else '   ┫\n'
            )
            txt += '┃'
            for j in range(self.width):
                txt += (
                    '   ┃'
                    if (i + 1, j + 1) not in self.neighbors[(i + 1, j)]
                    else '    '
                )
            txt += '\n'
        # Bas du tableau
        txt += '┗'
        for i in range(self.width - 1):
            txt += '━━━┻'
        txt += '━━━┛\n'

        return txt

    def add_wall(self, c1, c2) -> None:
        """
        Méthode d'instance permettant d'ajouter un mur entre les deux cases passées en paramètres si et seulement si les coordonnées sont
        cohérentes.

        Paramètres:
            `c1` (tuple) : première coordonnée rerpésentant une case.

            `c2` (tuple) : deuxième coordonnée rerpésentant une autre case.
        """
        # On teste si les sommets sont bien dans le labyrinthe
        assert (
            0 <= c1[0] < self.height
            and 0 <= c1[1] < self.width
            and 0 <= c2[0] < self.height
            and 0 <= c2[1] < self.width
        ), (
            "Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les "
            'dimensions du labyrinthe'
        )
        # Ajout du mur
        if c2 in self.neighbors[c1]:  # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2)  # on le retire
        if c1 in self.neighbors[c2]:  # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1)  # on le retire

        return None

    def remove_wall(self, c1, c2) -> None:
        """
        Méthode d'instance permettant de supprimer un mur entre les deux cases passées en paramètres si et seulement si les coordonnées sont
        cohérentes.
        Paramètres:
            `c1` (tuple) : première coordonnée rerpésentant une case.

            `c2` (tuple) : deuxième coordonnée rerpésentant une autre case.
        """
        # On teste si les sommets sont bien dans le labyrinthe
        assert (
            0 <= c1[0] < self.height
            and 0 <= c1[1] < self.width
            and 0 <= c2[0] < self.height
            and 0 <= c2[1] < self.width
        ), (
            "Erreur lors de la suppression d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec "
            'les dimensions du labyrinthe'
        )
        # Suppression du mur
        if (
            c2 not in self.neighbors[c1]
        ):  # Si c2 n'est pas dans les voisines de c1
            self.neighbors[c1].add(c2)  # on l'ajoute'
        if (
            c1 not in self.neighbors[c2]
        ):  # Si c3 n'est pas dans les voisines de c2
            self.neighbors[c2].add(c1)  # on l'ajoute
        return None

    def get_walls(self) -> list:
        """
        Méthode d'instance qui retourne la liste de tous les murs sous la forme d’une liste de tuple de cellules (
        sans redondance ou symétrie).
        """
        list_wall = []
        for h in range(self.height):
            for w in range(self.width):

                if (
                    h - 1 >= 0
                    and (h, w) not in self.neighbors[(h - 1, w)]
                    and (
                        ((h, w), (h - 1, w)) not in list_wall
                        and (
                            (h - 1, w),
                            (h, w),
                        )
                        not in list_wall
                    )
                ):
                    list_wall.append(((h, w), (h - 1, w)))

                if (
                    h + 1 <= self.height - 1
                    and (h, w) not in self.neighbors[(h + 1, w)]
                    and (
                        ((h, w), (h + 1, w))
                        and ((h + 1, w), (h, w)) not in list_wall
                    )
                ):
                    list_wall.append(((h, w), (h + 1, w)))

                if (
                    w - 1 >= 0
                    and (h, w) not in self.neighbors[(h, w - 1)]
                    and (
                        ((h, w), (h, w - 1)) not in list_wall
                        and ((h, w - 1), (h, w)) not in list_wall
                    )
                ):
                    list_wall.append(((h, w), (h, w - 1)))

                if (
                    w + 1 <= self.width - 1
                    and (h, w) not in self.neighbors[(h, w + 1)]
                    and (
                        ((h, w), (h, w + 1)) not in list_wall
                        and ((h, w + 1), (h, w)) not in list_wall
                    )
                ):
                    list_wall.append(((h, w), (h, w + 1)))

        return list_wall

    def fill(self) -> None:
        """
        Méthode d'instance qui ajoute tous les murs possibles dans un labyrinthe.
        """
        for h in range(self.height):
            for w in range(self.width):
                for voisin in self.neighbors[(h, w)].copy():
                    self.add_wall((h, w), voisin)
        return None

    def empty(self) -> None:
        """
        Méthode d'instance qui supprime tous les murs d'un labyrinthe.
        """
        list_wall = self.get_walls()
        for wall in list_wall:
            self.remove_wall(wall[0], wall[1])
        return None

    def get_contiguous_cells(self, c: tuple) -> list:
        """
        Méthode d'instance qui retourne la liste des cellules contigües à une cellule `c` (tuple) passée en paramètre dans la grille (sans s’occuper des
        éventuels murs).

        Paramètre:
            `c` (tuple) : coordonnées d'une cellule.

        Retour:
            Liste de toutes les cellules contigües à `c`.
        """
        list_contigue = []
        if c[0] - 1 >= 0:
            list_contigue.append((c[0] - 1, c[1]))
        if c[0] + 1 <= self.height - 1:
            list_contigue.append((c[0] + 1, c[1]))
        if c[1] - 1 >= 0:
            list_contigue.append((c[0], c[1] - 1))
        if c[1] + 1 <= self.width - 1:
            list_contigue.append((c[0], c[1] + 1))

        return list_contigue

    def get_reachable_cells(self, c: tuple) -> list:
        return list(self.neighbors[c].copy())

    def gen_btree(self, h: int, w: int) -> object:
        """
        Méthode d'instance qui génère un labyrinthe qui possède `h` lignes et `w`` colonnes en utilisant l’algorithme de
        construction par arbre binaire.

        Paramètres:
            `h` (int) : nombre de cases en hauteur du labyrinthe voulu.
            `w` (int) : nombre de cases en largeur du labyrinthe voulu.

        Retour:
            Retourne une instance de `Maze`.
        """
        new_maze = Maze(h, w, False)
        for h in range(new_maze.height):
            for w in range(new_maze.width):

                temp_wall = new_maze.get_walls()
                if (
                    random.choice([True, False])
                    and w + 1 <= new_maze.width - 1
                ):
                    if ((h, w), (h, w + 1)) in temp_wall:
                        new_maze.remove_wall((h, w), (h, w + 1))
                    elif h + 1 <= new_maze.height - 1:
                        new_maze.remove_wall((h, w), (h + 1, w))

                else:
                    if (
                        (h, w),
                        (h + 1, w),
                    ) in temp_wall and h + 1 <= new_maze.height - 1:
                        new_maze.remove_wall((h, w), (h + 1, w))
                    elif w + 1 <= new_maze.width - 1:
                        new_maze.remove_wall((h, w), (h, w + 1))

        return new_maze

    def gen_sidewinder(self, h: int, w: int) -> object:
        """
        Méthode d'instance qui génère un labyrinthe de `h` lignes et `w` colonnes en utilisant l’algorithme de construction
        Sidewinder.

        Paramètres:
            `h` (int) : nombre de cases en hauteur du labyrinthe voulu.
            `w` (int) : nombre de cases en largeur du labyrinthe voulu.

        Retour:
            Retourne une instance de `Maze`.
        """
        new_maze = Maze(h, w, False)

        for h in range(new_maze.height - 1):
            v_seq = []
            for w in range(new_maze.width - 1):
                v_seq.append((h, w))
                if random.choice([True, False]):
                    new_maze.remove_wall((h, w), (h, w + 1))
                else:
                    choix = random.choice(v_seq)
                    new_maze.remove_wall(choix, (choix[0] + 1, choix[1]))
                    v_seq.clear()
            v_seq.append((h, new_maze.width - 1))
            choix = random.choice(v_seq)
            new_maze.remove_wall(choix, (choix[0] + 1, choix[1]))

        for w in range(new_maze.width - 1):
            new_maze.remove_wall(
                (new_maze.height - 1, w), (new_maze.height - 1, w + 1)
            )
        return new_maze

    def gen_fusion(self, h, w) -> object:
        """
        Méthode d'instance qui génère un labyrinthe de `h` lignes et `w` colonnes parfait à l'aide de l’algorithme de fusion de chemins.

        Paramètres:
            `h` (int) : nombre de cases en hauteur du labyrinthe voulu.
            `w` (int) : nombre de cases en largeur du labyrinthe voulu.

        Retour:
            Retourne une instance de `Maze`.
        """
        new_maze = Maze(h, w, False)
        label = {(i, j): None for i in range(h) for j in range(w)}
        idx = 1
        for h in range(new_maze.height):
            for w in range(new_maze.width):
                # Ajout des label aux cellules
                label[(h, w)] = idx
                idx += 1
        list_wall = new_maze.get_walls()
        random.shuffle(list_wall)

        for wall in list_wall:
            if label[wall[0]] != label[wall[1]]:
                temp = label[wall[1]]
                for idx in label:
                    if label[idx] == temp:
                        label[idx] = label[wall[0]]
                new_maze.remove_wall(wall[0], wall[1])
        return new_maze

    def gen_exploration(self, h, w) -> object:
        """
        Methode d'instance qui génère un labyrinthe à `h` lignes et `w` colonnes parfait à l'aide de l’algorithme d’exploration exhaustive.

        Paramètres:
            `h` (int) : nombre de cases en hauteur du labyrinthe voulu.
            `w` (int) : nombre de cases en largeur du labyrinthe voulu.

        Retour:
            Retourne une instance de `Maze`.
        """
        new_maze = Maze(h, w, False)
        flag = {(i, j): False for i in range(h) for j in range(w)}
        pile = []
        temp = (random.randint(0, h - 1), random.randint(0, w - 1))
        pile.append(temp)
        flag[temp] = True
        while pile:
            temp = pile[len(pile) - 1]
            pile.pop(len(pile) - 1)
            temp_test = False
            temp_contiguous = new_maze.get_contiguous_cells(temp)
            for neighbors in temp_contiguous.copy():
                if not flag[neighbors]:
                    temp_test = True
                else:
                    temp_contiguous.remove(neighbors)
            if temp_test:
                pile.append(temp)
                choice = random.choice(temp_contiguous)
                new_maze.remove_wall(choice, temp)
                flag[choice] = True
                pile.append(choice)

        return new_maze

    def gen_wilson(self, h, w) -> object:
        """
        Methode d'instance qui génère un labyrinthe à `h` lignes et `w` colonnes parfait à l'aide de l’algorithme de Wilson.

        Paramètres:
            `h` (int) : nombre de cases en hauteur du labyrinthe voulu.
            `w` (int) : nombre de cases en largeur du labyrinthe voulu.

        Retour:
            Retourne une instance de `Maze`.
        """

        #Génération d'un labyrinthe plein
        new_maze = Maze(h, w, False)

        #Création de deux listes pour suivre les cellules marquer et non
        no_flag = [(i, j) for i in range(h) for j in range(w)]
        flag = [random.choice(no_flag)]

        # Jusqu'à fin du labyrinthe
        while no_flag:
            #1ʳᵉ celule du chemin
            path = [random.choice(no_flag)]

            # Génération d'un chemin
            new_path = False
            while not new_path:
                cell_voisine = new_maze.get_contiguous_cells(path[len(path) - 1])
                random.shuffle(cell_voisine)

                not_new = 0
                for cell in cell_voisine:
                    if cell in flag:
                        path.append(cell)
                        new_path = True
                        break
                    elif cell in path:
                        not_new += 1
                        continue
                    else:
                        path.append(cell)
                        break

                if not_new == len(cell_voisine):
                    path.clear()
                    break

            # Fin de la création d'un chemin
            if path:
                for i in range(len(path) - 1):
                    new_maze.remove_wall(path[i], path[i + 1])
                    flag.append(no_flag.pop(no_flag.index(path[i])))

                path.clear

        return new_maze


    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour:
            string
        """
        if content is None:
            content = {(i,j):' ' for i in range(self.height) for j in range(self.width)}
        else:
            # Python >=3.9
            #content = content | {(i, j): ' ' for i in range(
            #    self.height) for j in range(self.width) if (i,j) not in content}
            # Python <3.9
            new_content = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i,j) not in content}
            content = {**content, **new_content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += " "+content[(0,j)]+" ┃" if (0,j+1) not in self.neighbors[(0,j)] else " "+content[(0,j)]+"  "
        txt += " "+content[(0,self.width-1)]+" ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " "+content[(i+1,j)]+" ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else " "+content[(i+1,j)]+"  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt

    def solve_dfs(self, start:tuple, stop:tuple):
        """
        Méthode d'instance permettant de résoudre le labyrithe en "profondeur"

        Paramètres: 
            `start` (tuple) : cellule de départ du chemin
            `stop` (tuple) : celulle d'arrivée du chemin. 
        Retour: 
            `chemin` (list) : liste des coordonnées correspondant au chemin à parcourir.           
        """
        pile=[start]
        pred={}
        marked={}
        chemin=[]
        for i in range(self.height):
            for j in range(self.width):
                marked[(i,j)]=False
        marked[start]=True
        pred[start]=start
        while False in marked.values():
            c=pile.pop(0)
            if c==stop:
                break
            else :
                voisin=self.get_reachable_cells(c)
                for elt in voisin:
                    if marked[elt]==False :
                        marked[elt]=True
                        pile.insert(0,elt)
                        pred[elt]=c
        c=stop
        while c!=start:
            chemin.append(c)
            c=pred[c]
        chemin.append(start)
        return chemin

    def solve_bfs(self, start:tuple, stop:tuple):
        """
        Méthode d'instance permettant de résoudre le labyrithe en "profondeur"

        Paramètres: 
            `start` (tuple) : cellule de départ du chemin
            `stop` (tuple) : celulle d'arrivée du chemin. 
        Retour: 
            `chemin` (list) : liste des coordonnées correspondant au chemin à parcourir.           
        """
        file=[start]
        pred={}
        marked={}
        chemin=[]
        for i in range(self.height):
            for j in range(self.width):
                marked[(i,j)]=False
        marked[start]=True
        pred[start]=start
        while False in marked.values():
            c=file.pop(len(file)-1)
            if c==stop:
                break
            else :
                voisin=self.get_reachable_cells(c)
                for elt in voisin:
                    if marked[elt]==False :
                        marked[elt]=True
                        file.insert(0,elt)
                        pred[elt]=c
        c=stop
        while c!=start:
            chemin.append(c)
            c=pred[c]
        chemin.append(start)
        return chemin    

    def distance_geo(self, c1, c2):
        """
        Méthode d'instance permettant de trouver la plus courte distance géographique entre deux points à l'aide des algorithmes de résolution.
        Paramètres:
            `start` (tuple) : cellule de départ du chemin
            `stop` (tuple) : celulle d'arrivée du chemin. 
        Retour: 
            `len` (int) : plus courte distance à parcourir.  
        """
        resDfs=self.solve_dfs(c1,c2)
        resBfs=self.solve_bfs(c1,c2)
        #resRhr=self.solve_rhr(c1,c2)
        if len(resDfs)<len(resBfs) : # and len(resDfs) < len(resRhr):
            return len(resDfs)
        if len(resBfs)<len(resDfs) : # and len(resBfs) < len(resRhr):
            return len(resBfs)
        # if len(resRhr)<len(resBfs) : # and len(resRhr) < len(resDfs): return len(resRhr)

    def distance_man(self, c1, c2):
        """
        Méthode d'instance permettant de trouver la plus courte distance de Manhattan entre deux points à l'aide des algorithmes de résolution.
        Paramètres:
            `start` (tuple) : cellule de départ du chemin
            `stop` (tuple) : celulle d'arrivée du chemin. 
        Retour: 
            `len` (int) : plus courte distance à parcourir.  
        """
        return (c2[0]-c1[0])+(c2[1]-c1[1])