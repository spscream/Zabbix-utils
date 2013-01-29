This is utils for zabbix.

### FEATURES:
- Create and update hostgroup graphs.
- Create and update graphs for items with matching  key.
- Mass create of Items

### DEPENDENCIES:
- zabbix_api git://github.com/gescheit/scripts.git

### INSTALL:
1. Clone repo:

git clone https://github.com/spscream/Zabbix-utils zabbix-utils

2. Init submodules:
  
cd zabbix-utils; git submodule update --init

- Install zabbix_api python module
  cd pylib/externals/zabbix && sudo python setup.py install

### USAGE:

Add graphs to make_zabbix_graphs.py

1. Add graph for hostgroup 'Example' with graphed item 'system.cpu.load[,avg1]' and graph name 'Example: Processor load'
```python
gc.createGraph('Example' , 'system.cpu.load[,avg1]', 'Example: Processor load')
```
2. run ./make_zabbix_graphs.py -s zbx.example.org -u apiuser -p apipassword

### TODO:
 - python package
 - Configuration with python object;
 - Generators for Triggers, Items, Screens;
 - API Documentation.
