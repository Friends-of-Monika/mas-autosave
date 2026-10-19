# This file is part of Autosave Submod (see link below):
# https://github.com/friends-of-monika/mas-autosave

python early in _fom_autosave_persistent:
    import renpy

    def get_persistent_path():
        loadsave_loc = renpy.loadsave.location
        if hasattr(loadsave_loc, "locations"):
            return loadsave_loc.active_locations()[0].persistent
        return loadsave_loc.persistent
