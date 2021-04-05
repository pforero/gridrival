"Betting Odds."

from typing import Dict, Union

import pandas as pd


class WinningOdds:
    """Obtain probabilities from betting odds for the winner.

    Create a matrix of probabilities for the probability each Driver ends in each
    position from only the betting odds for winning.

    Attributes
    ----------
    odds: Series
        Betting odds for each driver to win. Includes house fee. Index is Driver's name.

    Methods
    -------
    probabilities
        Transform odds into winning probabilities.
    naive_grid
        Return a grid of probabilities using a naive method.
    rank_grid
        Return a grid of probabilities using a deterministic rank method.
    """

    def __init__(self, odds: pd.Series):

        self.odds = odds

    def probabilities(self) -> pd.Series:
        """Transform odds into winning probabilities.

        Returns
        -------
        norm_prob: Series
            Probabilities of winning from betting odds and normalized from house margin.
        """

        bet_prob = 1 / self.odds
        norm_prob = bet_prob / sum(bet_prob)

        return norm_prob

    def naive_grid(self) -> pd.DataFrame:
        """Return a grid of probabilities using a naive method.

        This method calculates the probability for each grid position in a naive way, by
        using the probability of winning from the odds, and the probability of not
        having placed in a higher position.

        Returns
        -------
        df: DataFrame
            Probabilities grid using a naive method.
        """

        df = pd.DataFrame(
            0, index=self.odds.index, columns=range(1, len(self.odds) + 1)
        )
        df[1] = self.probabilities()

        for i in range(1, len(self.odds) - 1):
            past_prob = df.sum(axis=1)
            new_prob = past_prob * (1 - past_prob)
            norm_prob = new_prob / sum(new_prob)
            df[i + 1] = norm_prob

        df[len(self.odds)] = 1 - df.sum(axis=1)

        return df

    def rank_grid(self) -> pd.DataFrame:
        """Return a grid of probabilities using a rank method.

        The rank method ranks all Drivers by odds and, and assumes in a deterministic
        way that the Driver will end in the position given by its rank. If more than one
        Driver have the same odds, the probabilities of the Drivers are split among the
        ranks.

        Returns
        -------
        df: DataFrame
            Probabilities grid using a rank method.
        """

        df = pd.DataFrame(0, index=self.odds.index, columns=range(1, 21))
        ranked_odds = self.odds.rank(method="min")
        grouped_ranks = ranked_odds.groupby(ranked_odds)

        for rank, driver in grouped_ranks:
            num_drivers = len(driver)
            df.loc[driver.index, rank : rank + num_drivers - 1] = 1 / num_drivers

        return df


TOP_1 = {
    "L. Hamilton": 2.25,
    "M. Verstappen": 2.25,
    "V. Bottas": 7.5,
    "S. Perez": 11,
    "D. Ricciardo": 41,
    "L. Norris": 41,
    "P. Gasly": 67,
    "S. Vettel": 151,
    "L. Stroll": 151,
    "C. Leclerc": 101,
    "F. Alonso": 151,
    "C. Sainz Jr": 67,
    "E. Ocon": 201,
    "Y. Tsunoda": 101,
    "G. Russell": 1001,
    "K. Raikkonen": 1001,
    "A. Giovinazzi": 1001,
    "N. Latifi": 2001,
    "M. Schumacher": 4001,
    "N. Mazepin": 3001,
}

QUAL_1 = {
    "L. Hamilton": 2.50,
    "M. Verstappen": 2.37,
    "V. Bottas": 6,
    "S. Perez": 9,
    "D. Ricciardo": 26,
    "L. Norris": 34,
    "P. Gasly": 51,
    "S. Vettel": 101,
    "L. Stroll": 101,
    "C. Leclerc": 101,
    "F. Alonso": 151,
    "C. Sainz Jr": 151,
    "E. Ocon": 151,
    "Y. Tsunoda": 126,
    "G. Russell": 1001,
    "K. Raikkonen": 1001,
    "A. Giovinazzi": 1001,
    "N. Latifi": 3001,
    "M. Schumacher": 3001,
    "N. Mazepin": 3001,
}

TOP_3 = {
    "L. Hamilton": 1.33,
    "M. Verstappen": 1.33,
    "V. Bottas": 1.72,
    "S. Perez": 2.1,
    "D. Ricciardo": 5,
    "L. Norris": 7,
    "P. Gasly": 9,
    "S. Vettel": 15,
    "L. Stroll": 15,
    "C. Leclerc": 15,
    "F. Alonso": 26,
    "C. Sainz Jr": 26,
    "E. Ocon": 26,
    "Y. Tsunoda": 21,
    "G. Russell": 101,
    "K. Raikkonen": 101,
    "A. Giovinazzi": 101,
    "N. Latifi": 1001,
    "M. Schumacher": 1001,
    "N. Mazepin": 1001,
}

TOP_6 = {
    "L. Hamilton": 1.2,
    "M. Verstappen": 1.2,
    "V. Bottas": 1.33,
    "S. Perez": 1.36,
    "D. Ricciardo": 1.66,
    "L. Norris": 1.83,
    "P. Gasly": 2.2,
    "S. Vettel": 2.5,
    "L. Stroll": 2.5,
    "C. Leclerc": 2.5,
    "F. Alonso": 6,
    "C. Sainz Jr": 6,
    "E. Ocon": 6,
    "Y. Tsunoda": 4,
    "G. Russell": 11,
    "K. Raikkonen": 11,
    "A. Giovinazzi": 11,
    "N. Latifi": 101,
    "M. Schumacher": 101,
    "N. Mazepin": 101,
}

TOP_10 = {
    "L. Hamilton": 1.12,
    "M. Verstappen": 1.12,
    "V. Bottas": 1.16,
    "S. Perez": 1.16,
    "D. Ricciardo": 1.25,
    "L. Norris": 1.33,
    "P. Gasly": 1.36,
    "S. Vettel": 1.53,
    "L. Stroll": 1.53,
    "C. Leclerc": 1.53,
    "F. Alonso": 1.72,
    "C. Sainz Jr": 1.8,
    "E. Ocon": 1.8,
    "Y. Tsunoda": 1.61,
    "G. Russell": 4,
    "K. Raikkonen": 4,
    "A. Giovinazzi": 4,
    "N. Latifi": 8.5,
    "M. Schumacher": 21,
    "N. Mazepin": 21,
}
