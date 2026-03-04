from setuptools import setup, find_packages
setup(
    name="diagram-ctl",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["networkx", "pygraphviz"],
    entry_points={"console_scripts": ["diagram-ctl=diagram_ctl.__main__:main"]},
)
