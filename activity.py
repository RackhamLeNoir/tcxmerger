
import datetime

from trackpoint import *

class Activity:
  def __init__(self):
    self.trackPoints = {}
    self.startTime = datetime.datetime(9999, 1, 1)
    self.totalTime = 0.0
    self.maxHeartRate = 0
    self.maxSpeed = 0.0

  def setID(self, id):
    self.id = id
  
  def setStartTime(self, startTime):
    if (startTime > self.startTime):
      self.startTime = startTime

  def setTotalTime(self, totalTime):
    if (totalTime > self.totalTime):
      self.totalTime = totalTime
  
  def setDistance(self, distance):
    self.distance = distance
  
  def setMaxSpeed(self, maxSpeed):
    if maxSpeed > self.maxSpeed:
      self.maxSpeed = maxSpeed

  def setCadence(self, cadence):
    self.cadence = cadence

  def setCalories(self, calories):
    self.calories = calories

  def setAverageHeartRate(self, averageHeartRate):
    self.averageHeartRate = averageHeartRate

  def setMaxHeartRate(self, maxHeartRate):
    if maxHeartRate > self.maxHeartRate:
      self.maxHeartRate = maxHeartRate

  def setTrackPointHeartRate(self, timestamp, heartRate):
    try:
      self.trackPoints[timestamp].setHeartRate(heartRate)
    except KeyError:
      self.trackPoints[timestamp] = TrackPoint()
      self.trackPoints[timestamp].setHeartRate(heartRate)

  def setTrackPointDistance(self, timestamp, distance):
    try:
      self.trackPoints[timestamp].setDistance(distance)
    except KeyError:
      self.trackPoints[timestamp] = TrackPoint()
      self.trackPoints[timestamp].setDistance(distance)

  def setTrackPointCadence(self, timestamp, cadence):
    try:
      self.trackPoints[timestamp].setCadence(cadence)
    except KeyError:
      self.trackPoints[timestamp] = TrackPoint()
      self.trackPoints[timestamp].setCadence(cadence)

  def setTrackPointSpeed(self, timestamp, speed):
    try:
      self.trackPoints[timestamp].setSpeed(speed)
    except KeyError:
      self.trackPoints[timestamp] = TrackPoint()
      self.trackPoints[timestamp].setSpeed(speed)

  def setTrackPointWatts(self, timestamp, watts):
    try:
      self.trackPoints[timestamp].setWatts(watts)
    except KeyError:
      self.trackPoints[timestamp] = TrackPoint()
      self.trackPoints[timestamp].setWatts(watts)

  def setTrackPointLocation(self, timestamp, latitude, longitude):
    try:
      self.trackPoints[timestamp].setLocation(latitude, longitude)
    except KeyError:
      self.trackPoints[timestamp] = TrackPoint()
      self.trackPoints[timestamp].setLocation(latitude, longitude)

  def setTrackPointAltitude(self, timestamp, altitude):
    try:
      self.trackPoints[timestamp].setAltitude(altitude)
    except KeyError:
      self.trackPoints[timestamp] = TrackPoint()
      self.trackPoints[timestamp].setAltitude(altitude)

  def sort(self):
    sorted(self.trackPoints)
