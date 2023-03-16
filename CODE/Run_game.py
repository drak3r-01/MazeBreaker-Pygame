import pygame
import pickle
from .Maze import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Fonction

def get_input(score) -> str:
    """
    Fonction permetant de détecter les entrées faites via un périphérique par l'utilisateur.
    """
    fin = False
    name = ""

    while not fin:

        # Parcours des events
        for i in pygame.event.get():

            if i.type == pygame.KEYDOWN:

                if i.key == pygame.K_a:
                    name += "A"
                if i.key == pygame.K_b:
                    name += "B"
                if i.key == pygame.K_c:
                    name += "C"
                if i.key == pygame.K_d:
                    name += "D"
                if i.key == pygame.K_e:
                    name += "E"
                if i.key == pygame.K_f:
                    name += "F"
                if i.key == pygame.K_g:
                    name += "G"
                if i.key == pygame.K_h:
                    name += "H"
                if i.key == pygame.K_i:
                    name += "I"
                if i.key == pygame.K_j:
                    name += "J"
                if i.key == pygame.K_k:
                    name += "K"
                if i.key == pygame.K_l:
                    name += "L"
                if i.key == pygame.K_m:
                    name += "M"
                if i.key == pygame.K_n:
                    name += "N"
                if i.key == pygame.K_o:
                    name += "O"
                if i.key == pygame.K_p:
                    name += "P"
                if i.key == pygame.K_q:
                    name += "Q"
                if i.key == pygame.K_r:
                    name += "R"
                if i.key == pygame.K_s:
                    name += "S"
                if i.key == pygame.K_t:
                    name += "T"
                if i.key == pygame.K_u:
                    name += "U"
                if i.key == pygame.K_v:
                    name += "V"
                if i.key == pygame.K_w:
                    name += "W"
                if i.key == pygame.K_x:
                    name += "X"
                if i.key == pygame.K_y:
                    name += "Y"
                if i.key == pygame.K_z:
                    name += "Z"

                if i.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                if i.key == pygame.K_RETURN:
                    fin = True
                    break
            if i.type == pygame.QUIT:
                pygame.quit()
                exit()

        name = name[:10]
        fenetre.blit(img_fond, (0, 0))
        fenetre.blit(img_nom_resize, (fenetre.get_rect().center[0] - 370, fenetre.get_rect().center[1] - 318))
        fenetre.blit(font2.render("Maze Breaker DELUXE", True, (255, 200, 0)), (fenetre.get_rect().center[0] - 298, fenetre.get_rect().center[1] - 300))

        fenetre.blit(pygame.transform.scale(img_titre, (900, 100)), (fenetre.get_rect().center[0] - 450, fenetre.get_rect().center[1] - 67))
        fenetre.blit(font2.render("New High Score  " + str(score), True, "darkblue"), (fenetre.get_rect().center[0] - font2.render("New High Score  " + str(score), True, "gold", "lightskyblue").get_rect()[2] / 2, fenetre.get_rect().center[1] - 50))

        fenetre.blit(pygame.transform.scale(img_titre, (424, 100)), (fenetre.get_rect().center[0] - 212, fenetre.get_rect().center[1] + 57))
        if name:
            fenetre.blit(font2.render(name, True, "black"), (fenetre.get_rect().center[0] - font2.render(name, True, "gold", "lightskyblue").get_rect()[2] / 2, fenetre.get_rect().center[1] + 75))
        else:
            fenetre.blit(font2.render("Enter Name", True, "black"), (fenetre.get_rect().center[0] - font2.render("Enter Name", True, "gold", "lightskyblue").get_rect()[2] / 2, fenetre.get_rect().center[1] + 75))
        pygame.display.update()
    return name[:9]


