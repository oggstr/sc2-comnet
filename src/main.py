import bnlearn as bn
from network import Network
from model import Model

def produce_model() -> None:
    """Produce and save a model as pickle file
    """
    net = Network()

    net.add_unit("Marine")
    net.add_unit("Reaper")
    net.add_unit("Marauder")
    net.add_unit("SiegeTank")

    net.add_feature("dmg", "hp")

    df, edges, continuous_columns = net.make_network()

    dag = bn.make_DAG(edges)

    df_discrete = bn.discretize(df, edges, continuous_columns, max_iterations=1)
    dag = bn.parameter_learning.fit(dag, df_discrete, methodtype="maximumlikelihood")

    """ q1 = bn.inference.fit(dag, variables=["result"], evidence={
        "Marine-count-player_A": 10,
        "Reaper-count-player_A": 0,
        "Marine-count-player_B": 10,
        "Reaper-count-player_B": 0,
    }) """
                        
    model = Model(dag, net.get_units(), net.get_features())

    model.save()

if __name__ == "__main__":
    produce_model()