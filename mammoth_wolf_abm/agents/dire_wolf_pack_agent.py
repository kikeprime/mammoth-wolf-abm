from importlib.metadata import version

from mesa.agent import Agent
from mesa.model import Model

from .mammoth_agent import MammothAgent
from .dire_wolf_agent import DireWolfAgent
import mammoth_wolf_abm.model as abm


class DireWolfPackAgent(Agent):
    def __init__(self, unique_id: int, model: Model, pack_id: int, pos: tuple[int, int]):
        if version("mesa") == "2.4.0":
            super().__init__(unique_id=unique_id, model=model)
        elif version("mesa") > "2.4.0":
            super().__init__(model=model)
        else:
            try:
                super().__init__(unique_id=unique_id, model=model)
            except TypeError or AttributeError:
                print("Incompatible mesa version.")

        self.unique_id = unique_id
        self.pack_id = pack_id
        self.model = model
        self.pos = pos
        self.members = []

    def move(self):
        """Implement movement of the pack."""
        self.model: abm.MammothWolfModel
        cells_to_move, cells_with_mammoth = self.get_dest_cells()
        dest_cell = None
        if len(cells_with_mammoth) > 0:
            # Extra limits on hunting goes here.
            dest_cell = self.model.random.choice(seq=cells_with_mammoth)
        elif len(cells_to_move) > 0:
            dest_cell = self.model.random.choice(seq=cells_to_move)
        if dest_cell is not None:
            self.pos = dest_cell
            for agent in self.members:
                self.model.grid.move_agent(agent=agent, pos=dest_cell)

    def add_member(self, dire_wolf: DireWolfAgent):
        self.model: abm.MammothWolfModel
        dire_wolf.pack = self.pack_id
        dire_wolf.child_data.pack = self.pack_id
        self.model.place_agent(agent=dire_wolf, pos=self.pos)
        self.members.append(dire_wolf)

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
