"Point system awarded by the fantasy league."

import pandas as pd
from pandas.core.series import Series

empty_grid = pd.DataFrame(0, index=range(1, 21), columns=range(1, 21))


def distance_func(x: pd.Series) -> pd.Series:
    return x.index - x.name


overtake_df = empty_grid.apply(distance_func) * 3
overtake_df[overtake_df <= 0] = 0

teammate_df = empty_grid.apply(distance_func)
teammate_df[teammate_df <= 0] = 0
teammate_df[(teammate_df > 0) & (teammate_df <= 3)] = 2
teammate_df[(teammate_df > 3) & (teammate_df <= 7)] = 5
teammate_df[(teammate_df > 7) & (teammate_df <= 12)] = 8
teammate_df[teammate_df > 12] = 12

personal_improvement = Series(0, range(-19, 20))
personal_improvement.loc[1] = 2
personal_improvement.loc[2] = 4
personal_improvement.loc[3] = 6
personal_improvement.loc[4] = 9
personal_improvement.loc[5] = 12
personal_improvement.loc[6] = 16
personal_improvement.loc[7] = 20
personal_improvement.loc[8] = 25
personal_improvement.loc[9:] = 30


class LeagueScoring:
    class Driver:

        QUALIFYING = pd.Series({i: 52 - (i * 2) for i in range(1, 21)})
        RACE = pd.Series({i: 103 - (i * 3) for i in range(1, 21)})
        COMPLETION = pd.Series(3, index=range(1, 5))
        OVERTAKE = overtake_df
        BEAT_TEAMMATE = teammate_df
        PERSONAL_IMPROVEMENT = personal_improvement

    class Team:

        QUALIFYING = pd.Series({i: 31 - i for i in range(1, 21)})
        RACE = pd.Series({i: 62 - (i * 2) for i in range(1, 21)})
