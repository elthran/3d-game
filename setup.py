from setuptools import setup

setup(
    name='elthran-3d-game',
    version='0.0.1',
    author='elthran',
    author_email='elthran@gmail.com',
    description='A 3d game.',
    url="https://github.com/elthran/3d-game",
    install_requires=[
        "panda3d==1.10.5",
        "pip==19.3.1",
    ],
    classifiers=["Programming Language :: Python :: 3.6"],
    python_requires='>=3.6',
    options={
        'build_apps': {
            'console_apps': {'launch_game': 'main.py'},
            'platforms': [
                # 'manylinux1_x86_64',
                'win_amd64',
                'macosx_10_6_x86_64'
            ],
            'plugins': ['pandagl', 'p3openal_audio'],
            'include_patterns': [
                'Models/**/*',
                'Fonts/*',
                'Sounds/*',
                'UI/*',
                'Music/*',
                '**/*.py',
                'Config.prc'
            ],
            'exclude_patterns': [
                'venv/',
                '.venv/',
                'build/'
            ]
        }
    }
)
