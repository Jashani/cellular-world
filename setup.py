from setuptools import setup, find_packages

README = 'Cellular World'

requires = ['numpy',
            'dataclasses',
            'perlin_noise',
            'pyyaml',
            'python-box']


def packages(namespace, dir):
    packages = find_packages(dir)
    return [f'{namespace}.{package}' for package in packages]


setup(name='cellular-world',
      version='1.0.0',
      description=README,
      long_description=README,
      package_dir={'': 'source'},
      classifiers=[
          "Programming Language :: Python",
      ],
      author='Yasha Rise',
      packages=packages('cellularworld', 'source/cellularworld'),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      # entry_points={'console_scripts': ['cellularworld = cellularworld.agent.hermes.maia:main']},
      )
