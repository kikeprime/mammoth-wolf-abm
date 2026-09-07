from dataclasses import dataclass

from .animal_data import AnimalData


@dataclass
class DireWolfData(AnimalData):
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
    hunt_success_rate: float
