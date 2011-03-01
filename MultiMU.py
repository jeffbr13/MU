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
	
def CycleThrough (WordList):
    Derivations = []
    for Word in WordList:               # For every word in the list,
        Derivatives = Transform(Word)   # get it's transformations,
        Derivations += Derivatives      # and put them in a big list.
    return Derivations                  # Return the list for the next cycle.

def Run (MaxCycles=10, StartWord='MI', EndWord='MU'):

    ppservers = ()
    NumCPUs = 

    Derivatives = [StartWord]   # List of words
    Cycles = 0

    while EndWord not in Derivatives:

        Cycles += 1
        print Cycles, str(len(Derivatives))
        if Cycles >= MaxCycles: # Stop if we can't find it in given number of cycles.
            return 'Could not derive in %s cycles' % MaxCycles
        else:
            Derivatives += CycleThrough(Derivatives)
                                            
    return (Cycles, StartWord, EndWord) # Returns a tuple at the end, if found.
	
	

if __name__ == '__main__':
    main()
