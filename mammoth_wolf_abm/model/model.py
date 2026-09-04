from dataclasses import asdict

from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from mammoth_wolf_abm.agents import GrassAgent, MammothAgent, MammothData


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
        self.width = width
        self.height = height
        self.torus = torus
        self.mammoth_data = MammothData(
            ep_gain=mammoth_ep_gain,
            max_age=mammoth_max_age,
            reproductive_age=mammoth_reproductive_age,
            gestation_period=mammoth_gestation_period,
            birth_interval=mammoth_birth_interval,
            is_child=False
        )

        self.schedule = RandomActivation(model=self)
        self.grid = MultiGrid(width=width, height=height, torus=torus)

        self.n_mammoth = n_mammoth

        if allow_seed:
            self.random.seed(a=random_seed)

        # Adding grass
        self.initialize_grass_agents(
            grass_regrow_rate=grass_regrow_rate,
            grass_regrow_rate_boosted=grass_regrow_rate_boosted
        )

        # Adding mammoths
        self.initialize_mammoth_agents()

        self.datacollector = DataCollector(
            model_reporters={
                "Ratio of grass patches (%)": count_grass_cells,
                "Number of mammoths": count_mammoths,
            }
        )
        self.datacollector.collect(model=self)

    def initialize_grass_agents(
            self,
            grass_regrow_rate: float,
            grass_regrow_rate_boosted: float
    ):
        """
        Fill all cells with grass agents.
        :param float grass_regrow_rate: Probability for a grazed cell to become grown grass
        :param float grass_regrow_rate_boosted: Probability for a grazed cell to become grown grass
        """
        for grass_id in range(self.width * self.height):
            grass = GrassAgent(
                unique_id=self.next_id(),
                model=self,
                grass_regrow_rate=grass_regrow_rate / 100.0,
                grass_regrow_rate_boosted=grass_regrow_rate_boosted / 100.0,
            )
            self.schedule.add(agent=grass)
            self.grid.place_agent(agent=grass, pos=(grass_id % self.width, grass_id // self.width))

    def initialize_mammoth_agents(self):
        """Generate and place the initial mammoth agents."""
        for i in range(self.n_mammoth):
            mammoth = MammothAgent(
                unique_id=self.next_id(),
                model=self,
                **asdict(self.mammoth_data)
            )
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.place_agent(agent=mammoth, pos=(x, y))

    def step(self):
        """Actions executed by the model during one step of the simulation."""
        self.schedule.step()
        self.datacollector.collect(model=self)

    def place_agent(self, agent, pos):
        """Place an agent."""
        self.schedule.add(agent=agent)
        self.grid.place_agent(agent=agent, pos=pos)


# Agent counters
def count_grass_cells(model: MammothWolfModel) -> float:
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


def count_mammoths(model: MammothWolfModel) -> int:
    """
    Return the number of mammoths.
    :param MammothWolfModel model: Model whose grass filled cells are counted
    :returns int: Number of mammoths
    """
    result = 0
    for agent in model.schedule.agents:
        if isinstance(agent, MammothAgent):
            result += 1
    return result
