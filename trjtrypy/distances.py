from trjtrypy.featureMappings import curve2vec
from scipy.spatial import distance
import numpy as np


def d_Q(landmarks, trajectory1, trajectory2, version='unsigned', sigma=1, p=2):
    '''

          Usage
                 The landmark-based signed/unsigned distance d_Q according to the
                 definitions in the related references is computed. 

          ----------------------------------------------------------------------------------------
          Parameters      
                        landmarks: ndarray of shape (len(landmarks), 2)
                                   An array containing coordinates of landmarks in each row. 
                                
                      trajectory1: ndarray of shape (len(trajectory1), 2)
                                   An array that contains the waypoints of trajectory1
                                   consecutively.

                      trajectory2: ndarray of shape (len(trajectory2), 2)
                                   An array that contains the waypoints of trajectory2
                                   consecutively.

                          version: str ('signed', 'unsigned'), default='unsigned'
                                   Determines which version of the feature mappings is utilized.

                            sigma: float, default=1 
                                   A positve real number specifying the Gaussian weight parameter
                                   employed in the definition of the signed distance. So, it will
                                   be effective only when version='signed'.

                                p: float (1<=p<=infinity), default=2
                                   Specifies the p-norm used in calculations.
                            
             ----------------------------------------------------------------------------------------
            Returns
                     float
                     The d_Q distance of trajectory1 and trajectory2.
                
    '''


    trajectories_fm=curve2vec(landmarks, [trajectory1,trajectory2], version=version, sigma=sigma)
    return distance.minkowski(trajectories_fm[0], trajectories_fm[1], p)/len(landmarks)**(1/p)


def d_Q_pi(landmarks, trajectory1, trajectory2, p=1):
    '''

          Usage
                 The landmark-based distance d_Q_pi according to the definition in the
                 related reference is computed. 

          ----------------------------------------------------------------------------------
          Parameters        
                        landmarks: ndarray of shape (len(landmarks), 2)
                                   An array containing coordinates of landmarks in each row. 
                                
                      trajectory1: ndarray of shape (len(trajectory1), 2)
                                   An array that contains the waypoints of trajectory1
                                   consecutively.

                     trajectory2: ndarray of shape (len(trajectory2), 2)
                                  An array that contains the waypoints of trajectory2
                                  consecutively.

                               p: float (1<=p<=infinity), default=2
                                  Specifies the p-norm used in calculations.
                                  
            ----------------------------------------------------------------------------------
            Returns
                     float
                     The d_Q_pi distance of trajectory1 and trajectory2.
                     
    '''
    
    trajectories_ArgminPnts=curve2vec(landmarks, [trajectory1,trajectory2], argPnts=True)

    ps_diff=np.subtract(trajectories_ArgminPnts[0]['ArgminPoints'], trajectories_ArgminPnts[1]['ArgminPoints'])
 
    NormsVec=np.linalg.norm(ps_diff, axis=1)

    return np.linalg.norm(NormsVec, ord=p)/len(landmarks)**(1/p)










