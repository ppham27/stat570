import numpy as np
import pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects import r


def load_data() -> pd.DataFrame:
    importr('lasso2')
    r.data('Prostate');
    prostate = pandas2ri.ri2py(r.Prostate)
    return prostate
