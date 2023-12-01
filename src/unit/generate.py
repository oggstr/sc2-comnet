import os
import json

IN_FILE = "type_id.json"
OUT_FILE = "ids.py"

FILTER_CONTAINS    = ["Destructible", "SlotBag", "Mineral", "TechLab", "Reactor", "Factory", "Supply", "Command", "Odin"]
FILTER_STARTS_WITH = ["LoadOutSpray", "DummyUnit", "Collapsible", "Loadout", "Defense", "Fireworks", "SM", "SS_", "Beacon", "Commentator", "Metal", "Security"]
FILTER_ENDS_WITH   = ["Dummy"]
FILTER_EXACT       = ["NotAUnit", "Ball"]

def generate() -> None:
    """Generate python definition for all type ids
    """
    units = parse()

    # Purge old file
    purge()

    units = exclude(units)
    __generate(units)

def parse() -> list[dict]:
    """Parse input json file

    Returns:
        list[dict]: list units
    """

    with open(f"{os.getcwd()}/{IN_FILE}", "r") as file:
        content = json.load(file)
        return [u for u in content["Units"]]

def exclude(units: list[dict]) -> list[dict]:
    """Exclude certain units based on their names

    Args:
        units (list[dict]): list units

    Returns:
        list[dict]: filtered list units
    """

    for string in FILTER_CONTAINS:
        units = list(filter(lambda u : string not in u["name"], units))

    for string in FILTER_STARTS_WITH:
        units = list(filter(lambda u : not u["name"].startswith(string), units))

    for string in FILTER_ENDS_WITH:
        units = list(filter(lambda u : not u["name"].endswith(string), units))

    for string in FILTER_EXACT:
        units = list(filter(lambda u : u["name"] != string, units))

    return units

def __generate(units: list[dict]) -> None:
    """Generate the output file

    Args:
        units (list[dict]): list units
    """

    with open(f"{os.getcwd()}/{OUT_FILE}", "w+") as file:
        lines = [f"{u['name']} = {u['id']}\n" for u in units]
        file.writelines(lines)


def purge() -> None:
    """Purge old file
    """

    if OUT_FILE in os.listdir(os.getcwd()):
        os.remove(f"{os.getcwd()}/{OUT_FILE}")

if __name__ == "__main__":
    generate()