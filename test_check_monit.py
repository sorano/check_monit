#!/usr/bin/env python3

import unittest
import unittest.mock as mock
import sys

sys.path.append('..')


from check_monit import main
from check_monit import commandline
from check_monit import print_output


class CLITesting(unittest.TestCase):

    def test_commandline(self):
        actual = commandline(['-H', 'localhost', '-P', 'password', '-U', 'user'])
        self.assertEqual(actual.host, 'localhost')
        self.assertEqual(actual.port, 2812)
        self.assertEqual(actual.user, 'user')
        self.assertEqual(actual.password, 'password')

class UtilTesting(unittest.TestCase):

    @mock.patch('builtins.print')
    def test_return_plugin(self, mock_print):
        actual = print_output(1, 2, 3, [{'name': 'foo', 'output': 'bar'}])

        calls = [mock.call('check_monit WARNING: Services 2/3'),
                 mock.call(''),
                 mock.call('### foo'),
                 mock.call('bar'),
                 mock.call('')]

        mock_print.assert_has_calls(calls)
