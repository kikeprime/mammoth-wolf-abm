from dataclasses import asdict, dataclass


@dataclass
class AnimalData:
    """Dataclass containing the data for the AnimalAgent.
    Attributes:
        ep_gain (int): energy point gained from eating
        max_age (int): maximum age allowed for this agent in years
        reproductive_age (float): minimum age allowed for reproduction in years
        gestation_period (int): gestation period in months
        birth_interval (int): birth_interval in months
        litter_size (int): number of offsprings per litter
        is_child (bool): whether the agent is child or not
    """
    ep_gain: int
    max_age: int
    reproductive_age: float
    gestation_period: int
    birth_interval: int
    litter_size: int
    is_child: bool

    def __iter__(self):
        """Allow dict to be used on this class' objects."""
        yield from asdict(self).items()