def get_wallcoord_forlaby(maze : object, nb_ligne: int, nb_colonne: int) -> list:
    """
    Fonction permettant de modifier les coordonnées pour tout les murs (du à l'affichage en sprite du jeu) en retournant la liste de tout les murs modifiés.

    Retour:
        `list` : liste de tout les nouvelles coordonnées des murs.
    """
    # Ajout des murs
    murs = maze.get_walls()
    new_cord = []

    # Transformation des coordonées pour convenir au tableau
    for mur in murs:
        temp1 = 0
        temp2 = 0
        temp3 = 0
        temp4 = 0
        if mur[0][0] == 0:
            temp1 = mur[0][0] + 1
        else:
            temp1 = mur[0][0] * 2 + 1

        if mur[0][1] == 0:
            temp2 = mur[0][1] + 1
        else:
            temp2 = mur[0][1] * 2 + 1

        if mur[1][0] == 0:
            temp3 = mur[1][0] + 1
        else:
            temp3 = mur[1][0] * 2 + 1

        if mur[1][1] == 0:
            temp4 = mur[1][1] + 1
        else:
            temp4 = mur[1][1] * 2 + 1

        new_cord.append(((temp1, temp2), (temp3, temp4)))

    # Création des coordonnées des nouveaux murs
    new_murs = []
    for mur in new_cord:
        if mur[0][0] != mur[1][0]:
            if mur[0][0] < mur[1][0]:
                new_murs.append((mur[0][0] + 1, mur[0][1]))
            else:
                new_murs.append((mur[1][0] + 1, mur[1][1]))
        else:
            if mur[0][1] < mur[1][1]:
                new_murs.append((mur[0][0], mur[0][1] + 1))
            else:
                new_murs.append((mur[1][0], mur[1][1] + 1))

    for ligne in range(2, nb_ligne * 2, 2):
        for colonne in range(2, nb_colonne * 2, 2):
            new_murs.append((ligne, colonne))

    return new_murs


def addDiamond(murs_list: list, nb_ligne: int, nb_colone: int, nbDiamond: int, nbPetitDiamond: int) -> list:
    """
    Fonction permettant de placer des diamants (petit ou grand bonus rapportant plus ou moins de points) sur la grille du labyrinthe.

    Paramètres:
        - `murs_list` (list) : liste des murs du labyrinthe.
        - `nb_ligne` (int) : nombre de ligne du labyrinthe.
        - `nb_colone` (int) : nombre de colonnes du labyrithe.
        - `nbDiamond` (int) : nombre de grands diamants à placer sur la grille du labyrithe.
        - `nbPetitDiamond` (int) : nombre de petits diamants à placer sur la grille du labyrithe.
    """
    murs = murs_list
    listPetit = []
    listGros = []
    listCase = [(i, j) for i in range(1, nb_ligne * 2 - 1, 2) for j in range(1, nb_colone * 2 - 1, 2)]
    for i in range(nbDiamond):
        while True:
            coord = listCase[randint(0, len(listCase) - 1)]
            if coord not in murs and coord != (1, 1):
                listGros.append(coord)
                listCase.pop(listCase.index(coord))
                break
    for i in range(nbPetitDiamond):
        while True:
            coord = listCase[randint(0, len(listCase) - 1)]
            if coord not in murs and coord != (1, 1):
                listPetit.append(coord)
                listCase.pop(listCase.index(coord))
                break

    return [listGros, listPetit]

def display_score(nb_ligne, score: int) -> None:
    """
    Fonction permettant de calculer et afficher le score du joueur.
    """
    strt = "Score : " + str(score) + "    |    Time : " + str((round((pygame.time.get_ticks() - start_clock) / 1000, 2)))
    fenetre.blit(font.render(strt, True, "white", "goldenrod3"), (0, 26 * (nb_ligne * 2 - 1) + 95))
    pygame.display.update()
    return

