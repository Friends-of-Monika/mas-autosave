default persistent._fom_autosave_config_cloud = None

init -1000 python:
    if persistent._fom_autosave_config_cloud is None:
        persistent._fom_autosave_config_cloud = {
            "user_key":  "",
            "key_shown": False
        }

init -896 python in _fom_autosave_cloud:
    from store._fom_autosave_http import request, urlencode
    from store._fom_autosave_common import PersistentBackup
    from store._fom_autosave_persistent import get_persistent_path
    from store._fom_autosave_crypto import derive_key, derive_user_id, encrypt, decrypt
    from store import persistent
    import store

    import json
    import re
    import uuid

    ENDPOINT = "https://autosave.worker.mon.icu"

    _UUID_RE = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )

    def is_valid_uuid(s):
        if isinstance(s, unicode):
            s = s.encode("ascii", "replace")
        return bool(_UUID_RE.match(s.strip()))

    def clear_user_key():
        persistent._fom_autosave_config_cloud["user_key"]  = ""
        persistent._fom_autosave_config_cloud["key_shown"] = False

    def restore_user_key(user_key):
        if isinstance(user_key, unicode):
            user_key = user_key.encode("ascii", "replace")
        persistent._fom_autosave_config_cloud["user_key"]  = user_key.strip().lower()
        persistent._fom_autosave_config_cloud["key_shown"] = True

    def generate_user_key():
        persistent._fom_autosave_config_cloud["user_key"]  = str(uuid.uuid4())
        persistent._fom_autosave_config_cloud["key_shown"] = False

    def format_display_code(user_key):
        return user_key

    def list_versions():
        user_key = persistent._fom_autosave_config_cloud.get("user_key", "")
        if not user_key:
            return []

        user_id  = derive_user_id(user_key)
        url      = "{0}/saves/{1}/versions".format(ENDPOINT, user_id)
        status, body = request("GET", url, {"Accept": "application/json"}, None)
        if status != 200:
            raise ValueError("Unexpected status {0}".format(status))

        return json.loads(body)


    class CloudBackup(PersistentBackup):
        def __init__(self, reason=None, version_sha=None):
            super(CloudBackup, self).__init__()
            self.reason      = reason
            self.version_sha = version_sha

        def is_configured(self):
            return bool(persistent._fom_autosave_config_cloud.get("user_key", ""))

        def upload(self):
            user_key = persistent._fom_autosave_config_cloud["user_key"]
            key      = derive_key(user_key)
            user_id  = derive_user_id(user_key)

            per_path = get_persistent_path()
            renpy.save_persistent()

            with open(per_path, "rb") as f:
                plaintext = f.read()

            ciphertext   = encrypt(plaintext, key)
            reason_param = urlencode({"reason": self.reason or "autosave"})
            url          = "{0}/saves/{1}/upload?{2}".format(ENDPOINT, user_id, reason_param)

            headers = {
                "Content-Type": "application/octet-stream",
                "User-Agent":   "MonikaAfterStory/{0}".format(renpy.config.version),
            }
            status, body = request("POST", url, headers, ciphertext)
            if status != 201:
                raise ValueError("Upload failed with status {0}".format(status))

        def download(self):
            user_key = persistent._fom_autosave_config_cloud["user_key"]
            key      = derive_key(user_key)
            user_id  = derive_user_id(user_key)

            url     = "{0}/saves/{1}/{2}".format(ENDPOINT, user_id, self.version_sha)
            headers = {"User-Agent": "Monika After Story v{0}".format(renpy.config.version)}
            status, body = request("GET", url, headers, None)
            if status != 200:
                raise ValueError("Download failed with status {0}".format(status))

            plaintext = decrypt(body, key)

            per_path = get_persistent_path()
            with open(per_path, "wb") as f:
                f.write(plaintext)


