"Betting Odds."
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
        Transform odds into normalized probabilities.
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


class RaceOdds:
    """Obtain probabilities from betting odds for the winner from race position odds.

    Create a matrix of probabilities for the probability each Driver ends in each
    position from the betting odds from winning, podium, top 6 and points.

    Attributes
    ----------
    win: Series
        Odds for each driver to win.
    pod: Series
        Odds for each driver to finish in the top 3.
    tp6: Series
        Odds for each driver to finish top 6.
    pnt: Series
        Odds for each driver to finish in the top 10.

    Methods
    -------
    probabilities
        Transform odds into normalized probabilities.
    """

    def __init__(self, odds: pd.Series):

        self.odds = odds

    def probabilities(self, total_probability=1) -> pd.Series:
        """Transform odds into winning probabilities.

        Parameters
        ----------
        total_probabilit: int
            Probability value of summing all probabilities together.

        Returns
        -------
        norm_prob: Series
            Probabilities of winning from betting odds and normalized from house margin.
        """

        bet_prob = 1 / self.odds
        norm_prob = bet_prob / sum(bet_prob) * total_probability

        return norm_prob


class RetirementOdds:
    """Obtain probabilities from betting odds for the probability of retiring.

    Create a matrix of probabilities for the probability each Driver completes a
    percentage of the race.

    Attributes
    ----------
    odds: Series
        Betting odds for each driver to retire first or not retire.
    no_ret: float
        Probability of no driver retiring.
    first_ret: Series
        Probability of each driver retiring first.
    
    Methods
    -------
    probabilities
        Transform odds into normalized probabilities.
    retirement_probabilities
        Transform first driver to retire odds in overall retirement probabilities.
    """

    def __init__(self, odds: pd.Series):

        self.odds = odds

        prob = self.probabilities()
        self.no_ret = prob["NO_RETIREMENT"]
        self.first_ret = prob.loc[prob.index!="NO_RETIREMENT"]

    def probabilities(self) -> pd.Series:
        """Transform odds into probabilities.

        Returns
        -------
        norm_prob: Series
            Probabilities of winning from betting odds and normalized from house margin.
        """

        bet_prob = 1 / self.odds
        norm_prob = bet_prob / sum(bet_prob)

        return norm_prob

    def retirement_probabilities(self) -> pd.Series:
        """Calculate the probability of each driver of not completing the race.

        Returns
        -------
        ret_prob: Series
            Probabilities for each driver of retiring during the race.
        """

        avg_ret = 1-self.no_ret**(1/20)
        multiplier = (avg_ret*20)/self.first_ret.sum()

        ret_prob = self.first_ret.multiply(multiplier)

        return ret_prob

    def completion_probabilities(self) -> pd.DataFrame:
        """Calculate the probabilities each driver completes a percentage of the race.

        Returns
        -------
        comp_prob: DataFrame
            Probabilities for each driver to complete a percentage of the race.
        """

        ret = self.retirement_probabilities()

        comp_prob = pd.concat(
            [
                ret * SUB_PROBABILITES[1],
                ret * SUB_PROBABILITES[2],
                ret * SUB_PROBABILITES[3],
                ret * SUB_PROBABILITES[4],
                (1-ret)
            ],
            axis = 1
        )

        return comp_prob


TOP_1 = {
    "L. Hamilton": 1.81,
    "M. Verstappen": 2,
    "V. Bottas": 12,
    "S. Perez": 35,
    "D. Ricciardo": 139,
    "L. Norris": 85,
    "P. Gasly": 70,
    "S. Vettel": 293,
    "L. Stroll": 489,
    "C. Leclerc": 79,
    "F. Alonso": 264,
    "C. Sainz Jr": 109,
    "E. Ocon": 293,
    "Y. Tsunoda": 219,
    "G. Russell": 979,
    "K. Raikkonen": 1001,
    "A. Giovinazzi": 1001,
    "N. Latifi": 2001,
    "M. Schumacher": 4001,
    "N. Mazepin": 6001,
}

