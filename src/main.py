import bnlearn as bn
from network import Network

net = Network()

net.add_unit("Marine")
net.add_unit("Reaper")

net.add_feature("dmg", "hp")

df, edges, continuous_columns = net.make_network()

DAG = bn.make_DAG(edges)

df_discrete = bn.discretize(df, edges, continuous_columns, max_iterations=1)

model = bn.parameter_learning.fit(DAG, df_discrete, methodtype="maximumlikelihood")

bn.plot(model, interactive=True)
#agg-count-player_A