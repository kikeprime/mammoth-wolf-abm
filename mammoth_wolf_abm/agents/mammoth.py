from importlib.metadata import version

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

    def step(self):
        """Actions of the agent during one step of the simulation."""
        self.move()
        self.ep -= 1
        self.eat()
        self.age += 1
        if self.age >= self.max_age or self.ep <= 0:
            self.destroy()

    def move(self):
        """Implement movement of the agent."""
        self.model: abm.MammothWolfModel
        cells_to_move = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=1
        )
        dest_cell = self.model.random.choice(seq=cells_to_move)
        self.model.grid.move_agent(agent=self, pos=dest_cell)

    def eat(self):
        """Implement eating of the agent."""
        pass

    def destroy(self):
        """Implement removal of the agent."""
        self.model: abm.MammothWolfModel
        self.model.grid.remove_agent(agent=self)
        self.model.schedule.remove(agent=self)
