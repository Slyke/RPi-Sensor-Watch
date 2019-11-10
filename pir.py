import time
import datetime
import os
import requests
import sys
from gpiozero import MotionSensor

pirGpioPort = int(os.environ.get('GPIO_PORT', 17));
httpUrl = os.environ.get('HTTP_URL', '');
httpAuth = os.environ.get('HTTP_AUTH', "");
httpDataInUrl = bool(os.environ.get('DATA_IN_QUERYSTRING', False));
httpMethod = os.environ.get('HTTP_METHOD', 'POST');

if (httpUrl == ''):
  print("Error: Env var 'HTTP_URL' is not set.");
  exit(1);

pir = MotionSensor(pirGpioPort);
print("[{} - {}]: Sending Requests To: {}".format(datetime.datetime.now(), time.time(), httpUrl))
print("[{} - {}]: Auth: {}".format(datetime.datetime.now(), time.time(), not(httpAuth == "")))
print("[{} - {}]: httpDataInUrl: {}".format(datetime.datetime.now(), time.time(), httpDataInUrl))
print("[{} - {}]: Request Method: {}".format(datetime.datetime.now(), time.time(), httpMethod))
print("[{} - {}]: GPIO: {}".format(datetime.datetime.now(), time.time(), pirGpioPort))
print("")
print("[{} - {}]: Motion Detector Activated".format(datetime.datetime.now(), time.time()))
print("")

motionDetected = False

def sendRequest(detectionState):
  jsonBody = { "motionState": detectionState }
  response = requests.post(url = httpUrl, json=jsonBody);

  print("Upload: {} - {}".format(response.status_code, response.content));

  #if (response.status_code == 200):
  #  print("Upload: {} - {}".format(response.status_code, response.content));
  #elif (response.status_code) == 404:
  #  print('Not Found.');

try:
  while True:
    time.sleep(0.01);
    # pir.wait_for_motion();
    if (pir.motion_detected and not motionDetected):
      motionDetected = True;
      print("[{} - {}]: Event: 'Motion detected', ".format(datetime.datetime.now(), time.time()), end = " ");
      sendRequest(True);
      time.sleep(0.5);
    elif (not pir.motion_detected and motionDetected):
      motionDetected = False
      # pir.wait_for_no_motion();
      print("[{} - {}]: Event: 'Motion detection end', ".format(datetime.datetime.now(), time.time()), end = " ");
      sendRequest(False);
      
    sys.stdout.flush();

except KeyboardInterrupt:
  pass
