import os
import sys

import mimetypes

from mammoth_wolf_abm.model import MammothWolfModel
from mammoth_wolf_abm.server import MammothWolfServer, params, viz_elements


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
if "text/css" not in mimetypes.guess_type(url="style.css"):
    mimetypes.add_type(type="text/css", ext=".css")

server.launch(open_browser=False)
