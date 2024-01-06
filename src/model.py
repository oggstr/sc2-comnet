from __future__ import annotations

from typing import Generator

import os
import pickle
from pathlib import Path
from contextlib import contextmanager

import bnlearn as bn
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD

class Model():
    """
    Wrapper object for bnlearn network.

    Abstracts away the specifics of how to query
    the network such that it can be used more easily.

    The underlying network uses discretization, so this
    object takes care of mapping values to ranges.
    For example, a unit count of 5 Marines may get mapped to
    a range of [4, 11].
    """

    dag: dict
    """bnlearn dag object
    """

    units: set[str]
    """Modeled units
    """

    units_attrs: list[str]
    """Modeled unit attributes
    """

    valid_counts: dict[str, list[int]]
    """Valid values for count nodes
    """

    evidence: dict[str, int]
    """Evidence set before prediction
    """

    evidence_nodes: set[str]
    """Evidence node names (count nodes)
    """

    def __init__(self: Model, dag: dict, modeled_units: list[str], modeled_attrs: list[tuple[str, str]]):
        """Create new model wrapper

        Args:
            self (Model): Self
            dag (dict): DAG
            modeled_units (list[str]): Modeled units
            modeled_attrs (list[tuple[str, str]]): Modeled unit attributes
        """
        self.dag              = dag
        self.units            = set(modeled_units)
        self.units_attrs      = [a for pair in modeled_attrs for a in pair]
        self.valid_counts     = {}
        self.evidence         = {}
        self.evidence_nodes   = set()

        for unit in self.units:
            self.evidence_nodes.add(f"{unit}-count-player_A")
            self.evidence_nodes.add(f"{unit}-count-player_B")

        self.__steal_valid_values()

    def __steal_valid_values(self: Model) -> None:
        """Helper function steals valid count values
        in a really hacky from way from the underlying model

        Args:
            self (Model): Self
        """
        network: BayesianNetwork = self.dag["model"]

        cpds: list[TabularCPD] = network.get_cpds()

        for cpd in cpds:
            node_name: str = cpd.variable

            # Inputs to this model will only ever be unit counts,
            # so skip any non-count nodes.
            if "count" not in node_name:
                continue

            # Hack-deluxe way of attaining valid values
            # for this count node :-)
            values = cpd.name_to_no[node_name].keys()
            self.valid_counts[node_name] = list(values)

    def save(self: Model) -> None:
        """Save self as .pkl file.

        Args:
            self (Model): Self
        """
        with open("sc2_combat_model.pkl", "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load() -> Model:
        """Load the model from stored .pkl file.

        Returns:
            Model: Model
        """
        with open("sc2_combat_model.pkl", "rb") as file:
            return pickle.load(file)

    @contextmanager
    def prediction(self: Model) -> Generator[None, None, None]:
        """Start a new prediction

        Args:
            self (Model): Self

        Yields:
            Generator[None, None, None]: Ignore this
        """
        try:
            yield
        finally:
            # Rest evidence for next predictions
            self.evidence = {}

    def use_unit_count(self: Model, player: int, unit: str, count: int) -> None:
        """Use unit count for some unit for some plater

        Args:
            self (Model): Self
            player (int): Player (0 or 1)
            unit (str): Unit name
            count (int): Count of unit
        """
        node = f"{unit}-count-player_{'A' if player == 0 else 'B'}"

        if node not in self.valid_counts:
            print(f"Warning: Unit {unit} not supported by model")
            return

        self.__use_node_count(node, count)

    def __use_node_count(self: Model, node: str, count: int) -> None:
        """Internal function sets a count value for some node.
        This function maps count to some value range.

        Args:
            self (Model): Self
            node (str): Node name
            count (int): Count value
        """
        value_ranges = self.valid_counts[node]

        # Find what range count is in
        for value_range in value_ranges:
            if count not in value_range:
                continue

            self.evidence[node] = value_range
            return

        # Backup, find closest value to given count
        value_ranges = sorted(value_ranges, key = lambda val_range: abs(val_range.mid - count))
        self.evidence[node] = value_ranges[0]

    def make_prediction(self: Model, player: int) -> float:
        """Make prediction

        Args:
            self (Model): Self
            player (int): Player (0 or 1)

        Returns:
            float: prediction player 0 wins
        """

        # Any count values not already set, are set to 0
        nodes = self.evidence_nodes.difference(set(self.evidence.keys()))
        for node in nodes:
            self.__use_node_count(node, 0)

        q = bn.inference.fit(self.dag, variables=["result"], evidence=self.evidence, verbose=0)
        try:
            return q.df["p"][player]
        except Exception as e:
            print(f"Failed to make prediction: {e}")
            return 0.0