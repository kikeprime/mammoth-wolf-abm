from mesa.model import Model

from .animal_agent import AnimalAgent
from .grass import GrassAgent
import mammoth_wolf_abm.model as abm


class MammothAgent(AnimalAgent):
    """Agent class for mammoths.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (MammothWolfModel): the MammothWolf model
        ep_gain (int): energy point gained from eating
        max_age (int): maximum age allowed for this agent in years
        reproductive_age (int): minimum age allowed for reproduction in years
        gestation_period (int): gestation period in months
        birth_interval (int): birth_interval in months
        litter_size (int): number of offsprings per litter
        is_child (bool): whether the agent is child or not
    """
    def __init__(
        self,
        unique_id: int,
        model: Model,
        ep_gain: int,
        max_age: int,
        reproductive_age: int,
        gestation_period: int,
        birth_interval: int,
        litter_size: int,
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

    def step(self):
        """Actions of the agent during one step of the simulation."""
        # Step 1: Move to a neighboring cell.
        self.move()
        # Step 2: Exhaust the agent. Currently, it decreases energy.
        self.exhaust()
        # Step 3: Eating.
        self.eat()
        # Step 4: Reproductive functions.
        self.reproduce()
        # Step 5: Aging.
        self.aging()
        # Step 6: Check natural death and starvation.
        self.check_death()

    def move(self):
        """Implement movement of the agent."""
        self.model: abm.MammothWolfModel
        cells_with_grown_grass = self.get_cells_with_grown_grass()
        cells_to_move = self.get_free_cells()
        dest_cell = None
        if len(cells_with_grown_grass) > 0:
            dest_cell = self.model.random.choice(seq=cells_with_grown_grass)
        elif len(cells_to_move) > 0:
            dest_cell = self.model.random.choice(seq=cells_to_move)
        if dest_cell is not None:
            self.model.grid.move_agent(agent=self, pos=dest_cell)

    def eat(self):
        """Implement eating of the agent."""
        self.model: abm.MammothWolfModel
        for agent in self.model.grid.get_cell_list_contents([self.pos]):
            if isinstance(agent, GrassAgent) and agent.grown:
                self.energy = self.ep_gain
                agent.grown = False
                if self.model.random.random() < 0.5:
                    agent.boosted = True

    def get_cells_with_grown_grass(self) -> list:
        """Return a list of cells with a grown grass."""
        self.model: abm.MammothWolfModel
        cells = []
        for cell in self.get_free_cells():
            grass = self.model.grid.get_cell_list_contents(cell)[0]
            grass: GrassAgent
            if grass.grown:
                cells.append(cell)
        return cells
