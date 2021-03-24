"F1 Drivers."

from pandas import Series

from gridrival.probabilities import DriverProbabilities
from gridrival.probabilities.completion import CompletionProbabilities, COMPLETE_RACE
from gridrival.scoring import LeagueScoring


DEFAULT_PROBABILITY = DriverProbabilities(Series(1 / 20, index=range(1, 21)))


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
        probabilities: DriverProbabilities = DEFAULT_PROBABILITY,
        completion: CompletionProbabilities = COMPLETE_RACE,
    ) -> None:

        self.name = name
        self.cost = cost
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

    def completion_points(self, team=False) -> float:
        """Expected points from race completion.

        Race completion is the percentile of the race completed by the driver.

        Returns
        -------
        return: float
            Expected points earned by the driver from race completion.
        """

        return sum(self.completion_prob * LeagueScoring.Driver.COMPLETION)

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

        points = self.expected_qualifying_points(team) + self.expected_race_points(team)

        if team is False:
            points = points + self.completion_points()

    def __eq__(self, driver: "Driver") -> bool:
        "Compare if two Drivers are the same Driver."
        return self.name == driver.name

    def __repr__(self) -> str:
        return self.name


LHamilton = Driver("L. Hamilton", 30 * 1e6)
MVerstappen = Driver("M. Verstappen", 28.7 * 1e6)
VBottas = Driver("V. Bottas", 27.4 * 1e6)
SPerez = Driver("S. Perez", 26.1 * 1e6)
DRicciardo = Driver("D. Ricciardo", 24.8 * 1e6)
FAlonso = Driver("F. Alonso", 23.5 * 1e6)
LNorris = Driver("L. Norris", 22.2 * 1e6)
CLeclerc = Driver("C. Leclerc", 20.9 * 1e6)
SVettel = Driver("S. Vettel", 19.6 * 1e6)
CSainz = Driver("C. Sainz Jr", 18.3 * 1e6)
LStroll = Driver("L. Stroll", 17 * 1e6)
PGasly = Driver("P. Gasly", 15.7 * 1e6)
EOcon = Driver("E. Ocon", 14.4 * 1e6)
KRaikkonen = Driver("K. Raikkonen", 13.1 * 1e6)
YTsunoda = Driver("Y. Tsunoda", 11.8 * 1e6)
AGiovinazzi = Driver("A. Giovinazzi", 10.5 * 1e6)
GRUssell = Driver("G. Russell", 9.2 * 1e6)
NLatifi = Driver("N. Latifi", 7.9 * 1e6)
MSchumacher = Driver("M. Schumacher", 6.6 * 1e6)
NMazepin = Driver("N. Mazepin", 5.3 * 1e6)

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
