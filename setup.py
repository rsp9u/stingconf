import sys
from setuptools import setup


tests_require = [
    'pytest',
    'pytest-mock',
]

if sys.version_info < (3, 0):
    tests_require.append('mock')

setup(
    name='stingconf',
    version='0.0.1',
    author='',
    author_email='',
    maintainer='rsp9u',
    maintainer_email='gctwt852@yahoo.co.jp',
    license='MIT',
    url='',
    description='Layered configuration library',
    packages=['stingconf'],
    install_requires=[
        'PyYAML',
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=tests_require,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
)
