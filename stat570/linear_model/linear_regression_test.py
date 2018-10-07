import unittest

import pandas as pd
from stat570.linear_model.linear_regression import LinearRegression
from sklearn.utils.estimator_checks import check_estimator
from sklearn import datasets


class LinearRegressionTestCase(unittest.TestCase):    
    def test_estimator_check(self):
        check_estimator(LinearRegression)

    def test_fit(self):
        boston = datasets.load_boston()
        feature_idx = [
            idx for idx, feature in enumerate(boston.feature_names)
            if feature in ['RM', 'LSTAT']]
        X = boston.data[:, feature_idx]
        y = boston.target
        linear_model = LinearRegression().fit(X, y)

        self.assertAlmostEqual(
            linear_model.residual_variance_,
            30.69445169247223)
        self.assertAlmostEqual(
            linear_model.coefficients_['estimate'][1],
            5.094788)

    def test_from_data_frame(self):
        boston = datasets.load_boston()
        medv = boston.target
        boston = pd.DataFrame(boston.data, columns=boston.feature_names)
        boston['MEDV'] = medv

        linear_model = LinearRegression.from_data_frame(
            boston, ['LSTAT', 'RM'], 'MEDV')

        self.assertAlmostEqual(
            linear_model.coefficients_.loc['RM']['estimate'],
            5.094788)
        self.assertAlmostEqual(
            linear_model.coefficients_.loc['LSTAT']['estimate'],
            -0.642358334244134)
        

if __name__ == '__main__':
    unittest.main()
