import pymc3 as pm
import theano.tensor as tt
import numpy as np

import data as sims
from data import Result
import unit.type_id as ti

MARINE = ti.register("Marine")
REAPER = ti.register("Reaper")

UNITS_MODELED = ti.count()

MATCHES = sims.parse()

MAX_UNIT = 100

def create_data():
    match_count = len(MATCHES)
    data_player_a = np.ndarray(shape=(UNITS_MODELED, match_count), dtype=int)
    data_player_b = np.ndarray(shape=(UNITS_MODELED, match_count), dtype=int)
    data_win = np.ndarray(shape=(match_count), dtype=float)
    for match, match_data in enumerate(MATCHES):

        # Player A
        for unit in range(UNITS_MODELED):
            data_player_a[unit][match] = match_data.get_a(ti.id(unit))

        # Player B
        for unit in range(UNITS_MODELED):
            # offset for player B
            data_player_b[unit][match] = match_data.get_b(ti.id(unit))

        data_win[match] = match_data.win

    return (data_player_a, data_player_b, data_win)

data_a, data_b, data_win = create_data()

with pm.Model() as combat_model:
    count_marine_A = pm.Poisson("count_marine_A", mu=1, shape=MAX_UNIT, observed=data_a[MARINE][:])
    count_marine_B = pm.Poisson("count_marine_B", mu=1, shape=MAX_UNIT, observed=data_b[MARINE][:])

    count_reaper_A = pm.Poisson("count_reaper_A", mu=1, shape=MAX_UNIT, observed=data_a[REAPER][:])
    count_reaper_B = pm.Poisson("count_reaper_B", mu=1, shape=MAX_UNIT, observed=data_b[REAPER][:])

    off_marine_A = pm.Normal('off_marine_A', mu=0, sd=1)
    off_marine_B = pm.Normal('off_marine_B', mu=0, sd=1)

    def_marine_A = pm.Normal('def_marine_A', mu=0, sd=1)
    def_marine_B = pm.Normal('def_marine_B', mu=0, sd=1)

    off_reaper_A = pm.Normal('off_reaper_A', mu=0, sd=1)
    off_reaper_B = pm.Normal('off_reaper_B', mu=0, sd=1)

    def_reaper_A = pm.Normal('def_reaper_A', mu=0, sd=1)
    def_reaper_B = pm.Normal('def_reaper_B', mu=0, sd=1)

    O_A = pm.Deterministic("O_A", tt.sum([off_marine_A, off_reaper_A]))
    O_B = pm.Deterministic("O_B", tt.sum([off_marine_B, off_reaper_B]))

    D_A = pm.Deterministic("D_A", tt.sum([def_marine_A, def_reaper_A]))
    D_B = pm.Deterministic("D_B", tt.sum([def_marine_B, def_reaper_B]))

    Agg = pm.Deterministic("Agg", O_A / D_B - O_B / D_A)

    R = pm.Deterministic('R', 1 / (1 + tt.exp(-tt.sum(Agg))))

    likelihood = pm.Normal('likelihood', mu=R, sd=1, observed=data_win)

#with combat_model:
    trace = pm.sample(100, tune=50)
