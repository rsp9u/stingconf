from setuptools import setup


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
    tests_require=[
        'pytest',
        'pytest-mock',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
)
