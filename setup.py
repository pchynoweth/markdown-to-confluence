from setuptools import setup

setup(
    name='markdown-to-confluence',
    version='0.1.0',
    description='Utility to publish markdown files to confluence',
    url='https://github.com/pchynoweth/markdown-to-confluence',
    license='Apache',
    scripts=['markdown-to-confluence'],
    packages=['markdown_to_confluence'],
    install_requires=[
        'certifi==2019.9.11',
        'chardet==3.0.4',
        'gitdb2==2.0.6',
        'GitPython>=3.0.4',
        'idna==2.8',
        'mistune==0.8.4',
        'PyYAML>=5.1.2',
        'requests>=2.22.0',
        'smmap2==2.0.5',
        'textwrap3==0.9.2',
        'urllib3',
        'yapf==0.28.0'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Apache License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
