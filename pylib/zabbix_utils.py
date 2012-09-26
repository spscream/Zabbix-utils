#!/usr/bin/python
from zabbix.zabbix_api import ZabbixAPI, ZabbixAPIException
from utils import getColor
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
        return self.zapi.template.get(params)[0]['templateid']

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
    def createItem(self, host, key, description, type=0, value_type=0, **params):
        """ Create zabbix item for host or template, if item already exists, skip it.
            Parameters:
            host - host or template name
            key - key for newly created item
            description - description of item
            type - type of item
            value_type - type of value
            params - additional params

            For details see http://www.zabbix.com/documentation/1.8/api/item
        """
        try:
            item = {
                '_key' : key,
                'templateid' : self.getTemplateByName(host),
                'description': description,
                'type' : type,
                'value_type' : value_type,
            }
            item.update(params)

            itemid = self.getItemByParams(item)
            if itemid:
                self._update(itemid[0]['itemid'], item)
            else:
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

class GraphCreator(BaseCreator):
    def createGraph(self, group, key, name, drawtype='2', width='900', height='200'):
        """ Create zabbix graph for hostgroup with graphitems determined by key.
            If graph already exists, update it.
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
            items = self.zapi.item.get({'group':group, 
                                        'sortfield':'itemid',
                                        'selectHosts':'extend',
                                        'filter' : {'key_': key}})
            # Add sorting as human expect
            def sort_by_host(items):
                convert = lambda text: int(text) if text.isdigit() else text
                alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
                return sorted(items, key=lambda item: alphanum_key(item['hosts'][0]['name']))

            sorted_items = sort_by_host(items)
            for item in sorted_items:
                gitem = {
                    'itemid' : item['itemid'],
                    'drawtype' : drawtype,
                    'color' : getColor(len(items), sorted_items.index(item)),
                    'yaxisside' : '0',
                    'sortorder' : sorted_items.index(item),
                    'calc_fnc' : '2',
                    'type' : '0',
                    'periods_cnt': '1',
                }
                gitems.append(gitem)

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
            graphid = self.getGraphByName(graph['name'])
            if graphid:
                self._update(graphid[0]['graphid'], graph)
            else:
                self._create(graph)
        except ZabbixAPIException, e:
            sys.stderr.write(str(e) + '\n')

    def _create(self, graph):
        self.zapi.graph.create(graph)

    def _update(self, graphid, graph):
        graph['graphid'] = graphid
        self.zapi.graph.update(graph)



