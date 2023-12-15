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

    dag: dict
    """bnlearn dag object
    """

    units: list[str]
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

    def __init__(self: Model, dag: dict, modeled_units: list[str], modeled_attrs: list[tuple[str, str]]):
        """Create new model wrapper

        Args:
            self (Model): Self
            dag (dict): DAG
            modeled_units (list[str]): Modeled units
            modeled_attrs (list[tuple[str, str]]): Modeled unit attributes
        """
        self.dag          = dag
        self.units        = modeled_units
        self.units_attrs  = [a for pair in modeled_attrs for a in pair]
        self.valid_counts = {}
        self.evidence     = {}

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
            if not "count" in node_name:
                continue

            # Hack-deluxe way of attaining valid values
            # for this count node :-)
            values = cpd.name_to_no[node_name].keys()
            self.valid_counts[node_name] = list(values)

    def save(self: Model) -> bool:
        with open("sc2_combat_model.pkl", "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load() -> Model:
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

        if not node in self.valid_counts:
            print(f"Warning: Unit {unit} not supported by model")
            return

        # Find closest value to given count
        values = self.valid_counts[node]
        value  = min(values, key = lambda val: abs(val-count))

        self.evidence[node] = value

    def make_prediction(self: Model) -> float:
        """Make prediction

        Args:
            self (Model): Self

        Returns:
            float: prediction player 0 wins
        """
        q = bn.inference.fit(self.dag, variables=["result"], evidence=self.evidence)
        try:
            return q.df["r"][0]
        except Exception as e:
            print("Failed to make prediction")
            return 0.0