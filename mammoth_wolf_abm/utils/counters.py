from mesa.model import Model

import mammoth_wolf_abm.model as abm
from mammoth_wolf_abm.agents import DireWolfAgent, DireWolfPackAgent, GrassAgent, MammothAgent


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


def count_dire_wolves(model: Model, pack: int = None) -> int:
    """
    Return the number of dire wolves.
    :param MammothWolfModel model: Model whose dire wolf agents are counted
    :param int pack: the dire wolf agent's pack
    :returns int: Number of dire wolves
    """
    model: abm.MammothWolfModel
    result = 0
    for agent in model.schedule.agents:
        if isinstance(agent, DireWolfAgent):
            if pack is None or agent.pack == pack:
                result += 1
    return result


def count_dire_wolf_packs(model: Model) -> int:
    """
    Return the number of dire wolf packs.
    :param MammothWolfModel model: Model whose dire wolf pack agents are counted
    :returns int: Number of dire wolf packs
    """
    model: abm.MammothWolfModel
    result = 0
    for agent in model.schedule.agents:
        if isinstance(agent, DireWolfPackAgent):
            result += 1
    return result
