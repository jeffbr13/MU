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

def DoCycles (EndWord, WordList, MaxCycles, Workers=1):

    ppservers = ()
    JobServer = pp.Server(Workers, ppservers=ppservers)
    print 'Job server started with %s worker processes.' % str(JobServer.get_ncpus())	
    int (Workers)
    
    Words = len(WordList)
    
    ChunkSize= Words/Workers
    
    Marker = 0
    Count = 1
    
    Cycles = 0
    
    while EndWord not in WordList:
        Cycles += 1
        print Cycles
        print str(len(WordList))
        
        if Cycles >= MaxCycles:
            return "Could not derive in %s cycles." % MaxCycles
            
        else:
        
            Derivations = []
            for Process in range(0,Workers):
                OwnChunk = WordList[Marker:(ChunkSize*Count)]
                Marker = (ChunkSize*Count)
                Count += 1
                Job = JobServer.submit(ApplyRules, (OwnChunk,), (Transform,), ('Rules',))
                Result = Job()
                Derivations.extend(Result)
            
            WordList.extend(Derivations)

    return ("Success!", Cycles, Endword,)


def Run (MaxCycles=10, StartWord='MI', EndWord='MIU'):


    Derivatives = [StartWord]   # List of words

                                            
    return (Cycles, StartWord, EndWord) # Returns a tuple at the end, if found.
	
	

if __name__ == '__main__':
    print Run()
