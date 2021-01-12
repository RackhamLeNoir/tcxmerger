class TrackPoint:
  def __init__(self):
    self.distance = 0
    self.cadence = 0
    self.heartRate = 0
    self.speed = 0
    self.watts = 0
    self.latitude = 0
    self.longitude = 0
    self.altitude = 0

  def setDistance(self, distance):
    self.distance = distance

  def setCadence(self, cadence):
    self.cadence = cadence

  def setHeartRate(self, heartRate):
    self.heartRate = heartRate
  
  def setSpeed(self, speed):
    self.speed = speed

  def setWatts(self, watts):
    self.watts = watts

  def setLocation(self, latitude, longitude):
    self.latitude = latitude
    self.longitude = longitude

  def setAltitude(self, altitude):
    self.altitude = altitude
