import optparse
import sys
from getpass import getpass

def get_options():
    """ command-line options """

    usage = "usage: %prog [options]"
    OptionParser = optparse.OptionParser
    parser = OptionParser(usage)

    parser.add_option("-s", "--server", action="store", type="string",
            dest="server", help="Zabbix Server URL (REQUIRED)")
    parser.add_option("-u", "--username", action="store", type="string",
            dest="username", help="Username (Will prompt if not given)")
    parser.add_option("-p", "--password", action="store", type="string",
            dest="password", help="Password (Will prompt if not given)")

    options, args = parser.parse_args()

    if not options.server:
        show_help(parser)

    if not options.username:
        options.username = raw_input('Username: ')

    if not options.password:
        options.password = getpass()

    if not options.username and not options.password:
        show_help(parser)

    return options, args

def show_help(p):
    p.print_help()
    sys.exit(-1)
