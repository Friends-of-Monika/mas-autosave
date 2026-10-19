# This file is part of Autosave Submod (see link below):
# https://github.com/friends-of-monika/mas-autosave

screen fom_autosave_screens__confirm(**properties):
    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")
    modal True
    zorder 200

    key "mas_game_menu" action NullAction()

    frame:
        vbox:
            align (0.5, 0.5)
            xfill True
            properties dict(properties)
            transclude
