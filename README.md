This is utils for zabbix.

FEATURES:
 - Create and update hostgroup graphs.

DEPENDENCIES:

- zabbix_api git://github.com/gescheit/scripts.git)

INSTALL:

- Clone repo:
  git clone https://github.com/spscream/Zabbix-utils zabbix-utils

- Init submodules:
  cd zabbix-utils; git submodule update --init

- Install zabbix_api python module
  cd pylib/externals/zabbix && sudo python setup.py install

USAGE:

1) Add graphs to make_zabbix_graphs.py
 e.g.:
 Add graph for hostgroup 'Example' with graphed item 'system.cpu.load[,avg1]' and graph name 'Example: Processor load'
    gc.createGraph('Example' , 'system.cpu.load[,avg1]', 'Example: Processor load')

2) run ./make_zabbix_graphs.py -s zbx.example.org -u apiuser -p apipassword

TODO:
 - Configuration with python object;
 - Generators for Triggers, Items, Screens;
 - API Documentation.
