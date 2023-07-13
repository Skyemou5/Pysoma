#!/usr/bin/env python

import argparse
import pprint
import random
import pathlib


parser = argparse.ArgumentParser()
subp = parser.add_subparsers(dest='subparser_name')

create_p = subp.add_parser('create', help='Create an empty sqlite database for storing results')
create_p.add_argument('database', type=pathlib.Path, default=pathlib.Path('data.db'),
                    nargs='?', help='Database file')
scrape_p = subp.add_parser('scrape', help='Query each Elasticsearch server and retrieve the names of each index')
scrape_p.add_argument('--database', type=pathlib.Path, default=pathlib.Path('data.db'),
                    help='Database file')
args = parser.parse_args()
if args.subparser_name == 'create':
    pass
elif args.subparser_name == 'scrape':
    pass

