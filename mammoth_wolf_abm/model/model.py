from mammoth_wolf_abm.agents import GrassAgent
from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation


class MammothWolfModel(Model):
    def __init__(
            self,
            width: int,
            height: int,
            torus: bool,
            grass_regrow_rate: float,
            allow_seed: bool,
            random_seed: int,
    ):
        super().__init__()
        self.schedule = RandomActivation(model=self)
        self.grid = MultiGrid(width=width, height=height, torus=torus)

        # Params here

        if allow_seed:
            self.random.seed(a=random_seed)

        # Adding animal agents here

        # Adding grass
        for grass_id in range(width * height):
            grass = GrassAgent(
                unique_id=self.next_id(),
                model=self,
                grass_regrow_rate=grass_regrow_rate / 100.0,
            )
            self.schedule.add(agent=grass)
            self.grid.place_agent(agent=grass, pos=(grass_id % width, grass_id // width))

        self.datacollector = DataCollector(
            model_reporters={
                "Ratio of grass patches (%)": grass_counter,
            }
        )
        self.datacollector.collect(model=self)

    def step(self) -> None:
        self.schedule.step()
        self.datacollector.collect(model=self)


# Agent counters
def grass_counter(model: MammothWolfModel) -> float:
    """Return percentage of grown grass."""
    result = 0
    for agent in model.schedule.agents:
        agent: GrassAgent
        if agent.grown:
            result += 1
    return 100 * result / float(model.grid.width * model.grid.height)
