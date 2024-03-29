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

    def __init__(
        self,
        race: Series,
        comp: Series,
        qual: Optional[Series] = None
    ) -> None:

        self.race = race
        self.comp = comp
        if qual is None:
            self.qual = race
        else:
            self.qual = qual

    def overtake_probabilities(self) -> DataFrame:
        """Create a matrix of overtake probabilities.

        Transform the qualification and race probabilities into a matrix(M,N) with the
        probabilities that the driver qualifies in m position and finishes the race in
        nth position.

        Returns
        -------
        return: DataFrame
            Matrix of probabilities of overtake positions.
        """
        return DataFrame(self.qual).dot(DataFrame(self.race).T)


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

    def __init__(
        self,
        race: DataFrame,
        comp: DataFrame,
        qual: Optional[DataFrame] = None
    ) -> None:

        self.race = race
        if qual is None:
            self.qual = race
        else:
            self.qual = qual
        self.comp = comp

    def driver_probabilities(self, driver: str) -> DriverProbabilities:
        """Return the probabilities for a single Driver.

        Returns
        -------
        return: DriverProbabilities
            Probabilities for each possible result position for a single Driver.
        """

        return DriverProbabilities(
            race=self.race.loc[driver],
            comp= self.comp.loc[driver],
            qual=self.qual.loc[driver]
        )


COMPLETE_RACE = Series(0, index=range(0, 5))
COMPLETE_RACE[4] = 1

DEFAULT_PROBABILITY = DriverProbabilities(
    race=Series(1 / 20, index=range(1, 21)),
    qual=Series(1 / 20, index=range(1, 21)),
    comp=Series(1, index=range(0, 5))
)
