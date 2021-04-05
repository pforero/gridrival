"F1 Drivers."
import copy

from pandas import DataFrame, Series

from gridrival.probabilities import DriverProbabilities
from gridrival.probabilities.completion import COMPLETE_RACE, CompletionProbabilities
from gridrival.scoring import LeagueScoring

DEFAULT_PROBABILITY = DriverProbabilities(Series(1 / 20, index=range(1, 21)))


class FixedInfo:
    """Fixed info.

    Save Name, Cost and Points as a dictionary for more efficient optimization.

    Attributes
    ----------
    name: str
        Name of Driver or Team.
    cost: float
        Cost of Driver or Team.
    points: float
        Expected points of Driver or Team.
    """

    def __init__(self, name: str, cost: float, points: float) -> None:

        self.name = name
        self.cost = cost
        self.points = points

    def __repr__(self) -> str:
        return self.name


class Driver:
    """A F1 Driver.

    A Driver is a racer that has a cost, a team and a probability of finishing in the
    race.

    A Driver's performance in a race (qualification + race) determines the points it is
    awarded in the fantasy league.

    Note
    ----
    In order to avoid Chicken and the Egg problem, the driver's team is assigned when
    creating the Team.

    Attributes
    ----------
    name: str
        Name of the Driver.
    cost: int
        Cost of the Driver in the fantansy league.
    team: Team
        Team in which the Driver belongs.
    rank: int
        Driver's rank given by the eight race rolling average.
    probabilities: DriverProbabilities
        Probabilities for where the Driver will finish in the next race.
    completion_prob: CompletionProbabilities
        Probabilities for completing the race.

    Methods
    -------
    qualifying_points
        Expected points earned from qualifying.
    race_points
        Expected points earned from the race.
    completion_points
        Expected points from race completion.
    points
        Expected points earned by the Driver.
    """

    def __init__(
        self,
        name: str,
        cost: int,
        rank: int,
        probabilities: DriverProbabilities = DEFAULT_PROBABILITY,
        completion: CompletionProbabilities = COMPLETE_RACE,
    ) -> None:

        self.name = name
        self.cost = cost
        self.rank = rank
        self.probabilities = probabilities
        self.completion_prob = completion

    def qualifying_points(self, team=False) -> float:
        """Expected points earned from qualifying.

        The expected points from qualification for driver and team points.

        Parameters
        ----------
        team: bool
            If True it returns the expected team points earned by the driver. If False
            it returns the expected driver points earned by the driver.

        Returns
        -------
        return: float
            Expected points earned by the driver in the qualifying stage.
        """

        if team:
            scoring = LeagueScoring.Team.QUALIFYING
        else:
            scoring = LeagueScoring.Driver.QUALIFYING

        return sum(self.probabilities.qual * scoring)

    def race_points(self, team=False) -> float:
        """Expected points earned from the race.

        The expected points from the race stage for driver and team points.

        Parameters
        ----------
        team: bool
            If True it returns the expected team points earned by the driver. If False
            it returns the expected driver points earned by the driver.

        Returns
        -------
        return: float
            Expected points earned by the driver in the race stage.
        """

        if team:
            scoring = LeagueScoring.Team.RACE
        else:
            scoring = LeagueScoring.Driver.RACE

        return sum(self.probabilities.race * scoring)

    def completion_points(self) -> float:
        """Expected points from race completion.

        Race completion is the percentile of the race completed by the driver.

        Returns
        -------
        return: float
            Expected points earned by the driver from race completion.
        """

        return sum(self.completion_prob.probabilities * LeagueScoring.Driver.COMPLETION)

    def overtake_points(self) -> float:
        """Expected points from overtaking.

        Overtaking is determined by the difference in positions between qualifying and
        the race result.

        Returns
        -------
        return: float
            Expected points earned by the driver from overtake.
        """

        return (
            (
                self.probabilities.overtake_probabilities()
                * LeagueScoring.Driver.OVERTAKE
            )
            .sum()
            .sum()
        )

    def beat_teammate_points(self) -> float:
        """Expected points from beating the other team mate.

        Beating other team mate points are determined by the probabilities a driver has
        of finishing a certain number of positions above its team mate.

        Returns
        -------
        return: float
            Expected points earned by the driver from beating its team mate.
        """

        expected_points = (
            self.beat_teammate_probabilities() * LeagueScoring.Driver.BEAT_TEAMMATE
        )

        return expected_points.sum().sum()

    def personal_improvement_points(self) -> float:
        """Expected points from personal improvement.

        Personal improvements are calculated given the probabilities of a driver
        finishing the race some positions above its rank.

        Returns
        -------
        return: float
            Expected points earned by the driver from personal improvement.
        """

        pos_improve = self.rank - Series(range(1, 21), range(1, 21))
        points_improve = LeagueScoring.Driver.PERSONAL_IMPROVEMENT.loc[pos_improve]
        points_improve.index = range(1, 21)

        expected_points = self.probabilities.race * points_improve

        return expected_points.sum()

    def points(self, team=False) -> float:
        """Total expected points.

        The expected points from the race for driver and team points.

        Note
        ----
        A driver can only earn points for the Team from the qualifying and race
        position.

        Parameters
        ----------
        team: bool
            If True it returns the expected team points earned by the driver. If False
            it returns the expected driver points earned by the driver.

        Returns
        -------
        points: float
            Expected points earned by the driver for a whole race.
        """

        points = self.qualifying_points(team) + self.race_points(team)

        if team is False:
            points += (
                self.completion_points()
                + self.overtake_points()
                + self.beat_teammate_points()
                + self.personal_improvement_points()
            )

        return points

    def to_fixed_info(self) -> FixedInfo:
        "Fix Driver info for easy optimization."

        return FixedInfo(name=self.name, cost=self.cost, points=self.points())

    def other_teammate(self):
        "Get the other team mate."
        if self.team.driver_1 == self:
            return self.team.driver_2
        return self.team.driver_1

    def beat_teammate_probabilities(self):
        "Get the probabilities of beating the other team mate."
        prob_driver = self.probabilities.race
        prob_teammate = self.other_teammate().probabilities.race

        df = DataFrame(0, index=range(1, 21), columns=range(1, 21))
        for pos, prob in prob_driver.items():
            conditional_prob = copy.copy(prob_teammate)
            conditional_prob[pos] = 0
            norm_prob = (conditional_prob * prob) / sum(conditional_prob)
            df[pos] = norm_prob

        return df

    def __eq__(self, driver: "Driver") -> bool:
        "Compare if two Drivers are the same Driver."
        return self.name == driver.name

    def __repr__(self) -> str:
        return self.name


