init -999 python in _fom_autosave_http:
    import contextlib
    import store
    import os

    script_dir = store.fom_getScriptDir(fallback="game/Submods/Autosave")
    script_dir = renpy.config.basedir + "/" + script_dir
    SSL_CERT_FILE = script_dir + "/misc/cacert.pem"

    @contextlib.contextmanager
    def use_cert(cert_file):
        try:
            ssl_cert_backup = os.environ.get("SSL_CERT_FILE", None)
            os.environ["SSL_CERT_FILE"] = cert_file
            yield

        finally:
            if ssl_cert_backup is not None:
                os.environ["SSL_CERT_FILE"] = ssl_cert_backup
            else:
                del os.environ["SSL_CERT_FILE"]

init -898 python in _fom_autosave_http:
    from store._fom_autosave_logging import logger
    import sys

    if sys.version_info.major == 2: # Python v2 only
        from urllib2 import HTTPError
        import urllib2
        import urllib

        def request(method, url, headers=None, body=None, timeout=10):
            with use_cert(SSL_CERT_FILE):
                if isinstance(method, unicode):
                    method = method.encode("ascii")
                if isinstance(url, unicode):
                    url = url.encode("ascii")
                req = urllib2.Request(url, data=body)
                req.get_method = lambda: method

                if headers is None:
                    headers = {}
                for k, v in headers.items():
                    if isinstance(k, unicode):
                        k = k.encode("ascii")
                    if isinstance(v, unicode):
                        v = v.encode("ascii")
                    req.add_header(k, v)

                logger.debug("[http] {method} {url}".format(method=method, url=url))
                opener = urllib2.build_opener(urllib2.HTTPHandler)

                try:
                    res = opener.open(req, timeout=timeout)
                    status = res.getcode()
                    res_body = res.read()
                except HTTPError as e:
                    logger.debug("[http] {0} {1} - {2} | {3}", method, url, e.code, repr(e.read()[:500]))
                    raise e

                logger.debug("[http] {0} {1} - {2}", method, url, status)
                return status, res_body

        def urlencode(s):
            return urllib.urlencode(s)
