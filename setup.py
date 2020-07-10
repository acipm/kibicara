from setuptools import find_packages, setup

setup(
    name='kibicara',
    version='0.1.0',
    description='distribute messages across different social media',
    url='https://github.com/acipm/kibicara',
    license='0BSD',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kibicara=kibicara.kibicara:Main',
        ]
    },
    install_requires=[
        'aiofiles',
        'aiogram',
        'aiosqlite',
        'argon2_cffi',
        'fastapi',
        'hypercorn',
        'ormantic @ https://github.com/dl6tom/ormantic/tarball/master#egg=ormantic-0.0.32',
        'passlib',
        'peony-twitter[all]',
        'pynacl',
        'python-multipart',
        'pytoml',
        'requests',
        'scrypt',
    ],
)
