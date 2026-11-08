import argparse

from mammoth_wolf_abm.model import MammothWolfModel
from mammoth_wolf_abm.server import params


def main(seed: int | None = None):
    param_dict = {}
    for key in params.keys():
        if type(params[key]) is int:
            param_dict[key] = params[key]
        else:
            param_dict[key] = params[key].value
    if seed is not None:
        param_dict["allow_seed"] = True
        param_dict["random_seed"] = seed
    else:
        param_dict["allow_seed"] = False
    model = MammothWolfModel(**param_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Mammoth - Dire Wolf ABM")
    parser.add_argument(
        dest="seed",
        type=int,
        nargs="?",
        default=None,
        help="Random Seed",
    )
    args = parser.parse_args()
    main(seed=args.seed)
