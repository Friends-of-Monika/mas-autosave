# This file is part of Autosave Submod (see link below):
# https://github.com/friends-of-monika/mas-autosave

init -1000 python in _fom_autosave_task:
    from store.mas_threading import MASAsyncWrapper

    class AsyncTask(object):
        def __init__(self, function, *args, **kwargs):
            self._function = function
            self._args = args
            self._kwargs = kwargs
            self._promise = None
            self._running = False
            self._result = None
            self._error = None

        def run_in_background(self):
            if self.is_complete() or self._running:
                raise RuntimeError("Task is either running or has already completed.")
            self._promise = MASAsyncWrapper(self._execute)
            self._promise.start()

        def is_complete(self):
            return self._promise is not None and self._promise.done()

        def is_running(self):
            return self._running

        def get(self):
            if not self.is_complete():
                raise RuntimeError("Task is either running or has not yet started.")
            if self._error is not None:
                raise self._error
            return self._result

        def _execute(self):
            try:
                self._running = True
                self._result = self._function(*self._args, **self._kwargs)
            except Exception as e:
                self._error = e
            finally:
                self._running = False
