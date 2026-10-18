# This file is part of Autosave Submod (see link below):
# https://github.com/friends-of-monika/mas-autosave

default persistent._fom_autosave_last_save = None

init -1000 python in _fom_autosave_timer:
    from datetime import datetime, timedelta
    from store import persistent

    BACKUP_FREQ = {
        0: (_("Hourly"), timedelta(seconds=3600)),
        1: (_("Daily"), timedelta(days=1)),
        2: (_("Weekly"), timedelta(days=7)),
        3: (_("Monthly"), timedelta(days=30)),
        4: (_("Off"), None)
    }

init 10 python in _fom_autosave_timer:
    from store.mas_submod_utils import functionplugin
    from store._fom_autosave_logging import logger
    from store import MASEventList, mas_all_ev_db_map
    import store

    expect_goodbye = False

    def has_period_elapsed():
        last = persistent._fom_autosave_last_save
        freq = persistent._fom_autosave_config_common["backup_freq"]
        now = datetime.now()

        delta = BACKUP_FREQ[freq][1]
        if delta is None:
            return False
        if last is None:
            return True

        return now - last > delta

    def try_timed_backup():
        if has_period_elapsed():
            logger.debug("Attempting timed backup (may be overridden if remote is not configured.)")
            freq_name = BACKUP_FREQ[persistent._fom_autosave_config_common["backup_freq"]][0]
            store._fom_autosave_common.backup_persistent(reason=_("{0} auto-backup").format(freq_name))

    @functionplugin("ch30_minute")
    def do_minute():
        try_timed_backup()

    @functionplugin("ch30_start")
    def do_start():
        try_timed_backup()

    @functionplugin("call_next_event")
    def do_event():
        event = MASEventList.peek()
        if event is None:
            return

        global expect_goodbye
        expect_goodbye = event.evl in mas_all_ev_db_map["BYE"]

    @functionplugin("_quit")
    def do_quit():
        if not expect_goodbye:
            return
        if persistent._fom_autosave_config_common["on_exit"]:
            renpy.call_in_new_context("fom_autosave_do_quit")

label fom_autosave_do_quit():
    $ mas_RaiseShield_core()

    $ store._fom_autosave_common.backup_persistent(reason=_("Goodbye"))
    while store._fom_autosave_common.is_any_pending:
        pause 0.5

    $ renpy.pause(1.5, hard=True)
    return
