#+STARTUP: showall

#+TITLE:     Video 14: python part 7 - code reuse
#+AUTHOR:    Kurt Schwehr
#+EMAIL:     schwehr@ccom.unh.edu
#+DATE:      <2011-10-16 Sun>
#+DESCRIPTION: Marine Research Data Manipulation and Practices
#+KEYWORDS: ipython matplotlib
#+LANGUAGE:  en
#+OPTIONS:   H:3 num:nil toc:t \n:nil @:t ::t |:t ^:t -:t f:t *:t <:t
#+OPTIONS:   TeX:t LaTeX:nil skip:t d:nil todo:t pri:nil tags:not-in-toc
#+INFOJS_OPT: view:nil toc:nil ltoc:t mouse:underline buttons:0 path:http://orgmode.org/org-info.js
#+LINK_HOME: http://vislab-ccom.unh.edu/~schwehr/Classes/2011/esci895-researchtools/


* Introduction

This video covers cleaning up the code from video 13 into the beginnings of a proper module

* Here is what we had before

#+BEGIN_SRC python
#!/usr/bin/env python

def load_gga(filename):
    'parse NMEA GGA GPS positions'

    x_list = [ ]
    y_list = [ ]
    
    for line_num, line in enumerate(open(filename)):
        if 'GGA' not in line:
            continue
        fields = line.split(',')
        y = int(fields[2][:2]) + float(fields[2][2:])/60.
        if fields[3] == 'S':
            y = -y
        x = int(fields[4][:3]) + float(fields[4][3:]) / 60.
        if fields[5] == 'W':
            x = -x

        x_list.append(x)
        y_list.append(y)

    return x_list, y_list
#+END_SRC

* What might we want to do to make this more reusable?

- put it in a nmea.py file
- Handle just one line in a function
- return a dictionary of values
- have a class that can handle a file
- add support for all the message types
- add some tests
- documentation
- command line

* Getting the data

My normal log files have extra metadata on the end.  Let's start with
a file that does not include this metadata.

#+BEGIN_SRC sh
wget http://vislab-ccom.unh.edu/~schwehr/Classes/2011/esci895-researchtools/examples/nmea.log.bz2
bunzip2 nmea.log.bz2
#+END_SRC

* Final code

#+BEGIN_SRC python
'''
nmea.py - Parse NMEA ascii messages from GPS and other devices
'''


#test_gga = '$GPGGA,000000,4308.1250,N,07056.3750,W,2,9,1.1,35.7,M,,,,*04'
test_gga = '$GPGGA,001559,4308.1255,N,07056.3761,W,2,9,1.0,36.6,M,,,,*08'

def gga(line):
    if 'GGA' not in line:
        return None
    results = { }
    
    results['talker'] = line[1:3]
    results['msg'] = 'GGA'

    fields = line.split(',')

    results['hr'] = int(fields[1][:2])
    results['min'] = int(fields[1][2:4])
    results['sec'] = int(fields[1][4:])

    # Latitude
    y = int(fields[2][:2]) + float(fields[2][2:])/60
    if fields[3] == 'S':
        y = -y
    results['y'] = y

    # Longitude
    x = int(fields[4][:3]) + float(fields[4][3:]) / 60.
    if fields[5] == 'W':
        x = -x
    results['x'] = x

    results['z'] = float(fields[9])

    return results

test_vtg = '$GPVTG,271.9,T,287.3,M,0.1,N,0.2,K,D*26'

def vtg(line):
    'Parse course over ground and ground speed'
    if 'VTG' not in line:
        return None
    results = { }
    fields = line.split(',')

    results['heading_true'] = float(fields[1])
    results['heading_mag'] = float(fields[3])
    results['speed_kph'] = float(fields[7])
    
    return results

# Create a generator that will loop over a file
def parse_nmea_file(filename):
    for line in open(filename):
        if 'GGA' in line:
            yield gga(line)
        if 'VTG' in line:
            yield vtg(line)

def load_ggas(filename):
    x = [ ]
    y = [ ]
    for line in open(filename):
        if 'GGA' in line:
            msg = gga(line)
            x.append(msg['x'])
            y.append(msg['y'])
    return x,y
#+END_SRC