def display_laby(nb_lignes: int, nb_colone: int, murlist, coord: tuple, direction_choix: int, list_diamond: list) -> None:
    """
    Fonction permettant de modifier le labyrinthe généré en labyrinthe prêt à être affiché.
    """
    Diamonds = list_diamond
    murs = murlist
    separation_vertical = 0

    fenetre.blit(img_fond, (0, 0))

    # Création du labyrinthe sans murs
    for ligne in range(nb_lignes + 1):
        separation_largeur = 0

        for colonne in range(nb_colone + 1):

            # Dessin du plateau vide
            if ligne == 0:
                fenetre.blit(img_murbord_resize, (separation_largeur, separation_vertical))

            elif ligne == nb_lignes:

                fenetre.blit(img_sol_resize, (separation_largeur, separation_vertical - 51 / resize + 22))
                fenetre.blit(img_murbord_resize, (separation_largeur, separation_vertical - 51 / resize))

            elif colonne == 0 or colonne == nb_colone:
                fenetre.blit(img_murbord_resize, (separation_largeur, separation_vertical - 51 / resize))

            else:
                fenetre.blit(img_sol_resize, (separation_largeur, separation_vertical))

            # Ajout du personnage
            if (ligne, colonne) == coord:
                fenetre.blit(direction[direction_choix], (separation_largeur, separation_vertical - 20))

            # Ajout des diamonds
            if (ligne, colonne) in Diamonds[0]:
                fenetre.blit(img_diamond_resize, (separation_largeur, separation_vertical - 25))
            elif (ligne, colonne) in Diamonds[1]:
                fenetre.blit(img_petitdiamond_resize, (separation_largeur, separation_vertical - 25))

            # Ajout fin
            if (ligne, colonne) == (nb_lignes - 1, nb_colone - 1):
                fenetre.blit(img_fin_resize, (separation_largeur, separation_vertical - 20))

            # Ajout des murs internes
            if (ligne, colonne) in murs:
                fenetre.blit(img_mur_resize, (separation_largeur, separation_vertical - 14))
            elif colonne % 2 == 0 and colonne != 0 and colonne - 1 != nb_colone - 1 and ligne % 2 == 0 and ligne != 0 and ligne - 1 != nb_lignes - 1:
                fenetre.blit(img_mur_resize, (separation_largeur, separation_vertical - 14))

            separation_largeur += 68 / resize

        if ligne == 0 or ligne == nb_lignes:
            separation_vertical += 98 / resize
        else:
            separation_vertical += 52 / resize

    return

