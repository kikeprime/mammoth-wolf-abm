from importlib.metadata import version
from mesa.agent import Agent

from mammoth_wolf_abm import MammothWolfModel

mesa_version = version("mesa")


class MammothWolfAgent(Agent):
    """
    Agent class for the animal agents.

    Define shared methods, implement default movement and reproduction, handle steps.

    Parameters:
        unique_id (int): Unique identifier for instance agent (legacy support)
        model (MammothWolfModel): the MammothWolf model
        ep_gain (int): energy point gained from eating rabbits
        ep_gain_grass (int): energy point gained from eating grass
        ep_gain_weed (int): energy point gained from eating weeds
        max_init_ep (int): maximum initial energy point
        reproduction_threshold (int): necessary energy point for reproduction
    """
    def __init__(self, unique_id: int, model: MammothWolfModel,
                 ep_gain: int, ep_gain_grass: int, ep_gain_weed: int,
                 max_init_ep: int, reproduction_threshold: int):
        if mesa_version == "2.4.0":
            super().__init__(unique_id=unique_id, model=model)
        elif mesa_version > "2.4.0":
            super().__init__(model=model)
        else:
            try:
                super().__init__(unique_id=unique_id, model=model)
            # Bare except because error type is unknown
            except:
                print("Incompatible mesa version.")

        self.ep_gain = ep_gain
        self.ep_gain_grass = ep_gain_grass
        self.ep_gain_weed = ep_gain_weed
        self.max_init_ep = max_init_ep
        self.reproduction_threshold = reproduction_threshold

        self.energy = self.model.random.randrange(self.max_init_ep)

        # True: female
        # False: male
        self.gender = None

        # The subclasses set this
        # 0: Fox
        # 1: Rabbit
        # 2: Grass (GrassAgent)
        # 3: Weed (GrassAgent)
        self.race = None

        self.can_reproduce = False

    def step(self):
        self.move()
        self.model: MammothWolfModel
        if self.model.model_type != 2:
            self.energy -= 1
            self.eat()
            self.reproduce()
            self.die()

    def move(self):
        """Default move method, no hunting and no flocking."""

        self.model: MammothWolfModel
        cells_to_move = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=1
        )
        dest_cell = self.model.random.choice(cells_to_move)
        self.model.grid.move_agent(agent=self, pos=dest_cell)

    # The subclasses will define this
    def eat(self):
        pass

    def reproduce(self):
        """Reproduction.

        In my model there should be at least one of each gender who can reproduce and the females will give birth.
        """
        self.model: MammothWolfModel
        if self.energy > self.reproduction_threshold:
            self.can_reproduce = True
            if self.model.model_type == 0:
                agent: MammothWolfAgent
                mates = [agent for agent in self.model.grid.get_cell_list_contents([self.pos])
                         if agent.race == self.race and agent.gender != self.gender and agent.can_reproduce]
                if len(mates) == 0:
                    return
            self.energy = self.energy // 2
            if self.model.model_type == 0 and self.gender is False:
                return
            if self.race == 0:
                child = WolfAgent(
                    unique_id=self.model.next_id(),
                    model=self.model,
                    ep_gain=self.ep_gain,
                    max_init_ep=self.max_init_ep,
                    reproduction_threshold=self.reproduction_threshold
                )
                child.gender = False
            else:
                child = MammothAgent(
                    unique_id=self.model.next_id(),
                    model=self.model,
                    ep_gain_grass=self.ep_gain_grass,
                    ep_gain_weed=self.ep_gain_weed,
                    max_init_ep=self.max_init_ep,
                    reproduction_threshold=self.reproduction_threshold
                )
                child.gender = True
            if self.model.model_type == 0:
                child.gender = self.random.choice([True, False])
            self.model.place_child(child=child, pos=self.pos)

    def die(self):
        """Death by starvation"""
        if self.energy < 0:
            self.destroy()

    def destroy(self):
        """Remove agents"""
        self.model: MammothWolfModel
        self.model.grid.remove_agent(agent=self)
        self.model.schedule.remove(agent=self)


