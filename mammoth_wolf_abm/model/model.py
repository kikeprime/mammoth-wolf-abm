from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


class MammothWolfModel(Model):
    def __init__(
            self,
            width: int,
            height: int,
            torus: bool,
            allow_seed: bool,
            random_seed: int
    ):
        super().__init__()
        self.schedule = RandomActivation(model=self)
        self.grid = MultiGrid(width=width, height=height, torus=torus)

        # Params here

        if allow_seed:
            self.random.seed(random_seed)

        # Adding agents here

        self.datacollector = DataCollector(
            model_reporters={}
        )
        self.datacollector.collect(self)
