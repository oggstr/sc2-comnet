from typing import Literal

import os
import json

from dataclasses import dataclass


#Which player won given simulation
PLAYER_A = 1.0
PLAYER_B = 0.0
TIE = 0.5


@dataclass
class Result:
    """Results of single simulation
    """
    units_a: dict[int, int]
    units_b: dict[int, int]
    win: Literal[1, 2, 3]

    def get_a(self, id: int) -> int:
        return self.units_a[id] if id in self.units_a else 0

    def get_b(self, id: int) -> int:
        return self.units_a[id] if id in self.units_a else 0

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
    return [f"./data/{file}" for file in os.listdir("./data")]

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
    win = TIE

    for unit in player_a:
        units_a[unit["UID"]] = unit["QTY"]

    for unit in player_b:
        units_b[unit["UID"]] = unit["QTY"]

    res = content["items"][0]["result"]
    if res == "p1_win":
        win = PLAYER_A
    if res == "p2_win":
        win = PLAYER_B

    return Result(units_a, units_b, win)

if __name__ == "__main__":
    # Test
    print(parse())