def start_one_laby_game(ligne: int, colonne: int, score: int, start_clock: int) -> tuple:
    """
    Fonction permettant la gestion des contrôles et des collisions pendant une partie.
    """
    nb_ligne = ligne
    nb_colone = colonne
    coord_joueur = (1, 1)
    diamond_value = 5000
    petit_diamond_value = 2500

    maze = Maze.gen_wilson(None, nb_ligne, nb_colone)
    murs = get_wallcoord_forlaby(maze, nb_ligne, nb_colone)
    Diamonds = addDiamond(murs, nb_ligne, nb_colone, 40, 70)

    display_laby(nb_ligne * 2, nb_colone * 2, murs, coord_joueur, 2, Diamonds)
    pygame.display.update()


    # Mouvement de joueur
    fin = False
    while not fin:
        display_score(nb_ligne, score)

        # Parcours des events
        for i in pygame.event.get():

            # Si une touche presser
            if i.type == pygame.KEYDOWN:

                # Si fleche UP presser
                if i.key == pygame.K_UP:
                    if coord_joueur[0] != 1 and (coord_joueur[0] - 1, coord_joueur[1]) not in murs:
                        coord_joueur = (coord_joueur[0] - 1, coord_joueur[1])

                        # Gestion des diamonds
                        if coord_joueur in Diamonds[0]:
                            score += diamond_value
                            Diamonds[0].pop(Diamonds[0].index(coord_joueur))
                            pygame.mixer.Sound.play(sound_diamond)
                        elif coord_joueur in Diamonds[1]:
                            score += petit_diamond_value
                            Diamonds[1].pop(Diamonds[1].index(coord_joueur))
                            pygame.mixer.Sound.play(sound_diamond)

                        # Gestion de la fin
                        if coord_joueur == (nb_ligne * 2 - 1, nb_colone * 2 - 1):
                            pygame.mixer.Sound.play(sound_fin)
                            fin = True
                            break

                        display_laby(nb_ligne * 2, nb_colone * 2, murs, coord_joueur, 0, Diamonds)
                        display_score(nb_ligne, score)
                        pygame.display.update()
                    else:
                        display_laby(nb_ligne * 2, nb_colone * 2, murs, coord_joueur, 0, Diamonds)
                        display_score(nb_ligne, score)
                        pygame.display.update()

                # Si fleche droite presser
                if i.key == pygame.K_RIGHT:
                    if coord_joueur[1] != nb_colone * 2 - 1 and (coord_joueur[0], coord_joueur[1] + 1) not in murs:
                        coord_joueur = (coord_joueur[0], coord_joueur[1] + 1)

                        # Gestion des diamonds
                        if coord_joueur in Diamonds[0]:
                            score += diamond_value
                            Diamonds[0].pop(Diamonds[0].index(coord_joueur))
                            pygame.mixer.Sound.play(sound_diamond)
                        elif coord_joueur in Diamonds[1]:
                            score += petit_diamond_value
                            Diamonds[1].pop(Diamonds[1].index(coord_joueur))
                            pygame.mixer.Sound.play(sound_diamond)

                        # Gestion de la fin
                        if coord_joueur == (nb_ligne * 2 - 1, nb_colone * 2 - 1):
                            pygame.mixer.Sound.play(sound_fin)
                            fin = True
                            break

                        display_laby(nb_ligne * 2, nb_colone * 2, murs, coord_joueur, 1, Diamonds)
                        display_score(nb_ligne, score)
                        pygame.display.update()
                    else:
                        display_laby(nb_ligne * 2, nb_colone * 2, murs, coord_joueur, 1, Diamonds)
                        display_score(nb_ligne, score)
                        pygame.display.update()

                # Si fleche bas presser
                if i.key == pygame.K_DOWN:
                    if coord_joueur[0] + 1 != nb_ligne * 2 and (coord_joueur[0] + 1, coord_joueur[1]) not in murs:
                        coord_joueur = (coord_joueur[0] + 1, coord_joueur[1])

                        # Gestion des diamonds
                        if coord_joueur in Diamonds[0]:
                            score += diamond_value
                            Diamonds[0].pop(Diamonds[0].index(coord_joueur))
                            pygame.mixer.Sound.play(sound_diamond)
                        elif coord_joueur in Diamonds[1]:
                            score += petit_diamond_value
                            Diamonds[1].pop(Diamonds[1].index(coord_joueur))
                            pygame.mixer.Sound.play(sound_diamond)

                        # Gestion de la fin
                        if coord_joueur == (nb_ligne * 2 - 1, nb_colone * 2 - 1):
                            pygame.mixer.Sound.play(sound_fin)
                            fin = True
                            break

                        display_laby(nb_ligne * 2, nb_colone * 2, murs, coord_joueur, 2, Diamonds)
                        display_score(nb_ligne, score)
                        pygame.display.update()
                    else:
                        display_laby(nb_ligne * 2, nb_colone * 2, murs, coord_joueur, 2, Diamonds)
                        display_score(nb_ligne, score)
                        pygame.display.update()

                # Si fleche gauche presser
                if i.key == pygame.K_LEFT:
                    if coord_joueur[1] != 1 and (coord_joueur[0], coord_joueur[1] - 1) not in murs:
                        coord_joueur = (coord_joueur[0], coord_joueur[1] - 1)

                        # Gestion des diamonds
                        if coord_joueur in Diamonds[0]:
                            score += diamond_value
                            Diamonds[0].pop(Diamonds[0].index(coord_joueur))
                            pygame.mixer.Sound.play(sound_diamond)
                        elif coord_joueur in Diamonds[1]:
                            score += petit_diamond_value
                            Diamonds[1].pop(Diamonds[1].index(coord_joueur))
                            pygame.mixer.Sound.play(sound_diamond)

                        # Gestion de la fin
                        if coord_joueur == (nb_ligne * 2 - 1, nb_colone * 2 - 1):
                            pygame.mixer.Sound.play(sound_fin)
                            fin = True
                            break

                        display_laby(nb_ligne * 2, nb_colone * 2, murs, coord_joueur, 3, Diamonds)
                        display_score(nb_ligne, score)
                        pygame.display.update()
                    else:
                        display_laby(nb_ligne * 2, nb_colone * 2, murs, coord_joueur, 3, Diamonds)
                        display_score(nb_ligne, score)
                        pygame.display.update()

            display_score(nb_ligne, score)

        # Permet de quitter le jeu
            if i.type == pygame.QUIT:
                pygame.quit()
                exit()

    return (score, (pygame.time.get_ticks() - start_clock) / 1000)

