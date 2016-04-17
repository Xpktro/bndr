# coding:utf-8
from distutils.core import setup

setup(
    name='bndr',
    packages=['bndr'],
    install_requires=['pillow'],
    entry_points={
        'console_scripts': ['bndrimg = bndr.bndrimg:main',
                            'bndtxt = bndr.bndrtxt:main']
    },
    version='1.0',
    description='A library + command line tool to facilitate '
                'databending/glitch art.',
    author='Moisés Cachay',
    author_email='xpktro@gmail.com',
    url='https://github.com/Xpktro/bndr',
    download_url='https://github.com/Xpktro/bndr/tarball/1.0',
    keywords=['glitch', 'art', 'databend', 'bend'],
    classifiers=[],
)
