from os.path import dirname, join
from setuptools import setup

from lan_presenter import __version__

with open(join(dirname(__file__), 'README.md')) as readme_file:
    long_description = readme_file.read()


setup(
    name='lan-presenter',
    version=__version__,
    description='Presenter remote control over local network connection',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tibor Hári',
    author_email='hartib@gmail.com',
    url='https://github.com/tiborhari/lan-presenter/',
    packages=['lan_presenter'],
    package_data={'lan_presenter': ['index.html']},
    entry_points={
        'console_scripts': [
            'lan_presenter=lan_presenter.__main__:main',
        ],
    },
    python_requires='>=3.6, <4',
    install_requires=[
        'aiohttp~=3.8.1',
        'keyboard~=0.13.5',
        'qrcode~=7.3.1'
    ],
    extras_require={
        'dev': [
            'flake8==3.7.9',
        ]
    },
)