def display_menu(choix: bool) -> None:
    """
    Fonction permettant la gestion du menu principal du jeu.
    """
    fenetre.blit(img_fond, (0, 0))
    fenetre.blit(img_logo_resize, (fenetre.get_rect().center[0] - 700, fenetre.get_rect().center[1] - 200))
    fenetre.blit(img_start_resize, (fenetre.get_rect().center[0] - 128, fenetre.get_rect().center[1] - 100))
    fenetre.blit(img_quit_resize, (fenetre.get_rect().center[0] - 128, fenetre.get_rect().center[1] + 30))

    fenetre.blit(img_nom_resize, (fenetre.get_rect().center[0] - 370, fenetre.get_rect().center[1] - 318))
    fenetre.blit(font2.render("Maze Breaker DELUXE", True, (255, 200, 0)), (fenetre.get_rect().center[0] - 298, fenetre.get_rect().center[1] - 300))


    # Display high player
    central = pygame.transform.scale(img_titre, (430, 50))
    fenetre.blit(central, (fenetre.get_rect().center[0] + 267, fenetre.get_rect().center[1] - 160))
    fenetre.blit(font.render("Top Player :", True, "darkblue"), (fenetre.get_rect().center[0] - font.render("Top Player :", True, "gold").get_rect()[2] / 2 + 482, fenetre.get_rect().center[1] - 147))


    central = pygame.transform.scale(img_titre, (430, 50))
    player = str(higth_player[list(higth_player)[0]]) + ": " + str(list(higth_player)[0])
    fenetre.blit(central, (fenetre.get_rect().center[0] + 267, fenetre.get_rect().center[1] - 70))
    fenetre.blit(font.render(player, True, "red"), (fenetre.get_rect().center[0] - font.render(player, True, "red").get_rect()[2] / 2 + 482, fenetre.get_rect().center[1] - 57))



    player = str(higth_player[list(higth_player)[1]]) + ": " + str(list(higth_player)[1])
    fenetre.blit(central, (fenetre.get_rect().center[0] + 267, fenetre.get_rect().center[1]))
    fenetre.blit(font.render(player, True, "yellow"), (fenetre.get_rect().center[0] - font.render(player, True, "yellow").get_rect()[2] / 2 + 482, fenetre.get_rect().center[1] + 13))




    player = str(higth_player[list(higth_player)[2]]) + ": " + str(list(higth_player)[2])
    fenetre.blit(central, (fenetre.get_rect().center[0] + 267, fenetre.get_rect().center[1] + 70))
    fenetre.blit(font.render(player, True, "lime"), (fenetre.get_rect().center[0] - font.render(player, True, "lime").get_rect()[2] / 2 + 482, fenetre.get_rect().center[1] + 83))


    if choix:
        fenetre.blit(img_fleche_resize, (fenetre.get_rect().center[0] - 250, fenetre.get_rect().center[1] - 100))
    else:
        fenetre.blit(img_fleche_resize, (fenetre.get_rect().center[0] - 250, fenetre.get_rect().center[1] + 30))

    pygame.display.update()
    return

def display_new(score: int) -> str:
    """
    Fonction permettant la gestion de l'écran de saisie du nouveau meilleur record (en fin de partie).
    """
    fenetre.blit(img_fond, (0, 0))
    fenetre.blit(img_nom_resize, (fenetre.get_rect().center[0] - 370, fenetre.get_rect().center[1] - 318))
    fenetre.blit(font2.render("Maze Breaker DELUXE", True, (255, 200, 0)), (fenetre.get_rect().center[0] - 298, fenetre.get_rect().center[1] - 300))

    fenetre.blit(img_nom_resize, (fenetre.get_rect().center[0] - 200, fenetre.get_rect().center[1] - 318))
    fenetre.blit(font2.render("New High Score  " + str(score), True, "gold", "lightskyblue"), (fenetre.get_rect().center[0] - 298, fenetre.get_rect().center[1] - 200))
    pygame.display.update()
    return get_input(score)
    

