"Helpers."

import pandas as pd

from gridrival.objects import Driver

TALENT_DRIVER_COST = 18*1e6

DefaultProbability = pd.Series({i: 1/20 for i in range(1,21)})

EmptyDriver = Driver("EMPTY", 0, pd.Series({i: 0 for i in range(1,21)}))
