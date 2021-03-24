"Outcome probabilities for a race."

from typing import Optional

from pandas import DataFrame, Series


class DriverProbabilities:
    """Probabilities for a Driver's outcomes in a race.

    Probabilities are a series of probabilities each position on the grid the Driver can
    end up.

    The probabilities are independent for both qualifying and the race.

    Attributes
    ----------
    race: Series
        Probabilities to end the race stage in each grid position.
    qual: DataFrame
        Probabilities to end the qualifying stage in each grid position.
    """

    def __init__(self, race: Series, qual: Optional[Series] = None) -> None:

        self.race = race
        if qual is None:
            self.qual = race
        else:
            self.qual = qual


class GridProbabilities:
    """Probabilities for different outcomes in a race.

    Probabilities are the matrix of probabilities each Driver ends in each grid
    position.

    The probabilities are independent for both qualifying and the race.

    Attributes
    ----------
    race: DataFrame
        Probabilities for each Driver to end the race stage in each grid position.
    qual: DataFrame
        Probabilities for each Driver to end the qualifying stage in each grid position.

    Methods
    -------
    driver_probabilities: Series
        Return the probabilities for a single Driver.
    """

    def __init__(self, race: DataFrame, qual: Optional[DataFrame] = None) -> None:

        self.race = race
        if qual is None:
            self.qual = race
        else:
            self.qual = qual

    def driver_probabilities(self, driver: str) -> DriverProbabilities:
        """Return the probabilities for a single Driver.

        Returns
        -------
        return: DriverProbabilities
            Probabilities for each possible result position for a single Driver.
        """

        return DriverProbabilities(
            race=self.race.loc[driver], qual=self.qual.loc[driver]
        )
