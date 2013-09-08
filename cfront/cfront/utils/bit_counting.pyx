from __future__ import division
import numpy as np
import sys
cimport cython

from cython.operator cimport dereference as deref, preincrement as inc

# "cimport" is used to import special compile-time information
# about the numpy module (this is stored in a file numpy.pxd which is
# currently part of the Cython distribution).
cimport numpy as np
# We now need to fix a datatype for our arrays. I've used the variable
# DTYPE for this, which is assigned to the usual NumPy runtime
# type info object.
DTYPE = np.uint8
DTYPE32 = np.uint32


# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.uint8_t DTYPE_t
ctypedef np.uint32_t DTYPE32_t
# "def" can type its arguments but not have a return type. The type of the
# arguments for a "def" function is checked at run-time when entering the
# function.
#
# The arrays f, g and h is typed as "np.ndarray" instances. The only effect
# this has is to a) insert checks that the function arguments really are
# NumPy arrays, and b) make some attribute access like f.shape[0] much
# more efficient. (In this example this doesn't matter though.)
def less_than_bits(np.ndarray[DTYPE_t, ndim=1] f, np.ndarray[DTYPE_t, ndim=1] g, np.int threshold):
    #if g.shape[0] % 2 != 1 or g.shape[1] % 2 != 1:
    #    raise ValueError("Only odd dimensions on filter supported")
    assert f.dtype == DTYPE
    assert g.dtype == DTYPE
    # The "cdef" keyword is also used within functions to type variables. It
    # can only be used at the top indendation level (there are non-trivial
    # problems with allowing them in other places, though we'd love to see
    # good and thought out proposals for it).
    #
    # For the indices, the "int" type is used. This corresponds to a C int,
    # other C types (like "unsigned int") could have been used instead.
    # Purists could use "Py_ssize_t" which is the proper Python type for
    # array indices.

    cdef DTYPE32_t n_els = f.shape[0]
    cdef DTYPE32_t n_outputs = g.shape[0]

    if n_outputs != n_els:
        raise ValueError("make sure that n_outputs = n_els")

    # It is very important to type ALL your variables. You do not get any
    # warnings if not, only much slower code (they are implicitly typed as
    # Python objects).
    #cdef int s_from, s_to, t_from, t_to
    # For the value variable, we want to use the same data type as is
    # stored in the array, so we use "DTYPE_t" as defined above.
    # NB! An important side-effect of this is that if "value" overflows its
    # datatype size, it will simply wrap around like in C, rather than raise
    # an error like in Python.

    cdef DTYPE32_t x
    cdef DTYPE_t value, bit_counter, temp_countdown
    for x in range(n_outputs):
        bit_counter = 0

        #explicity unroll the loop...
        temp_countdown = f[x]
        while(temp_countdown):
            bit_counter+= temp_countdown & 1
            temp_countdown >>=1

        temp_countdown = f[x+1]
        while(temp_countdown):
            bit_counter+= temp_countdown & 1
            temp_countdown >>=1

        temp_countdown = f[x+2]
        while(temp_countdown):
            bit_counter+= temp_countdown & 1
            temp_countdown >>=1

        temp_countdown = f[x+3]
        while(temp_countdown): 
            bit_counter+= temp_countdown & 1
            temp_countdown >>=1


        g[x] = 1 if bit_counter <= threshold else 0
    return
    
@cython.boundscheck(False) # turn of bounds-checking for entire function
def striding_8bit_comparison(np.ndarray[DTYPE_t, ndim=1] f
                                , np.ndarray[DTYPE_t, ndim=1] g
                                , np.ndarray[DTYPE32_t, ndim=1] h
                                , DTYPE_t threshold):
    cdef unsigned long stride = g.shape[0]
    cdef unsigned long n_elts = f.shape[0]
    if n_elts % stride != 0:
        raise ValueError("n_elts must be a multiple of stride")

    cdef unsigned long loops = long(n_elts/stride)
    cdef unsigned long innerloops = long(stride)
    cdef unsigned long n_outputs = h.shape[0]
    if n_outputs != loops:
        raise ValueError("n_outputs (third arg) should equal n_elts/stride")

    cdef unsigned long x, y,z, idx
    cdef unsigned char n
    cdef unsigned char mismatch_counter    
    
    cdef unsigned long match_count = 0
    cdef unsigned long mc_inc = 1


    print innerloops
    print "starting c loop"
    #result = []
    for x in range(loops):
        mismatch_counter = 0
        for y in range(innerloops):
            idx = stride * x + y
            n = f[idx] ^ g[y]
            #mismatch_counter+= __builtin_popcount(temp_xor)
            #computes the "or" of adjacent bits (these are single nucleotides)
            n = ((n & 0xAA) >> 1) | (n & 0x55)
            # Now every two bits are a two bit integer that indicate how many bits were
            # set in those two bits in the original number
            n = ((n & 0xCC) >> 2) + (n & 0x33)
            #Now we're at 4 bits
            n = ((n & 0xF0) >> 4) + (n & 0x0F)
            mismatch_counter += n
            # 8 bits

            #code to do the same thing for 32 bits
            #this doesn't really work... takes like a millisecond per comparison!
            #n = ((n & 0xAAAAAAAA) >> 1) + (n & 0x55555555)
            #// Now every two bits are a two bit integer that indicate how many bits were
            #// set in those two bits in the original number
            #
            #n = ((n & 0xCCCCCCCC) >> 2) + (n & 0x33333333)
            #// Now we're at 4 bits
            #
            #n = ((n & 0xF0F0F0F0) >> 4) + (n & 0x0F0F0F0F)
            #// 8 bits
            #
            #n = ((n & 0xFF00FF00) >> 8) + (n & 0x00FF00FF)
            #// 16 bits
            #
            #n = ((n & 0xFFFF0000) >> 16) + (n & 0x0000FFFF)
            #// kaboom - 32 bits



        if mismatch_counter < threshold:
            h[<unsigned long> (match_count) ] = <unsigned long> (x)
            match_count = match_count + mc_inc


    return match_count

def fill_with_4_ints(np.ndarray[DTYPE_t, ndim=1] f, np.ndarray[DTYPE_t, ndim=1] g):
    #f an array of ints with which to fill g
    #g an unitialized array of ints to be filled by repeating instances of f

    cdef DTYPE32_t n = f.shape[0]
    cdef DTYPE32_t pattern_length = g.shape[0]
    cdef long loops = long(n/4)
    cdef long i
    
    #check to ensure that input types are as expected
    if n % 4 != 0 :
        raise ValueError("please input an array f with a multiple of 4 elts")
    if pattern_length != 4:
        raise ValueError("please input 4 characters")


    print g[1]
    print loops

    for i in range(loops):
        f[4*i] = g[0]
        f[4*i+1] = g[1]
        f[4*i+2] = g[2]
        f[4*i+3] = g[3]
        
    return
    
    
    
