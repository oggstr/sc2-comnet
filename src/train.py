import bnlearn as bn
from network import Network
from model import Model

# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                 MODEL TRAINING                    #
#                                                   #
# Warning: This takes can take a really long time!  #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

def produce_model() -> None:
    """Produce and save a model as pickle file
    """
    net = Network()

    # Add units modeled by the network
    net.add_unit("Marine")
    net.add_unit("Reaper")
    net.add_unit("Marauder")
    net.add_unit("SiegeTank")

    # Add feature tuples modeled by the network
    net.add_feature("dmg", "hp")

    # Produce training data, edges,
    # and which columns are continuos (needed for discretization)
    df, edges, continuous_columns = net.make_network()

    # Create DAG from edges
    dag = bn.make_DAG(edges)

    # Discretize
    df_discrete = bn.discretize(df, edges, continuous_columns, max_iterations=8)

    # Train using MLE
    dag = bn.parameter_learning.fit(dag, df_discrete, methodtype="maximumlikelihood")

    # Save model
    model = Model(dag, net.get_units(), net.get_features())
    model.save()

if __name__ == "__main__":
    produce_model()