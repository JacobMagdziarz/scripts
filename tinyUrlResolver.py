#!/usr/bin/python

import sys 
import getopt 
import itertools
import requests
import signal

def signal_handler(signal, frame):
    print('Caught interrupt')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main(argv):
  charSet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']
  urlLength=8

  try:
      opts, args, = getopt.getopt(argv,"hl:u:")
  except getopt.Getopterror:
    print 'tinyUrlResolver.py -l <urlLength> -u <url>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'tinyUrlResolver.py -l <urlLength> -u <url>'
      sys.exit()
    if opt == '-l':
      urlLength = int(arg)
    if opt == '-u':
      url = arg
      unshortenUrl(url)
      sys.exit(1)
  resolve(charSet, urlLength)

def resolve(charSet, urlLength):
  for subString in itertools.combinations(charSet, urlLength):
    unshortenUrl('https://tinyurl.com/' + ''.join(subString))

def unshortenUrl(url):
    try:
        resolved = requests.head(url, allow_redirects=True).url
        if url != resolved:
          print url + " --> " + resolved
        else:
          print url + " [Unused]"
    except:
        try:
            headers = requests.head(url).headers
            print url + " --> " + headers.get('Location') + " [Unresolvable]"
        except:
            print url + " [Unknown error]"

if __name__ == '__main__':
  main(sys.argv[1:])
