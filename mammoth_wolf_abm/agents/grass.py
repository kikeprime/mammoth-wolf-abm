from importlib.metadata import version

from mesa.agent import Agent
from mesa.model import Model


class GrassAgent(Agent):
    """
    Agent class for grass.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (MammothWolfModel): the MammothWolf model
        grass_regrow_rate (float): Probability for a grazed cell to become grown grass
        grass_regrow_rate_boosted (float): Probability for a grazed cell to become grown grass if boosted by mammoths
    """
    def __init__(
            self,
            unique_id: int,
            model: Model,
            grass_regrow_rate: float,
            grass_regrow_rate_boosted: float
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
        self.grass_regrow_rate_boosted = grass_regrow_rate_boosted

        self.race = 2
        self.grown = False
        self.boosted = False
        self.grow()

    def step(self):
        """Actions of the agent during one step of the simulation."""
        self.grow()

    def grow(self):
        """Handle countdown and regrowing."""
        if not self.grown:
            rate = self.grass_regrow_rate_boosted if self.boosted else self.grass_regrow_rate
            if self.model.random.random() < rate:
                self.grown = True
                self.boosted = False
