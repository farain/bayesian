#!/usr/local/extlib/bin/python

import random
import string


EPSILON         = 0.0000001
ITERATION       = 100
NUM_SEQUENCES   = 100
LEN_SEQUENCE    = 30 
MOTIF           = 'bayesian' # for test only
LEN_MOTIF       = len( MOTIF )
SAMPLE_SPACE    = string.ascii_lowercase 

locations   = []
sequences   = []
model       = []

def generateRandomString():
    
    motif_location = random.randint( 0, LEN_SEQUENCE - LEN_MOTIF )
    prefix = ''.join( random.choice( SAMPLE_SPACE ) for _ in range( 0, motif_location ) )
    suffix = ''.join( random.choice( SAMPLE_SPACE ) for _ in range( motif_location+LEN_MOTIF, LEN_SEQUENCE ) )

    return prefix + MOTIF + suffix
    #return ''.join( random.choice( SAMPLE_SPACE ) for _ in range( LEN_SEQUENCE ) )


def initialize():

    for i in range( NUM_SEQUENCES ):
        locations.append( random.randint(0, LEN_SEQUENCE - LEN_MOTIF) )
        sequences.append( generateRandomString() )

    for i in range( LEN_MOTIF ):
        i_state = []

        for j in range( len( SAMPLE_SPACE ) ):
            i_state.append( 1.0 / len( SAMPLE_SPACE ) )

        model.append( i_state )


def calculateProbability( motif ):

    prob = 1.0
    for i in range( LEN_MOTIF ):
        idx = SAMPLE_SPACE.find( motif[i] )
        prob *= model[i][idx]
        
    return prob
    

def updateLocations():
    
    for i in range( NUM_SEQUENCES ):
        
        prob_list = []
        for j in range( LEN_SEQUENCE - LEN_MOTIF ):
            prob = calculateProbability( sequences[i][j:j+LEN_MOTIF] )
            prob_list.append( prob )

        locations[i] = prob_list.index( max( prob_list ) ) 

            
def updateModel():
    
    for i in range( LEN_MOTIF ):
        count_list = [EPSILON] * len( SAMPLE_SPACE )
        for j in range( NUM_SEQUENCES ):
            
            item = sequences[j][ locations[j] + i ]
            item_idx = SAMPLE_SPACE.find( item )
            count_list[ item_idx ] += 1.0

        # model probability update
        for k in range( len( SAMPLE_SPACE ) ):
            model[i][k] = count_list[k] / sum( count_list )


def printMotifLocations():

    for i in range( NUM_SEQUENCES ):
        print sequences[i][ locations[i]:locations[i]+LEN_MOTIF ] , sequences[i]

### RUN ### 

initialize()

print 'MOTIF =', MOTIF
print locations
print 'update model'
for _ in range( ITERATION ):
    updateLocations()
    updateModel()

print 'update done'

printMotifLocations()
print locations


###########
