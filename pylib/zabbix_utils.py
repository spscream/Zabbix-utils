#!/usr/bin/python
# -*- coding: utf8 -*-
from zabbix_api import ZabbixAPI, ZabbixAPIException
from utils import invertColor, getColor
import sys
import re

class BaseCreator(object):
    """ Base class for Zabbix creator """
    def __init__(self,options):
        self.options = options
        self.server = 'http://%s/api_jsonrpc.php ' % self.options.server
        self.username = self.options.username
        self.password = self.options.password
        self.zbxLogin()

    def zbxLogin(self):
        self.zapi = ZabbixAPI(server=self.server,log_level=0)
        try:
            self.zapi.login(self.username, self.password)
            print "Zabbix API Version: %s" % self.zapi.api_version()
            print "Logged in: %s" % str(self.zapi.test_login())
        except ZabbixAPIException, e:
            sys.stderr.write(str(e) + '\n')

    def getTemplateByName(self, name):
        params = {
            "filter" : {
                "host" : name
            }
        }
        return self.zapi.template.get(params)[0]

    def getItemByParams(self, params):
        params = {
            "search" : params
        }
        return self.zapi.item.get(params)

    def getHostByName(self, name):
        params = {
            "search" : {
                "host" : name
            }
        }
        return self.zapi.host.get(params)

    def getGraphByName(self, name):
        params = {
            "search" : {
                "name" : name
            }
        }
        return self.zapi.graph.get(params)


class ItemCreator(BaseCreator):
    def createItem(self, host, key, name, delay=60, history=14, trends=30, type=0, value_type=0, **params):
        """ Create zabbix item for host or template, if item already exists, skip it.
            Parameters:
            host - host or template name
            key - key for newly created item
            name - name of item
            delay - update interval of item
            history - how long to keep item history (days) 
            trends - How long to keep item trends (days) 
            type - type of item
            value_type - type of value
            params - additional params

            For details see http://www.zabbix.com/documentation/1.8/api/item
        """
        try:
            item = {
                'key_' : key,
                'name': name,
                'description': name,
                'delay': delay,
                'history': history,
                'trends': trends,
                'type' : type,
                'value_type' : value_type,
            }
            item.update(params)
            print item
            itemids = self.getItemByParams({'key_': item['key_']})
            if itemids:
                for itemid in itemids:
                    #item.update({'templateid':self.getTemplateByName(host)})
                    self._update(itemid['itemid'], item)
            else:
                item.update({'hostid':self.getTemplateByName(host)['templateid']})
                self._create(item)

        except ZabbixAPIException, e:
            sys.stderr.write(str(e) + '\n')

    def isExists(self, item):
        return self.zapi.item.exists(item)

    def _create(self, item):
        self.zapi.item.create(item)

    def _update(self, itemid, item):
        item['itemid'] = itemid
        self.zapi.item.update(item)

class MassItemCreator(ItemCreator):
    def createItems(self, host, items):
        """
        Create zabbix items for host or template, if item are already exist, update it.

        Paratemers:
        host - name of host or template, where items should be created
        items - list of parameters where parameter is dict with parameters like for ItemCreator
        """
        existing = {}
        for i in self.getTemplateByName(host, selectItems='extend')['items']:
            existing[i['key_']] = i
        new_items = []
        updating_items = []
        hostid = self.getTemplateByName(host)['templateid']
        for item in items:
            if item['key_'] in existing.keys():
                updated = existing[item['key_']]
                updated.update(item)
                updating_items.append(updated)
            else:
                new_items.append(item)
        for item in new_items:
            item.update({'hostid': hostid})
        for item in updating_items:
            item.pop('templateid', None)
        self.zapi.item.create(new_items)
        self.zapi.item.update(updating_items)

