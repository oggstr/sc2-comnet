import unit.ids as ids
"""
To pack data into arrays, we need to convert
unit IDs to indices. This module handles that.

First register a set of units by name. Then fetch
their respective indices via helper methods.
"""

# Count of registered units
__count__ = 0

# Tracks id -> index
__ID_2_IDX__ = {}

# Tacks index -> id
__IDX_2_ID__ = {}

# Tracks index -> unit name
__NAME__    = {}

def register(name: str) -> int:
    """Register some unit to be used

    Args:
        name (str): Name of unit

        Returns:
            int: index
    """
    global __count__

    try:
        id = getattr(ids, name)
    except AttributeError as e:
        print(e)
        exit(1)

    i = __count__

    __ID_2_IDX__[id] = i
    __IDX_2_ID__[i]  = id

    __NAME__[i] = name

    __count__ = i + 1
    return i

def index(id: int) -> int:
    """Convert unit id to index

    Args:
        id (int): unit it

    Returns:
        int: index
    """

    try:
        return __ID_2_IDX__[id]
    except KeyError:
        print(f"Unit id {id} not registered in type_id module")
        exit(1)

def id(index: int) -> int:
    """Convert index to unit id

    Args:
        index (int): index

    Returns:
        int: unit id
    """

    try:
        return __IDX_2_ID__[index]
    except KeyError:
        print(f"Index {index} doesn't exist, make sure all units are registered")
        exit(1)

def count() -> int:
    """Get count of registered units

    Returns:
        int: count
    """

    return __count__

def name(index: int) -> str:
    """Get unit name of some index

    Args:
        index (int): index

    Returns:
        str: unit name
    """
    try:
        return __NAME__[index]
    except KeyError:
        print(f"Index {index} doesn't exist, make sure all units are registered")
        exit(1)