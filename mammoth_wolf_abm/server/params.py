import sys

import json5

from mesa_viz_tornado.modules import CanvasGrid, ChartModule
from mesa_viz_tornado.UserParam import *


def mw_model_portrayal(agent):
    """
    Handle agent portrayals.

    Return the agent portrayal dictionary.
    """

    if agent is None:
        return

    portrayal = {}
    return portrayal


with open("mammoth_wolf_abm/server/param_dicts.json5", "r") as file:
    param_dicts = json5.load(file)

# Grid sizes must be adjusted here too.
canvas_element = CanvasGrid(
    portrayal_method=mw_model_portrayal,
    **param_dicts["canvas_element"]
)

chart_element = ChartModule(series=param_dicts["chart_list"][:-1], data_collector_name="datacollector")
chart_element_grass = ChartModule(series=param_dicts["chart_list"][-1:], data_collector_name="datacollector")

viz_elements = [canvas_element, chart_element, chart_element_grass]

params = {}
for k, v in param_dicts["params"].items():
    params[k] = v
    if type(v) is dict and "type" in v:
        cls = getattr(sys.modules[__name__], v["type"])
        params[k] = cls(**v["params"])
