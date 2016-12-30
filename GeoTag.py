import os
from os.path import join
import ExifToolWrapper


class PhotoDateGeoTag: 


	def __init__(self, name, date, lat, lon): 
		self.name = name
		self.date = date
		self.lat = lat
		self.lon = lon

	def __repr__(self):
		return "PhotoDateGeoTag()"

	def __str__(self):
		return "%s, %s, %s, %s" % (self.name, self.date, self.lat, self.lon)



def CreateKMLFileForFiles():
	
	path = "K:\\images\\2016\\JPEG\\"

	dateGeoTagList = []
	
	with ExifToolWrapper.ExifToolWrapper() as e:
		for photo in os.listdir(path):    
			if photo.endswith(".jpg") or photo.endswith(".ARW"):
	
				metadata = e.execute('-n','-DateTimeOriginal','-GPSLatitude','-GPSLatitudeRef','-GPSLongitude','-GPSLongitudeRef', join(path, photo))
				metadata = metadata.split("\n")
				
				name = photo
				date = metadata[0][34:44],metadata[0][45:53]
				lat = (metadata[1].split(":")[1])
				lon = (metadata[3].split(":")[1])

				if len(lat)>1:
					dateGeoTagList.append(PhotoDateGeoTag(name,date,float(lat),float(lon)))


	
	dateGeoTagList.sort(key=lambda x : x.name, reverse=False)

	import simplekml
	
	kml = simplekml.Kml(name="PhotoTour")

	tagcounter = 0
	linecounter = 0
	previoustag = None
	
	for tag in dateGeoTagList:


		point = kml.newpoint(name=tag.name, coords=[(tag.lon,tag.lat)])
		point.timestamp.when = tag.date[0]

		if not previoustag is None:
			if previoustag.lat != tag.lat and previoustag.lon != tag.lon:

				linestring = kml.newlinestring(name="L")
				linestring.coords = [(previoustag.lon,previoustag.lat), (tag.lon,tag.lat)]
				linestring.altitudemode = simplekml.AltitudeMode.relativetoground
				
				linecounter += 1


		tagcounter += 1
		previoustag = tag

	kml.save("PhotoTour2.kml")
	print "Tags %d" % tagcounter
	print "Lines %d" % linecounter




import time
start = time.clock()

CreateKMLFileForFiles()

end = time.clock()
print "Finsihed running in:"
seconds = end - start
m, s = divmod(seconds,60)
h, m = divmod(m, 60)
print "%d:%02d:%d" % (h,m,s)

