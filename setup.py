import setuptools

with open('README.rst') as file:

    readme = file.read()

name = 'md4c'

version = '0.1.4'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

setuptools.setup(
    name = name,
    version = version,
    author = author,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Markdown parsing.',
    long_description = readme,
    include_package_data = True,
    extras_require = {
        'html': [
            'bs4'
        ],
        'ascii': [
            'sty'
        ]
    }
)
