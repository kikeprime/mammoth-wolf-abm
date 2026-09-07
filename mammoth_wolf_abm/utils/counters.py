from mesa.model import Model

import mammoth_wolf_abm.model as abm
from mammoth_wolf_abm.agents import DireWolfAgent, GrassAgent, MammothAgent


def count_grass_cells(model: Model) -> float:
    """
    Return percentage of grown grass.
    :param MammothWolfModel model: Model whose grass filled cells are counted
    :returns float: Percentage of cells filled with grass
    """
    model: abm.MammothWolfModel
    result = 0
    for agent in model.schedule.agents:
        if isinstance(agent, GrassAgent):
            agent: GrassAgent
            if agent.grown:
                result += 1
    return 100 * result / float(model.grid.width * model.grid.height)


def count_mammoths(model: Model) -> int:
    """
    Return the number of mammoths.
    :param MammothWolfModel model: Model whose mammoth agents are counted
    :returns int: Number of mammoths
    """
    model: abm.MammothWolfModel
    result = 0
    for agent in model.schedule.agents:
        if isinstance(agent, MammothAgent):
            result += 1
    return result


def count_dire_wolves(model: Model) -> int:
    """
    Return the number of dire wolves.
    :param MammothWolfModel model: Model whose dire wolf agents are counted
    :returns int: Number of dire wolves
    """
    model: abm.MammothWolfModel
    result = 0
    for agent in model.schedule.agents:
        if isinstance(agent, DireWolfAgent):
            result += 1
    return result
