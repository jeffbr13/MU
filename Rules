#!/usr/bin/python
# Copyright (C) 2011 Ben Jeffrey. All Rights Reserved.

def Instruct():
    return 'You are in the wrong script. Be instructed by this.'

def Transform(Word):
    """
    Given a string, returns a list of all possible
    derivations according to the MU puzzle rules.
    """
    Word = str(Word)    # Ensure input is a string
    Transformed = []
    
    if Word[-1] == 'I': # Rule 1:   xxI -> xxIU
        Transformed.append(Word + 'U')
    if Word[0] == 'M':  # Rule 2:   Mxx -> Mxxxx
        Transformed.append(Word+Word[1:])
    if 'III' in Word:   # Rule 3:   xxIIIxx -> xxUxx
        Transformed.append(Word.replace('III', 'U'))
    if 'UU' in Word:    # Rule 4:   xxUUxx -> xxxx
        Transformed.append(Word.replace('UU', ''))

    return Transformed # Returns list of all applied transformations.

if __name__ == '__main__':
    print Instruct()
