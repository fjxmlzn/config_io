from pathlib import Path
from setuptools import setup

SHORT = 'Advanced config reading/writing/parsing for yaml/json configs.'

this_directory = Path(__file__).parent
LONG = (this_directory / "README.md").read_text()

setup(
    name='config_io',
    version='0.2.0',
    packages=['config_io'],
    author='Zinan Lin',
    author_email='linzinan1995@gmail.com',
    description=SHORT,
    long_description=LONG,
    long_description_content_type='text/markdown',
    keywords='config yaml json python addict',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='Any',
    license='MIT License',
    url='https://github.com/fjxmlzn/config_io',
    install_requires=['addict', 'pyyaml'],
    package_data={'': ['LICENSE']}
)
