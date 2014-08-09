from __future__ import print_function

import os
import sys

from ooni.report import __version__
from ooni.report import tool
from ooni.settings import config

from twisted.python import usage


class Options(usage.Options):

    synopsis = """%s [options] upload | status
""" % (os.path.basename(sys.argv[0]),)

    optParameters = [
        ["collector", "c", None,
         "Specify the collector to upload the result to."],
        ["bouncer", "b", None,
         "Specify the bouncer to query for a collector."]
    ]

    def opt_version(self):
        print("oonireport version: %s" % __version__)
        sys.exit(0)

    def parseArgs(self, *args):
        self['command'] = args[0]
        if self['command'] not in ("upload", "status"):
            raise usage.UsageError(
                "Must specify either command upload or status"
            )
        if self['command'] == "upload":
            try:
                self['report_file'] = args[1]
            except IndexError:
                self['report_file'] = None


def parse_options():
    options = Options()
    try:
        options.parseOptions()
    except Exception as exc:
        print(exc)
    return dict(options)


def tor_check():
    if not config.tor.socks_port:
        print("Currently oonireport requires that you start Tor yourself "
              "and set the socks_port inside of ooniprobe.conf")
        sys.exit(1)


def run():
    config.read_config_file()
    options = parse_options()
    if options['command'] == "upload" and options['report_file']:
        tor_check()
        return tool.upload(options['report_file'],
                           options['collector'],
                           options['bouncer'])
    elif options['command'] == "upload":
        tor_check()
        return tool.upload_all(options['collector'],
                               options['bouncer'])
    elif options['command'] == "status":
        return tool.status()