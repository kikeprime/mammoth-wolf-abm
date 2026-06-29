"""
This file is responsible for creating the server and its components.
"""

from mesa_viz_tornado.ModularVisualization import ModularServer
import tornado.web
import mimetypes

import mammoth_wolf_abm as mw
from .params import params, viz_elements


# Accessing the files from root instead of from /local/custom
class MammothWolfServer(ModularServer):
    """
    Attach the module's folder to the web server's root then reinitialize the server.
    """

    def __init__(
            self,
            model_cls,
            visualization_elements,
            name="Mesa Model",
            model_params=None,
            port=None
    ):
        """Override ModularServer.__init__"""
        # call ModularServer.__init__
        super().__init__(
            model_cls=model_cls,
            visualization_elements=visualization_elements,
            name=name,
            model_params=model_params,
            port=port
        )

        # Attach the module's folder to the web server's root
        self.handlers.append((r"/(.*)", tornado.web.StaticFileHandler, {"path": ""}))

        # Reinitialize server by calling tornado.web.Application.__init__
        # Taken from the end of ModularServer.__init__
        super(ModularServer, self).__init__(self.handlers, **self.settings)


server = MammothWolfServer(
    model_cls=mw.MammothWolfModel,
    visualization_elements=viz_elements,
    name="Mammoths and Wolves",
    model_params=params
)
# server.local_js_includes.add("custom/js/LangSwitch.js")

# Windows fix
if "text/css" not in mimetypes.guess_type("style.css"):
    mimetypes.add_type("text/css", ".css")
