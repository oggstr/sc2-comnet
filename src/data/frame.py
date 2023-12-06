from pandas import DataFrame

from unit import ids as id
from parse import Result, PLAYER_A, PLAYER_B

def spawn_data_frame() -> DataFrame:
    #match_result = parse()
    match_result = [
        Result({id.Marine: 10}, {id.Marine: 9}, PLAYER_A),
        Result({id.Marine: 20}, {id.Marine: 10}, PLAYER_A),
        Result({id.Marine: 5}, {id.Marine: 15}, PLAYER_B),
        Result({id.Marine: 1}, {id.Marine: 17}, PLAYER_B),
        Result({id.Marine: 17}, {id.Marine: 5}, PLAYER_A),
    ]

    # 12 count of dists in model
    data: dict[str, list[str]] = {
        "count_a": [],
        "count_b": [],
        "dmg_a": [],
        "hp_a": [],
        "dmg_b": [],
        "hp_b": [],
        "agg_off_a": [],
        "agg_def_a": [],
        "agg_off_b": [],
        "agg_def_b": [],
        "agg": [],
        "res": []
    }

    for match in match_result:
        count_a = match.units_a[id.Marine]
        count_b = match.units_b[id.Marine]

        data["count_a"].append(count_a)
        data["count_b"].append(count_b)
        data["dmg_a"].append(9.8)
        data["hp_a"].append(45)
        data["dmg_b"].append(9.8)
        data["hp_b"].append(45)
        data["agg_off_a"].append(count_a * 9.8)
        data["agg_def_a"].append(count_a * 45)
        data["agg_off_b"].append(count_b * 9.8)
        data["agg_def_b"].append(count_b * 45)
        data["agg"].append((count_a * 9.8 / count_b * 45) - (count_b * 9.8 / count_a * 45))
        data["res"].append(match.win)

    return DataFrame(data)