from dataclasses import asdict, dataclass


@dataclass
class DireWolfData:
    """Dataclass containing the data for the DireWolfAgent.
    Attributes:
        ep_gain (int): energy point gained from eating
        max_age (int): maximum age allowed for this agent in years
        reproductive_age (int): minimum age allowed for reproduction in years
        gestation_period (int): gestation period in months
        birth_interval (int): birth_interval in months
        hunt_success_rate (float): Probability of successful hunt in percentage
        is_child (bool): whether the agent is child or not
    """
    ep_gain: int
    max_age: int
    reproductive_age: int
    gestation_period: int
    birth_interval: int
    hunt_success_rate: float
    is_child: bool

    def __iter__(self):
        """Allow dict to be used on this class' objects."""
        yield from asdict(self).items()
