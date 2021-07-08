from trjtrypy.distsbase import DistsBase
import numpy as np




def curve2vec(landmarks, trajectories, version='unsigned', sigma=1, segIndx=False, argPnts=False):
    '''

          Usage
                 Maps each trajectory in trajectories to a vector of size len(landmarks) using the signed
                 or unsigned feature mapping introduced in the references.

          -------------------------------------------------------------------------------------------------
          Parameters      
                         landmarks: ndarray of shape (len(landmarks), 2)
                                    An array of points in R^2 that their distances from trajectories should be
                                    measured.

                      trajectories: ndarray of shape (len(trajectories), )
                                    Trajectories are piecewise linear curves in R^2 of shape (n, 2).

                           version: str ('signed', 'unsigned'), default='unsigned'
                                    Determines which version of the feature mappings is utilized.

                             sigma: float, default=1
                                    A positve real number specifying the Gaussian weight parameter employed 
                                    in the definition of the signed feature mapping. So, it will be
                                    effective only when version='signed'.

                          segIndx: bool (True, False), default=False
                                   Being True or False determines whether the function outputs the indices
                                   of segments selected by the landmarks.

                          argPnts: bool (True, False), default=False
                                   Setting True or False specifies if the function outputs the  
                                   nearest points on trajectories to landmarks.
                                   
          --------------------------------------------------------------------------------------------------
          Returns
                  ndarray
                  The array of mapped vectors under the signed/unsigned feature mapping. Moreover, when segIndx
                  or argPnts are called an array of dictionaries including the feature mapping values,
                  selected segments' indices or argmin points respectively for all trajectories is given.
                  
    '''
    D=DistsBase()
    if segIndx and argPnts:
        if version=='unsigned':
            return np.array([{'UnsignedCurve2Vec':D.APntSetDistACrv(landmarks, trajectory, ArgminPnts=True, InUse=True), 'SelectedSegmentsIndex':D.SlctdSgmnts, 'ArgminPoints':np.array(D.SlctdPntsOnSgmnts)} for trajectory in trajectories])
        else:
            return np.array([{'SignedCurve2Vec':D.APntSetSignedDistACrv(landmarks, trajectory, sigma, ArgminPnts=True, InUse=True), 'SelectedSegmentsIndex':D.SlctdSgmnts, 'ArgminPoints':np.array(D.SlctdPntsOnSgmnts)} for trajectory in trajectories])

    if segIndx:
        if version=='unsigned':
            return np.array([{'UnsignedCurve2Vec':D.APntSetDistACrv(landmarks, trajectory, InUse=True), 'SelectedSegmentsIndex':D.SlctdSgmnts} for trajectory in trajectories])
        else:
            return np.array([{'SignedCurve2Vec':D.APntSetSignedDistACrv(landmarks, trajectory, sigma, InUse=True), 'SelectedSegmentsIndex':D.SlctdSgmnts} for trajectory in trajectories])

    if argPnts:
        if version=='unsigned':
            return np.array([{'UnsignedCurve2Vec':D.APntSetDistACrv(landmarks, trajectory, ArgminPnts=True, InUse=True), 'ArgminPoints':np.array(D.SlctdPntsOnSgmnts)} for trajectory in trajectories])
        else:
            return np.array([{'SignedCurve2Vec':D.APntSetSignedDistACrv(landmarks, trajectory, sigma, ArgminPnts=True, InUse=True), 'ArgminPoints':np.array(D.SlctdPntsOnSgmnts)} for trajectory in trajectories])
    
    
    if version=='unsigned':
        return np.array([D.APntSetDistACrv(landmarks, trajectory) for trajectory in trajectories])
    else:
        return np.array([D.APntSetSignedDistACrv(landmarks, trajectory, sigma) for trajectory in trajectories])
