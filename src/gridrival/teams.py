"F1 Teams"

from gridrival.drivers import (
    AGiovinazzi,
    CLeclerc,
    CSainz,
    DRicciardo,
    Driver,
    EOcon,
    FAlonso,
    FixedInfo,
    GRUssell,
    KRaikkonen,
    LHamilton,
    LNorris,
    LStroll,
    MSchumacher,
    MVerstappen,
    NLatifi,
    NMazepin,
    PGasly,
    SPerez,
    SVettel,
    VBottas,
    YTsunoda,
)


class Team:
    """A F1 Team.

    A Team is a collection of two Drivers which can earn team points.

    Attributes
    ----------
    name: str
        Name of the Team.
    cost: int
        Cost of the Team in the fantansy league.
    driver_1: Driver
        Driver which belongs to the Team.
    driver_2: Driver
        Driver which belongs to the Team.

    Methods
    -------
    points
        Expected team points earned by the Team.
    """

    def __init__(
        self, name: str, driver_1: Driver, driver_2: Driver, cost: int
    ) -> None:

        self.name = name
        self.driver_1 = driver_1
        self.driver_2 = driver_2
        self.cost = cost

        driver_1.team = self
        driver_2.team = self

    def qualifying_points(self) -> float:
        """Expected team points earned from qualifying.

        The expected team points from qualification for both Team Drivers.

        Returns
        -------
        return: float
            Expected points earned by the Drivers in the qualifying stage.
        """

        return self.driver_1.qualifying_points(
            team=True
        ) + self.driver_2.qualifying_points(team=True)

    def race_points(self) -> float:
        """Expected team points earned from the race stage.

        The expected team points from the race stage for both Team Drivers.

        Returns
        -------
        return: float
            Expected points earned by the Drivers in the race stage.
        """

        return self.driver_1.race_points(team=True) + self.driver_2.race_points(
            team=True
        )

    def points(self) -> float:
        """Expected team points earned from the race.

        The expected team points from the race for both Team Drivers.

        Returns
        -------
        return: float
            Expected points earned by the Drivers in the race.
        """

        return self.driver_1.points(team=True) + self.driver_2.points(team=True)

    def to_fixed_info(self) -> FixedInfo:
        "Fix Team info for easy optimization."

        return FixedInfo(name=self.name, cost=self.cost, points=self.points())

    def __contains__(self, driver: Driver) -> bool:
        "A Team contains a Driver if it is one of its two Drivers."
        return (self.driver_1 == driver) or (self.driver_2 == driver)

    def __eq__(self, team: "Team") -> bool:
        "Compare if two Teams are the same Team."
        return self.name == team.name

    def __repr__(self) -> str:
        return self.name


Mercedes = Team("Mercedes", LHamilton, VBottas, 25.3 * 1e6)
RedBull = Team("Red Bull", MVerstappen, SPerez, 27.0 * 1e6)
McLaren = Team("McLaren", DRicciardo, LNorris, 24.2 * 1e6)
AstonMartin = Team("Aston Martin", SVettel, LStroll, 17.6 * 1e6)
Alpine = Team("Alpine", FAlonso, EOcon, 17.0 * 1e6)
Ferrari = Team("Ferrari", CLeclerc, CSainz, 20.5 * 1e6)
AlphaTauri = Team("AlphaTauri", PGasly, YTsunoda, 17.3 * 1e6)
AlfaRomeo = Team("Alfa Romeo", KRaikkonen, AGiovinazzi, 11.6 * 1e6)
Haas = Team("Haas", MSchumacher, NMazepin, 5.9 * 1e6)
Williams = Team("Williams", GRUssell, NLatifi, 7.5 * 1e6)

TEAMS = [
    Mercedes,
    RedBull,
    McLaren,
    AstonMartin,
    Alpine,
    Ferrari,
    AlphaTauri,
    AlfaRomeo,
    Haas,
    Williams,
]
