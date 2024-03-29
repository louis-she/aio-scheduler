#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'aioredis', 'python-daemon']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Chenglu She",
    author_email='chenglu.she@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="",
    entry_points={
        'console_scripts': [
            'aio_scheduler=aio_scheduler.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description="",
    include_package_data=True,
    keywords='asyncio,redis scheduler',
    name='aio-scheduler',
    packages=find_packages(include=['aio_scheduler', 'aio_scheduler.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/louis-she/aio_scheduler',
    version='0.1.2',
    zip_safe=False,
)
