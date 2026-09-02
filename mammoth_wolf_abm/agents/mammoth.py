from importlib.metadata import version

from .grass import GrassAgent
import mammoth_wolf_abm.model as abm
from mesa.agent import Agent
from mesa.model import Model


class MammothAgent(Agent):
    """Agent class for mammoths.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (MammothWolfModel): the MammothWolf model
        ep_gain (int): energy point gained from eating
        max_age (int): maximum age allowed for this agent in years
        reproductive_age (int): minimum age allowed for reproduction in years
        gestation_period (int): gestation period in months
        birth_interval (int): birth_interval in months
    """
    def __init__(
            self,
            unique_id: int,
            model: Model,
            ep_gain: int,
            max_age: int,
            reproductive_age: int,
            gestation_period: int,
            birth_interval: int
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

        self.ep_gain = ep_gain
        self.max_age = max_age * 365
        self.reproductive_age = reproductive_age * 365
        self.gestation_period = gestation_period * 30
        self.birth_interval = birth_interval * 30

        self.race = 1
        self.age = self.model.random.randint(a=0, b=self.max_age)
        self.ep = self.model.random.randint(a=1, b=self.ep_gain)
        self.gestation = 0
        self.is_gestating = False
        self.interbirth = 0

        if self.age >= self.reproductive_age:
            self.gestation = self.model.random.randint(a=0, b=self.gestation_period)
            if self.gestation == 0:
                self.interbirth = self.model.random.randint(a=0, b=self.birth_interval)
            else:
                self.is_gestating = True

    def step(self):
        """Actions of the agent during one step of the simulation."""
        self.move()
        self.ep -= 1
        self.eat()
        self.reproduce()
        self.age += 1
        if self.age >= self.max_age or self.ep <= 0:
            self.destroy()

    def get_free_cells(self) -> list:
        """Get the list of the free neighboring cells."""
        self.model: abm.MammothWolfModel
        cells = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=1
        )
        free_cells = []
        for cell in cells:
            if len(self.model.grid.get_cell_list_contents(cell)) == 1:
                free_cells.append(cell)
        return free_cells

    def move(self):
        """Implement movement of the agent."""
        self.model: abm.MammothWolfModel
        cells_to_move = self.get_free_cells()
        if len(cells_to_move) > 0:
            dest_cell = self.model.random.choice(seq=cells_to_move)
            self.model.grid.move_agent(agent=self, pos=dest_cell)

    def eat(self):
        """Implement eating of the agent."""
        self.model: abm.MammothWolfModel
        for agent in self.model.grid.get_cell_list_contents([self.pos]):
            if isinstance(agent, GrassAgent) and agent.grown:
                self.ep = self.ep_gain
                agent.grown = False
                if self.model.random.random() < 0.5:
                    agent.boosted = True

    def can_gestate(self) -> bool:
        """Returns true if the agent can reproduce."""
        age = self.age >= self.reproductive_age
        interbirth = self.interbirth <= 0
        return age and not self.is_gestating and interbirth

    def can_reproduce(self) -> bool:
        """Returns true if the agent can reproduce."""
        age = self.age >= self.reproductive_age
        gestation = self.gestation <= 0
        cell = len(self.get_free_cells()) > 0
        return age and gestation and self.is_gestating and cell

    def reproduce(self):
        """Handle reproduction of the agent."""
        if self.can_gestate():
            self.gestation = self.gestation_period
            self.is_gestating = True
        elif self.can_reproduce():
            self.model: abm.MammothWolfModel
            child = MammothAgent(
                unique_id=self.model.next_id(),
                model=self.model,
                ep_gain=self.ep_gain,
                max_age=self.max_age//365,
                reproductive_age=self.reproductive_age//365,
                gestation_period=self.gestation_period//30,
                birth_interval=self.birth_interval//30
            )
            cells_to_move = self.get_free_cells()
            dest_cell = self.model.random.choice(seq=cells_to_move)
            self.model.place_agent(agent=child, pos=dest_cell)
            self.is_gestating = False
            self.interbirth = self.birth_interval
        elif self.gestation > 0:
            self.gestation -= 1
        elif self.interbirth > 0:
            self.interbirth -= 1

    def destroy(self):
        """Implement removal of the agent."""
        self.model: abm.MammothWolfModel
        self.model.grid.remove_agent(agent=self)
        self.model.schedule.remove(agent=self)
