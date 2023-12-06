import unit.ids as ids

""" Unit id system

Make it easy to convert between unit ids and unit names.
Requires that a unit is registered.

Doubles as a bit of a sanity check.
"""

# Count of registered units
# __count = 0

# Tracks id -> name
ID_2_NAME = {}

def register(name: str) -> int:
    """Register some unit to be used

    Args:
        name (str): Name of unit

        Returns:
            int: id
    """
    try:
        unit_id = getattr(ids, name)
        ID_2_NAME[unit_id] = name
        return unit_id
    except AttributeError as e:
        raise Exception(f"Unit {name} does not exist, double check your spelling")

def name_of(unit_id: int | str) -> str:
    """Get unit name of some id

    Args:
        index (int): id

    Returns:
        str: unit name
    """
    if type(unit_id) == str and not unit_id.isdecimal():
        raise Exception(f"Unable to find name of id {unit_id}")

    unit_id = int(unit_id)

    if unit_id in ID_2_NAME:
        return ID_2_NAME[unit_id]

    for name in dir(ids):
        if getattr(ids, name) == unit_id:
            ID_2_NAME[unit_id] = name
            return name

    raise Exception(f"Unable to get name of id {unit_id}")

def id_of(unit_name: str) -> int:
    for attr in dir(ids):
        if attr == unit_name:
            return getattr(ids, attr)

    raise Exception(f"Unable to find name of unit {unit_name}")    