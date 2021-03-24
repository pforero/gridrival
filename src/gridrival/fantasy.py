"Roaster for a Fantasy Team."

from typing import Tuple

import pandas as pd

from gridrival.drivers import Driver
from gridrival.probabilities import DriverProbabilities
from gridrival.teams import Team

EmptyDriver = Driver(
    "EMPTY_DRIVER", 0, DriverProbabilities(pd.Series(0, index=range(1, 21)))
)
TALENT_DRIVER_COST = 18 * 1e6


class FantasyTeam:
    """A Fantasy is a line-up allowed by the fantasy league.

    A line-up is composed of five Drivers and one Team. Also one of the five Drivers can
    be designated as Talent Driver.

    A Talent Driver is a Driver whose cost is below 18M and whose points are awarded
    double. For simplicity, we assume that the Talent Driver is always the Driver whose
    cost is higher below 18M.

    Attributes
    ----------
    drivers: list of Driver
        The roaster of selected Drivers.
    team: Team
        The selected team.
    talent_driver: Driver
        Driver whose cost is below 18M and whose points are awarded double.

    Methods
    -------
    cost
        Calculate total cost of Fantasy Team.
    points
        Expected points earned by the Fantasy Team in the race.
    """

    def __init__(
        self, drivers: Tuple[Driver, Driver, Driver, Driver, Driver], team: Team
    ):

        self.drivers = drivers
        self.team = team
        self.talent_driver = self._find_talent_driver()

    def cost(self) -> float:
        """Calculate total cost of Fantasy Team.

        Creates the total cost of all the drivers and the team.

        Returns
        -------
        return: float
            Total cost of fantasy team.
        """

        return sum(driver.cost for driver in self.drivers) + self.team.cost

    def points(self) -> float:
        """Expected points earned by the Fantasy Team in the race.

        Creates the total expected points of all the drivers and the team for the race.

        Returns
        -------
        points: float
            Total expected points for the fantasy team.
        """

        return (
            sum(driver.points() for driver in self.drivers)
            + self.team.points()
            + self.talent_driver.points()
        )

    def _find_talent_driver(self) -> Driver:
        "Find the highest cost Driver with cost below 18M."

        drivers_cost = [
            driver.cost for driver in self.drivers if driver.cost <= TALENT_DRIVER_COST
        ]

        try:
            max_cost = max(drivers_cost)
        except ValueError:
            return EmptyDriver
        else:
            talent_driver = [
                driver for driver in self.drivers if driver.cost == max_cost
            ]
            return talent_driver[0]

    def __repr__(self) -> str:
        return str([self.drivers, self.team, self.talent_driver])
