from typing import Literal
from dataclasses import dataclass

import os
import json

# Which player won given simulation
PLAYER_A = 1
PLAYER_B = 0

@dataclass
class Result:
    """Results of single simulation
    """
    units_a: dict[int, int]
    units_b: dict[int, int]
    win: Literal[0, 1]

    def get_a(self, unit_id: int) -> int:
        return self.units_a[unit_id] if unit_id in self.units_a else 0

    def get_b(self, unit_id: int) -> int:
        return self.units_a[unit_id] if unit_id in self.units_a else 0

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
    return [f"./data-set/{file}" for file in os.listdir("./data-set")]

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
    win = None

    for unit in player_a:
        units_a[unit["UID"]] = unit["QTY"]

    for unit in player_b:
        units_b[unit["UID"]] = unit["QTY"]

    res = content["items"][0]["result"]
    if res == "p1_win":
        win = PLAYER_A
    if res == "p2_win":
        win = PLAYER_B

    if win is None:
        raise Exception("Bad match resulted in tie")

    return Result(units_a, units_b, win)

if __name__ == "__main__":
    # Test
    print(parse())