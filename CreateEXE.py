from cx_Freeze import setup, Executable

executables = [
    Executable(script="__main__.py", icon="./CODE/ASSET/LOGO.ico", base="Win32GUI")
]

buildOptions = dict(
    # Module python utilisé
    includes=["random", "pickle", "pygame"],
    # Fichier python / asset
    include_files=["./CODE/ASSET/diamond.png",
                   "./CODE/ASSET/diamond.wav",
                   "./CODE/ASSET/exit.png",
                   "./CODE/ASSET/finlevel.wav",
                   "./CODE/ASSET/fleche.png",
                   "./CODE/ASSET/fond.png",
                   "./CODE/ASSET/font.ttf",
                   "./CODE/ASSET/herobas.png",
                   "./CODE/ASSET/herodroite.png",
                   "./CODE/ASSET/herogauche.png",
                   "./CODE/ASSET/herohaut.png",
                   "./CODE/ASSET/LOGO.png",
                   "./CODE/ASSET/menu_click.wav",
                   "./CODE/ASSET/menu_click2.wav",
                   "./CODE/ASSET/mur.png",
                   "./CODE/ASSET/murbord.png",
                   "./CODE/ASSET/music_game.mp3",
                   "./CODE/ASSET/music_menu.mp3",
                   "./CODE/ASSET/petitdiamond.png",
                   "./CODE/ASSET/quit.png",
                   "./CODE/ASSET/sol.png",
                   "./CODE/ASSET/start.png",
                   "./CODE/ASSET/titre.png",
                   "./CODE/ASSET/titre.ttf",
                   "./CODE/Save.pkl",
                   "./CODE/Maze.py",
                   "./CODE/Run_game.py"
                   ]
)

setup(
    name="Maze Breaker DELUXE",
    version="1.0",
    description="Jeu Maze Breaker DELUXE",
    author="Drak3r-01",
    options=dict(build_exe=buildOptions),
    executables=executables
)
