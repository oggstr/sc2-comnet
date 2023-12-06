from __future__ import annotations
from typing import Literal

import regex
from pandas import DataFrame

import data.parse as data
import unit.type_id as tid
import unit.attribute as attr

Player  = Literal['a', 'b']
Feature = tuple[str, str]

class Network():

    units: list[int]
    "List unit ids"

    features: list[Feature]
    "list unit features"

    continuous_columns: list[str]
    "List continuous columns"

    def __init__(self: Network) -> None:
        self.units = []
        self.features = []
        self.continuous_columns = []

    def add_unit(self: Network, unit_name: str) -> Network:
        self.units.append(tid.id_of(unit_name))
        return self

    def add_feature(self: Network, offensive: str, defensive: str) -> Network:
        if not attr.exists(offensive):
            raise Exception(f"Offensive attribute {offensive} does not exist")

        if not attr.exists(defensive):
            raise Exception(f"Defensive attribute {defensive} does not exist")

        self.features.append((offensive, defensive))
        return self

    def make_data_frame(self: Network) -> DataFrame:
        unit_plates, agg_plates = self.__make_plates()

        data_frame = Network.__collect_columns(unit_plates, agg_plates)
        matches = data.parse()

        for m in matches:
            for unit_plate in unit_plates:
                for name in unit_plate.get_node_names():

                    unit, feat, player = UnitPlate.decompose_name(name)
                    if feat == "count":
                        val = m.get_a(tid.id_of(unit)) if player == "player_A" else m.get_b(unit)
                    else:
                        val = attr.get(unit, feat)

                    data_frame[name].append(val)

            for agg_plate in agg_plates:
                for name in agg_plate.get_node_names():
                    feat, player = AggregationPlate.decompose_name(name)

                    total = 0
                    for unit in self.units:
                        unit  = tid.name_of(unit)

                        count = f"{unit}-count-{player}"
                        val   = f"{unit}-{feat}-{player}"

                        total += data_frame[val][-1] * data_frame[count][-1]

                    data_frame[name].append(total)

                agg_name = agg_plate.get_aggregation_node_name()
                feat_off, feat_def = AggregationPlate.decompose_name(agg_name)
                a1 = f"agg-{feat_off}-player_A"
                a2 = f"agg-{feat_def}-player_A"
                b1 = f"agg-{feat_off}-player_B"
                b2 = f"agg-{feat_def}-player_B"


                print(data_frame)
                data_frame[agg_name].append((data_frame[a1][-1] / data_frame[b2][-1]) - (data_frame[b1][-1] / data_frame[a2][-1]))

            data_frame["result"].append(m.win)

        return DataFrame(data_frame)

    def __make_plates(self: Network):
        unit_plates = [UnitPlate(tid.name_of(u), self.features) for u in self.units]
        agg_plates  = [AggregationPlate(f) for f in self.features]

        return (unit_plates, agg_plates)

    def __collect_columns(unit_plates: list[UnitPlate], agg_plates: list[AggregationPlate]) -> dict[str, list]:
        cols = {}
        for unit in unit_plates:
            for n in unit.get_node_names():
                cols[n] = []

        for agg in agg_plates:
            for n in agg.get_node_names():
                cols[n] = []

            n = agg.get_aggregation_node_name()
            cols[n] = []

        cols["result"] = []

        return cols

feat_expr = regex.compile(r"(?:[A-z]+-)([A-z]+)(?:-[A-z]+)")
def get_feat(node: str) -> str:
    return feat_expr.findall(node)[0]

class UnitPlate():

    unit: str

    features: list[Feature]

    def __init__(self: UnitPlate, unit: str, features: list[Feature]) -> None:
        self.unit = unit
        self.features = features

    def get_node_names(self: UnitPlate) -> list[str]:
        names = []

        names.append(f"{self.unit}-count-player_A")
        names.append(f"{self.unit}-count-player_B")

        for feat in self.features:
            feat_off, feat_def = feat
            names.append(f"{self.unit}-{feat_off}-player_A")
            names.append(f"{self.unit}-{feat_def}-player_A")
            names.append(f"{self.unit}-{feat_off}-player_B")
            names.append(f"{self.unit}-{feat_def}-player_B")

        return names

    def get_edges(self: UnitPlate) -> list[str]:
        edges = []

        expr = regex.compile(r"[A-z]+-player_[AB]")
        for name in self.get_node_names():
            res = expr.findall(name)
            edge = (name, f"agg-{res[0]}")
            edges.append(edge)

        return edges

    def decompose_name(name: str) -> list[str, str, str]:
        return name.split("-")

class AggregationPlate():

    feature: Feature

    def __init__(self: AggregationPlate, feature: Feature) -> None:
        self.feature = feature

    def get_node_names(self: AggregationPlate) -> list[str]:
        feat_off, feat_def = self.feature
        return [
            f"agg-{feat_off}-player_A",
            f"agg-{feat_def}-player_A",
            f"agg-{feat_off}-player_B",
            f"agg-{feat_def}-player_B"
        ]

    def get_aggregation_node_name(self: UnitPlate) -> str:
        feat_off, feat_def = self.feature
        return f"agg-{feat_off}-{feat_def}"

    def get_edges(self: AggregationPlate) -> str:
        edges = []

        feat_off, feat_def = self.feature
        agg_node = f"agg-{feat_off}-{feat_def}"
        for name in self.get_node_names():
            edges.append((name, agg_node))

        edges.append((agg_node, "result"))

        return edges

    def decompose_name(name: str) -> list[str, str]:
        return name.split("-")[1:]