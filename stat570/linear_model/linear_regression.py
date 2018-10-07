"""Model for ordinary least-squares regression."""

from collections import OrderedDict
import logging
from typing import List

import numpy as np
import pandas as pd
from scipy import linalg, stats
from sklearn.base import BaseEstimator
from sklearn.utils import check_X_y


class LinearRegression(BaseEstimator):

    def __init__(self, fit_intercept = True) -> None:
        super(LinearRegression, self).__init__()
        self.fit_intercept = fit_intercept

    def fit(self, X: np.array, y: np.array) -> 'LinearRegression':
        check_X_y(X, y)
        if self.fit_intercept:
            X = np.hstack((np.ones((len(X), 1)), X))

        X = np.array(X, dtype=np.float64)
        y = np.array(y, dtype=np.float64)

        if X.shape[0] < X.shape[1]:
            logging.warning('Cannot fit: there are more covariates than observations.')
            return self

        # Estimate the coefficients by solving the least squares problem.
        gram_matrix = np.matmul(X.T, X)
        beta = linalg.solve(gram_matrix, np.matmul(X.T, y))

        # Calculate residual variance using our estimate for the coefficients.
        residuals = y - np.matmul(X, beta)
        self.residual_variance_ = np.sum(np.square(residuals))/(len(y) - len(beta))

        # Do a hypothesis test for each beta_j, where the null hypothesis is beta_j = 0.
        beta_std_error = np.sqrt(np.diag(linalg.cho_solve(
            linalg.cho_factor(gram_matrix), np.eye(len(beta))))*self.residual_variance_)
        beta_t_statistic = beta/beta_std_error
        beta_p_value = 2*(stats.t.sf(np.abs(beta_t_statistic), df=len(y) - len(beta)))

        self.coefficients_ = pd.DataFrame(OrderedDict([
            ('estimate', beta),
            ('std_error', beta_std_error),
            ('t-statistic', beta_t_statistic),
            ('p-value', beta_p_value),
        ]))
        
        return self

    @staticmethod
    def from_data_frame(
            data_frame: pd.DataFrame,
            covariates: List[str], response: str) -> 'LinearRegression':
        # Extract covariates.
        X = data_frame[covariates].as_matrix()
        y = data_frame[response].as_matrix()
        # Fit model.
        linear_regression = LinearRegression().fit(X, y)
        linear_regression.coefficients_.index = ['(intercept)'] + covariates
        return linear_regression
