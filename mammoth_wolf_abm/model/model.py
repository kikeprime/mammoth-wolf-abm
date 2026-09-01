from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from mammoth_wolf_abm.agents import GrassAgent, MammothAgent


class MammothWolfModel(Model):
    """
    The class for the Mammoth-Dire Wolf model.

    Parameters:
        width (int): Width of the grid
        height (int): height of the grid
        grass_regrow_rate (float): Probability for a grazed cell to become grown grass
        grass_regrow_rate_boosted (float): Probability for a grazed cell to become grown grass if boosted by mammoths
        allow_seed (bool): Toggle random seed
        random_seed (int): Random seed
    """
    def step(self):
        """Actions executed by the model during one step of the simulation."""
        self.schedule.step()
        self.datacollector.collect(model=self)

    def __init__(
            self,
            width: int,
            height: int,
            torus: bool,
            n_mammoth: int,
            grass_regrow_rate: float,
            grass_regrow_rate_boosted: float,
            mammoth_ep_gain: int,
            mammoth_max_age: int,
            mammoth_reproductive_age: int,
            mammoth_gestation_period: int,
            mammoth_birth_interval: int,
            allow_seed: bool,
            random_seed: int,
    ):
        super().__init__()
        self.schedule = RandomActivation(model=self)
        self.grid = MultiGrid(width=width, height=height, torus=torus)

        self.n_mammoth = n_mammoth

        if allow_seed:
            self.random.seed(a=random_seed)

        # Adding mammoths
        for i in range(self.n_mammoth):
            mammoth = MammothAgent(
                unique_id=self.next_id(),
                model=self,
                ep_gain=mammoth_ep_gain,
                max_age=mammoth_max_age,
                reproductive_age=mammoth_reproductive_age,
                gestation_period=mammoth_gestation_period,
                birth_interval=mammoth_birth_interval
            )
            self.schedule.add(mammoth)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(mammoth, (x, y))

        # Adding grass
        self.initialize_grass_agents(
            width=width,
            height=height,
            grass_regrow_rate=grass_regrow_rate,
            grass_regrow_rate_boosted=grass_regrow_rate_boosted
        )

        self.datacollector = DataCollector(
            model_reporters={
                "Ratio of grass patches (%)": grass_cell_counter,
            }
        )
        self.datacollector.collect(model=self)

    def initialize_grass_agents(
            self,
            width: int,
            height: int,
            grass_regrow_rate: float,
            grass_regrow_rate_boosted: float
    ):
        """
        Fill all cells with grass agents.
        :param int width: Width of the grid
        :param int height: height of the grid
        :param float grass_regrow_rate: Probability for a grazed cell to become grown grass
        :param float grass_regrow_rate_boosted: Probability for a grazed cell to become grown grass
        """
        for grass_id in range(width * height):
            grass = GrassAgent(
                unique_id=self.next_id(),
                model=self,
                grass_regrow_rate=grass_regrow_rate / 100.0,
                grass_regrow_rate_boosted=grass_regrow_rate_boosted / 100.0,
            )
            self.schedule.add(agent=grass)
            self.grid.place_agent(agent=grass, pos=(grass_id % width, grass_id // width))


# Agent counters
def grass_cell_counter(model: MammothWolfModel) -> float:
    """
    Return percentage of grown grass.
    :param MammothWolfModel model: Model whose grass filled cells are counted
    :returns float: Percentage of cells filled with grass
    """
    result = 0
    for agent in model.schedule.agents:
        if isinstance(agent, GrassAgent):
            agent: GrassAgent
            if agent.grown:
                result += 1
    return 100 * result / float(model.grid.width * model.grid.height)