class GraphCreator(BaseCreator):
    def createGraphByHostgroup(self, group, key, name, drawtype='2', width='900', height='200'):
        """ Creates zabbix graph for hostgroup with graphitems determined by key.
            If graph already exists, updates it.
            Parameters:
            group - host group
            key - item key which will be graphed
            name - graph name
            drawtype - Line(0), filled region(1), bold line(2), dot(3), dashed(4), gradient(5)
            width - width of graph
            height - height of graph
        """
        try:
            gitems = []
            items = self.zapi.item.get({'group': group,
                                        'sortfield': 'itemid',
                                        'selectHosts': 'extend',
                                        'filter' : {'key_': key}})
            # Add sorting as human expect
            def sort_by_host(items):
                convert = lambda text: int(text) if text.isdigit() else text
                alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
                return sorted(items, key=lambda item: alphanum_key(item['hosts'][0]['name']))

            sorted_items = sort_by_host(items)
            for item in sorted_items:
                gitem = self._makeGraphItem(item['itemid'],
                                            drawtype,
                                            getColor(len(items), sorted_items.index(item)),
                                            sorted_items.index(item))
                gitems.append(gitem)
            graph = self._makeGraph(gitems, name, width, height)
            self._createGraph(graph)
        except ZabbixAPIException, e:
            sys.stderr.write(str(e) + '\n')

    def createGraphByKeyPattern(self, template, keypattern, name, drawtype='2', width='900', height='200'):
        """ Creates zabbix template graph for items with key matched pattern.
            If graph already exists, updates it.
            Parameters:
            template - template name
            keypattern - key pattern which should match items for graphing
            name - graph name
            drawtype - Line(0), filled region(1), bold line(2), dot(3), dashed(4), gradient(5)
            width - width of graph
            height - height of graph
        """
        try:
            gitems = []
            items = self.zapi.item.get({'sortfield':'itemid',
                                        'templated': True,
                                        'search' : {'key_': keypattern},
                                        'searchWildcardsEnabled': True}
            )
            from pprint import pprint
            pprint(items)
            for item in items:
                gitem = self._makeGraphItem(item['itemid'],
                                            drawtype,
                                            getColor(len(items), items.index(item)),
                                            items.index(item))
                gitems.append(gitem)
            graph = self._makeGraph(gitems, name, width, height)
            self._createGraph(graph)
        except ZabbixAPIException, e:
            sys.stderr.write(str(e) + '\n')


    def _createGraph(self, graph):
        graphid = self.getGraphByName(graph['name'])
        if graphid:
            graph['graphid'] = graphid[0]['graphid']
            self.zapi.graph.update(graph)
        else:
            self.zapi.graph.create(graph)

    def _makeGraphItem(self, itemid, drawtype, color, sortorder):
        gitem = {
                    'itemid' : itemid,
                    'drawtype' : drawtype,
                    'color' : color,
                    'yaxisside' : '0',
                    'sortorder' : sortorder,
                    'calc_fnc' : '2',
                    'type' : '0',
                    'periods_cnt': '1',
                }
        return gitem

    def _makeGraph(self, gitems, name, width, height):
        graph = {
                "gitems" : gitems,
                "name" : name,
                "width" : width,
                "height" : height,
                "yaxismin" : "0.0000",
                "yaxismax" : "10.0000",
                "show_work_period" : "1",
                "show_triggers" : "1",
                "graphtype" : "0",
                "show_legend" : "1",
                "show_3d" : "0",
                "percent_left" : "0.0000",
                "percent_right" : "0.0000",
                "ymin_type":"0",
                "ymax_type":"0",
                "ymin_itemid":"0",
                "ymax_itemid":"0"
            }
        return graph

    def _create(self, graph):
        self.zapi.graph.create(graph)

    def _update(self, graphid, graph):
        graph['graphid'] = graphid
        self.zapi.graph.update(graph)

class CacheFileReader(object):
    def __init__(self, file):
        self.items = {}
        self.file = open(file, 'r')
        self.read()

    def read(self):
        TIMESTAMP_RE=re.compile("^\d*$")
        #DATA_RE="^(?P<key>[\w]+)[\s]+(?P<value>[\w]+)[\s]*(?P<params>[\w]*)"
        DATA_RE="^\s*(?P<key>[\w\.\[\]]+)\s+(?P<value>\w+)\s*(?P<params>.*)$"
        for line in self.file:
            m = re.match(DATA_RE, line)
            if m:
                self.items[m.group('key')] = {
                    'value': m.group('value'),
                    'params': m.group('params')
                }
