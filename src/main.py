import bnlearn as bn
from network import Network

net = Network()

net.add_unit("Marine")
net.add_unit("Reaper")

net.add_feature("dmg", "hp")

df = net.make_data_frame()
print(df)

exit(1)
df = get_data_frame()

edges: list[tuple[str, str]] = [
    ("count_a", "agg_off_a"),
    ("count_a", "agg_def_a"),
    ("dmg_a", "agg_off_a"),
    ("hp_a", "agg_def_a"),

    ("count_b", "agg_off_b"),
    ("count_b", "agg_def_b"),
    ("dmg_b", "agg_off_b"),
    ("hp_b", "agg_def_b"),

    ("agg_off_a", "agg"),
    ("agg_def_a", "agg"),
    ("agg_off_b", "agg"),
    ("agg_def_b", "agg"),

    ("agg", "res"),
]

DAG = bn.make_DAG(edges)

continuous_columns = ["agg_off_a", "agg_def_a", "agg_off_b", "agg_def_b", "agg"]
df_discrete = bn.discretize(df, edges, continuous_columns, max_iterations=1)

model = bn.parameter_learning.fit(DAG, df_discrete, methodtype="maximumlikelihood")

bn.plot(model, interactive=True)