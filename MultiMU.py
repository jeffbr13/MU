#!/usr/bin/python
# Copyright (C) 2011 Ben Jeffrey. All Rights Reserved.
import Rules
import pp
import sys

Transform = Rules.Transform

def ApplyRules (WordList):
    Derivations = []
    for Word in WordList:
        WordDerivatives = Rules.Transform(Word)
        Derivations.extend(WordDerivatives)
     return Derivations


def CycleThrough (WordList, Workers=1):

    int (Workers)
    
    Words = len(WordList)
    
    ChunkSize= Words/Processors
    
    Marker = 0
    Count = 1
    
    Derivations = []
    
    for Process in range(0,Workers):
        OwnChunk = WordList[Marker:(ChunkSize*Count)]
        Marker = (ChunkSize*Count)
        Count += 1
        Job = JobServer.submit(ApplyRules, (OwnChunk,), (Transform,), ('Rules',))
        Result = Job()
        Derivations.extend(Result)
        # DO STUFF HERE
    
#    for Word in WordList:               # For every word in the list,
#        Derivatives = MU.Transform(Word)   # get it's transformations,
#        Derivations += Derivatives      # and put them in a big list.
#    return Derivations                  # Return the list for the next cycle.

def Run (MaxCycles=10, StartWord='MI', EndWord='MU'):

    ppservers = ()
    NumCPUs = 2
	JobServer = pp.Server(NumCPUs, ppservers=ppservers)
	print 'Job server started with %s worker processes.' % str(JobServer.get_ncpus())
	
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