QUAL_1 = {
    "L. Hamilton": 1.57,
    "M. Verstappen": 4.33,
    "V. Bottas": 4.33,
    "S. Perez": 21,
    "D. Ricciardo": 101,
    "L. Norris": 41,
    "P. Gasly": 151,
    "S. Vettel": 1001,
    "L. Stroll": 251,
    "C. Leclerc": 41,
    "F. Alonso": 251,
    "C. Sainz Jr": 67,
    "E. Ocon": 251,
    "Y. Tsunoda": 501,
    "G. Russell": 1001,
    "K. Raikkonen": 1001,
    "A. Giovinazzi": 1001,
    "N. Latifi": 1001,
    "M. Schumacher": 2001,
    "N. Mazepin": 3001,
}

TOP_3 = {
    "L. Hamilton": 1.25,
    "M. Verstappen": 1.33,
    "V. Bottas": 1.9,
    "S. Perez": 2.5,
    "D. Ricciardo": 11,
    "L. Norris": 7,
    "P. Gasly": 13,
    "S. Vettel": 41,
    "L. Stroll": 17,
    "C. Leclerc": 4,
    "F. Alonso": 17,
    "C. Sainz Jr": 7.5,
    "E. Ocon": 34,
    "Y. Tsunoda": 67,
    "G. Russell": 151,
    "K. Raikkonen": 251,
    "A. Giovinazzi": 151,
    "N. Latifi": 251,
    "M. Schumacher": 251,
    "N. Mazepin": 251,
}

TOP_6 = {
    "L. Hamilton": 1.18,
    "M. Verstappen": 1.26,
    "V. Bottas": 1.3,
    "S. Perez": 1.3,
    "D. Ricciardo": 2.2,
    "L. Norris": 1.33,
    "P. Gasly": 2.2,
    "S. Vettel": 9.5,
    "L. Stroll": 5.1,
    "C. Leclerc": 1.33,
    "F. Alonso": 5.1,
    "C. Sainz Jr": 1.57,
    "E. Ocon": 9.5,
    "Y. Tsunoda": 29,
    "G. Russell": 51,
    "K. Raikkonen": 51,
    "A. Giovinazzi": 51,
    "N. Latifi": 71,
    "M. Schumacher": 101,
    "N. Mazepin": 101,
}

TOP_10 = {
    "L. Hamilton": 1.14,
    "M. Verstappen": 1.14,
    "V. Bottas": 1.23,
    "S. Perez": 1.23,
    "D. Ricciardo": 1.44,
    "L. Norris": 1.23,
    "P. Gasly": 1.44,
    "S. Vettel": 2.2,
    "L. Stroll": 1.57,
    "C. Leclerc": 1.23,
    "F. Alonso": 1.57,
    "C. Sainz Jr": 1.23,
    "E. Ocon": 1.66,
    "Y. Tsunoda": 2.2,
    "G. Russell": 4,
    "K. Raikkonen": 6,
    "A. Giovinazzi": 4,
    "N. Latifi": 9.5,
    "M. Schumacher": 17,
    "N. Mazepin": 23,
}

RET_1 = {
    "L. Hamilton": 23,
    "M. Verstappen": 15,
    "V. Bottas": 17,
    "S. Perez": 23,
    "D. Ricciardo": 21,
    "L. Norris": 26,
    "P. Gasly": 19,
    "S. Vettel": 21,
    "L. Stroll": 15,
    "C. Leclerc": 21,
    "F. Alonso": 23,
    "C. Sainz Jr": 21,
    "E. Ocon": 15,
    "Y. Tsunoda": 15,
    "G. Russell": 17,
    "K. Raikkonen": 21,
    "A. Giovinazzi": 21,
    "N. Latifi": 17,
    "M. Schumacher": 17,
    "N. Mazepin": 12,
    "NO_RETIREMENT": 10,
}

SUB_PROBABILITES = {
    1: 0.5,
    2: 0.25,
    3: 0.125,
    4: 0.125
}