LHamilton = Driver("L. Hamilton", 30.3 * 1e6, 1)
MVerstappen = Driver("M. Verstappen", 29.7 * 1e6, 2)
VBottas = Driver("V. Bottas", 27.5 * 1e6, 3)
SPerez = Driver("S. Perez", 26.1 * 1e6, 4)
LNorris = Driver("L. Norris", 24.0 * 1e6, 5)
DRicciardo = Driver("D. Ricciardo", 23.9 * 1e6, 6)
CLeclerc = Driver("C. Leclerc", 21.8 * 1e6, 7)
FAlonso = Driver("F. Alonso", 21.5 * 1e6, 8)
CSainz = Driver("C. Sainz Jr", 18.5 * 1e6, 9)
SVettel = Driver("S. Vettel", 17.6 * 1e6, 10)
LStroll = Driver("L. Stroll", 17.1 * 1e6, 11)
PGasly = Driver("P. Gasly", 14.5 * 1e6, 12)
EOcon = Driver("E. Ocon", 14.4 * 1e6, 13)
YTsunoda = Driver("Y. Tsunoda", 13.8 * 1e6, 14)
KRaikkonen = Driver("K. Raikkonen", 13.8 * 1e6, 15)
AGiovinazzi = Driver("A. Giovinazzi", 11.0 * 1e6, 16)
GRUssell = Driver("G. Russell", 9.2 * 1e6, 17)
MSchumacher = Driver("M. Schumacher", 6.8 * 1e6, 18)
NLatifi = Driver("N. Latifi", 6.6 * 1e6, 19)
NMazepin = Driver("N. Mazepin", 4.2 * 1e6, 20)

DRIVERS = [
    LHamilton,
    MVerstappen,
    VBottas,
    SPerez,
    DRicciardo,
    FAlonso,
    LNorris,
    CLeclerc,
    SVettel,
    CSainz,
    LStroll,
    PGasly,
    EOcon,
    KRaikkonen,
    YTsunoda,
    AGiovinazzi,
    GRUssell,
    NLatifi,
    MSchumacher,
    NMazepin,
]
