from importlib.metadata import version
from mammoth_wolf_abm.model import MammothWolfModel
from mesa.agent import Agent


class GrassAgent(Agent):
    """
    Agent class for grass.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (MammothWolfModel): the MammothWolf model
        grass_regrow_rate (float): Number of steps after grazed cell becomes grown grass again
    """
    def __init__(
            self,
            unique_id: int,
            model: MammothWolfModel,
            grass_regrow_rate: float,
    ):
        if version("mesa") == "2.4.0":
            super().__init__(unique_id=unique_id, model=model)
        elif version("mesa") > "2.4.0":
            super().__init__(model=model)
        else:
            try:
                super().__init__(unique_id=unique_id, model=model)
            except TypeError or AttributeError:
                print("Incompatible mesa version.")

        self.grass_regrow_rate = grass_regrow_rate
        self.race = 2
        self.grown = False
        self.grow()

    def step(self):
        self.grow()

    def grow(self):
        """Handle countdown and regrowing."""
        if not self.grown:
            if self.model.random.random() < self.grass_regrow_rate:
                self.race = 2
                self.grown = True
