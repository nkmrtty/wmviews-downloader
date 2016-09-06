from setuptools import find_packages, setup


setup(
    name='wmviews-downloader',
    version='0.0.1',
    author='Tatsuya Nakamura',
    author_email='nkmrtty.com@gmail.com',
    description='Tools for downloading Wikimedia pageview data',
    license='MIT',
    url='https://github.com/nkmrtty/wmviews-downloader',
    packages=find_packages(),
    keywords=['wikimedia', 'wikipedia', 'pageview'],
    install_requires=['requests', 'futures']
)
