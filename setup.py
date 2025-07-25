from setuptools import setup, find_packages

setup(
    name='TCP Scanner [Command-Line Interface]',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'scanTCP = main:main',  # CLI command
        ],
    },
    author='Lin Lin Aung',
    description='TCP Scanner [Command-Line Interface] with logging system, argparse for CLI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/yourproject',  # optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)