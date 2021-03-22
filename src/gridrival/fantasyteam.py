"My Team optimization."

from itertools import combinations, product
from typing import List, Tuple

from gridrival.helpers import EmptyDriver, TALENT_DRIVER_COST
from gridrival.objects import Driver, Team

class FantasyTeam:

    def __init__(
        self,
        drivers: Tuple[Driver, Driver, Driver, Driver, Driver],
        team: Team
    ):

        self.drivers = drivers
        self.team = team
        self.talent_driver = self._find_talent_driver()

    def cost(self):

        return sum(driver.cost for driver in self.drivers) + self.team.cost

    def expected_qualifying_points(self):

        return (
            sum(driver.expected_qualifying_points() for driver in self.drivers)
            + self.team.expected_qualifying_points()
            + self.talent_driver.expected_qualifying_points()
        )

    def expected_race_points(self):

        return (
            sum(driver.expected_race_points() for driver in self.drivers)
            + self.team.expected_race_points()
            + self.talent_driver.expected_race_points()
        )

    def expected_points(self):

        return self.expected_qualifying_points() + self.expected_race_points()
    
    def _find_talent_driver(self):

        driver_costs = [driver.cost for driver in self.drivers]

        if len(driver_costs) == 0:
            return EmptyDriver
        else:
            
            max_talented = max(
                [
                    driver.expected_points()
                    for driver in driver_costs
                    if driver.cost <= TALENT_DRIVER_COST
                ]
            )

            talented_driver = [
                driver
                for driver in self.drivers
                if driver.expected_points() == max_talented
            ]

            return talented_driver[0]

def universe_teams(drivers: List[Driver], teams: List[Team]):
    return [
        FantasyTeam(drivers=comb_teams[0], team=comb_teams[1])
        for comb_teams in product(combinations(drivers, 5), teams)
    ]