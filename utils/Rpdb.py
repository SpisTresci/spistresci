import rpdb2

class debug(object):
    started=False

    @staticmethod
    def _break(remote=False, unencrypted=False):
        if debug.started:
            rpdb2.setbreak()
        else:
            rpdb2.start_embedded_debugger_interactive_password(remote, unencrypted)
            debug.started = True

    def __init__(self, remote=False, unencrypted=False):
        self.remote = remote
        self.unencrypted = unencrypted

    def __call__(self, f):
        def wrapped(*args):
            debug._break(self.remote, self.unencrypted)
            f(*args, **kwargs)
        return wrapped

