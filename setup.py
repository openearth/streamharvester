#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # we also require opencv and numpy but we expect these to be pre-installed
    # otherwise compile time is a bit long
    # Expects libyaml:
    'pyyaml',
    'netCDF4',
    'scikit-image',
    'livestreamer',
    'celery[sqlalchemy]'
]

test_requirements = [
    'tox',
    'coverage'
]

setup(
    name='streamharvester',
    version='0.1.0',
    description="Harvest social media streams and webcams.",
    long_description=readme + '\n\n' + history,
    author="Fedor Baart",
    author_email='fedor.baart@deltares.nl',
    url='https://github.com/openearth/streamharvester',
    packages=[
        'streamharvester',
    ],
    package_dir={
        'streamharvester': 'streamharvester'
    },
    package_data={
        'streamharvester': [
            'data/*.json',
            'data/*.yml'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords='streamharvester',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Gnu Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'streamharvester=streamharvester.commands:main',
        ],
    },
    test_suite='tests',
    tests_require=test_requirements
)
