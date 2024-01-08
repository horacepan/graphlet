from setuptools import setup, find_packages

setup(
    name='graphlet',
    version='0.1.0',
    packages=find_packages(),
    description='A lightweight graph-based compute library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Horace Pan',
    url='https://github.com/horacepan/graphlet',
    install_requires=[
        "networkx", "numpy", "pandas", "matplotlib", "requests", "pydantic"
    ],
    python_requires='>=3.9',
)