def display_end(score: int) -> None:
    """
    Fonction permettant la gestion de l'écran de fin de partie.
    """
    fenetre.blit(img_fond, (0, 0))
    fenetre.blit(img_nom_resize, (fenetre.get_rect().center[0] - 370, fenetre.get_rect().center[1] - 318))
    fenetre.blit(font2.render("Maze Breaker DELUXE", True, (255, 200, 0)), (fenetre.get_rect().center[0] - 298, fenetre.get_rect().center[1] - 300))

    fenetre.blit(pygame.transform.scale(img_titre, (700, 100)), (fenetre.get_rect().center[0] - 350, fenetre.get_rect().center[1] - 87))
    fenetre.blit(font2.render("GAME OVER", True, "red"), (fenetre.get_rect().center[0] - font2.render("GAME OVER", True, "gold").get_rect()[2] / 2, fenetre.get_rect().center[1] - 70))

    fenetre.blit(pygame.transform.scale(img_titre, (700, 100)), (fenetre.get_rect().center[0] - 350, fenetre.get_rect().center[1] + 50))
    fenetre.blit(font.render("Your Score : " + str(score), True, "black"), (fenetre.get_rect().center[0] - font.render("Your Score : " + str(score), True, "gold", "lightskyblue").get_rect()[2] / 2, fenetre.get_rect().center[1] + 88))
    pygame.display.update()

    time = pygame.time.get_ticks() / 1000 + 7
    while pygame.time.get_ticks() / 1000 <= time:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                exit()

