default persistent._fom_autosave_config_common = None

init -1000 python:
    if persistent._fom_autosave_config_common is None:
        persistent._fom_autosave_config_common = {
            "backup_freq": 1,
            "on_exit": False,
            "show_load_warning": True
        }

init -978 python in _fom_autosave_config:
    from store import mas_registerAPIKey
    from store import persistent

    def on_github_key_change(api_key):
        persistent._fom_autosave_config_github["repo_name"] = ""
        return True, ""

    KEY_ID_GITHUB = "fom_autosave_config_github_apikey"
    mas_registerAPIKey(KEY_ID_GITHUB, _("[[Autosave] Github API token"), on_change=on_github_key_change)


screen fom_autosave_settings():
    $ tooltip_disp   = renpy.get_screen("submods", "screens").scope["tooltip"]
    $ backend        = persistent._fom_autosave_config_common.get("backend", "github")
    $ backup_class   = store._fom_autosave_common.get_backup_class()
    $ backup_service = backup_class(reason=_("forced save")) if backup_class else None
    $ is_configured  = backup_service.is_configured() if backup_service else False
    $ can_save       = store._fom_autosave_common.is_safe_to_backup()

    if persistent._fom_autosave_last_save:
        $ last_backup = persistent._fom_autosave_last_save.strftime("%Y-%m-%d at %H:%M:%S")
    else:
        $ last_backup = None

    vbox:
        style_prefix "check"
        xmaximum 900
        xfill True

        text _("Feeling confused and need help setting up? {b}Click {a=https://github.com/Friends-of-Monika/mas-autosave?tab=readme-ov-file#-configuring}here{/a}.{/b}")
        null height 10

        # Backend picker
        text _("Storage backend (only one can be used):")
        hbox spacing 5:
            textbutton _("Cloud storage"):
                selected backend == "cloud"
                action SetDict(persistent._fom_autosave_config_common, "backend", "cloud")
            textbutton _("Github"):
                selected backend == "github"
                action SetDict(persistent._fom_autosave_config_common, "backend", "github")

        null height 10

        # GitHub-specific config
        if backend == "github":
            $ github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
            $ repo_name      = persistent._fom_autosave_config_github.get("repo_name", None)

            text _("Github setup checklist:")
            hbox:
                if github_api_key:
                    text _("- API token {color=#84cc16}is set{/color}")
                else:
                    text _("- API token {color=#ef4444}is not set{/color}")

                textbutton _("Open API keys menu"):
                    action Show("mas_apikeys")
                    hovered SetField(tooltip_disp, "value", _("Click to open API keys menu."))
                    unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                    xoffset -12

            hbox:
                if repo_name:
                    text _("- Repository {color=#84cc16}is set{/color}{space=10}([repo_name])")
                else:
                    text _("- Repository {color=#ef4444}is not selected{/color}")

                textbutton _("Select repository"):
                    sensitive bool(github_api_key)
                    action Show("fom_autosave_settings__repo_select")
                    hovered SetField(tooltip_disp, "value", _("Click to select repository to use for backing up."))
                    unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                    xoffset -12

            if can_save:
                text _("- There are {color=#84cc16}no issues{/color} blocking backups")

            if store.mas_globals.tt_detected:
                text _("- {b}{color=#ef4444}Time travel{/color}{/b} detected")

            if persistent._mas_load_in_finalfarewell_mode:
                text _("- {b}{color=#ef4444}Monika has left{/color}{/b}")

            if persistent._mas_moni_chksum is not None:
                text _("- Monika is away")

        # Cloud storage-specific config
        elif backend == "cloud":
            $ cloud_key_set = bool(persistent._fom_autosave_config_cloud.get("user_key", ""))

            text _("Cloud storage setup checklist:")
            hbox:
                if cloud_key_set:
                    text _("- Backup code {color=#84cc16}is set{/color}")
                else:
                    text _("- Backup code {color=#ef4444}is not configured{/color}")

                if cloud_key_set:
                    textbutton _("Show backup code"):
                        action Show("fom_autosave_settings__cloud_setup", None, False)
                        hovered SetField(tooltip_disp, "value", _("Click to view your cloud backup code."))
                        unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                        xoffset -12

                    textbutton _("Reset code"):
                        action Function(store._fom_autosave_cloud.clear_user_key)
                        hovered SetField(tooltip_disp, "value", _("Click to clear the current backup code."))
                        unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                else:
                    textbutton _("Generate backup code"):
                        action [
                            Function(store._fom_autosave_cloud.generate_user_key),
                            Show("fom_autosave_settings__cloud_setup", None, True)
                        ]
                        hovered SetField(tooltip_disp, "value", _("Click to generate a new cloud backup code."))
                        unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                        xoffset -12

                    textbutton _("Restore backup code"):
                        action Show("fom_autosave_settings__cloud_restore")
                        hovered SetField(tooltip_disp, "value", _("Click to restore a backup code from another device."))
                        unhovered SetField(tooltip_disp, "value", tooltip_disp.default)

            if can_save:
                text _("- There are {color=#84cc16}no issues{/color} blocking backups")

            if store.mas_globals.tt_detected:
                text _("- {b}{color=#ef4444}Time travel{/color}{/b} is detected in this session.")

            if persistent._mas_moni_chksum is not None:
                text _("- {b}{color=#ef4444}Monika is away{/color}{/b} — backups are disabled while she is out.")

            if persistent._mas_load_in_finalfarewell_mode:
                text _("- {b}{color=#ef4444}Final farewell{/color}{/b} has occurred — backups are disabled.")

        null height 10

        # Shared: frequency + on-exit (apply to whichever backend is active)
        hbox:
            use fom_autosave_settings__slider(
                title=_("Backup frequency"),
                value=DictValue(persistent._fom_autosave_config_common, "backup_freq", offset=0, range=len(store._fom_autosave_timer.BACKUP_FREQ) - 1),
                display=store._fom_autosave_timer.BACKUP_FREQ[persistent._fom_autosave_config_common["backup_freq"]][0],
                tooltip=_("You can set automatic backup frequency by adjusting this slider."))

            textbutton _("Save on goodbye"):
                selected persistent._fom_autosave_config_common["on_exit"]
                action ToggleDict(persistent._fom_autosave_config_common, "on_exit")
                hovered SetField(tooltip_disp, "value", _("You can toggle automatic backup on 'Goodbye' by clicking here."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)

        if last_backup:
            text _("Last successful backup was on [last_backup]")

        null height 10

        $ load_action = Show("fom_autosave_settings__commit_select") if backend == "github" else Show("fom_autosave_settings__version_select")

        hbox:
            textbutton _("Force save"):
                sensitive is_configured
                if can_save:
                    action Show("fom_autosave_settings__force_save", None, backup_service)
                else:
                    action Show("fom_autosave_settings__timetravel_error")

                hovered SetField(tooltip_disp, "value", _("Click to force save the persistent."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                xoffset -22

            textbutton _("Load persistent"):
                sensitive is_configured
                action load_action
                hovered SetField(tooltip_disp, "value", _("Click to select saved persistent to load."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                xoffset -32

screen fom_autosave_settings__repo_select():
    default github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
    default promise = store._fom_autosave_task.AsyncTask(store._fom_autosave_github.get_own_repos, github_api_key)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)
    modal True
    zorder 200

    default back_action = Hide("fom_autosave_settings__repo_select")

    default repos = None
    default error = None

    python:
        try:
            if promise.is_complete():
                status, repos = promise.get()
        except Exception as e:
            if error is None:
                store._fom_autosave_logging.logger.error(_("Failed to load repositories: {0}"), e)
                error = e

    use fom_autosave_screens__confirm(xmaximum=500, ymaximum=400, spacing=30):
        style_prefix "confirm"

        text _("Select repository"):
            style "confirm_prompt"
            xalign 0.5

        if not promise.is_complete():
            text _("Loading..."):
                xalign 0.5
                text_align 0.5

        elif error is not None:
            text _("Failed to load repositories. Check logs."):
                xalign 0.5
                text_align 0.5

        else:
            hbox:
                viewport id "repos":
                    xalign 0.5
                    xfill True
                    yfill True

                    mousewheel True
                    draggable True

                    vbox:
                        for repo in repos:
                            textbutton repo["name"] action ([
                                SetDict(persistent._fom_autosave_config_github, "repo_owner", repo["owner"]["login"]),
                                SetDict(persistent._fom_autosave_config_github, "repo_name", repo["name"]),
                                Hide("fom_autosave_settings__repo_select")
                            ])

                vbar value YScrollValue("repos")

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Back"):
                action back_action
                sensitive promise.is_complete()

    if promise.is_complete():
        key "K_ESCAPE" action back_action

screen fom_autosave_settings__force_save(backup_service):
    default promise = store._fom_autosave_task.AsyncTask(backup_service.upload)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)
    modal True
    zorder 200

    default ok_action = Hide("fom_autosave_settings__force_save")

    default error = None

    python:
        try:
            if promise.is_complete():
                promise.get()
        except Exception as e:
            if error is None:
                store._fom_autosave_logging.logger.error(_("Failed to upload save: {0}"), e)
                error = e

    use fom_autosave_screens__confirm(xmaximum=400, ymaximum=200, spacing=30):
        style_prefix "confirm"

        text _("Force save"):
            style "confirm_prompt"
            xalign 0.5

        if not promise.is_complete():
            text _("Saving..."):
                xalign 0.5
                text_align 0.5
        elif error is not None:
            text _("Failed to save. Check logs."):
                xalign 0.5
                text_align 0.5
        else:
            text _("Saved!"):
                xalign 0.5
                text_align 0.5

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Back"):
                action ok_action
                sensitive promise.is_complete()

    if promise.is_complete():
        key "K_ESCAPE" action ok_action
        key "K_RETURN" action ok_action

screen fom_autosave_settings__slider(title, value, display, tooltip):
    $ tooltip_disp = renpy.get_screen("submods", "screens").scope["tooltip"]
    hbox spacing 10:
        text title
        bar value value style "slider_slider" xsize 200:
            hovered SetField(tooltip_disp, "value", tooltip)
            unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
        text display

screen fom_autosave_settings__commit_select():
    default github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
    default backup_service = store._fom_autosave_github.GithubBackup(None)
    default promise = store._fom_autosave_task.AsyncTask(store._fom_autosave_github.list_commits,
        repo_owner=persistent._fom_autosave_config_github["repo_owner"],
        repo_name=persistent._fom_autosave_config_github["repo_name"],
        repo_path="persistent",
        token=github_api_key)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)
    modal True
    zorder 200

    default back_action = Hide("fom_autosave_settings__commit_select")

    default commits = None
    default error = None

    python:
        try:
            if promise.is_complete():
                status, commits = promise.get()
        except Exception as e:
            if error is None:
                store._fom_autosave_logging.logger.error(_("Failed to load saves: {0}"), e)
                error = e

    use fom_autosave_screens__confirm(xmaximum=800, ymaximum=400, spacing=30):
        style_prefix "confirm"

        text _("Load persistent"):
            style "confirm_prompt"
            xalign 0.5

        if not promise.is_complete():
            text _("Loading..."):
                xalign 0.5
                text_align 0.5

        elif error is not None:
            text _("Failed to load saves. Check logs."):
                xalign 0.5
                text_align 0.5

        else:
            hbox:
                viewport id "commits":
                    xalign 0.5
                    xfill True
                    yfill True

                    mousewheel True
                    draggable True

                    vbox spacing 10:
                        for commit in commits:
                            $ commit_name = commit["commit"]["message"]
                            $ commit_date = datetime.datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
                            $ commit_date_friendly = commit_date.strftime("%Y-%m-%d at %H:%M:%S")
                            $ commit_sha = commit["sha"]

                            vbox:
                                textbutton "[commit_name!q]" action ([
                                    Hide("fom_autosave_settings__commit_select"),
                                    SetField(backup_service, "commit", commit_sha),
                                    Show("fom_autosave_settings__load_commit", None, backup_service)])

                                text _("{size=-6}Uploaded on [commit_date_friendly]{/size}") xoffset 5
                                text "{alpha=0.5}{size=-10}[commit_sha]{/size}{/alpha}" xoffset 5

                vbar value YScrollValue("commits")

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Back"):
                action back_action
                sensitive promise.is_complete()

    if promise.is_complete():
        key "K_ESCAPE" action back_action

screen fom_autosave_settings__load_commit(backup_service):
    default promise = store._fom_autosave_task.AsyncTask(backup_service.download)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)
    modal True
    zorder 200

    default ok_action = [SetField(renpy.persistent, "should_save_persistent", False), Quit(confirm=False)]
    default back_action = Hide("fom_autosave_settings__load_commit")

    default error = None

    python:
        try:
            if promise.is_complete():
                promise.get()
        except Exception as e:
            if error is None:
                store._fom_autosave_logging.logger.error(_("Failed to load persistent: {0}"), e)
                error = e

    use fom_autosave_screens__confirm(xmaximum=500, ymaximum=200, spacing=30):
        style_prefix "confirm"

        text _("Load persistent"):
            style "confirm_prompt"
            xalign 0.5

        if not promise.is_complete():
            text _("Loading..."):
                xalign 0.5
                text_align 0.5
        elif error is not None:
            text _("Failed to load persistent. Check logs.\n"
                   "{i}Your current persistent was not overwritten.{/i}"):
                xalign 0.5
                text_align 0.5
        else:
            text _("Persistent loaded.\n"
                   "The game needs to be restarted now."):
                xalign 0.5
                text_align 0.5

        hbox:
            xalign 0.5
            spacing 10

            if not promise.is_complete() or error is not None:
                textbutton _("Back"):
                    action back_action
                    sensitive promise.is_complete()
            else:
                textbutton _("Restart"):
                    action ok_action
                    sensitive promise.is_complete()

    if not promise.is_complete() or error is not None:
        key "K_ESCAPE" action back_action
    else:
        key "K_RETURN" action ok_action

screen fom_autosave_settings__timetravel_error():
    default ok_action = Hide("fom_autosave_settings__timetravel_error")

    modal True
    zorder 200

    use fom_autosave_screens__confirm(xmaximum=600, ymaximum=200, spacing=30):
        style_prefix "confirm"

        text _("Force save"):
            style "confirm_prompt"
            xalign 0.5

        text _("{b}{color=#ef4444}Time travel{/color}{/b} has been detected in this session.\n"
               "Refusing to save."):
            xalign 0.5
            text_align 0.5

        hbox xalign 0.5 spacing 10:
            textbutton _("Back") action ok_action

    key "K_ESCAPE" action ok_action
    key "K_RETURN" action ok_action
