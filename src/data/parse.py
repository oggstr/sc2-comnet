from __future__ import annotations

from typing import Literal
from dataclasses import dataclass

import os
import json
from functools import reduce
from pathlib import Path

import unit.type_id as tid

# Which player won given simulation
PLAYER_A = 1
PLAYER_B = 0

@dataclass
class Result:
    """Results of single simulation
    """
    units_a: dict[int, int]
    units_b: dict[int, int]
    win: int

    def get_a(self, unit_name: str) -> int:
        unit_id = tid.id_of(unit_name)
        return self.units_a[unit_id] if unit_id in self.units_a else 0

    def get_b(self, unit_name: str) -> int:
        unit_id = tid.id_of(unit_name)
        return self.units_b[unit_id] if unit_id in self.units_b else 0

def parse() -> list[Result]:
    """Parse all json files in /data
    into Result objects

    Returns:
        list[Result]: List results
    """
    result_data = []
    for f in file_list():
        with open(f, "r") as file:
            content = json.load(file)
            result_data.append(result(content))

    return result_data

def file_list() -> list[str]:
    """Return list files to parse

    Returns:
        list[str]: List files
    """
    path = Path(__file__).parent.resolve()
    return [f"{path}/../data-set/{file}" for file in os.listdir(f"{path}/../data-set")]

def result(content: dict) -> Result:
    """Create result object from JSON content

    Args:
        content (dict): JSON

    Returns:
        Result: Result object
    """
    player_a = content["combination"]["SP1"]
    player_b = content["combination"]["SP2"]

    units_a = {}
    units_b = {}

    for unit in player_a:
        units_a[unit["UID"]] = unit["QTY"]

    for unit in player_b:
        units_b[unit["UID"]] = unit["QTY"]

    res = list(map(lambda item: 1.0 if item["result"] == "p1_win" else 0.0, content["items"]))
    res = round(reduce(lambda a, b: a + b, res) / len(res))

    return Result(units_a, units_b, res)

if __name__ == "__main__":
    # Test
    print(parse())