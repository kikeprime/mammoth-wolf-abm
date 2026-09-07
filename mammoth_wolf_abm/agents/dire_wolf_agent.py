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
        reproductive_age (int): minimum age allowed for reproduction in years
        gestation_period (int): gestation period in months
        birth_interval (int): birth_interval in months
        hunt_success_rate (float): Probability of successful hunt in percentage
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
            is_child=is_child
        )

        self.hunt_success_rate = hunt_success_rate / 100
        self.child_data = DireWolfData(
            ep_gain=ep_gain,
            max_age=max_age,
            reproductive_age=reproductive_age,
            gestation_period=gestation_period,
            birth_interval=birth_interval,
            hunt_success_rate=hunt_success_rate,
            is_child=True
        )

    def move(self):
        """Implement movement of the agent."""
        self.model: abm.MammothWolfModel
        cells_to_move, cells_with_mammoth = self.get_dest_cells()
        if len(cells_with_mammoth) > 0:
            # Extra limits on hunting goes here.
            dest_cell = self.model.random.choice(seq=cells_with_mammoth)
            self.model.grid.move_agent(agent=self, pos=dest_cell)
        elif len(cells_to_move) > 0:
            dest_cell = self.model.random.choice(seq=cells_to_move)
            self.model.grid.move_agent(agent=self, pos=dest_cell)

    def eat(self):
        """Implement eating of the agent."""
        self.model: abm.MammothWolfModel
        contents = self.model.grid.get_cell_list_contents(self.pos)
        for agent in contents:
            if isinstance(agent, MammothAgent):
                if self.model.random.random() < self.hunt_success_rate:
                    agent.energy = -2 * agent.ep_gain
                    self.energy = self.ep_gain

    def get_dest_cells(self) -> tuple[list, list]:
        """Get the list of the possible destination cells.
        :returns tuple[list, list]: tuple of lists with possible destination cells and cells with a mammoth
        """
        self.model: abm.MammothWolfModel
        cells = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=1
        )
        dest_cells = []
        cells_with_mammoth = []
        for cell in cells:
            contents = self.model.grid.get_cell_list_contents(cell)
            if len(contents) == 1:
                dest_cells.append(cell)
            if len(contents) == 2 and isinstance(contents[1], MammothAgent):
                dest_cells.append(cell)
                cells_with_mammoth.append(cell)
        return dest_cells, cells_with_mammoth
