from dataclasses import dataclass


@dataclass
class MammothData:
    """Dataclass containing the data for the MammothAgent.
    Attributes:
        ep_gain (int): energy point gained from eating
        max_age (int): maximum age allowed for this agent in years
        reproductive_age (int): minimum age allowed for reproduction in years
        gestation_period (int): gestation period in months
        birth_interval (int): birth_interval in months
        is_child (bool): whether the agent is child or not
    """
    ep_gain: int
    max_age: int
    reproductive_age: int
    gestation_period: int
    birth_interval: int
    is_child: bool
