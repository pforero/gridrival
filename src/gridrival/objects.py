"Objects"

from pandas import Series

from gridrival.helpers import DefaultProbability
from gridrival.scoring import LeagueScoring

class Driver:

    def __init__(self, name: str, cost: int, probabilities: Series = DefaultProbability):

        self.name = name
        self.cost = cost
        self.probabilities = probabilities
    
    def expected_qualifying_points(self, team=False):

        if team:
            scoring = LeagueScoring.Team.QUALIFYING
        else:
            scoring = LeagueScoring.Driver.QUALIFYING

        return sum(self.probabilities * scoring)

    def expected_race_points(self, team=False):

        if team:
            scoring = LeagueScoring.Team.RACE
        else:
            scoring = LeagueScoring.Driver.RACE

        return sum(self.probabilities * scoring)

    def expected_points(self, team=False):

        return self.expected_qualifying_points(team) + self.expected_race_points(team)

    def cost_per_expected_point(self, team=False):

        return self.cost / self.expected_points(team)


class Team:

    def __init__(self, name:str, driver_1: Driver, driver_2: Driver, cost: int):

        self.name = name
        self.driver_1 = driver_1
        self.driver_2 = driver_2
        self.cost = cost

        driver_1.team = self
        driver_2.team = self
    
    def expected_qualifying_points(self):

        return (
            self.driver_1.expected_qualifying_points(team=True)
            + self.driver_2.expected_qualifying_points(team=True)
        )

    def expected_race_points(self):

        return (
            self.driver_1.expected_race_points(team=True)
            + self.driver_2.expected_race_points(team=True)
        )

    def expected_points(self):

        return self.expected_qualifying_points() + self.expected_race_points()

    def cost_per_expected_point(self):

        return self.cost / self.expected_points()