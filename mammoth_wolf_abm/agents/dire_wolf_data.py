from dataclasses import dataclass

from .animal_data import AnimalData


@dataclass
class DireWolfData(AnimalData):
    """Dataclass containing the data for the DireWolfAgent.
    Attributes:
        hunt_success_rate (float): Probability of successful hunt in percentage
    """
    hunt_success_rate: float
