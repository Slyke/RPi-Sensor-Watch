import time
import datetime
import os
import requests
import sys
from gpiozero import MotionSensor, LED

pirGpioPort = int(os.environ.get('GPIO_PORT', 17));
pirGpioPortLed = int(os.environ.get('GPIO_PORT_LED', 26));
httpUrl = os.environ.get('HTTP_URL', '');
httpAuthUsername = os.environ.get('HTTP_AUTH_USERNAME', "");
httpAuthPassword = os.environ.get('HTTP_AUTH_PASSWORD', "");
httpDataInUrl = bool(os.environ.get('DATA_IN_QUERYSTRING', False));
httpMethod = os.environ.get('HTTP_METHOD', 'POST');
stationId = os.environ.get('STATION_ID', 'DoorCam1');

if (httpUrl == ''):
  print("Error: Env var 'HTTP_URL' is not set.");
  exit(1);

pir = MotionSensor(pirGpioPort);
motionLed = LED(pirGpioPortLed);

print("[{} - {}]: Sending Requests To: {}".format(datetime.datetime.now(), time.time(), httpUrl))
print("[{} - {}]: Auth: {}".format(datetime.datetime.now(), time.time(), (not(httpAuthUsername == "") and not(httpAuthPassword == ""))))
print("[{} - {}]: httpDataInUrl: {}".format(datetime.datetime.now(), time.time(), httpDataInUrl))
print("[{} - {}]: Request Method: {}".format(datetime.datetime.now(), time.time(), httpMethod))
print("[{} - {}]: GPIO: {}".format(datetime.datetime.now(), time.time(), pirGpioPort))
print("[{} - {}]: LED: {}".format(datetime.datetime.now(), time.time(), pirGpioPortLed))
print("[{} - {}]: StationId: {}".format(datetime.datetime.now(), time.time(), stationId))
print("")
print("[{} - {}]: Motion Detector Activated".format(datetime.datetime.now(), time.time()))
print("")

motionDetected = False

def sendRequest(detectionState):
  jsonBody = { "motionState": detectionState, "stationId": stationId }
  response = requests.request(method = httpMethod, url = httpUrl, json=jsonBody, auth=(httpAuthUsername, httpAuthPassword));

  print("Upload: {} - {}".format(response.status_code, response.content));

try:
  while True:
    time.sleep(0.01);
    # pir.wait_for_motion();
    if (pir.motion_detected and not motionDetected):
      motionDetected = True;
      print("[{} - {}]: Event: 'Motion detected', ".format(datetime.datetime.now(), time.time()), end = " ");
      sendRequest(True);
      motionLed.on();
      time.sleep(0.5);
    elif (not pir.motion_detected and motionDetected):
      motionDetected = False
      # pir.wait_for_no_motion();
      print("[{} - {}]: Event: 'Motion detection end', ".format(datetime.datetime.now(), time.time()), end = " ");
      sendRequest(False);
      motionLed.off();

    sys.stdout.flush();

except KeyboardInterrupt:
  pass
