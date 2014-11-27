#!/usr/bin/python
#------------------------------------------
#
#    A script to periodically download a
#    Tor relay's descriptor and write it to
#    the disk
#
# Author : Luiz Kill
# Date   : 21/11/2014
#
# http://lzkill.com
#
#------------------------------------------

import os
import sys
import time
from stem.descriptor import DocumentHandler
from stem.descriptor.remote import DescriptorDownloader 

DOWNLOAD_DELAY = 60.0
FINGERPRINT = [""]

PATHNAME="/var/lib/rpimonitor/stat/tor_desc"

def main():
	try:
		dump = open(PATHNAME,"wb")
		
		downloader = DescriptorDownloader()

		while True:
			query = downloader.get_server_descriptors(fingerprints=FINGERPRINT)

			for desc in query.run():
				dump.seek(0)
				dump.write("Nickname " + str(desc.nickname)+"\n")
				dump.write("Fingerprint " + "".join(str(desc.fingerprint).split())+"\n")
				dump.write("Published " + str(desc.published)+"\n")
				dump.write("Address " + str(desc.address)+"\n")
				dump.write("Version " + str(desc.tor_version)+"\n")
				dump.write("Uptime " + str(desc.uptime)+"\n")
				dump.write("Average_Bandwidth " + str(desc.average_bandwidth)+"\n")
				dump.write("Burst_Bandwidth " + str(desc.burst_bandwidth)+"\n")
				dump.write("Observed_Bandwidth " + str(desc.observed_bandwidth)+"\n")
				dump.write("Hibernating " + str(desc.hibernating)+"\n")

			time.sleep(DOWNLOAD_DELAY)

	except Exception as exc:
		print 'Unable to retrieve the server descriptors: %s' % exc


if __name__ == '__main__':
	main()

