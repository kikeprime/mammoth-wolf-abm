import os
import sys

from mammoth_wolf_abm.server import server


PROJECT_PATH = os.path.realpath("__file__")
sys.path.append(PROJECT_PATH)

server.launch()
