import bnlearn as bn
from network import Network
from model import Model

net = Network()

net.add_unit("Marine")
net.add_unit("Reaper")

net.add_feature("dmg", "hp")

df, edges, continuous_columns = net.make_network()

dag = bn.make_DAG(edges)

df_discrete = bn.discretize(df, edges, continuous_columns, max_iterations=1)
dag = bn.parameter_learning.fit(dag, df_discrete, methodtype="maximumlikelihood")

model = Model(dag, net.get_units(), net.get_features())

model.save()

""" with model.prediction():
    model.use_unit_count(0, "Marine", 10)
    model.use_unit_count(0, "Reaper", 0)
    model.use_unit_count(1, "Marine", 10)
    model.use_unit_count(1, "Reaper", 0)
    q = model.make_prediction() """

""" q1 = bn.inference.fit(model, variables=["result"], evidence={
    "Marine-count-player_A": 10,
    "Reaper-count-player_A": 0,
    "Marine-count-player_B": 10,
    "Reaper-count-player_B": 0,
})
print(q1) """
#bn.plot(model, interactive=True)
#agg-count-player_A