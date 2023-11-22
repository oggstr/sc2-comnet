import pymc3 as pm
import theano.tensor as tt

# Number of unit types
U = 100

#observed_data = ...

with pm.Model() as combat_model:
    unit_counts_A = pm.Poisson('unit_counts_A', mu=1, shape=U)
    unit_counts_B = pm.Poisson('unit_counts_B', mu=1, shape=U)

    offense_A = pm.Normal('offense_A', mu=0, sd=1)
    defense_A = pm.Normal('defense_A', mu=0, sd=1)
    offense_B = pm.Normal('offense_B', mu=0, sd=1)
    defense_B = pm.Normal('defense_B', mu=0, sd=1)

    O_A = pm.Deterministic("O_A", tt.sum(offense_A))
    D_A = pm.Deterministic("D_A", tt.sum(offense_A))
    O_B = pm.Deterministic("O_B", tt.sum(offense_A))
    D_B = pm.Deterministic("D_B", tt.sum(offense_A))

    Agg = pm.Deterministic("Agg", O_A / D_B - O_B / D_A)

    R = pm.Deterministic('R', 1 / (1 + tt.exp(-tt.sum(Agg))))

    #likelihood = pm.Normal('likelihood', mu=R, sd=1, observed=observed_data)

with combat_model:
    trace = pm.sample(100, tune=50)
