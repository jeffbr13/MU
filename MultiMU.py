#!/usr/bin/python
# Copyright (C) 2011 Ben Jeffrey. All Rights Reserved.
import MU
import pp
import sys


def main():
	"""
	The main program loop goes here.
	"""
	ppservers = ()
	
	NumCPUs = 2
	
	JobServer = pp.Server(NumCPUs, ppservers=ppservers)
	
	print "Job Server started with %s worker processes." % JobServer.get_ncpus()

if __name__ == '__main__':
    main()
