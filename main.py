import argparse

from mammoth_wolf_abm.model import MammothWolfModel
from mammoth_wolf_abm.server import params


def main(seed: int | float | None = None, steps: int = 0):
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
    for i in range(steps):
        model.step()
    df = model.datacollector.get_model_vars_dataframe()
    df.to_csv(
        f"mammoth-wolf-abm-{model.seed}.csv",
        sep=";",
        decimal=",",
        index=False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Mammoth - Dire Wolf ABM")
    parser.add_argument(
        "--seed",
        type=float,
        default=None,
        help="Random Seed",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=36500,
        help="Steps",
    )
    args = parser.parse_args()
    main(seed=args.seed, steps=args.steps)
