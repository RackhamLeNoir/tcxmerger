#from datetime import datetime
#datetime.datetime(year, month, day, hour=0, minute=0, second=0)
from xml.dom import minidom
import xml.etree.ElementTree as et

from datetime import datetime

class TCXParser:

  @staticmethod
  def loadGarmin(activity, filename):
    mydoc = minidom.parse(filename)
    activity.setID(mydoc.getElementsByTagName('Id')[0].firstChild.data)
    strStartTime = mydoc.getElementsByTagName('Lap')[0].attributes['StartTime'].value
    starttime = datetime.strptime(strStartTime, "%Y-%m-%dT%H:%M:%S.000Z")
    activity.setStartTime(starttime)
    activity.setTotalTime(float(mydoc.getElementsByTagName('TotalTimeSeconds')[0].firstChild.data))
    activity.setCalories(int(mydoc.getElementsByTagName('Calories')[0].firstChild.data))
    activity.setAverageHeartRate(int(mydoc.getElementsByTagName('AverageHeartRateBpm')[0].getElementsByTagName('Value')[0].firstChild.data))
    activity.setMaxHeartRate(int(mydoc.getElementsByTagName('MaximumHeartRateBpm')[0].getElementsByTagName('Value')[0].firstChild.data))

    trackPoints = mydoc.getElementsByTagName('Trackpoint')
    for tp in trackPoints:
      timestamp = int(datetime.strptime(tp.getElementsByTagName('Time')[0].firstChild.data, "%Y-%m-%dT%H:%M:%S.000Z").timestamp())
      heartRate = int(tp.getElementsByTagName('HeartRateBpm')[0].getElementsByTagName('Value')[0].firstChild.data)
      activity.setTrackPointHeartRate(timestamp, heartRate)

  @staticmethod
  def loadTacx(activity, filename):
    mydoc = minidom.parse(filename)
