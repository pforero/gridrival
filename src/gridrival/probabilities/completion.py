"Probabilities for completing quartiles of the race."

from pandas import Series

class CompletionProbabilities:
    """Probability of completing quartiles of the race.

    In each race a driver can finish 1/4, 1/2, 3/4 or the full race.

    The probabilities are those that the driver completes that much of the race,
    therefore probabilities must be less or equal than the previous quartile.

    Attributes
    ----------
    probabilities: Series
        Probabilities of winning a quartile of the race.
    """

    def __init__(self, prob: Series) -> None:
        self.probabilities = prob


COMPLETE_RACE = CompletionProbabilities(Series(1, index=range(1,5)))
