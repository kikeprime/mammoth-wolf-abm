from mesa.model import Model

from .animal_agent import AnimalAgent
from .dire_wolf_data import DireWolfData
from .mammoth_agent import MammothAgent
import mammoth_wolf_abm.model as abm


class DireWolfAgent(AnimalAgent):
    """Agent class for dire wolves.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (MammothWolfModel): the MammothWolf model
        ep_gain (int): energy point gained from eating
        max_age (int): maximum age allowed for this agent in years
        reproductive_age (float): minimum age allowed for reproduction in years
        gestation_period (int): gestation period in months
        birth_interval (int): birth_interval in months
        litter_size (int): number of offsprings per litter
        hunt_success_rate (float): Probability of successful hunt in percentage
        is_child (bool): whether the agent is child or not
    """
    def __init__(
        self,
        unique_id: int,
        model: Model,
        pack: int,
        ep_gain: int,
        max_age: int,
        reproductive_age: float,
        gestation_period: int,
        birth_interval: int,
        litter_size: int,
        hunt_success_rate: float,
        is_child: bool,
    ):
        super().__init__(
            unique_id=unique_id,
            model=model,
            ep_gain=ep_gain,
            max_age=max_age,
            reproductive_age=reproductive_age,
            gestation_period=gestation_period,
            birth_interval=birth_interval,
            litter_size=litter_size,
            is_child=is_child
        )

        self.hunt_success_rate = hunt_success_rate / 100
        self.pack = pack

        self.child_data = DireWolfData(
            ep_gain=ep_gain,
            max_age=max_age,
            reproductive_age=reproductive_age,
            gestation_period=gestation_period,
            birth_interval=birth_interval,
            litter_size=litter_size,
            hunt_success_rate=hunt_success_rate,
            is_child=True
        )

    def step(self):
        """Actions of the agent during one step of the simulation."""
        # Step 1: Exhaust the agent.
        self.exhaust()
        # Step 2: Eating.
        self.eat()
        # Step 3: Reproductive functions.
        # self.reproduce()
        # Step 4: Aging.
        self.aging()
        # Step 5: Check natural death and starvation.
        self.check_death()

    def move(self):
        """DireWolfPackAgent moves the agent."""
        pass

    def eat(self):
        """Implement hunting of the dire wolves.
        Successful hunt fills all wolf's belly.
        """
        self.model: abm.MammothWolfModel
        contents = self.model.grid.get_cell_list_contents(self.pos)
        for agent in contents:
            if isinstance(agent, MammothAgent):
                if self.model.random.random() < self.hunt_success_rate:
                    agent.die()
                    for dire_wolf in self.model.packs[self.pack].members:
                        if dire_wolf.pack == self.pack:
                            dire_wolf.energy = dire_wolf.ep_gain
