import unittest
import numpy as np
from trjtrypy import distances


class TestDistances(unittest.TestCase):

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

    def test_d_Q(self):
        landmarks=self.landmarks[0]
        trajectory1=self.trajectories[0]
        trajectory2=self.trajectories[1]

        # default unsigned and 2-norm
        expected=1.0479279172
        
        result=distances.d_Q(landmarks, trajectory1, trajectory2)

        self.assertAlmostEqual(expected, result)

        # unsigned 5-norm
        expected=1.0479279172
        
        result=distances.d_Q(landmarks, trajectory1, trajectory2)
        
        self.assertAlmostEqual(expected, result)

        
        # signed
        expected=0.1705698949

        result=distances.d_Q(landmarks, trajectory1, trajectory2, version='signed')

        self.assertAlmostEqual(expected, result)




    def test_d_Q_pi(self):
        landmarks=self.landmarks[0]
        trajectory1=self.trajectories[0]
        trajectory2=self.trajectories[1]

        expected=0.9779724396

        result=distances.d_Q_pi(landmarks, trajectory1, trajectory2)

        self.assertAlmostEqual(expected, result)


    








        
