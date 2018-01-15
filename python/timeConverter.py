def timeConverter( strTime ):
	# int seconds = timeConverter( string strTime )
	# Converts HHMMSS input string to integer seconds
	#
	length = len(strTime)
	if length > 6:
		seconds = 0
	else:
		h = int(strTime[0:2])
		m = int(strTime[2:4])
		s = int(strTime[4:6])

		seconds = s + m*60 + h*3600
	return seconds
