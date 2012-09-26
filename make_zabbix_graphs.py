#!/usr/bin/python
# -*- coding: utf8 -*-
from pylib.options import get_options
from pylib.zabbix_utils import GraphCreator

class ZabbixTemplate:
    def __init__(self, config):
        self.config = config
        self.parse()

    def parse(self):
        pass

if  __name__ == "__main__":
    options, args = get_options()
    gc = GraphCreator(options)
    # Example 
    gc.createGraph('Example' , 'system.cpu.load[,avg1]', 'Example: Processor load')
