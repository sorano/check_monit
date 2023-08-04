#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 NETWAYS GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import argparse
import os
from xml.etree import ElementTree

import requests


script_name = os.path.basename(sys.argv[0])

icinga_status = {
  0: 'OK',
  1: 'WARNING',
  2: 'CRITICAL',
  3: 'UNKNOWN'
}

def print_output(status, count_ok, count_all, items):
    print('{0} {1}: Services {2}/{3}'.format(
      script_name,
      icinga_status[status],
      count_ok,
      count_all
    ))

    if len(items):
      print("")
      for item in items:
        print('### {0}'.format(item['name']))
        print(item['output'])
        print("")

def service_output(service_type, element):
  if service_type == 0:
    block = float(element.findall('block/percent')[0].text)
    inode = float(element.findall('inode/percent')[0].text)
    return 'user={0}%;inodes={1}%'.format(block, inode)

  if service_type == 5:
    output = []

    load1 = float(element.findall('system/load/avg01')[0].text)
    load5 = float(element.findall('system/load/avg05')[0].text)
    load15 = float(element.findall('system/load/avg15')[0].text)
    output.append('load={0},{1},{2}'.format(load1, load5, load15))

    user = float(element.findall('system/cpu/user')[0].text)
    system = float(element.findall('system/cpu/system')[0].text)
    nice = float(element.findall('system/cpu/nice')[0].text)
    hardirq = float(element.findall('system/cpu/hardirq')[0].text)
    output.append('user={0}%;system={1}%;nice={2}%;hardirq={3}%'.format(user, system, nice, hardirq))

    memory = float(element.findall('system/memory/percent')[0].text)
    output.append('memory={0}%'.format(memory))

    return ';'.join(output)

  if service_type == 7:
    # status = float(element.findall('program/status')[0].text)
    return element.findall('program/output')[0].text

  return 'Service (type={0}) not implemented'.format(service_type)


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('-H', '--host', dest='host',
                    required=True,
                    type=str,
                    help='Monit hostname')

  parser.add_argument('-p', '--port', dest='port',
                  default=2812,
                  type=int,
                  help='Port')

  parser.add_argument('-U', '--user', dest='user',
                  required=True,
                  type=str,
                  help='HTTP username')

  parser.add_argument('-P', '--pass', dest='password',
                  required=True,
                  type=str,
                  help='HTTP password')

  args = parser.parse_args()

  url = 'http://{0}:{1}/_status?format=xml'.format(args.host, args.port)

  try:
    r = requests.get(url, auth=(args.user, args.password), timeout=5)
  except Exception as e: # pylint: disable=broad-except
    print('{0} UNKNOWN: Socket error={1}'.format(script_name, str(e)))
    return 3

  status_code = r.status_code

  if status_code != 200:
    print('{0} UNKNOWN: HTTP status={1}'.format(script_name, status_code))
    return 3

  try:
    tree = ElementTree.fromstring(r.content)
  except Exception as e: # pylint: disable=broad-except
    print('{0} UNKNOWN: XML error={1}'.format(script_name, str(e)))
    return 3

  items = []
  services = tree.findall('service')

  count_all = 0
  count_ok = 0

  for service in services:
    monitor = int(service.find('monitor').text)
    if monitor == 1:
      status = int(service.find('status').text)
      if status == 0:
        count_ok += 1

      count_all += 1

      items.append({
        "name": service.find('name').text,
        "status": status,
        "output": service_output(int(service.get('type')), service)
      })

  status = 0

  if count_ok < count_all:
    status = 2

  if count_ok == 0:
    status = 2

  print_output(status, count_ok, count_all, items)

  return status

if __name__ == '__main__':
  sys.exit(main())
