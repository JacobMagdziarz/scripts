#!/usr/local/bin/python

import requests, sys, getopt

def main(argv):
  urlList = ''
  url = ''
  path = '/'
  respCode = "200"

  try:
    opts, args, = getopt.getopt(argv,"hu:f:p:r:")
  except getopt.GetoptError():
    print 'checkResp.py -p <path> -r <respondeCode> -u <url> -f <urlList>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'checkResp.py -p <path> -r <responseCode> -u <url> -f <urlList>'
      sys.exit()
    if opt == '-p':
      path = arg
    if opt == '-r':
      respCode = arg
    if opt == '-u':
      url = arg
    if opt == '-f':
      urlList = arg
  if (url):
    print checkUrl(url, path, respCode)
  if (urlList):
    print checkUrlList(urlList, path, respCode)

def checkUrlList(urlList, path, respCode):
  return True

def checkUrl(url, path="/", respCode="200"):
  r = requests.head(url + path, verify = False)
  print respCode
  print r.status_code 
  return r.status_code == respCode

if __name__ == '__main__':
  main(sys.argv[1:])
 # respCode = 401
 # for i in open(urlList).readlines():