class WolfAgent(MammothWolfAgent):
    """
    Agent class for wolves.

    Implement eating sheep and active hunt.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (MammothWolfModel): the MammothWolf model
        ep_gain (int): energy point gained from eating rabbits
        max_init_ep (int): maximum initial energy point
        reproduction_threshold (int): necessary energy point for reproduction
    """
    def __init__(
            self, unique_id: int,
            model: MammothWolfModel,
            ep_gain: int,
            max_init_ep: int,
            reproduction_threshold: int
    ):
        super().__init__(
            unique_id=unique_id,
            model=model,
            ep_gain=ep_gain,
            ep_gain_grass=0,
            ep_gain_weed=0,
            max_init_ep=max_init_ep,
            reproduction_threshold=reproduction_threshold
        )
        self.race = 0

    def eat(self):
        self.model: MammothWolfModel
        agent: MammothAgent
        rabbit = [agent for agent in self.model.grid.get_cell_list_contents([self.pos]) if agent.race == 1]
        if len(rabbit) > 0:
            self.model.random.choice(rabbit).energy = -1  # the safest method to kill them
            self.energy += self.ep_gain

    def move(self):
        """
        Implement active hunt.

        Hunting if the parameter is true.
        Choose a neighboring cell with sheep.
        """
        self.model: MammothWolfModel
        if self.allow_hunt():
            cells = self.model.grid.get_neighborhood(
                pos=self.pos,
                moore=True,
                include_center=False,
                radius=1
            )
            cells_to_move = []
            cell_contents = {cell: self.model.grid.get_cell_list_contents([cell]) for cell in cells}
            for cell in cell_contents.keys():
                if cell_contents[cell] is not None:
                    cell_contents[cell] = {type(agent) for agent in cell_contents[cell]}
                    if MammothAgent in cell_contents[cell]:
                        cells_to_move.append(cell)
            if len(cells_to_move) > 0:
                dest_cell = self.model.random.choice(cells_to_move)
            else:
                dest_cell = self.model.random.choice(cells)
            self.model.grid.move_agent(self, dest_cell)
        else:
            super().move()

    def allow_hunt(self) -> bool:
        self.model: MammothWolfModel
        return (self.model.allow_hunt and self.energy > 0 and
                self.model.random.random() < (self.energy ** self.model.hunt_exponent))


class MammothAgent(MammothWolfAgent):
    """Agent class for mammoths.

    Implement grazing and flocking.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (MammothWolfModel): the MammothWolf model
        ep_gain_grass (int): energy point gained from eating grass
        ep_gain_weed (int): energy point gained from eating weeds
        max_init_ep (int): maximum initial energy point
        reproduction_threshold (int): necessary energy point for reproduction
    """
    def __init__(
            self, unique_id: int,
            model: MammothWolfModel,
            ep_gain_grass: int,
            ep_gain_weed: int,
            max_init_ep: int,
            reproduction_threshold: int
    ):
        super().__init__(
            unique_id=unique_id,
            model=model,
            ep_gain=0,
            ep_gain_grass=ep_gain_grass,
            ep_gain_weed=ep_gain_weed,
            max_init_ep=max_init_ep,
            reproduction_threshold=reproduction_threshold
        )
        self.race = 1

    def eat(self):
        self.model: MammothWolfModel
        agent: GrassAgent
        for agent in self.model.grid.get_cell_list_contents([self.pos]):
            if agent.race >= 2 and agent.grown:
                self.energy += self.ep_gain_grass
                if agent.race == 3:
                    self.energy += self.ep_gain_weed - self.ep_gain_grass
                agent.grown = False

    def move(self):
        """Implement flocking."""
        self.model: MammothWolfModel
        if self.model.allow_flocking and self.energy > 0:  # if energy is too low focus on survival
            cells = self.model.grid.get_neighborhood(
                pos=self.pos,
                moore=True,
                include_center=False,
                radius=1
            )
            cells_to_move = []
            cell_contents = {cell: self.model.grid.get_cell_list_contents([cell]) for cell in cells}
            for cell in cell_contents.keys():
                if cell_contents[cell] is not None:
                    cell_contents[cell] = {type(agent) for agent in cell_contents[cell]}
                    if MammothAgent in cell_contents[cell]:
                        # Include center to not make reproduction impossible
                        for neighbor in self.model.grid.get_neighborhood(
                                pos=cell,
                                moore=True,
                                include_center=True,
                                radius=1
                        ):
                            if neighbor in cells:
                                cells_to_move.append(cell)
            if len(cells_to_move) > 0:
                dest_cell = self.model.random.choice(cells_to_move)
            else:
                dest_cell = self.model.random.choice(cells)
            self.model.grid.move_agent(agent=self, pos=dest_cell)
        else:
            super().move()


class GrassAgent(Agent):
    """
    Agent class for grass.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (MammothWolfModel): the MammothWolf model
        grass_regrow_rate (float): Number of steps after grazed cell becomes grown grass again
        weed_regrow_rate (float): Number of steps after grazed cell becomes grown weed again
    """
    def __init__(
            self,
            unique_id: int,
            model: MammothWolfModel,
            grass_regrow_rate: float,
            weed_regrow_rate: float
    ):
        if mesa_version == "2.4.0":
            super().__init__(unique_id=unique_id, model=model)
        elif mesa_version > "2.4.0":
            super().__init__(model=model)
        else:
            try:
                super().__init__(unique_id=unique_id, model=model)
            except:
                print("Incompatible mesa version.")

        self.grass_regrow_rate = grass_regrow_rate
        self.weed_regrow_rate = weed_regrow_rate
        self.race = 2
        self.grown = False
        self.grow()

    def step(self):
        self.grow()

    def grow(self):
        """Handle countdown and regrowing."""
        if not self.grown:
            if self.model.random.random() < self.weed_regrow_rate:
                self.race = 3
                self.grown = True
            if self.model.random.random() < self.grass_regrow_rate:
                self.race = 2
                self.grown = True