screen fom_autosave_settings__cloud_restore():
    modal True
    zorder 200

    default entered = ""
    default back_action = Hide("fom_autosave_settings__cloud_restore")

    use fom_autosave_screens__confirm(xmaximum=540, ymaximum=240, spacing=20):
        style_prefix "confirm"

        text _("Restore backup code"):
            style "confirm_prompt"
            xalign 0.5

        text _("Enter the backup code from your other device:"):
            xalign 0.5
            text_align 0.5

        input:
            value ScreenVariableInputValue("entered")
            length 36
            pixel_width 460
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Confirm"):
                sensitive store._fom_autosave_cloud.is_valid_uuid(entered)
                action [
                    Function(store._fom_autosave_cloud.restore_user_key, entered),
                    back_action
                ]

            textbutton _("Back"):
                action back_action

    key "K_ESCAPE" action back_action


screen fom_autosave_settings__cloud_setup(first_time):
    modal True
    zorder 200

    $ user_key_hex = persistent._fom_autosave_config_cloud.get("user_key", "")
    $ display_code = store._fom_autosave_cloud.format_display_code(user_key_hex)
    $ ok_action    = Hide("fom_autosave_settings__cloud_setup")

    use fom_autosave_screens__confirm(xmaximum=620, ymaximum=360, spacing=20):
        style_prefix "confirm"

        text _("Your backup code"):
            style "confirm_prompt"
            xalign 0.5

        if first_time:
            text _("Write this down or save it somewhere safe.\nYou will need it to restore your saves on another device.\n{b}If you lose this code, your cloud saves are unrecoverable.{/b}"):
                xalign 0.5
                text_align 0.5

        text "[display_code]":
            xalign 0.5
            text_align 0.5

        if first_time:
            textbutton " " + _("I have written down the code"):
                style "generic_fancy_check_button"
                selected persistent._fom_autosave_config_cloud["key_shown"]
                action ToggleDict(persistent._fom_autosave_config_cloud, "key_shown")
                xalign 0.5

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Done"):
                sensitive (persistent._fom_autosave_config_cloud["key_shown"] or not first_time)
                action ok_action

            if first_time:
                textbutton _("Back"):
                    action [Function(store._fom_autosave_cloud.clear_user_key), ok_action]

    if persistent._fom_autosave_config_cloud["key_shown"] or not first_time:
        key "K_ESCAPE" action ok_action
        key "K_RETURN" action ok_action


screen fom_autosave_settings__version_select():
    default promise = store._fom_autosave_task.AsyncTask(store._fom_autosave_cloud.list_versions)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)
    modal True
    zorder 200

    default back_action = Hide("fom_autosave_settings__version_select")
    default versions    = None
    default error       = None

    python:
        try:
            if promise.is_complete():
                versions = promise.get()
        except Exception as e:
            if error is None:
                store._fom_autosave_logging.logger.error(_("Failed to load versions: {0}"), e)
                error = e

    use fom_autosave_screens__confirm(xmaximum=700, ymaximum=400, spacing=30):
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

        elif not versions:
            text _("No saves found."):
                xalign 0.5
                text_align 0.5

        else:
            $ backup_service = store._fom_autosave_cloud.CloudBackup(None)
            hbox:
                viewport id "versions":
                    xalign 0.5
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True

                    vbox spacing 10:
                        for version in versions:
                            $ v_reason = version.get("reason", _("Automatic backup"))
                            $ v_date   = version["timestamp"][:19].replace("T", " ")
                            $ v_sha    = version["sha256"]

                            vbox:
                                textbutton "[v_reason!q]" action ([
                                    Hide("fom_autosave_settings__version_select"),
                                    SetField(backup_service, "version_sha", v_sha),
                                    Show("fom_autosave_settings__load_commit", None, backup_service)
                                ])
                                text _("{size=-6}Saved on [v_date]{/size}") xoffset 5
                                text "{alpha=0.5}{size=-10}[v_sha]{/size}{/alpha}" xoffset 5

                vbar value YScrollValue("versions")

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Back"):
                action back_action
                sensitive promise.is_complete()

    if promise.is_complete():
        key "K_ESCAPE" action back_action
