# Development
1. install `pyenv`
2. Find appropiate python version with:
`pyenv install --list`
3. Install it with `pyenv install 3.7.5`
4. Set local version via `pyenv local 3.7.5`
> (optionally) install a global python version `pyenv global 3.7.5`
5. Install `pipenv` via `pip install --user pipenv` (you pip will now be the pyenv pip)
6. Close and reopen your terminal.
7. Check setup is correct going to game directory and then running:
  `python -V` -> 3.7.5
8. Install this project with `pipenv --python 3.7.5 install --dev`. Check
the install was correct via:
  `pipenv --py` -> /home/marlen/.local/share/virtualenvs/3d-game-ZGdGqwS4/bin/python
> generating the lock file takes a _long_ time.
9. Activate virtual environment `pipenv shell`
10. Install new packages with `pipenv install <package>` or for dev dependencies `pipenv install --dev <package>`
11. Run the app, `bin/dev boot`

## dev command
Run `bin/dev` to print out current options.
```
dev
  -h --help  List possibly command usages.
  boot       Boot the app in development mode - python main.py
  build      Build the app - python setup.py build_apps
  launch     Launch the built version of the game -
               build/manylinux1_x86_64/launch_game
  clean      Clean the build directory - rm -rf build/*
  debug      Debug this script - echo "\$@=$@"

```


## Old Instructions

To run the game without Python, just run:

`$ python3 setup.py build_apps`

To make a packaged version to send, just run:

`$ python3 setup.py bdist_apps`
