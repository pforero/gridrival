"Roaster for a Fantasy Team."

from typing import Tuple

import pandas as pd

from gridrival.drivers import FixedInfo
from gridrival.probabilities import DriverProbabilities

EmptyDriver = FixedInfo("EMPTY_DRIVER", 0, 0)
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
    drivers: list of FixedInfo
        The roaster of selected Drivers.
    team: FixedInfo
        The selected team.
    talent_driver: FixedInfo
        Driver whose cost is below 18M and whose points are awarded double.

    Methods
    -------
    cost
        Calculate total cost of Fantasy Team.
    points
        Expected points earned by the Fantasy Team in the race.
    """

    def __init__(
        self,
        drivers: Tuple[FixedInfo, FixedInfo, FixedInfo, FixedInfo, FixedInfo],
        team: FixedInfo,
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
            sum(driver.points for driver in self.drivers)
            + self.team.points
            + self.talent_driver.points
        )

    def _find_talent_driver(self) -> FixedInfo:
        "Find the highest point Driver with cost below 18M."

        drivers_points = [
            driver.points
            for driver in self.drivers
            if driver.cost <= TALENT_DRIVER_COST
        ]

        try:
            max_points = max(drivers_points)
        except ValueError:
            return EmptyDriver
        else:
            talent_driver = [
                driver for driver in self.drivers if driver.points == max_points
            ]
            return talent_driver[0]

    def __contains__(self, fixed: FixedInfo) -> bool:
        "A Fantasy Teams contains a Team or Driver in the Fantasy Team."
        return (fixed in self.drivers) or (self.team == fixed)

    def __repr__(self) -> str:
        return str([self.drivers, self.team, self.talent_driver])
