"Optimization for Best F1 Team."
from itertools import combinations, product
from typing import List, Union

from pandas import DataFrame

from gridrival.drivers import Driver, FixedInfo
from gridrival.fantasy import FantasyTeam
from gridrival.teams import Team


class BasicSolver:
    """Basic Solver just obtains the Fantasy Team with the most expected points which
    meet the constraints.

    Attributes
    ----------
    drivers: list of FixedInfo
        List of drivers available for the Fantasy Team.
    teams: list of FixedInfo
        List of teams available for the Fantasy Team.
    in_constraint: list of Driver and Team
        Drivers and Teams which much be included in the Fantasy Team.
    out_constraint: list of Driver and Team
        Drivers and Teams which can not be included in the Fantasy Team.
    budget: int
        Maximum budget for the Fantasy Team.
    """

    def __init__(
        self,
        drivers: List[FixedInfo],
        teams: List[FixedInfo],
        in_constraint: List[Union[Driver, Team]],
        out_constraint: List[Union[Driver, Team]],
        budget: int,
    ) -> None:

        self.drivers = drivers
        self.teams = teams
        self.in_constraint = in_constraint
        self.out_constraint = out_constraint
        self.budget = budget

        self.universe = self._get_constrained_universe()

    def solve(self) -> FantasyTeam:
        "Solve for the best Fantasy Team within constraints."

        ft_points = [ft.points() for ft in self.universe]

        max_points = max(ft_points)

        best_ft = [ft for ft in self.universe if ft.points() == max_points]

        return best_ft[0]

    def to_dataframe(self) -> DataFrame:
        "Create DataFrame with all teams that meet the constraints."

        data = [
            {
                "driver_1": ft.drivers[0],
                "driver_2": ft.drivers[1],
                "driver_3": ft.drivers[2],
                "driver_4": ft.drivers[3],
                "driver_5": ft.drivers[4],
                "team": ft.team,
                "talent_driver": ft.talent_driver,
                "cost": ft.cost(),
                "points": ft.points(),
            }
            for ft in self.universe
        ]

        return DataFrame(data)

    def _get_constrained_universe(self) -> list:
        "Get the universe of Fantasy Teams which meet the constraints."

        universe = product(combinations(self.drivers, 5), self.teams)
        ft_universe = [FantasyTeam(comb[0], comb[1]) for comb in universe]

        budget_universe = [ft for ft in ft_universe if ft.cost() <= self.budget]

        constraint_universe = []

        for ft in budget_universe:

            if any(in_element not in ft for in_element in self.in_constraint):
                continue

            if any(out_element in ft for out_element in self.out_constraint):
                continue

            constraint_universe.append(ft)

        return constraint_universe
