import os
import enum

class Mode(enum.Enum):
    READ_WRITE = "read-write"
    READ_ONLY = "read-only"

class Config(object):

    def __init__(self) -> None:
        self.MNT_DIR = os.getenv("MNT_DIR", "/mnt/nfs/filestore")
        self.MODE = Mode( os.getenv("MODE", Mode.READ_ONLY) )