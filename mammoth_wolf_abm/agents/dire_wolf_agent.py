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

    def exhaust(self):
        """Implement exhaustion of the agent."""
        self.energy -= 1

    def eat(self):
        """Implement eating of the agent."""
        self.model: abm.MammothWolfModel
        contents = self.model.grid.get_cell_list_contents(self.pos)
        for agent in contents:
            if isinstance(agent, MammothAgent):
                if self.model.random.random() < self.hunt_success_rate:
                    agent.die()
                    self.energy = self.ep_gain

    def reproduce(self):
        """Handle reproduction of the agent."""
        # Make the agent enter gestation if possible.
        if self.can_gestate():
            self.gestation = self.gestation_period
            self.is_gestating = True
        # If the reason it can't gestate is
        # being due to give birth
        # then it will give birth.
        elif self.can_reproduce():
            self.model: abm.MammothWolfModel
            child = DireWolfAgent(
                unique_id=self.model.next_id(),
                model=self.model,
                **dict(self.child_data)
            )
            cells_to_move = self.get_free_cells()
            dest_cell = self.model.random.choice(seq=cells_to_move)
            self.model.place_agent(agent=child, pos=dest_cell)
            self.is_gestating = False
            self.interbirth = self.birth_interval
        # If the agent is gestating progress it.
        elif self.gestation > 0:
            self.gestation -= 1
        # If the agent is between giving births progress the interbirth period.
        elif self.interbirth > 0:
            self.interbirth -= 1

    def aging(self):
        """Handle aging of the agent."""
        self.age += 1

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
