from __future__ import division
import numpy as np
import sys
cimport cython

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
ctypedef np.uint64_t DTYPE32_t
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
def striding_bitpair_comparison(np.ndarray[DTYPE_t, ndim=1] f
                                , np.ndarray[DTYPE_t, ndim=1] g
                                , np.ndarray[DTYPE_t, ndim=1] h
                                , DTYPE_t threshold):
    cdef long stride = g.shape[0]
    cdef long n_elts = f.shape[0]
    if n_elts % stride != 0:
        raise ValueError("n_elts must be a multiple of stride")

    cdef long loops = long(n_elts/stride)
    cdef long innerloops = long(stride)
    cdef long n_outputs = h.shape[0]
    if n_outputs != loops:
        raise ValueError("n_outputs (third arg) should equal n_elts/stride")

    cdef DTYPE_t p0, p1, q0, q1, mismatch_counter, temp_xor
    cdef long x, y, idx
    

    for x in range(loops):
        mismatch_counter = 0
        for y in range(innerloops):
            idx = stride * x + 2 * y
            temp_xor = 127 #f[idx] ^ g[y]
            while(temp_xor):
                mismatch_counter += temp_xor & 1
                temp_xor >>=1
            #p0 = f[idx]
            #p1 = f[idx+1]
            #q0 = g[y * 2]
            #q1 = g[y * 2 + 1]
            #if p0 != q0 or p1 != q1:
            #    mismatch_counter += 1
        if mismatch_counter < threshold:
            idx = 1
        #    h[0] = 1
            
            

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
    
    
    
