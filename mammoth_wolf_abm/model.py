import numpy as np
from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from scipy.integrate import solve_ivp

import mammoth_wolf_abm as mw


class MammothWolfModel(Model):
    """
    Class for the RabbitGrassWeed model.

    Parameters:
        width (int): Width of the grid
        height (int): Height of the grid
        torus (bool): Torus for grid
        model_type (str): Model type
        n_mammoth (int): Initial number of rabbits
        n_wolf (int): Initial number of foxes
        mammoth_ep_gain_grass (int): Energy point gain for rabbits from grass
        mammoth_ep_gain_weed (int): Energy point gain for rabbits from weed
        wolf_ep_gain (int): Energy point gain for foxes
        mammoth_max_init_ep (int): maximum initial energy point for rabbits
        wolf_max_init_ep (int): maximum initial energy point for foxes
        mammoth_reproduction_threshold (int): Reproduction threshold for rabbits
        wolf_reproduction_threshold (int): Reproduction threshold for foxes
        grass_regrow_rate (int): Probability of grass growth (%)
        weed_regrow_rate (int): Probability of weed growth (%)
        allow_flocking (bool): Allow flocking
        allow_hunt (bool): Allow hunt
        hunt_exponent (float): Limiter exponent for hunt
        a (float): a parameter of the Lotka-Volterra model
        b (float): b parameter of the Lotka-Volterra model
        c (float): c parameter of the Lotka-Volterra model
        d (float): d parameter of the Lotka-Volterra model
        allow_seed (bool): Allow seed usage
        random_seed (int): Random seed
    """

    def __init__(self, width: int, height: int, torus: bool,
                 model_type: str, n_mammoth: int, n_wolf: int,
                 mammoth_ep_gain_grass: int, mammoth_ep_gain_weed: int, wolf_ep_gain: int,
                 mammoth_max_init_ep: int, wolf_max_init_ep: int,
                 mammoth_reproduction_threshold: int, wolf_reproduction_threshold: int,
                 grass_regrow_rate: int, weed_regrow_rate: int,
                 allow_flocking: bool, allow_hunt: bool, hunt_exponent: float,
                 a: float, b: float, c: float, d: float,
                 allow_seed: bool, random_seed: int):
        super().__init__()
        self.schedule = RandomActivation(model=self)
        self.grid = MultiGrid(width=width, height=height, torus=torus)

        # model-version in the NetLogo code
        model_types = {
            "Extended model": 0,
            "Rabbits, Grass and Weeds model": 1,
            "Foxes and Rabbits Lotka-Volterra model": 2,
            "Bővített modell": 0,
            "Nyulak, fű és gyomnövények modell": 1,
            "Rókák és nyulak Lotka-Volterra-modell": 2
        }
        self.model_type = model_types[model_type]

        self.n_mammoth = n_mammoth
        self.n_wolf = n_wolf
        self.mammoth_ep_gain_grass = mammoth_ep_gain_grass
        self.mammoth_ep_gain_weed = mammoth_ep_gain_weed
        self.wolf_ep_gain = wolf_ep_gain
        self.mammoth_max_init_ep = mammoth_max_init_ep
        self.wolf_max_init_ep = wolf_max_init_ep
        self.mammoth_reproduction_threshold = mammoth_reproduction_threshold
        self.wolf_reproduction_threshold = wolf_reproduction_threshold

        self.a, self.b, self.c, self.d = abs(a), abs(b), abs(c), abs(d)

        self.allow_hunt = allow_hunt
        self.allow_flocking = allow_flocking
        self.hunt_exponent = -abs(hunt_exponent)

        if allow_seed:
            self.random.seed(random_seed)

        # Adding mammoths
        for i in range(self.n_mammoth):
            mammoth = mw.MammothAgent(
                unique_id=self.next_id(),
                model=self,
                ep_gain_grass=self.mammoth_ep_gain_grass,
                ep_gain_weed=self.mammoth_ep_gain_weed,
                max_init_ep=self.mammoth_max_init_ep,
                reproduction_threshold=self.mammoth_reproduction_threshold
            )
            if self.model_type == 0:
                mammoth.gender = self.random.choice([True, False])
            else:
                mammoth.gender = True
            self.schedule.add(mammoth)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(mammoth, (x, y))

        # Adding wolves
        for i in range(self.n_wolf):
            wolf = mw.WolfAgent(
                unique_id=self.next_id(),
                model=self,
                ep_gain=self.wolf_ep_gain,
                max_init_ep=self.wolf_max_init_ep,
                reproduction_threshold=self.wolf_reproduction_threshold
            )
            if self.model_type == 0:
                wolf.gender = self.random.choice([True, False])
            else:
                wolf.gender = False
            self.schedule.add(agent=wolf)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(agent=wolf, pos=(x, y))

        # Adding grass and weeds
        for grass_id in range(width * height):
            grass = mw.GrassAgent(
                unique_id=self.next_id(),
                model=self,
                grass_regrow_rate=grass_regrow_rate / 100.0,
                weed_regrow_rate=weed_regrow_rate / 100.0
            )
            self.schedule.add(agent=grass)
            self.grid.place_agent(agent=grass, pos=(grass_id % width, grass_id // width))

        self.datacollector = DataCollector(
            model_reporters={
                "Number of rabbits": self.mammoth_counter,
                "Number of foxes": self.wolf_counter,
                "Number of female rabbits": self.female_mammoth_counter,
                "Number of male rabbits": self.male_mammoth_counter,
                "Number of female foxes": self.female_wolf_counter,
                "Number of male foxes": self.male_wolf_counter,
                "Ratio of grass patches (%)": self.grass_counter,
                "Ratio of weed patches (%)": self.weed_counter
            }
        )
        self.datacollector.collect(self)
        if self.model_type == 2:
            self.solution = solve_ivp(
                fun=self.lotka_volterra,
                t_span=(0, 10000),
                y0=[self.n_mammoth, self.n_wolf],
                method="RK45",
                dense_output=True,
                atol=1e-8,
                rtol=1e-6
            )

    def lotka_volterra(self, t, z):
        x, y = z
        dxdt = self.a * x - self.b * x * y
        dydt = -self.c * y + self.d * x * y
        return [dxdt, dydt]

    def step(self):
        self.schedule.step()
        if self.model_type == 2:
            self.lv_step()
        self.datacollector.collect(self)

    def lv_step(self):
        if self.schedule.steps < 10000:
            mammoths = np.round(self.solution.y[0][self.schedule.steps]).astype(int)
            wolves = np.round(self.solution.y[1][self.schedule.steps]).astype(int)
            print(mammoths)
            print(wolves)
            dx = mammoths - self.mammoth_counter(self)
            if dx < 0:
                agent: mw.MammothAgent
                for agent in self.schedule.agents:
                    if isinstance(agent, mw.MammothAgent) and self.mammoth_counter(self) > mammoths:
                        agent.destroy()
            else:
                for i in range(dx):
                    mammoth = mw.MammothAgent(
                        unique_id=self.next_id(),
                        model=self,
                        ep_gain_grass=self.mammoth_ep_gain_grass,
                        ep_gain_weed=self.mammoth_ep_gain_weed,
                        max_init_ep=self.mammoth_max_init_ep,
                        reproduction_threshold=self.mammoth_reproduction_threshold
                    )
                    mammoth.gender = True
                    self.schedule.add(mammoth)
                    self.grid.place_agent(mammoth, (0, 0))
            dy = wolves - self.wolf_counter(self)
            if dy < 0:
                agent: mw.WolfAgent
                for agent in self.schedule.agents:
                    if isinstance(agent, mw.WolfAgent) and self.wolf_counter(self) > wolves:
                        agent.destroy()
            else:
                for i in range(dy):
                    wolf = mw.WolfAgent(
                        unique_id=self.next_id(),
                        model=self,
                        ep_gain=self.wolf_ep_gain,
                        max_init_ep=self.wolf_max_init_ep,
                        reproduction_threshold=self.wolf_reproduction_threshold
                    )
                    wolf.gender = False
                    self.schedule.add(wolf)
                    self.grid.place_agent(wolf, (0, 0))

    def place_child(self, child, pos):
        self.schedule.add(agent=child)
        neighborhood = self.grid.get_neighborhood(pos=pos, moore=True, include_center=False, radius=1)
        self.grid.place_agent(agent=child, pos=self.random.choice(neighborhood))

    # Agent counters
    @staticmethod
    def agent_counter(model, race: int, by_gender=False, gender=False) -> int:
        """
        Count number of rabbits and foxes.

        Parameters:
            model (MammothWolfModel): model instance
            race (int): agent race
            by_gender (bool): whether to count specific gender (optional)
            gender (bool): specify gender (optional)
        """
        result = 0
        for agent in model.schedule.agents:
            agent: mw.MammothAgent | mw.WolfAgent
            if agent.race == race:
                if by_gender and agent.gender == gender or not by_gender:
                    result += 1
        return result

    @staticmethod
    def wolf_counter(model) -> int:
        return model.agent_counter(model=model, race=0)

    @staticmethod
    def mammoth_counter(model) -> int:
        return model.agent_counter(model=model, race=1)

    @staticmethod
    def female_wolf_counter(model) -> int:
        return model.agent_counter(model=model, race=0, by_gender=True, gender=True)

    @staticmethod
    def male_wolf_counter(model) -> int:
        return model.agent_counter(model=model, race=0, by_gender=True, gender=False)

    @staticmethod
    def female_mammoth_counter(model) -> int:
        return model.agent_counter(model=model, race=1, by_gender=True, gender=True)

    @staticmethod
    def male_mammoth_counter(model) -> int:
        return model.agent_counter(model=model, race=1, by_gender=True, gender=False)

    @staticmethod
    def grass_counter(model) -> float:
        """Return percentage of grown grass."""
        result = 0
        for agent in model.schedule.agents:
            agent: mw.GrassAgent
            if agent.race == 2 and agent.grown:
                result += 1
        return 100 * result / float(model.grid.width * model.grid.height)

    @staticmethod
    def weed_counter(model) -> float:
        """Return percentage of grown weed."""
        result = 0
        for agent in model.schedule.agents:
            agent: mw.GrassAgent
            if agent.race == 3 and agent.grown:
                result += 1
        return 100 * result / float(model.grid.width * model.grid.height)
