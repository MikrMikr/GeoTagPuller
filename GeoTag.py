import os, sys, getopt
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



def CreateKMLFileForFiles(inFolder, outFile=None, recurse=False):
	
	dateGeoTagList = []
	
	if outFile is None:
		outFile=os.path.realpath(os.path.join(sys.path[0], "PhotoTour2.kml"))
	
	
	with ExifToolWrapper.ExifToolWrapper() as e:
	
		
		for root,dirList,fileList in os.walk(inFolder):
			for f in fileList:
				if f.endswith(".jpg") or f.endswith(".ARW"):
		
					metadata = e.execute('-n','-DateTimeOriginal','-GPSLatitude','-GPSLatitudeRef','-GPSLongitude','-GPSLongitudeRef', join(root, f))
					metadata = metadata.split("\n")
					
					name = f
					date = metadata[0][34:44],metadata[0][45:53]
					lat = (metadata[1].split(":")[1])
					lon = (metadata[3].split(":")[1])
	
					if len(lat)>1:
						dateGeoTagList.append(PhotoDateGeoTag(name,date,float(lat),float(lon)))

			if not recurse:
				break
	
	
	dateGeoTagList.sort(key=lambda x : x.name, reverse=False)

	
	import simplekml
	
	kml = simplekml.Kml(name=os.path.splitext(os.path.basename(outFile))[0])

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

	kml.save(outFile)
	print "Saved to %s" %outFile
	print "Tags %d" % tagcounter
	print "Lines %d" % linecounter



	
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "i:or", ["inFolder=", "outFile"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		#usage()
		sys.exit(2)
	outFile = None
	inFolder = None
	recurse = False
	for o, a in opts:
		if o == "-r":
			recurse = True
		elif o in ("-i", "--inFolder"):
			inFolder = a
		elif o in ("-o", "--outFile"):
			outFile = a
		else:
			assert False, "unhandled option"
	
	
	
	
	import time
	start = time.clock()
	
	CreateKMLFileForFiles(inFolder, outFile, recurse)
	
	end = time.clock()

	seconds = end - start
	m, s = divmod(seconds,60)
	h, m = divmod(m, 60)
	print " Finsihed running in: %d:%02d:%d" % (h,m,s)

	
if __name__ == "__main__":
    main()
