init -999 python in _fom_autosave_lib:
    from store import fom_getScriptDir
    import sys

    fom_autosave_lib_path = renpy.config.basedir + "/" + fom_getScriptDir(fallback="game/Submods/Autosave") + "/lib"
    if fom_autosave_lib_path not in sys.path:
        sys.path.insert(0, fom_autosave_lib_path)
