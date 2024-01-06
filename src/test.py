from typing import Callable

from model import Model

from time import time, process_time

# # # # # # # # # # # # # # # # # # #
#            MODEL TESTING          #
#                                   #
# Runs a series of queries against  #
# a saved model and prints results. #
# # # # # # # # # # # # # # # # # # #

# Various prediction test cases
unit_setups: list[list[dict[str, int], dict[str, int]]] = [
    [{"Marine": 30, "Reaper": 20, "SiegeTank": 20}, {"Marine": 200}],
    [{"Marine": 50, "Reaper": 10, "SiegeTank": 2}, {"Marine": 100, "Reaper": 10, "SiegeTank": 10}],
    [{"Marine": 100, "Reaper": 0, "SiegeTank": 1}, {"Marine": 100, "Reaper": 0, "SiegeTank": 0}],
]

def make_prediction(model: Model, unit_setup: list[dict[str, int]]) -> None:
    """Make a prediction, print results, and
    time it took to make prediction.

    Args:
        model (Model): Model
        setup_fn (Callable): Setup function
    """
    print("-------- Prediction --------")
    with model.prediction():
        print("Prediction setup...", end="")
        set_unit_counts(model, unit_setup)
        print("done")

        print("Making prediction...", end="")
        p0, t0 = process_time(), time()
        # Get prediction of player 0 winning
        prob = model.make_prediction(0)
        p1, t1 = process_time(), time()

        print("done")
        print(f"Prediction took {t1-t0} seconds ({p1-p0} CPU time)")
        print(f"Prediction player 0 win: {prob}")

def set_unit_counts(model: Model, unit_setup: list[dict[str, int]]) -> None:
    """Setup 1

    Args:
        model (Model): Model
    """
    for player, units in enumerate(unit_setup):
        print(f"Player {player} units:")
        for unit, count in units.items():
            print(f"{unit}: {count}")
            model.use_unit_count(0, unit, count)

if __name__ == "__main__":
    print("Loading model...", end="")
    p0, t0 = process_time(), time()
    model = Model.load()
    p1, t1 = process_time(), time()
    print("done")
    print(f"Loading model took {t1-t0} seconds ({p1-p0} CPU time)")

    for unit_setup in unit_setups:
        make_prediction(model, unit_setup)
