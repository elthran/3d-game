from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='elthran-3d-game',
    version='0.0.1',
    author='elthran',
    author_email='elthran@gmail.com',
    description='A 3d game.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elthran/3d-game",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=["panda3d==1.10.5"],
    classifiers=["Programming Language :: Python :: 3.6"],
    python_requires='>=3.6'
)
