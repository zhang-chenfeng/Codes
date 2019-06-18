import cx_Freeze

executables = [cx_Freeze.Executable("Main.py")]

cx_Freeze.setup(
    name = "Hit The Frogs",
    options = {"build_exe": {"packages": ["pygame"],
                             "include_files":["ban.png",
                                               "chunk.png",
                                               "d_hit.png",
                                               "d_idle.png",
                                               "dock.png",
                                               "eye.png",
                                               "frog_2x_1.png",
                                               "frog_die.wav",
                                               "Highscore.txt",
                                               "organ.png",
                                               "sound.wav",
                                               "stain.png",
                                               "sun.png"]}},
    executables = executables
    )
