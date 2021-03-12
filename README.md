# check_monit

## Usage

```
./check_monit.py -H hostname -U 'user' -P 'password'
check_monit.py OK: Services 3/3

### xxxx.netways.de
load=0.33,0.29,0.26;user=0.8%;system=0.7%;nice=0.0%;hardirq=0.2%;memory=8.3%

### RootFs
user=1.1%;inodes=0.3%

### gmirror-status
Name    Status  Components
mirror/OPNsense  COMPLETE  ada0 (ACTIVE)
                           ada1 (ACTIVE)

```

## License

***Copyright 2021 NETWAYS GmbH***

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
