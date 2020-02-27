from setuptools import find_packages, setup

setup(
    name='ultron',
    version='1.0.0a0',
    description='ultron - An EVE Online Discord Bot',
    url='https://github.com/shibdib/firetail',
    author='Sheppard',
    license='MIT License',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Role-Playing',
        'Topic :: Communications :: Chat',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='eve online eveonline community discord bot',

    # find_packages(exclude=['contrib', 'docs', 'tests'])
    packages=find_packages(),

    install_requires=[
        'discord.py[voice]',
        'python-dateutil>=2.6',
        'asyncpg>=0.13',
        'pytz',
        'youtube_dl',
        'aiohttp==3.6.2',
        'feedparser',
        'requests'
    ],

    dependency_links=[
        'git+https://github.com/Rapptz/discord.py[voice]'
    ],

    entry_points={
        'console_scripts': [
            'ultron=ultron.launcher:main',
            'ultron-bot=ultron.__main__:main'
        ],
    },
)
