from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivationByType

from mammoth_wolf_abm.agents import AnimalData, DireWolfAgent, DireWolfData, DireWolfPackAgent, GrassAgent, MammothAgent
import mammoth_wolf_abm.utils.counters as counters


class MammothWolfModel(Model):
    """
    The class for the Mammoth-Dire Wolf model.

    Parameters:
        width (int): Width of the grid
        height (int): Height of the grid
        torus (bool): Whether the grid is torus or not
        n_mammoth (int): Initial number of woolly mammoths
        n_dire_wolf (int): Initial number of dire wolves
        grass_regrow_rate (float): Probability for a grazed cell to become grown grass
        grass_regrow_rate_boosted (float): Probability for a grazed cell to become grown grass if boosted by mammoths
        mammoth_ep_gain (int): energy point gained from eating for mammoths
        mammoth_max_age (int): maximum age allowed for this agent in years for mammoths
        mammoth_reproductive_age (int): minimum age allowed for reproduction in years for mammoths
        mammoth_gestation_period (int): gestation period in months for mammoths
        mammoth_birth_interval (int): birth_interval in months for mammoths
        mammoth_litter_size (int): number of offsprings per litter for mammoths
        dire_wolf_ep_gain (int): energy point gained from eating for dire wolves
        dire_wolf_max_age (int): maximum age allowed for this agent in years for dire wolves
        dire_wolf_reproductive_age (int): minimum age allowed for reproduction in years for dire wolves
        dire_wolf_gestation_period (int): gestation period in months for dire wolves
        dire_wolf_birth_interval (int): birth_interval in months for dire wolves
        dire_wolf_litter_size (int): number of offsprings per litter for dire wolves
        dire_wolf_hunt_success_rate (float): Probability of successful hunt in percentage for dire wolves
        max_dire_wolf_pack_size (int): maximum size of a dire wolf pack
        allow_seed (bool): Toggle random seed
        random_seed (int): Random seed
    """
    def __init__(
        self,
        width: int,
        height: int,
        torus: bool,
        n_mammoth: int,
        n_dire_wolf: int,
        grass_regrow_rate: float,
        grass_regrow_rate_boosted: float,
        mammoth_ep_gain: int,
        mammoth_max_age: int,
        mammoth_reproductive_age: int,
        mammoth_gestation_period: int,
        mammoth_birth_interval: int,
        mammoth_litter_size: int,
        dire_wolf_ep_gain: int,
        dire_wolf_max_age: int,
        dire_wolf_reproductive_age: int,
        dire_wolf_gestation_period: int,
        dire_wolf_birth_interval: int,
        dire_wolf_litter_size: int,
        dire_wolf_hunt_success_rate: float,
        max_dire_wolf_pack_size: int,
        allow_seed: bool,
        random_seed: int,
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.torus = torus

        self.mammoth_data = AnimalData(
            ep_gain=mammoth_ep_gain,
            max_age=mammoth_max_age,
            reproductive_age=mammoth_reproductive_age,
            gestation_period=mammoth_gestation_period,
            birth_interval=mammoth_birth_interval,
            litter_size=mammoth_litter_size,
            is_child=False
        )
        self.dire_wolf_data = DireWolfData(
            ep_gain=dire_wolf_ep_gain,
            max_age=dire_wolf_max_age,
            reproductive_age=dire_wolf_reproductive_age,
            gestation_period=dire_wolf_gestation_period,
            birth_interval=dire_wolf_birth_interval,
            litter_size=dire_wolf_litter_size,
            hunt_success_rate=dire_wolf_hunt_success_rate,
            is_child=False
        )

        self.schedule = RandomActivationByType(model=self)
        self.grid = MultiGrid(width=width, height=height, torus=torus)

        self.n_mammoth = n_mammoth
        self.n_dire_wolf = n_dire_wolf
        self.max_dire_wolf_pack_size = max_dire_wolf_pack_size

        self.packs = []

        if allow_seed:
            self.random.seed(a=random_seed)

        # Adding grass
        self.initialize_grass_agents(
            grass_regrow_rate=grass_regrow_rate,
            grass_regrow_rate_boosted=grass_regrow_rate_boosted
        )

        # Adding mammoths and dire wolves
        self.initialize_mammoth_agents()
        self.initialize_dire_wolf_agents()

        self.count_dire_wolves = counters.count_dire_wolves
        self.datacollector = DataCollector(
            model_reporters={
                "Ratio of grass patches (%)": counters.count_grass_cells,
                "Number of mammoths": counters.count_mammoths,
                "Number of dire wolves": counters.count_dire_wolves,
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
            self.place_agent(agent=grass, pos=(grass_id % self.width, grass_id // self.width))

    def initialize_mammoth_agents(self):
        """Generate and place the initial mammoth agents."""
        for i in range(self.n_mammoth):
            mammoth = MammothAgent(
                unique_id=self.next_id(),
                model=self,
                **dict(self.mammoth_data)
            )
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.place_agent(agent=mammoth, pos=(x, y))

    def initialize_dire_wolf_agents(self):
        """Generate and place the initial dire wolf agents."""
        x = 0
        y = 0
        pack = None
        for i in range(self.n_dire_wolf):
            if i % self.max_dire_wolf_pack_size == 0:
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                pack = DireWolfPackAgent(
                    unique_id=self.next_id(),
                    model=self,
                    pack_id=len(self.packs),
                )
                self.place_agent(agent=pack, pos=(x, y))
                self.packs.append(pack)
            dire_wolf = DireWolfAgent(
                unique_id=self.next_id(),
                model=self,
                pack=pack.pack_id,
                **dict(self.dire_wolf_data)
            )
            pack.add_member(dire_wolf=dire_wolf)
            self.place_agent(agent=dire_wolf, pos=(x, y))

    def step(self):
        """Actions executed by the model during one step of the simulation."""
        self.schedule.step_type(agenttype=GrassAgent)
        self.schedule.step_type(agenttype=MammothAgent)
        self.schedule.step_type(agenttype=DireWolfPackAgent)
        self.schedule.step_type(agenttype=DireWolfAgent)
        self.datacollector.collect(model=self)

    def place_agent(self, agent, pos):
        """Place an agent."""
        self.schedule.add(agent=agent)
        self.grid.place_agent(agent=agent, pos=pos)
