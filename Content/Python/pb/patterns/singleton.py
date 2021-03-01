from pb import LogHelper

def singleton(cls):
    insts = {}
    def get(*args, **kwargs):
        if not cls in insts:
            insts[cls] = cls(*args, **kwargs)
        return insts[cls]
    return get
