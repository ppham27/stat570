import numpy as np
import pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects import r


def load_data() -> pd.DataFrame:
    importr('faraway')
    r.data('chredlin');
    chredlin = pandas2ri.ri2py(r.chredlin)
    chredlin = chredlin.set_index(pandas2ri.ri2py(r.chredlin.rownames))
    chredlin['log_income'] = np.log(chredlin['income'])
    return chredlin
