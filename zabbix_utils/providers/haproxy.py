from zabbix_utils.lib import MassItemCreator

__author__ = 'amalaev'

class HaproxyDataProvider(object):
    items = {'scur' : dict(name='Current sessions', delta=0, history=7, type=2),
             'stot' : dict(name='Total sessions', delta=2, history=7, type=2),
             'bin' : dict(name='Bytes in', delta=2, history=7, type=2),
             'bout' : dict(name='Bytes out', delta=2, history=7, type=2),
             'econ' : dict(name='Connection errors', delta=2, history=7, type=2),
             'eresp' : dict(name='Request errors', delta=2, history=7, type=2),
             'rate' : dict(name='Session rate per second', delta=0, history=7, type=2),
             'cli_abrt' : dict(name='Client aborted sessions', delta=2, history=7, type=2),
             'srv_abrt' : dict(name='Server aborted sessions', delta=2, history=7, type=2),
             'hrsp_4xx' : dict(name='4xx responses', delta=2, history=7, type=2),
             'hrsp_5xx' : dict(name='5xx responses', delta=2, history=7, type=2)
    }

    graphs = {''}

    def __init__(self, options, name):
        self.template = name
        self.mc = MassItemCreator(options)

    def addFromFile(self, file):
        file = open(file, 'r+')
        headers = file.readline()[2:-2].split(',')
        self.data = {}
        for line in iter(file.readline, ''):
            items = line[:-2].split(',')
            if len(items) == len(headers):
                if items[0] not in self.data:
                    self.data[items[0]] = {}
                self.data[items[0]][items[1]] = dict(zip(headers,items))

    def createItems(self):
        items = []
        for cluster in self.data:
            for srv in self.data[cluster]:
                for item in self.data[cluster][srv]:
                    if item in self.items:
                        key = "%s.%s.%s" % (cluster, srv, item)
                        params = dict(self.items[item])
                        params['name'] = "[%s:%s] %s" % (cluster, srv, self.items[item]['name'])
                        items.append(self.mc.genItem(key, **params))
        self.mc.createItems(self.template, items)


    def createGraphs(self):
        graphs = []
        for cluster in self.data:
            for srv in self.data[cluster]:
                if srv in ['BACKEND','FRONTEND']:
                    pass



    def sentValues(self):
        pass