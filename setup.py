from setuptools import setup

setup(name='easyplotly',
      version='0.1',
      description='A wrapper library for creating dynamic Plotly visualizations.',
      url='https://bitbucket.spectrum-health.org:7991/stash/projects/QSE/repos/easyplotly/',
      author='Amanda Park',
      author_email='amanda.park@spectrumhealth.org',
      license='MIT',
      packages=['easyplotly'],
      install_requires=[
            'pandas',
            'plotly',
            'numpy'
        ],
      zip_safe=False)

