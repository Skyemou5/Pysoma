# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import tempfile
import unittest

import dumpenv
import subx


class MyTestCase(unittest.TestCase):

    def test_dumpenv(self):
        os.environ['umlaut_latin1'] = 'umlaut ü'.encode('latin1')
        os.environ['umlaut_utf8'] = 'umlaut ü'.encode('utf8')
        output_directory = dumpenv.get_output_directory()
        out_dir = dumpenv.create_data_and_dump_it(output_directory)

        # EXTEND README IF A NEW FILE GETS CREATED
        self.assertEqual(['PATH', 'PYTHONPATH', 'locale_module', 'localeconv','os', 'os_environ', 'pip_freeze',
                          'platform', 'site', 'sys', 'sys_path'],
                         sorted(os.listdir(out_dir)))

    def test_normalize_line__magic(self):
        os.environ['env_name_x'] = '/home/bar'
        self.assertEqual(
            '${env_name_x}/y',
            dumpenv.normalize_line__magic('/home/bar/y', 'env_name_x'))

    def test_output_directory_argument_parsing__no_arg(self):
        assert not 'DUMPENV_OUTPUT_DIRECTORY' in os.environ, 'your environment is not clean. DUMPENV_OUTPUT_DIRECTORY is set'
        self.assertIn('Dumped environment to directory /tmp/dumpenv_', subx.call(['dumpenv']).stdout)

    def test_output_directory_argument_parsing__short_arg(self):
        out_dir = os.path.join(tempfile.mktemp())
        self.assertIn('Dumped environment to directory %s' % out_dir, subx.call(['dumpenv', '-o', out_dir]).stdout)

    def test_output_directory_argument_parsing__environment_variable(self):
        out_dir = os.path.join(tempfile.mktemp())
        env = dict(os.environ)
        env['DUMPENV_OUTPUT_DIRECTORY'] = out_dir
        self.assertIn('Dumped environment to directory %s' % out_dir, subx.call(['dumpenv'], env=env).stdout)

    def test_normalize_line__object_at_memory(self):
        self.assertEqual('meta_path: [<six._SixMetaPathImporter object at 0x...>]', dumpenv.normalize_line('meta_path: [<six._SixMetaPathImporter object at 0x7f8840eb0d10>]'))

    def test_localeconv_module(self):
        localeconv = '\n'.join(dumpenv.localeconv())
        self.assertIn('currency_symbol:', localeconv)
        self.assertIn('decimal_point:', localeconv)

    def test_locale_module(self):
        locale_output = '\n'.join(dumpenv.locale_module())
        self.assertIn('getdefaultlocale():', locale_output)
