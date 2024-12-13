import os
from pathlib import Path
import sys

BUNDLE_PATH = getattr(sys, "_MEIPASS", Path(os.path.abspath(os.path.dirname(__file__))).parent)

def get_file(path):
    abspath = os.path.abspath(os.path.join(BUNDLE_PATH, path))
    if not os.path.exists(abspath):
        abspath = path
    return abspath