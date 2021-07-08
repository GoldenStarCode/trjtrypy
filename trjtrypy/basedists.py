from trjtrypy.distsbase import DistsBase
import numpy as np


def distance(points, curves, version='unsigned', segIndx=False, argPnts=False):
    '''

        Usage
               Calculates the distance of each point in points from each curve in curves
               at the same time.

        ----------------------------------------------------------------------------------
        Parameters
                     points: ndarray of shape (len(points),)
                             An array that contains coordinates of points
                             in each row.
                             
                     curves: ndarray of shape (len(curves),)
                             Piecewise linear curves in R^2 of shape (n, 2).
                             Notice n can be different for each curve.
                             
                    version: str ('unsigned', 'signed'), default='unsigned'
                             Determines unsigned or signed distacne that is going
                             to be computed.
                             
                    segIndx: bool (True, False), default=False
                             Being True or False determines whether the
                             function outputs the indices of segments selected
                             by the points.

                    argPnts: bool (True, False), default=False
                             Setting True or False specifies if the function outputs
                             the nearest points on curves to points.
                                   
        ----------------------------------------------------------------------------------                           
        Returns
                  ndarray
                  The array of unsigned/signed distances.
                  Moreover, when segIndx or argPnts are called an array of dictionaries
                  including the distance values, selected segments' indices or
                  argmin points respectively for all curves is given.
                                         
    '''

    D=DistsBase()
    if segIndx and argPnts:
        if version=='unsigned':
            return np.array([{'UnsignedDistance':D.APntSetDistACrv(points, curve, ArgminPnts=True, InUse=True), 'SelectedSegmentsIndex':D.SlctdSgmnts, 'ArgminPoints':np.array(D.SlctdPntsOnSgmnts)} for curve in curves])
        else:
            return np.array([{'SignedDistance':np.multiply(np.sign(D.APntSetSignedDistACrv(points, curve, ArgminPnts=True, InUse=True)), D.UnsignedDist), 'SelectedSegmentsIndex':D.SlctdSgmnts, 'ArgminPoints':np.array(D.SlctdPntsOnSgmnts)} for curve in curves])

    if segIndx:
        if version=='unsigned':
            return np.array([{'UnsignedDistance':D.APntSetDistACrv(points, curve, InUse=True), 'SelectedSegmentsIndex':D.SlctdSgmnts} for curve in curves])
        else:
            return np.array([{'SignedDistance':np.multiply(np.sign(D.APntSetSignedDistACrv(points, curve, InUse=True)), D.UnsignedDist), 'SelectedSegmentsIndex':D.SlctdSgmnts} for curve in curves])

    if argPnts:
        if version=='unsigned':
            return np.array([{'UnsignedDistance':D.APntSetDistACrv(points, curve, ArgminPnts=True, InUse=True), 'ArgminPoints':np.array(D.SlctdPntsOnSgmnts)} for curve in curves])
        else:
            return np.array([{'SignedDistance':np.multiply(np.sign(D.APntSetSignedDistACrv(points, curve, ArgminPnts=True, InUse=True)), D.UnsignedDist), 'ArgminPoints':np.array(D.SlctdPntsOnSgmnts)} for curve in curves])
    
    
    if version=='unsigned':
        return np.array([D.APntSetDistACrv(points, curve) for curve in curves])
    else:
        return np.array([np.multiply(np.sign(D.APntSetSignedDistACrv(points, curve, InUse=True)), D.UnsignedDist) for curve in curves])
    
