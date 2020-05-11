from setuptools import setup, find_packages

setup(
    name             = 'differential_privacy',
    version          = '1.0',
    description      = 'apply differential_privacy in medical data',
    author           = 'MinDong Sung',
    author_email     = 'sungmindong@gmail.com',
    #url              = 'https://github.com/rampart81/pyquibase',
    #download_url     = 'https://githur.com/rampart81/pyquibase/archive/1.0.tar.gz',
    install_requires = [],
    packages         = find_packages(exclude = ['docs', 'tests*']),
    keywords         = ['liquibase', 'db migration'],
    python_requires  = '>=3',
    package_data     =  {},
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3.6'
    ]
)