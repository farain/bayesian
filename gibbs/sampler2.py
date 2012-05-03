#!/usr/local/extlib/bin/python

# use conditional probability 

import random
import string


EPSILON         = 0.0000001
ITERATION       = 20
NUM_SEQUENCES   = 50
LEN_SEQUENCE    = 100 
MOTIF           = 'bayesian' # for test only
LEN_MOTIF       = len( MOTIF )
SAMPLE_SPACE    = string.ascii_lowercase 
LEN_SAMPLE_SPACE= len( string.ascii_lowercase )

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

    for i in range( LEN_SAMPLE_SPACE ):
        temp_list = [EPSILON] * LEN_SAMPLE_SPACE
        model.append( temp_list )

def _calculateProbability( motif ):

    prob = 1.0
    for i in range( LEN_MOTIF - 1):
        mother_idx = SAMPLE_SPACE.find( motif[i] )
        child_idx = SAMPLE_SPACE.find( motif[i+1] )
        prob *= model[mother_idx][child_idx]
        
    return prob
    

def _normalize( prob_list ):
    total_prob = sum( prob_list )

    for i in range( len( prob_list ) ):
        prob_list[i] = prob_list[i] / total_prob

    return prob_list
        

def _sampleFromDistribution( prob_list ):
    count_list = []

    prob_list = _normalize( prob_list )

    for i in range( len( prob_list ) ):
        count = int( prob_list[i] * 100 )
        if count > 0:
            temp_list = [i] * count
            count_list.extend( temp_list )

    rand_idx = random.randint( 0, len( count_list ) - 1 )
    return count_list[ rand_idx ]
    #return  prob_list.index( max( prob_list ) ) 



def updateLocations():
    
    for i in range( NUM_SEQUENCES ):
        
        prob_list = []
        for j in range( LEN_SEQUENCE - LEN_MOTIF ):
            prob = _calculateProbability( sequences[i][j:j+LEN_MOTIF] )
            prob_list.append( prob )

        locations[i] = _sampleFromDistribution( prob_list ) 

            
def updateModel():
    
    for i in range( NUM_SEQUENCES ):
        item = sequences[i][ locations[i] : locations[i] + LEN_MOTIF ]

        for j in range( LEN_MOTIF - 1):
            mother_item_idx = SAMPLE_SPACE.find( item[j] )
            child_item_idx = SAMPLE_SPACE.find( item[j+1] )
            model[ mother_item_idx ][ child_item_idx] += 0.1 

    # model probability update
    for i in range( LEN_SAMPLE_SPACE ):
        for j in range( LEN_SAMPLE_SPACE ):
            model[i][j] = model[i][j] / sum( model[i] )


def printMotifLocations():

    for i in range( NUM_SEQUENCES ):
        print sequences[i][ locations[i]:locations[i]+LEN_MOTIF ] , sequences[i]

### RUN ### 

initialize()

print 'MOTIF =', MOTIF
print locations
print 'update model'
for _ in range( ITERATION ):
    updateModel()
    updateLocations()

print 'update done'

printMotifLocations()
print locations

###########
