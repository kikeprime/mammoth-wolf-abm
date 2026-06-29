"""
Simulation of MammothWolf without the server app.
"""

import matplotlib.pyplot as plt

from mammoth_wolf_abm import MammothWolfModel


def main():
    width = 30
    height = 30
    torus = True
    model_type = "Mammoths and Wolves model"
    n_mammoth = 150
    n_wolf = 50
    mammoth_ep_gain_grass = 5
    mammoth_ep_gain_weed = 0
    wolf_ep_gain = 5
    mammoth_max_init_ep = 10
    wolf_max_init_ep = 10
    mammoth_reproduction_threshold = 15
    wolf_reproduction_threshold = 15
    grass_regrow_rate = 30
    weed_regrow_rate = 0
    allow_hunt = True
    allow_flocking = False
    hunt_exponent = -0.5
    a = 1
    b = 1
    c = 1
    d = 1
    allow_seed = True
    seed = 474
    model = MammothWolfModel(
        width=width,
        height=height,
        torus=torus,
        model_type=model_type,
        n_mammoth=n_mammoth,
        n_wolf=n_wolf,
        mammoth_ep_gain_grass=mammoth_ep_gain_grass,
        mammoth_ep_gain_weed=mammoth_ep_gain_weed,
        wolf_ep_gain=wolf_ep_gain,
        mammoth_max_init_ep=mammoth_max_init_ep,
        wolf_max_init_ep=wolf_max_init_ep,
        mammoth_reproduction_threshold=mammoth_reproduction_threshold,
        wolf_reproduction_threshold=wolf_reproduction_threshold,
        grass_regrow_rate=grass_regrow_rate,
        weed_regrow_rate=weed_regrow_rate,
        allow_flocking=allow_flocking,
        allow_hunt=allow_hunt,
        hunt_exponent=hunt_exponent,
        a=a, b=b, c=c, d=d,
        allow_seed=allow_seed,
        random_seed=seed
    )
    t = 100
    for sim_t in range(t):
        model.step()

    df = model.datacollector.get_model_vars_dataframe()
    df.index.name = "Step"
    df[df.columns[:2]].plot()
    plt.show()
    df[df.columns[-2:]].plot()
    plt.show()
    print(df)


main()
