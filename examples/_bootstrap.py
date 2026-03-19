from __future__ import annotations

import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
SRC_DIR = ROOT_DIR / 'src'

current_dir_string = str(CURRENT_DIR)
if current_dir_string in sys.path:
    sys.path.remove(current_dir_string)

src_dir_string = str(SRC_DIR)
if src_dir_string not in sys.path:
    sys.path.insert(0, src_dir_string)
