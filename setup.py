try:
    from setuptools import setup
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

setup(
    name='zabbix_utils',
    description = "Python zabbix utils for working with zabbix API.",
    version='0.1',
    url='https://github.com/spscream/Zabbix-utils',
    packages=['zabbix_utils'],
    install_requires=[
        'setuptools',
        'argparse',
    ],
    license='GPLv2',
    author='amalaev',
    author_email='scream@spuge.net',
    include_package_data = True,
    zip_safe = True
)
