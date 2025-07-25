from setuptools import setup, find_packages

setup(
    name='tcp-scanner-cli',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'scanTCP = scanner.main:main',
        ],
    },
    author='Lin Lin Aung',
    description='A command-line TCP port scanner with subnet sweep and logging',
    python_requires='>=3.6',
)