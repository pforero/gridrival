"Point system awarded by the fantasy league."

import pandas as pd


class LeagueScoring:
    class Driver:

        QUALIFYING = pd.Series({i: 52 - (i * 2) for i in range(1, 21)})
        RACE = pd.Series({i: 103 - (i * 3) for i in range(1, 21)})
        COMPLETION = pd.Series(3, index=range(1,4))

    class Team:

        QUALIFYING = pd.Series({i: 31 - i for i in range(1, 21)})
        RACE = pd.Series({i: 62 - (i * 2) for i in range(1, 21)})
