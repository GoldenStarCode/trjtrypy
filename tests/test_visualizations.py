import unittest
import numpy as np
from trjtrypy import visualizations
from trjtrypy.featureMappings import curve2vec

class TestVisualizations(unittest.TestCase):

    #generating data

    trajectories=[
        
        np.array([ [-2,2], [2,-2] ]),
        
        np.array([
                   [-2,2], [-1,2], [-2,1],
                   [-1,0], [-1,1], [0,2],
                   [1,1], [0,1], [0,0],
                   [0,-1], [0,-2], [-1,-1],
                   [1,-1], [2,0]
                ])
    ]

    landmarks=[

        np.array([ [-3,2], [-3,3], [-2,-2],
                   [-2,3], [2,-3], [2,2],
                   [3,-3], [3,-2]
                ]),
        
        np.array([ [-2.5,1.5], [-2.5,2], [-2.5,2.5],
                   [-2,0], [-1.5,1], [-1.5,2.5],
                   [-0.5,-0.5], [-0.5,0.5], [-0.5,1],
                   [0,1.5], [0.5,-0.5], [0.5,1.5],
                   [2,-1], [2,0.5], [2.5,0], [2.5,0.5]
                ])
    ]

    def test_draw_landmarks_trajectory(self):

        landmarks=self.landmarks[1]
        trajectory=self.trajectories[1]
        # default
        visualizations.draw_landmarks_trajectory(landmarks, trajectory)

        # signed
        visualizations.draw_landmarks_trajectory(landmarks, trajectory, version='signed')
        
        # does not draw trajectory
        visualizations.draw_landmarks_trajectory(landmarks, trajectory, trj=False)

        # does not draw landmarks
        visualizations.draw_landmarks_trajectory(landmarks, trajectory, lndmarks=False)

        # does not draw distances
        visualizations.draw_landmarks_trajectory(landmarks, trajectory, dists=False)

        # does not draw argmin points
        visualizations.draw_landmarks_trajectory(landmarks, trajectory, argminpnts=False)

        # zoom in fixed size
        visualizations.draw_landmarks_trajectory(landmarks, trajectory, zoom=10)

        # change figure size
        visualizations.draw_landmarks_trajectory(landmarks, trajectory, figsize=(20,20))

        self.assertRaises(ValueError, visualizations.draw_landmarks_trajectory, landmarks, trajectory, zoom=-10)
                


    def test_colorcoding(self):

        trajectory=self.trajectories[1]

        def vecfunc(x,y):
            return curve2vec([[x,y]], [trajectory])[0]
        vecfunc=np.vectorize(vecfunc)

        # default
        visualizations.colorcoding(vecfunc, trajectory)

        # change zoom
        visualizations.colorcoding(vecfunc, trajectory, zoom=10)


        # change figure size
        visualizations.colorcoding(vecfunc, trajectory, figsize=(20,20))

        # change dpi
        visualizations.colorcoding(vecfunc, trajectory, dpi=100)

        

        # for signed version
        def vecfunc(x,y):
            return curve2vec([[x,y]], [trajectory], version='signed')[0]
        vecfunc=np.vectorize(vecfunc)
        
        self.assertRaises(ValueError, visualizations.colorcoding, vecfunc, trajectory, dpi=0)
        self.assertRaises(ValueError, visualizations.colorcoding, vecfunc, trajectory, zoom=-20)

        
        visualizations.colorcoding(vecfunc, trajectory, version='signed', dpi=100)


































    
