import unit.ids as id
import unit.type_id as tid

""" Attribute system

Glorified wrapper over a dict.
"""


def get(unit: int | str, attr: str) -> float:
    """Get unit attribute

    Args:
        unit (int): Unit id
        attr (str): Attribute name

    Returns:
        int: value
    """
    try:
        if unit.isdecimal():
            unit = int(unit)
            return ATTR[unit][attr]

        return ATTR[unit][attr]

    except KeyError:
        raise Exception(f"Unable to find attribute {attr} for unit {unit}")

def exists(attr: str) -> bool:
    return attr in ATTR_NAMES


# Registered unit attributes using unit ids
ATTR: dict[int | str, dict[str, float]] = {}

ATTR_NAMES: set[str] = set()

def __add_unit(unit: id) -> None:
    """Add unit"""
    ATTR[unit] = {}
    ATTR[tid.name_of(unit)] = {}

def __add_attr(unit: id, attr: str, val: float | int) -> None:
    """Add attribute for unit"""
    val = float(val)
    ATTR[unit][attr] = val
    ATTR[tid.name_of(unit)][attr] = val
    ATTR_NAMES.add(attr)


__add_unit(id.Marine)
__add_attr(id.Marine, "dmg", 9.8)
__add_attr(id.Marine, "hp", 45)

__add_unit(id.Reaper)
__add_attr(id.Reaper, "dmg", 10.1)
__add_attr(id.Reaper, "hp", 60)