#    activity.setID(mydoc.getElementsByTagName('Id')[0].data)
    strStartTime = mydoc.getElementsByTagName('Lap')[0].attributes['StartTime'].value
    activity.setStartTime(datetime.strptime(strStartTime, "%Y-%m-%dT%H:%M:%S.000Z"))
    activity.setTotalTime(float(mydoc.getElementsByTagName('TotalTimeSeconds')[0].firstChild.data))
    activity.setDistance(float(mydoc.getElementsByTagName('DistanceMeters')[0].firstChild.data))
    activity.setCadence(int(mydoc.getElementsByTagName('Cadence')[0].firstChild.data))
    activity.setMaxSpeed(float(mydoc.getElementsByTagName('MaximumSpeed')[0].firstChild.data))

    trackPoints = mydoc.getElementsByTagName('Trackpoint')
    for tp in trackPoints:
      timestamp = int(datetime.strptime(tp.getElementsByTagName('Time')[0].firstChild.data, "%Y-%m-%dT%H:%M:%S.000Z").timestamp())
      distance = float(tp.getElementsByTagName('DistanceMeters')[0].firstChild.data)
      cadence = int(tp.getElementsByTagName('Cadence')[0].firstChild.data)
      speed = float(tp.getElementsByTagName('ns3:Speed')[0].firstChild.data)
      watts = int(tp.getElementsByTagName('ns3:Watts')[0].firstChild.data)
      activity.setTrackPointDistance(timestamp, distance)
      activity.setTrackPointCadence(timestamp, cadence)
      activity.setTrackPointSpeed(timestamp, speed)
      activity.setTrackPointWatts(timestamp, watts)

  @staticmethod
  def writeTCX(activity, filename):
    data = et.Element('TrainingCenterDatabase')
    data.set('xsi:schemaLocation', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd')
    data.set('xmlns:ns5', 'http://www.garmin.com/xmlschemas/ActivityGoals/v1')
    data.set('xmlns:ns3', 'http://www.garmin.com/xmlschemas/ActivityExtension/v2')
    data.set('xmlns:ns2', 'http://www.garmin.com/xmlschemas/UserProfile/v2')
    data.set('xmlns', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
    data.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    data.set('xmlns:ns4', 'http://www.garmin.com/xmlschemas/ProfileExtension/v1')

    dataactivities = et.SubElement(data, 'Activities')
    dataactivity = et.SubElement(dataactivities, 'Activity')
    dataactivity.set('Sport', "Biking")
    dataid = et.SubElement(dataactivity, 'Id')
    dataid.text = activity.id
    datalap= et.SubElement(dataactivity, 'Lap')

    datatotaltime = et.SubElement(datalap, 'TotalTimeSeconds')
    datatotaltime.text = f"{activity.totalTime:.1f}"
    datadistance = et.SubElement(datalap, 'DistanceMeters')
    datadistance.text = f"{activity.distance:.2f}"
    datamaxspeed = et.SubElement(datalap, 'MaximumSpeed')
    datamaxspeed.text = f"{activity.maxSpeed:.14f}"
    datacalories = et.SubElement(datalap, 'Calories')
    datacalories.text = str(activity.calories)
    dataaverageheartrate = et.SubElement(datalap, 'AverageHeartRateBpm')
    dataaverageheartratevalue = et.SubElement(dataaverageheartrate, 'Value')
    dataaverageheartratevalue.text = str(activity.averageHeartRate)
    datamaxheartrate = et.SubElement(datalap, 'MaximumHeartRateBpm')
    datamaxheartratevalue = et.SubElement(datamaxheartrate, 'Value')
    datamaxheartratevalue.text = str(activity.maxHeartRate)
    dataintensity = et.SubElement(datalap, 'Intensity')
    dataintensity.text = 'Active'
    datacadence = et.SubElement(datalap, 'Cadence')
    datacadence.text = str(activity.cadence)
    datatriggermethod = et.SubElement(datalap, 'TriggerMethod')
    datatriggermethod.text = 'Manual'
    datatrack = et.SubElement(datalap, 'Track')

    timestamps = sorted(activity.trackPoints)
    lastDistance = 0.0
    lastCadence = 0
    lastHeartRate = 0
    lastSpeed = 0
    lastWatts = 0
    for timestamp in timestamps:
      tp = activity.trackPoints[timestamp]
      datatp = et.SubElement(datatrack, 'Trackpoint')
      datatptime = et.SubElement(datatp, 'Time')
      datatptime.text = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S.000Z")
      datatpdistance = et.SubElement(datatp, 'DistanceMeters')
      if tp.distance > 0.0:
        datatpdistance.text = f"{tp.distance:.12f}"
        lastDistance = tp.distance
      else:
        datatpdistance.text = f"{lastDistance:.12f}"
      datatpcadence = et.SubElement(datatp, 'Cadence')
      if tp.cadence > 0:
        datatpcadence.text = str(tp.cadence)
        lastCadence = tp.cadence
      else:
        datatpcadence.text = str(lastCadence)
      datatpheartRate = et.SubElement(datatp, 'HeartRateBpm')
      datatpheartratevalue = et.SubElement(datatpheartRate, 'Value')
      if tp.heartRate > 0:
        datatpheartratevalue.text = str(tp.heartRate)
        lastHeartRate = tp.heartRate
      else:
        datatpheartratevalue.text = str(lastHeartRate)
      datatpextensions = et.SubElement(datatp, 'Extensions')
      datatpextensionstpx = et.SubElement(datatpextensions, 'ns3:TPX')
      datatpspeed = et.SubElement(datatpextensionstpx, 'ns3:Speed')
      if tp.speed > 0:  
        datatpspeed.text = f"{tp.speed:.15f}"
        lastSpeed = tp.speed
      else:
        datatpspeed.text = f"{lastSpeed:.15f}"
      datatpwatts = et.SubElement(datatpextensionstpx, 'ns3:Watts')
      if tp.watts > 0:
        datatpwatts.text = str(tp.watts)
        lastWatts = tp.watts
      else:
        datatpwatts.text = str(lastWatts)

    datacreator = et.SubElement(dataactivity, 'Creator')
    datacreator.set('xsi:type', 'Device_t')
    datacreatorname = et.SubElement(datacreator, 'Name')
    datacreatorname.text = 'Tacx Training App (MacOS)'
    datacreatorunitid = et.SubElement(datacreator, 'UnitId')
    datacreatorproductid = et.SubElement(datacreator, 'ProductID')
    datacreatorproductid.text = '534'
    datacreatorversion = et.SubElement(datacreator, 'Version')
    datacreatorversionmajor = et.SubElement(datacreatorversion, 'VersionMajor')
    datacreatorversionmajor.text = '1'
    datacreatorversionminor = et.SubElement(datacreatorversion, 'VersionMinor')
    datacreatorversionminor.text = '22'
    datacreatorbuildmajor = et.SubElement(datacreatorversion, 'BuildMajor')
    datacreatorbuildmajor.text = '0'
    datacreatorbuildminor = et.SubElement(datacreatorversion, 'BuildMinor')
    datacreatorbuildminor.text = '0'

    dataauthor = et.SubElement(data, 'Author')
    dataauthor.set('xsi:type', 'Application_t')
    dataauthorname = et.SubElement(dataauthor, 'Name')
    dataauthorname.text = 'Connect Api'
    dataauthorbuild = et.SubElement(dataauthor, 'Build')
    dataauthorversion = et.SubElement(dataauthorbuild, 'Version')
    dataauthorversionmajor = et.SubElement(dataauthorversion, 'VersionMajor')
    dataauthorversionmajor.text = '0'
    dataauthorversionminor = et.SubElement(dataauthorversion, 'VersionMinor')
    dataauthorversionminor.text = '0'
    dataauthorbuildmajor = et.SubElement(dataauthorversion, 'BuildMajor')
    dataauthorbuildmajor = '0'
    dataauthorbuildminor = et.SubElement(dataauthorversion, 'BuildMinor')
    dataauthorbuildminor = '0'
    dataauthorlangid = et.SubElement(dataauthor, 'LangID')
    dataauthorlangid.text = 'en'
    dataauthorpartnumber = et.SubElement(dataauthor, 'PartNumber')
    dataauthorpartnumber.text = '006-D2449-00'

    mydata = et.tostring(data)
    myfile = open(filename, 'wb')
    header = bytearray('<?xml version="1.0" encoding="UTF-8"?>', 'UTF8')
    myfile.write(header)
    myfile.write(mydata)
