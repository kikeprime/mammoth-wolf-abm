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


# Grid sizes must be adjusted here too.
canvas_element = CanvasGrid(
    portrayal_method=mw_model_portrayal,
    grid_width=30,
    grid_height=30,
    canvas_width=600,
    canvas_height=600
)

chart_list = [
    {"Label": "Number of mammoths", "Color": "brown"},
    {"Label": "Number of wolves", "Color": "gray"},
    {"Label": "Ratio of grass patches (%)", "Color": "green"},
]
chart_element = ChartModule(series=chart_list[:-1], data_collector_name="datacollector")
chart_element_grass = ChartModule(series=chart_list[-1:], data_collector_name="datacollector")

viz_elements = [canvas_element, chart_element, chart_element_grass]

params = {
    "width": 30,
    "height": 30,
    "torus": Checkbox(name="Torus", value=True, description="Whether the edges are connected or not."),
    "allow_seed": Checkbox(name="Allow Seed", value=True),
    # Cannot be named "seed" otherwise it cannot be turned off
    "random_seed": NumberInput(name="Random Seed", value=474, description="Seed for random number generator functions")
}
