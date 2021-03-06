#!/usr/bin/env python

""" aadb.py: Advanced Adb

Written by: Patrick Farrell

This program allow the user to manage multiple Android adb devices
from the command line.  Please see the README for documentation.


The MIT License (MIT)

Copyright (c) 2015 Patrick Farrell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import sys
import time

import subprocess

class AdvancedAdb():

	def __init__(self):
		self.devices = []
		self.findDevices()

	# Determine the Android devices that are present
	# TODO: Store more that is available from the output
	def findDevices(self):

		firstLine = True
		p = subprocess.Popen('adb devices -l', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			if firstLine == True:
				firstLine = False
				continue

			args = line.split() # split without any arguments splits on whitespace
			if len(args) > 2:
				self.devices.append(args[2])

	# Gets the device indexes the user specified and returns an array of them
	def getDeviceIndexes(self, arguments):

		num_args = len(arguments)
		deviceIndexes = []
		arg_index = 0

		# First search for any device indexes provides on the command line
		if num_args > 1:
			# Argument 1 is the name of the script, skip it
			for i in range(1, num_args):
				arg_index += 1
				# Check if this argument is a digit and add to the device index list
				if arguments[i].isdigit():
					deviceIndexes.append(int(arguments[i]))
				else:
					# Once we find an argument that is not a number, end parsing device indexes
					break

		return deviceIndexes, arg_index

	# Get the number of devices that are currently present, will match
	# the number of devices that show up in "adb devices"
	def getNumDevicesPresent(self):
		return len(self.devices)

	# index should be passed in as an integer
	def getDeviceAtIndex(self, index):

		if index >= 0 and index < self.getNumDevicesPresent():
			return self.devices[index]
		else:
			print "Error: No device present at index %d" % index
			return ""

	def openShellSession(self, index):

		if self.getNumDevicesPresent() > 0:
			device = self.getDeviceAtIndex(index)
			print "Opening shell session to device index %d (%s)" % (index, device)
			os.system('adb -s %s shell' % device)
		else:
			print "No devices present"

	# Print the Android devices that are present.
	def printDevices(self):
		for device in self.devices:
			print device

	def runCommandOnDevice(self, command, device, printOutput=True):

		command = '\"' + command + '\"'	
		aadbCommand = 'adb -s %s shell %s' % (device, command)
		print "aadbCommand is: %s" % aadbCommand
		p = subprocess.Popen(aadbCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		if printOutput:
			print "Device: %s" % device
			for line in p.stdout.readlines():
				if len(line) > 0:
					print line.rstrip()

		retval = p.wait()

	# Run a command on an individual device specified by the index in the devices array
	def runCommandOnDeviceIndex(self, command, index, printOutput=True):
		#print "Command I am going to run is: " + command
		if index >= 0 and index <= len(self.devices):
			self.runCommandOnDevice(command, self.devices[index], printOutput)
		else:
			print "Error: Invalid device index"

	def runCommandOnAllDevices(self, command, printOutput=True):

		print "runCommandOnAllDevices"
		for device in self.devices:
			self.runCommandOnDevice(command, device, printOutput)

	# Run the commandList on all currently connected devices
	# Command list contain the same number of entries as devices that are currently connected
	# and it will run the commands in order of how the devices show up in "adb devices"
	def runCommandListOnAllDevices(self, commandsList, printOutput=True):

		# Check that we have the same number of commands as we have devices
		if len(commandsList) == len(self.devices):
			for i in range(0, len(self.devices)):
				self.runCommandOnDevice(commandsList[i], self.devices[i], printOutput)
		else:
			print "Error: Must specify the same number of commands as devices present"

	# Push a file to a remote device
	def pushToDevice(self, device, localFile, destinationOnDevice, printOutput=True):

		p = subprocess.Popen('adb -s %s push %s %s' % (device, localFile, destinationOnDevice), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		if printOutput:
			print "Device: %s" % device
			for line in p.stdout.readlines():
				print line.rstrip()
		retval = p.wait()

	# This function allows you to push a list of files on the host machine to all connected devices.
	def pushFileListToAllDevices(self, fileList, destinationOnDevice, printOutput=True):

		if len(fileList) > 0:
			for fileName in fileList:
				print "*** Pushing %s to devices ***" % fileName
				self.pushToAllDevices(fileName, destinationOnDevice, printOutput)

	def pushDirectoryToAllDevices(self, directory, destinationOnDevice, printOutput=True):

		if os.path.isdir(directory):
			# Just using pushToAllDevices here since adb push doesn't care if it is
			# a directory or individual file.  Maybe merge these functions?
			print "*** Pushing directory %s to devices ***" % directory
			self.pushToAllDevices(directory, destinationOnDevice, printOutput)
		else:
			print "Error: Invalid directory specified, exiting..."
			exit

	# Push a file to all devices that are connected
	def pushToAllDevices(self, localFile, destinationOnDevice, printOutput=True):

		for device in self.devices:
			self.pushToDevice(device, localFile, destinationOnDevice, printOutput)

	# Push a file to the devices specified by index
	def pushToDeviceIndex(self, index, localFile, destinationOnDevice, printOutput=True):
		if index >= 0 and index <= len(self.devices):
			self.pushToDevice(self.devices[index], localFile, destinationOnDevice)
		else:
			print "Error: Invalid device index"

	# Pulls an individual file down from the Android device specified
	def pullFromDevice(self, device, fileDestinationOnDevice, localDestination='', printOutput=True):

		p = subprocess.Popen('adb -s %s pull %s %s' % (device, fileDestinationOnDevice, localDestination), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		if printOutput:
			print "Device: %s" % device
			for line in p.stdout.readlines():
				print line.rstrip()
		retval = p.wait()

	def pullFromDeviceIndex(self, index, fileDestinationOnDevice, localDestination='', printOutput=True):
		self.pullFromDevice(self.devices[index], fileDestinationOnDevice, localDestination)

	def deleteFileOnAllDevices(self, filePathToDelete):

		self.runCommandOnAllDevices("rm %s" % filePathToDelete)

	def printUsage(self):

		print "Usage: aadb"
		print "TODO: Finish this usage"
		sys.exit()


if __name__ == '__main__':

	aadb = AdvancedAdb()

	num_args = len(sys.argv)
	deviceIndexes = []
	arg_index = 0

	# First search for any device indexes provides on the command line
	if num_args > 1:
		deviceIndexes, arg_index = aadb.getDeviceIndexes(sys.argv)

		# Open an interactive shell session to the first device
		if sys.argv[arg_index] == 'shell':
			arg_index += 1
			if arg_index == num_args:

				#TODO: See if we can clean up this logic a little bit
				if aadb.getNumDevicesPresent() > 1 and len(deviceIndexes) == 1: # More than one device present and only one index specified
					aadb.openShellSession(deviceIndexes[0]) # Shell into the device specified
				elif aadb.getNumDevicesPresent() == 1 and len(deviceIndexes) != 0:
					print "error: one device present, do not specify index"
				elif aadb.getNumDevicesPresent() > 1 and len(deviceIndexes) > 0:
					print "error: more than one device present, do not specify index"
				elif aadb.getNumDevicesPresent() > 1 and len(deviceIndexes) == 0: # More than one device present and no index specified
						print "error: more than one device present, provide device index"
				elif aadb.getNumDevicesPresent() == 1 and len(deviceIndexes) == 0: # One device present and no indexes specifed
						# Connect to only device present
						aadb.openShellSession(0)
				else:
					print "No devices present, cannot open shell..."
			else:
				# Check if there is only one argument after "shell", possibly indicating that the user has specified a command in quotes
				# Example: aadb 0 shell "cat /proc/cpuinfo"
				shellCommand = ""
				if num_args == 4:
					shellCommand = sys.argv[3]
				else:
					# Otherwise user just specified command.
					# Example: aadb 1 shell cat /proc/cpuinfo
					for i in range(arg_index, num_args):
						shellCommand += sys.argv[arg_index] + " "
						arg_index += 1

				# if devices indexes were specified, run shell command over only indexes provided
				if len(deviceIndexes) > 0:
					for deviceIndex in deviceIndexes:
						aadb.runCommandOnDeviceIndex(shellCommand, deviceIndex)
				else:
					# If no devices specified on the command line, run command over all attached devices
					aadb.runCommandOnAllDevices(shellCommand)

		elif sys.argv[arg_index] == 'devices':
			os.system("adb devices -l") #TODO: Make like adb command where you have to pass -l

		elif sys.argv[arg_index] == 'push':
			arg_index += 1

			# Check if local file and destination file have been provided, otherwise print usage
			if arg_index == num_args or (arg_index + 1) == num_args:
				aadb.printUsage()
			else:
				local = sys.argv[arg_index]
				arg_index += 1
				remote = sys.argv[arg_index]

			if len(deviceIndexes) > 0:
				# Push file to all devices specified
				for deviceIndex in deviceIndexes:
					aadb.pushToDeviceIndex(deviceIndex, local, remote)
			else:
				aadb.pushToAllDevices(local, remote)

		elif sys.argv[arg_index] == 'reboot':
			shellCommand = "reboot"
			aadb.runCommandOnAllDevices(shellCommand)
