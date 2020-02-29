from os.path import dirname, join
from setuptools import setup

with open(join(dirname(__file__), 'README.md')) as readme_file:
    long_description = readme_file.read()


setup(
    name='lan-presenter',
    version='0.1.0',
    description='Presenter remote control over local network connection',
    long_description=long_description,
    long_description_content_type='Description-Content-Type: text/markdown; '
                                  'charset=UTF-8; variant=GFM',
    author='Tibor Hári',
    author_email='hartib@gmail.com',
    url='https://github.com/tiborhari/lan-presenter/',
    py_modules=['lan_presenter'],
    data_files=['index.html'],
    package_data={'django_admin_reset': ['templates/admin/*.html',
                                         'locale/*/LC_MESSAGES/*.[mp]o']},
    entry_points={
        'console_scripts': [
            'lan_presenter=lan_presenter:main',
        ],
    },
    python_requires='>=3.6, <4',
    install_requires=[
        'aiohttp>=3.6.2,<3.7',
        'keyboard>=0.13.4,<0.14',
    ],
    extras_require={
        'dev': [
            'flake8==3.7.9',
        ]
    },
)
