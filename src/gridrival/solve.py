"Solve for the optimal Team."

from pandas import Series

from gridrival.drivers import DRIVERS, CSainz, GRUssell, MVerstappen, PGasly, YTsunoda
from gridrival.optimization.basic import BasicSolver
from gridrival.probabilities import GridProbabilities
from gridrival.probabilities.betting_odds import TOP_1, WinningOdds
from gridrival.teams import TEAMS, Ferrari


def main() -> None:

    # Use Winning Odds for Grid Probabilities
    Top1Odds = WinningOdds(Series(TOP_1))
    Prob = GridProbabilities(Top1Odds.naive_grid())

    # Update Driver Probabilities
    for driver in DRIVERS:
        driver.probabilities = Prob.driver_probabilities(driver.name)

    # Fix Driver and Team points
    fixed_drivers = [driver.to_fixed_info() for driver in DRIVERS]
    fixed_teams = [team.to_fixed_info() for team in TEAMS]

    # Use Basic Solver
    solver = BasicSolver(
        fixed_drivers,
        fixed_teams,
        [PGasly, Ferrari],
        [CSainz, YTsunoda, GRUssell, MVerstappen],
        103.4 * 1e6,
    )

    # print solution
    print(solver.solve())
