from setuptools import setup, find_packages

setup(
    name             = 'differential_privacy',
    version          = '1.0',
    description      = 'apply differential_privacy in medical data',
    author           = 'MinDong Sung',
    
    install_requires = [
        "joblib==0.14.1",
        "numpy==1.18.4",
        "pandas==1.0.3",
        "python-dateutil==2.8.1",
        "pytz==2020.1",
        "scikit-learn==0.22.2.post1",
        "scipy==1.4.1",
        "six==1.14.0",
        "sklearn==0.0",
    ],
    classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False    
)