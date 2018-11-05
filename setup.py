from setuptools import setup

setup(name='stat570',
      version='0.0.2',
      description='Code to solve exercises for UW\'s STAT 570',
      url='https://gitlab.cs.washington.edu/pmp10/stat570',
      author='Philip Pham',
      author_email='pmp10@uw.edu',
      license='MIT',
      packages=[
          'stat570',
          'stat570.linear_model',
          'stat570.mcmc',
      ],
      package_data = {
          'stat570': ['LICENSE', 'README.md'],
      },
      zip_safe=False)
