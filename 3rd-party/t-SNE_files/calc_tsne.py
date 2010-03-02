#! /usr/bin/env python
"""
Python wrapper to execute c++ tSNE implementation
for more information on tSNE, go to :
http://ticc.uvt.nl/~lvdrmaaten/Laurens_van_der_Maaten/t-SNE.html

HOW TO USE
Just call the method calc_tsne(dataMatrix)

Created by Philippe Hamel
hamelphi@iro.umontreal.ca
October 24th 2008

Modified by Joseph Turian (also of UMontreal):
    * Added USE_PCA parameter.
    * Call tolist() on matrix before iterating and writing its data out.
    * Do all t-SNE temporary output in a temporary directory, to prevent
    it from clobbering its own output (if two copies of this process
    are running).
    * print everything to stderr, not stdout.
    * Assume that tsne executables are in the same directory as this module.

TODO:
    * Make tsne.pca == calc_tsne.PCA
"""

from struct import *
import sys
import os
from numpy import *

TSNE_DIRECTORY = os.path.dirname(__file__)

#def calc_tsne(dataMatrix,NO_DIMS=2,PERPLEX=30,INITIAL_DIMS=30,landmarks=1,USE_PCA=True):
#def calc_tsne(dataMatrix,NO_DIMS=2,PERPLEX=30,INITIAL_DIMS=30,landmarks=1,USE_PCA=False):
def tsne(X = array([]), no_dims = 2, initial_dims = 50, perplexity = 30.0, landmarks=1, use_pca=False):
    """
    This is the main function.
    X is a 2D numpy array containing your data (each row is a data point)
    Remark : landmarks is a ratio (0<landmarks<=1)
    If landmarks == 1 , it returns the list of points in the same order as the input
    """

    # Move into a temporary directory
    import os, tempfile
    oldwd = os.getcwd()
    tmpd = tempfile.mkdtemp()
    os.chdir(tmpd)
    try:
        print >> sys.stderr, "Writing temporary t-SNE data to", tmpd

        if use_pca:
            X=PCA(X,initial_dims)
        writeDat(X, no_dims,perplexity, landmarks)
        tSNE()
        Xmat,LM,costs=readResult()
        clearData()
        if landmarks==1:
            X=reOrder(Xmat,LM)
            os.chdir(oldwd)
            return X
        return Xmat,LM
    except:
        os.chdir(oldwd)
        raise

def PCA(dataMatrix, INITIAL_DIMS) :
    """
    Performs PCA on data.
    Reduces the dimensionality to INITIAL_DIMS
    """
    print >> sys.stderr, 'Performing PCA'

    dataMatrix= dataMatrix-dataMatrix.mean(axis=0)

    if dataMatrix.shape[1]<INITIAL_DIMS:
        INITIAL_DIMS=dataMatrix.shape[1]

    (eigValues,eigVectors)=linalg.eig(cov(dataMatrix.T))
    perm=argsort(-eigValues)
    eigVectors=eigVectors[:,perm[0:INITIAL_DIMS]]
    return dataMatrix

def readbin(type,file) :
    """
    used to read binary data from a file
    """
    return unpack(type,file.read(calcsize(type)))

def writeDat(dataMatrix,NO_DIMS,PERPLEX,landmarks):
    """
    Generates data.dat
    """
    print >> sys.stderr, 'Writing data.dat'
    print >> sys.stderr, 'Dimension of projection : %i \nPerplexity : %i \nLandmarks(ratio) : %f'%(NO_DIMS,PERPLEX,landmarks)
    n,d = dataMatrix.shape
    f = open('data.dat', 'wb')
    f.write(pack('=iiid',n,d,NO_DIMS,PERPLEX))
    f.write(pack('=d',landmarks))
    for inst in dataMatrix.tolist() :
#    for inst in dataMatrix :
        for el in inst :
            f.write(pack('=d',el))
    f.close()


def tSNE():
    """
    Calls the tsne c++ implementation depending on the platform
    """
    platform=sys.platform
    print >> sys.stderr,'Platform detected : %s'%platform
    if platform in ['mac', 'darwin'] :
        cmd='tSNE_maci'
    elif platform == 'win32' :
        cmd='tSNE_win'
    elif platform == 'linux2' :
        cmd='tSNE_linux'
    else :
        print >> sys.stderr, 'Not sure about the platform, we will try linux version...'
        cmd='tSNE_linux'
    cmd = os.path.join(TSNE_DIRECTORY, cmd)
    print >> sys.stderr, 'Calling executable "%s"'%cmd
    os.system(cmd)
    

def readResult():
    """
    Reads result from result.dat
    """
    print >> sys.stderr, 'Reading result.dat'
    f=open('result.dat','rb')
    n,ND=readbin('ii',f)
    Xmat=empty((n,ND))
    for i in range(n):
        for j in range(ND):
            Xmat[i,j]=readbin('d',f)[0]
    LM=readbin('%ii'%n,f)
    costs=readbin('%id'%n,f)
    f.close()
    return (Xmat,LM,costs)

def reOrder(Xmat, LM):
    """
    Re-order the data in the original order
    Call only if landmarks==1
    """
    print >> sys.stderr, 'Reordering results'
    X=zeros(Xmat.shape)
    for i,lm in enumerate(LM):
        X[lm]=Xmat[i]
    return X

def clearData():
    """
    Clears files data.dat and result.dat
    """
    print >> sys.stderr, 'Clearing data.dat and result.dat'
    os.system('rm data.dat')
    os.system('rm result.dat')
