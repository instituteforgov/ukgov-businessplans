'''
Created on Jul 21, 2012

@author: petrbouchal
''' 'Function to open the most recent non-hidden file of a given extension if specified'

import os
def openlatestfile(path='./', accessmode='rb', extension=''):
    filedir = os.path.abspath(path)

    try:
        os.listdir(filedir)
    except Exception:
        errorstring = 'Could not open path'
        print errorstring
        return errorstring
        raise
        exit
    filedata = [os.path.normcase(f)
                for f in os.listdir(filedir)]
    if extension != '':
        extwithdot = '.' + extension
        noextension = False
    else:
        noextension = True
    oldestdate = 0
    filedata2 = []
    if noextension == False:
        filefound = 0
        for soubor in filedata:
            if os.path.splitext(os.path.join(filedir, soubor))[1] == extwithdot:
                filedate = os.stat(os.path.join(filedir, soubor)).st_ctime
                file2 = [soubor, filedate]
                filedata2.append(file2)
                filetoopen = os.path.join(filedir, filedata2[0][0])
                if ((filedate >= oldestdate) & (file2[0] != '.DS_Store')):
                    oldestdate = filedate
                    filetoopen = os.path.join(filedir, file2[0])
                finalfile = open(filetoopen, accessmode)
                filefound += 1

        if filefound == 0:
            errorstring = 'No file of that extension found.'
    elif noextension == True:
        filefound = 0
        for soubor in filedata:
            if ((os.path.isfile(os.path.join(filedir, soubor))) & (soubor[0] != '.')):
                filedate = os.stat(os.path.join(filedir, soubor)).st_ctime
                file2 = [soubor, filedate]
                filedata2.append(file2)
                filetoopen = os.path.join(filedir, filedata2[0][0])
                if ((filedate >= oldestdate)):
                    oldestdate = filedate
                    filetoopen = os.path.join(filedir, file2[0])
                filefound += 1
        if filefound == 0:
            errorstring = 'Only directories found - no file to open.'

    if (filefound > 0):
        finalfile = open(filetoopen, accessmode)
        return finalfile
    else:
        return errorstring
        print errorstring
