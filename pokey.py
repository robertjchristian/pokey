#########################################################
#
# Pokey Test Application
#
# robc
#
#########################################################

import sys

#########################################################
# Test version compatibility
#########################################################
#if sys.version_info < (2, 6, 6) or sys.version_info >= (3, 0):
#  print( "\nMust be run with Python version v such that 2.6.6<=v<3.\n")
#  sys.exit(1)

#########################################################
# Test for requests module (only non-native lib)
#########################################################
try:
  import requests
except ImportError:
  print( "\nMust have requests module installed.  Run setup.sh for prerequisites.\n")
  sys.exit(1)

#########################################################
# Additional imports
#########################################################
import argparse, os, time
from subprocess import call

#########################################################
# Prep test metadata and assertion objects
#########################################################
def prep_test_data(base_url, input_folder):
    # determine url
    with open (input_folder + "/url", "r") as url_file:      
      url=url_file.readline().strip() # assumed on first line
      if not url.startswith("http"): url = base_url + url # handle relative versus absolute url 
      
    # obtain headers as dictionary, *defaulting* content-type since 
    # some http/app servers will fail with a 500 if it does not exist
    headers = { 'content-type': 'text/xml' }
    try:
      with open (input_folder + "/headers", "r") as headers_file:      
        for line in headers_file.readlines():
          if len(line.strip()) == 0: continue # ignore blank lines
          if line.startswith("content-length"): continue # ignore user-specified content-length
          h = line.strip().split(":")        
          headers[h[0]] = h[1]
    except IOError as e:
      pass # some connections don't have headers
    
    # fetch request_body as bytes from payload file
    try:
      with open(input_folder + "/payload",'rb') as payload_file:
        request_body = payload_file.read()
    except IOError as e:
      request_body = None

    # fetch expected response message
    try:
      with open(input_folder + "/expected_response_message",'r') as expected_response_message_file:
        expected_response_message = expected_response_message_file.readline().strip()
    except IOError as e:
        expected_response_message = "200 OK" # Assume positive case

    # fetch expected response message
    expected_response_body = None
    try:
      with open(input_folder + "/expected_response_body",'r') as expected_response_body_file:
        expected_response_body = expected_response_body_file.read()
    except IOError as e:
        pass

    # return test input data
    return url, headers, request_body, expected_response_message, expected_response_body
    
#########################################################
# Parse command line args for base url and base test
# folder
#########################################################
def parse_args():
  parser = argparse.ArgumentParser(description='Pokey is a simple to use HTTP Test Utility')
  parser.add_argument('--baseurl', action="store", type=str, help="Base URL prefixed to relative urls.")
  parser.add_argument('--path', action="store", default="./tests", type=str, help="Folder containing tests.")
  parse_result = parser.parse_args()
  return parse_result.baseurl, parse_result.path

#########################################################
# Entry point
#########################################################

# keep track of overall test time
overall_elapsed = 0

# get args
base_url, path = parse_args()

failed = False
totalfailed = 0

# get list of test folders (folders in path containing at least an url file)
testfolders = []
for root, dirnames, filenames in os.walk(path):
  try: 
    with open (os.path.join(root, "url"), "r"): 
      testfolders.append(root)
  except IOError as e: 
    pass # non-test directory
  
# for each subfolder of the base test path, run the test
for input_folder in testfolders:

  print( "\n-----------------------------------------------\nInspecting: " + input_folder)

  # get test data
  url, headers, request_body, expected_response_message, expected_response_body = prep_test_data(base_url, input_folder)

  # run the test
  start_time = time.time()
  # TODO verify should be True by default, and allow override via command line parameter

  if request_body is None:
    r = requests.get(url, headers=headers, verify=False)  
  else:
    r = requests.post(url, data=request_body, headers=headers, verify=False)  

  time_elapsed = time.time() - start_time
  overall_elapsed += time_elapsed
  response_message = str(r.status_code) + " " + r.reason

  print( "URL: " + url)
  print( "Seconds elapsed: " + '%s' % float('%f' % (time_elapsed)))
  print( "Response Expected: [" + expected_response_message + "]")
  print( "Response Actual:   [" + response_message + "]")

  # test expected response message assertion
  if not expected_response_message.strip() == response_message.strip():
    print( "!! Failed expected response message assertion.")
    failed = True

  # test expected response body assertion
  if not expected_response_message == None and not expected_response_message == response_message:
    print( "!! Failed expected response body assertion.")
    failed = True

  if failed:
    print( "Test failed.\n-----------------------------------------------")
    totalfailed = totalfailed + 1
    # TODO check for a fast fail flag 
    # helpful if using for TDD or continuous integration
  else:
    print( "Test passed.\n-----------------------------------------------")
    


print( "\n***********************************************")
if failed:
  print( str(totalfailed) + " tests failed.")
else:
  print( "All tests passed!")

print( "Overall seconds elapsed: " + '%s'  % float('%f' % (overall_elapsed)))
print( "***********************************************")
print( "\nDone.\n")
