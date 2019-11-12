import Adafruit_DHT
import os
import time
import requests
import datetime
import sys

pirGpioPort = int(os.environ.get('GPIO_PORT', 4));
httpUrl = os.environ.get('HTTP_URL', '');
httpAuthUsername = os.environ.get('HTTP_AUTH_USERNAME', "");
httpAuthPassword = os.environ.get('HTTP_AUTH_PASSWORD', "");
httpDataInUrl = bool(os.environ.get('DATA_IN_QUERYSTRING', False));
httpMethod = os.environ.get('HTTP_METHOD', 'POST');
dhtSensor = int(os.environ.get('DHT_SENSOR_TYPE', 22));
sensorPolling = int(os.environ.get('SENSOR_POLL_WAIT', 120));
stationId = os.environ.get('STATION_ID', 'DoorCam1');

# DHT_SENSOR = Adafruit_DHT.DHT22
DHT_SENSOR = dhtSensor

print("[{} - {}]: Sending Requests To: {}".format(datetime.datetime.now(), time.time(), httpUrl))
print("[{} - {}]: Auth: {}".format(datetime.datetime.now(), time.time(), (not(httpAuthUsername == "") and not(httpAuthPassword == ""))))
print("[{} - {}]: httpDataInUrl: {}".format(datetime.datetime.now(), time.time(), httpDataInUrl))
print("[{} - {}]: Request Method: {}".format(datetime.datetime.now(), time.time(), httpMethod))
print("[{} - {}]: GPIO: {}".format(datetime.datetime.now(), time.time(), pirGpioPort))
print("[{} - {}]: GPIO: {}".format(datetime.datetime.now(), time.time(), pirGpioPort))
print("[{} - {}]: Sensor Polling Rate: every {} seconds".format(datetime.datetime.now(), time.time(), sensorPolling))
print("[{} - {}]: DHT Sensor Type: {}".format(datetime.datetime.now(), time.time(), dhtSensor))
print("[{} - {}]: StationId: {}".format(datetime.datetime.now(), time.time(), stationId))
print("")
print("[{} - {}]: DHT Sensor Polling Activated".format(datetime.datetime.now(), time.time()))
print("")

def sendRequest(humidity, temperature, failure):
  jsonBody = { "temperature": temperature, "humidity": humidity, "stationId": stationId, "sensorFailure": failure }
  response = requests.request(method = httpMethod, url = httpUrl, json=jsonBody, auth=(httpAuthUsername, httpAuthPassword));

  print("Upload: {} - {}".format(response.status_code, response.content));

while True:
  humidity, temperature = Adafruit_DHT.read_retry(dhtSensor, pirGpioPort)

  if humidity is not None and temperature is not None:
    print("[{0} - {1}]: Event: 'Sensor Poll: Temperature = {2:0.1f}*C  Humidity = {3:0.1f}%', ".format(datetime.datetime.now(), time.time(), temperature, humidity), end = " ");
    sendRequest(humidity, temperature, False);
  else:
    print("[{} - {}]: Event: 'Sensor Poll: Failed to retrieve data from humidity sensor.', ", end = " ")
    sendRequest(0, 0, True);

  sys.stdout.flush();
  time.sleep(sensorPolling);