def game():
    """
    Fonction permettant la gestion de la fenêtre graphique du jeu.
    """
    nb_ligne = 12
    nb_colonne = 22

    global resize
    resize = 2

    global fenetre
    fenetre = pygame.display.set_mode((34 * (nb_colonne * 2 + 1), 26 * (nb_ligne * 2 - 1) + 94 + 35))
    pygame.display.set_caption('Maze Breaker DELUXE')
    logo = pygame.image.load('./CODE/ASSET/LOGO.png')
    pygame.display.set_icon(logo)

    # Importation police
    global font
    font = pygame.font.Font('./CODE/ASSET/font.ttf', 32)
    global font2
    font2 = pygame.font.Font('./CODE/ASSET/titre.ttf', 64)

    # Importation des img
    img_sol = pygame.image.load("./CODE/ASSET/sol.png").convert_alpha()
    img_murbord = pygame.image.load("./CODE/ASSET/murbord.png").convert_alpha()
    img_mur = pygame.image.load("./CODE/ASSET/mur.png").convert_alpha()

    img_joueurbas = pygame.image.load("./CODE/ASSET/herobas.png").convert_alpha()
    img_joueurdroite = pygame.image.load("./CODE/ASSET/herodroite.png").convert_alpha()
    img_joueurhaut = pygame.image.load("./CODE/ASSET/herohaut.png").convert_alpha()
    img_joueurgauche = pygame.image.load("./CODE/ASSET/herogauche.png").convert_alpha()

    img_petitdiamond = pygame.image.load("./CODE/ASSET/petitdiamond.png")
    img_diamond = pygame.image.load("./CODE/ASSET/diamond.png")

    img_fin = pygame.image.load("./CODE/ASSET/exit.png")

    global img_fond
    img_fond = pygame.image.load("./CODE/ASSET/fond.png")

    img_start = pygame.image.load("./CODE/ASSET/start.png")
    img_quit = pygame.image.load("./CODE/ASSET/quit.png")
    img_fleche = pygame.image.load("./CODE/ASSET/fleche.png")
    global img_titre
    img_titre = pygame.image.load("./CODE/ASSET/titre.png")


    # Re dimension
    global img_sol_resize
    img_sol_resize = pygame.transform.scale(img_sol, (69/resize, 98/resize))
    global img_murbord_resize
    img_murbord_resize = pygame.transform.scale(img_murbord, (69 / resize, 98 / resize))
    global img_mur_resize
    img_mur_resize = pygame.transform.scale(img_mur, (69 / resize, 66 / resize))

    img_joueurbas_resize = pygame.transform.scale(img_joueurbas, (69 / resize, 69 / resize))
    img_joueurdroite_resize = pygame.transform.scale(img_joueurdroite, (69 / resize, 69 / resize))
    img_joueurhaut_resize = pygame.transform.scale(img_joueurhaut, (69 / resize, 69 / resize))
    img_joueurgauche_resize = pygame.transform.scale(img_joueurgauche, (69 / resize, 69 / resize))

    global img_petitdiamond_resize
    img_petitdiamond_resize = pygame.transform.scale(img_petitdiamond, (69 / resize, 69 / resize))
    global img_diamond_resize
    img_diamond_resize = pygame.transform.scale(img_diamond, (69 / resize, 69 / resize))

    global img_fin_resize
    img_fin_resize = pygame.transform.scale(img_fin, (69 / resize, 69 / resize))

    global img_logo_resize
    img_logo_resize = pygame.transform.scale(logo, (400, 400))
    global img_start_resize
    img_start_resize = pygame.transform.scale(img_start, (256, 112))
    global img_quit_resize
    img_quit_resize = pygame.transform.scale(img_quit, (256, 112))
    global img_fleche_resize
    img_fleche_resize = pygame.transform.scale(img_fleche, (112, 112))
    global img_nom_resize
    img_nom_resize = pygame.transform.scale(img_titre, (740, 100))


    # Création des directions
    global direction
    direction = (img_joueurhaut_resize, img_joueurdroite_resize, img_joueurbas_resize, img_joueurgauche_resize)

    # Importation des sons
    global sound_fin
    sound_fin = pygame.mixer.Sound("./CODE/ASSET/finlevel.wav")
    global sound_diamond
    sound_diamond = pygame.mixer.Sound("./CODE/ASSET/diamond.wav")
    score = 0

    global sound_menu
    sound_menu = pygame.mixer.Sound("./CODE/ASSET/menu_click.wav")
    global sound_menu2
    sound_menu2 = pygame.mixer.Sound("./CODE/ASSET/menu_click2.wav")

    global higth_player
    # Lancement Jeu
    while True:
        # display_end(score)
        """
        # Reset Save
        higth_player = {100000: "Nobody 1", 200000: "Nobody 2", 300000: "Nobody 3"}
        with open('./CODE/Save.pkl', 'wb') as f:
            pickle.dump(higth_player, f)
        """

        # Lecture de la save
        with open('./CODE/Save.pkl', 'rb') as f:
            higth_player = pickle.load(f)
        higth_player = dict(sorted(higth_player.items(), reverse = True))

        # Gestion de la save
        print(higth_player)
        for testscore in higth_player.copy():
            if score > testscore:
                higth_player[score] = display_new(score)
                higth_player = dict(sorted(higth_player.items(), reverse=True))
                higth_player.pop(list(higth_player)[3])
                break
        higth_player = dict(sorted(higth_player.items(), reverse=True))

        # Écriture de la save
        with open('./CODE/Save.pkl', 'wb') as f:
            pickle.dump(higth_player, f)
        print(higth_player)

        pygame.mixer.music.load("./CODE/ASSET/music_menu.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # Lancement menu
        choix = True
        menu = True
        while menu:
            display_menu(choix)
            for i in pygame.event.get():

                if i.type == pygame.KEYDOWN:

                    # Si fleche UP presser
                    if i.key == pygame.K_UP or i.key == pygame.K_DOWN:
                        choix = not choix
                        pygame.mixer.Sound.play(sound_menu)

                    if i.key == pygame.K_SPACE or i.key == pygame.K_RETURN:
                        if choix:
                            menu = False
                            pygame.mixer.Sound.play(sound_menu2)
                        else:
                            pygame.quit()
                            exit()

                if i.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        # Début Partie

        # Lancement de la musique
        pygame.mixer.music.load("./CODE/ASSET/music_game.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # Fin importation

        time = 0
        score = 0
        # Gestion du temps START
        global start_clock
        start_clock = pygame.time.get_ticks()
        # Gestion de l'enchainement de 3 platos
        for i in range(5):
            var_fin_plato = start_one_laby_game(nb_ligne, nb_colonne, score, start_clock)
            score = var_fin_plato[0]
            time = var_fin_plato[1]
        print(score, time)
        score = int(round(score - 5555.5 * time + 2000000, 0))
        print(score, time)
        # Fin partie
        display_end(score)
