import os
import sys

import mimetypes

from mammoth_wolf_abm.model import MammothWolfModel
from mammoth_wolf_abm.server import MammothWolfServer, viz_elements, params


PROJECT_PATH = os.path.realpath("__file__")
sys.path.append(PROJECT_PATH)

server = MammothWolfServer(
    model_cls=MammothWolfModel,
    visualization_elements=viz_elements,
    name="Mammoths and Wolves",
    model_params=params
)
# server.local_js_includes.add("custom/js/LangSwitch.js")

# Windows fix
if "text/css" not in mimetypes.guess_type("style.css"):
    mimetypes.add_type("text/css", ".css")

server.launch()
