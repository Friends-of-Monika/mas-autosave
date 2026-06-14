init -990 python:
    store.mas_submod_utils.Submod(
        author="Friends of Monika",
        name="Autosave",
        description=_("Automatic backing up to Github {b}{color=#ef4444}[[BETA]{/color}{/b}"),
        version="0.1.0",
        settings_pane="fom_autosave_settings"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Autosave",
            user_name="friends-of-monika",
            repository_name="mas-autosave",
            extraction_depth=2
        )
