"""
This file is responsible for creating the server and its components.
"""

from mesa_viz_tornado.ModularVisualization import ModularServer
from mesa_viz_tornado.modules import CanvasGrid, ChartModule
from mesa_viz_tornado.UserParam import *
import tornado.web
import mimetypes

import mammoth_wolf_abm as mw


# Accessing the files from root instead of from /local/custom
class MammothWolfServer(ModularServer):
    """
    Attach the module's folder to the web server's root then reinitialize the server.
    """

    def __init__(self,
                 model_cls,
                 visualization_elements,
                 name="Mesa Model",
                 model_params=None,
                 port=None):
        """Override ModularServer.__init__"""
        # call ModularServer.__init__
        super().__init__(model_cls=model_cls,
                         visualization_elements=visualization_elements,
                         name=name,
                         model_params=model_params,
                         port=port)

        # Attach the module's folder to the web server's root
        self.handlers.append((r"/(.*)", tornado.web.StaticFileHandler, {"path": ""}))

        # Reinitialize server by calling tornado.web.Application.__init__
        # Taken from the end of ModularServer.__init__
        super(ModularServer, self).__init__(self.handlers, **self.settings)


def ws_model_portrayal(agent):
    """
    Handle agent portrayals, including icons by gender.

    Return the agent portrayal dictionary.
    """

    if agent is None:
        return

    portrayal = {}
    if isinstance(agent, mw.WolfAgent):
        if agent.gender:
            portrayal["Shape"] = "mammoth_wolf_abm/pics/ffox.png"
        else:
            portrayal["Shape"] = "mammoth_wolf_abm/pics/fox.png"
        portrayal["Layer"] = 1
        portrayal["EP"] = agent.energy + 1
    if isinstance(agent, mw.MammothAgent):
        if agent.gender:
            portrayal["Shape"] = "mammoth_wolf_abm/pics/frabbit.png"
        else:
            portrayal["Shape"] = "mammoth_wolf_abm/pics/rabbit.png"
        portrayal["Layer"] = 1
        portrayal["EP"] = agent.energy + 1
    if isinstance(agent, mw.GrassAgent):
        if agent.grown:
            if agent.race == 2:
                portrayal["Color"] = ["green"]
            else:
                portrayal["Color"] = ["purple"]
        else:
            portrayal["Color"] = ["#663300"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


# Grid sizes must be adjusted here too.
canvas_element = CanvasGrid(portrayal_method=ws_model_portrayal,
                            grid_width=30, grid_height=30,
                            canvas_width=600, canvas_height=600)

chart_list = [
    {"Label": "Number of mammoths", "Color": "blue"},
    {"Label": "Number of female mammoths", "Color": "gray"},
    {"Label": "Number of male mammoths", "Color": "#975C24"},
    {"Label": "Number of wolves", "Color": "black"},
    {"Label": "Number of female wolves", "Color": "orange"},
    {"Label": "Number of male wolves", "Color": "red"},
    {"Label": "Ratio of grass patches (%)", "Color": "green"},
    {"Label": "Ratio of weed patches (%)", "Color": "purple"}
]
chart_element = ChartModule(series=chart_list[:-2], data_collector_name="datacollector")
chart_element_grass = ChartModule(series=chart_list[-2:], data_collector_name="datacollector")

viz_elements = [canvas_element, chart_element, chart_element_grass]

model_types = ["Extended model", "Mammoths and Wolves model", "Mammoths and Wolves Lotka-Volterra model"]
params = {
    "width": 30,
    "height": 30,
    "torus": Checkbox(name="Torus", value=True, description="Whether the edges are connected or not."),
    "model_type": Choice(name="Model type", value=model_types[1], choices=model_types),
    "n_mammoth": Slider(name="Initial number of mammoths", value=150, min_value=0, max_value=200, step=1),
    "n_wolf": Slider(name="Initial number of wolves", value=0, min_value=0, max_value=200, step=1),
    "mammoth_ep_gain_grass": Slider(name="EP gain from eating grass (mammoths)",
                                   value=5, min_value=0, max_value=100, step=1),
    "mammoth_ep_gain_weed": Slider(name="EP gain from eating weeds (mammoths)",
                                  value=0, min_value=0, max_value=100, step=1),
    "wolf_ep_gain": Slider(name="EP gain from eating mammoths (wolves)",
                          value=5, min_value=0, max_value=100, step=1),
    "mammoth_max_init_ep": Slider(name="Mammoths' maximal initial EP",
                                 value=10, min_value=1, max_value=100, step=1),
    "wolf_max_init_ep": Slider(name="Wolves' maximal initial EP",
                              value=10, min_value=1, max_value=100, step=1),
    "mammoth_reproduction_threshold": Slider("Mammoths' reproduction threshold (EP)",
                                            value=15, min_value=1, max_value=100, step=1),
    "wolf_reproduction_threshold": Slider(name="Wolves' reproduction threshold (EP)",
                                         value=15, min_value=1, max_value=100, step=1),
    "grass_regrow_rate": Slider(name="Grass' regrow rate (%)", value=6, min_value=0, max_value=100, step=1),
    "weed_regrow_rate": Slider(name="Weeds' regrow rate (%)", value=0, min_value=0, max_value=100, step=1),
    "allow_flocking": Checkbox(name="Allow flocking", value=False, description="The rabbits will flock."),
    "allow_hunt": Checkbox(name="Allow hunt", value=True, description="The foxes actively hunt."),
    "hunt_exponent": NumberInput(name="Hunt limiter exponent", value=-0.5, description="Limiting the hunting"),
    "a": NumberInput(name="a", value=0.1),
    "b": NumberInput(name="b", value=0.02),
    "c": NumberInput(name="c", value=0.4),
    "d": NumberInput(name="d", value=0.02),
    "allow_seed": Checkbox(name="Allow Seed", value=True),
    # Cannot be named "seed" otherwise it cannot be turned off
    "random_seed": NumberInput(name="Random Seed", value=474, description="Seed for random number generator functions")
}

server = MammothWolfServer(
    model_cls=mw.MammothWolfModel,
    visualization_elements=viz_elements,
    name="Mammoths and Wolves",
    model_params=params
)
server.local_js_includes.add("custom/mammoth_wolf_abm/js/LangSwitch.js")

# Windows fix
if "text/css" not in mimetypes.guess_type("style.css"):
    mimetypes.add_type("text/css", ".css")
