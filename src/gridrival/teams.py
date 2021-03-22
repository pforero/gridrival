"F1 Teams"

from gridrival.drivers import AGiovinazzi, CLeclerc, CSainz, DRicciardo, EOcon, FAlonso, GRUssell, KRaikkonen, LNorris, LStroll, MSchumacher, MVerstappen, NLatifi, NMazepin, PGasly, SPerez, SVettel, VBottas, LHamilton, YTsunoda, 
from gridrival.objects import Team

Mercedes = Team("Mercedes", LHamilton, VBottas, 30*1e6)
RedBull = Team("Red Bull", MVerstappen, SPerez, 27.2*1e6)
McLaren = Team("McLaren", DRicciardo, LNorris, 24.4*1e6)
AstonMartin = Team("Aston Martin", SVettel, LStroll, 21.6*1e6)
Alpine = Team("Alpine", FAlonso, EOcon, 18.8*1e6)
Ferrari = Team("Ferrari", CLeclerc, CSainz, 16.0*1e6)
AlphaTauri = Team ("AlphaTauri", PGasly, YTsunoda, 13.2*1e6)
AlfaRomeo = Team("Alfa Romeo", KRaikkonen, AGiovinazzi, 10.4*1e6)
Haas = Team("Haas", MSchumacher, NMazepin, 7.6*1e6)
Williams = Team("Williams", GRUssell, NLatifi, 4.8*1e6)

__all__ = [
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