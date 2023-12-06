from pomegranate.distributions import Categorical, Normal, Bernoulli
from pomegranate.gmm import GeneralMixtureModel

from data import get_data


def spawn_model():
    units_A = Categorical()
    units_B = Categorical()

    dmg_A = Normal()
    hp_A  = Normal()

    dmg_B = Normal()
    hp_B  = Normal()

    agg_off_A = Normal()
    agg_def_A = Normal()

    agg_off_B = Normal()
    agg_def_B = Normal()

    agg = Normal()

    result = Bernoulli()

    model = GeneralMixtureModel()

    model.add_distribution(units_A)
    model.add_distribution(units_B)
    model.add_distribution(dmg_A)
    model.add_distribution(hp_A)
    model.add_distribution(dmg_B)
    model.add_distribution(hp_B)
    model.add_distribution(agg_off_A)
    model.add_distribution(agg_def_A)
    model.add_distribution(agg_off_B)
    model.add_distribution(agg_def_B)
    model.add_distribution(agg)
    model.add_distribution(result)

    model.add_edges([
        (dmg_A, agg_off_A), (hp_A, agg_def_A), (units_A, agg_off_A), (units_A, agg_def_A),
        (dmg_B, agg_off_B), (hp_B, agg_def_B), (units_B, agg_off_B), (units_B, agg_def_B),
        (agg_off_A, agg), (agg_def_A, agg), (agg_off_B, agg), (agg_def_B, agg),
        (agg, result)
    ])

    return model

data = get_data()
model = spawn_model()
model.fit(data)
