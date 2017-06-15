#!/usr/bin/env python

"""A python library to read config files that require indexing."""

__author__ = 'Kyle Laplante'
__copyright__ = 'Copyright 2013, Kyle Laplante'
__date__ = '06-20-2013'

__license__ = 'GPL'
__version__  = '1.2'
__email__ = 'kyle.laplante@gmail.com'


class IndexConfigParserException(Exception):
    pass


class IndexConfigParser(dict):

    '''A class to parse configuration files that require indexing.
This class returns a dictionary that you can call to retrieve items
from your config file.

To use this parser to its full potential create config files in the
following format for example:

(Example config file)

# Home server
server_1 = somename
ip_1     = 1.2.3.4
location_1 = san jose

# Remote server
server_2 = someothername
ip_2     = 4.3.2.1
location_2 = boston

# Universal configs
universal_key = something universal
my_username = kyle


You can keep raising the indexed number as much as you want.
The way to use this library is to pick a config definition
that you know will be different for each index. In this case I would
use "server" as the "defining key" and that would make each server name
into its own dictionary and the key/value pairs for it would be the config
key/values that are associated with the same index number.

There are 3 lists that are created on each parse:
keys = this is a list of the keys that are not indexed
       (used for universal purposes)
index_keys = this is a list of all the keys that are indexed
             (this is generated based on the defining key)
all_keys = this is a list of all the keys combined 

Examples:

import IndexConfigParser

(The following code will print the dictionaries of each index key)
icp = IndexConfigParser.IndexConfigParser("/home/kyle/config.cfg", "server")
for key in icp.index_keys:
    print icp[key]

(The following is how to call a specific key in the index key dict)
icp = IndexConfigParser.IndexConfigParser("/home/kyle/config.cfg", "server")
var = "somename"
icp[var]["ip"]
(Using the example config file above this would return "1.2.3.4")
'''

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError, e:
            raise IndexConfigParserException(
                "%s is not a valid key." % e.args[0])

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __init__(self, *args, **kwargs):
        '''Required arguments: file & def_key
        file = config file to be parsed (must be first arg).
        def_key = The "defining key" to associate all other values of that index to.
                  (must be second arg).'''

        for k, v in kwargs.items():
            setattr(self, k, v)

        if len(args) > 2:
            raise IndexConfigParserException(
                "Only 2 arguments accepted. You gave %d" % len(args))
        elif len(args) < 2:
            raise IndexConfigParserException(
                "Not enough arguments. Expected 2. You gave %d" % len(args))
        else:
            file = args[0]
            def_key = args[1]

        self.keys = []
        self.all_keys = []
        self.index_keys = []

        lines = filter(lambda x: not x.startswith('#')
                       and x != '', [line.strip() for line in open(file)])

        for line in lines:
            try:
                line_key = line.split('=')[0].strip()
                self.all_keys.append(line_key)
                line_val = line.split('=')[1].strip()
                setattr(self, line.split('=')[
                        0].strip(), line.split('=')[1].strip())
                try:
                    if not isinstance(int(line_key.split('_')[-1]), int):
                        self.keys.append(line_key)
                except ValueError:
                    self.keys.append(line_key)
            except IndexError:
                pass

        for k, v in self.__dict__.items():
            if '_'.join(k.split('_')[:-1]) == def_key:
                self.__dict__[v] = {}
                self.index_keys.append(v)
                index = k.split('_')[-1]
                for a, b in self.__dict__.items():
                    if a.split('_')[-1] == index:
                        self.__dict__[v]['_'.join(a.split('_')[:-1])] = b

        if len(self.index_keys) == 0:
            self.index_keys = "No index keys available for '%s'" % def_key
