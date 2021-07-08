import unittest
import numpy as np
from trjtrypy.featureMappings import curve2vec


class TestFeatureMapping(unittest.TestCase):
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

    def test_unsigned_curve2vec(self):

        landmarks=self.landmarks[0]
        trajectories=self.trajectories

        # default unsigned curve2vec
        expected=np.array([
            np.array([1,1.41421356,2.82842712,1,1,2.82842712,1.41421356,1]),
            np.array([1,1.41421356,1.41421356,1,2.23606798,1.41421356,2.82842712,2.12132034])
        ])

        result=curve2vec(landmarks, trajectories)

        for i in range(len(expected[0])):self.assertAlmostEqual(expected[0][i], result[0][i])
        for i in range(len(expected[1])):self.assertAlmostEqual(expected[1][i], result[1][i])


        # segIndx=True

        expected=np.array([
            {'UnsignedCurve2Vec':np.array([1,1.41421356,2.82842712,1,1,2.82842712,1.41421356,1]),
             'SelectedSegmentsIndex':np.array([0, 0, 0, 0, 0, 0, 0, 0])
            },
            {'UnsignedCurve2Vec':np.array([1,1.41421356,1.41421356,1,2.23606798,1.41421356,2.82842712,2.12132034]),
             'SelectedSegmentsIndex':np.array([ 0,  0, 10,  0,  9,  5, 11, 12])
            }
        ])

        result=curve2vec(landmarks, trajectories, segIndx=True)

        for i in range(len(expected[0]['UnsignedCurve2Vec'])):self.assertAlmostEqual(expected[0]['UnsignedCurve2Vec'][i], result[0]['UnsignedCurve2Vec'][i])
        for i in range(len(expected[0]['SelectedSegmentsIndex'])):self.assertAlmostEqual(expected[0]['SelectedSegmentsIndex'][i], result[0]['SelectedSegmentsIndex'][i])

        for i in range(len(expected[1]['UnsignedCurve2Vec'])):self.assertAlmostEqual(expected[1]['UnsignedCurve2Vec'][i], result[1]['UnsignedCurve2Vec'][i])
        for i in range(len(expected[1]['SelectedSegmentsIndex'])):self.assertAlmostEqual(expected[1]['SelectedSegmentsIndex'][i], result[1]['SelectedSegmentsIndex'][i])


        # argPnts=True

        expected=np.array([
            {'UnsignedCurve2Vec':np.array([1,1.41421356,2.82842712,1,1,2.82842712,1.41421356,1]),
             'ArgminPoints':np.array([ [-2,2], [-2,2], [0,0], [-2,2], [2,-2], [0,0], [2,-2], [2,-2] ])
            },
            {'UnsignedCurve2Vec':np.array([1,1.41421356,1.41421356,1,2.23606798,1.41421356,2.82842712,2.12132034]),
             'ArgminPoints':np.array([ [-2,2], [-2,2], [-1,-1], [-2,2], [0,-2], [1,1], [1,-1], [1.5,-0.5] ])
            }
        ])

        result=curve2vec(landmarks, trajectories, argPnts=True)

        for i in range(len(expected[0]['UnsignedCurve2Vec'])):self.assertAlmostEqual(expected[0]['UnsignedCurve2Vec'][i], result[0]['UnsignedCurve2Vec'][i])
        for i in range(len(expected[0]['ArgminPoints'])):
            self.assertAlmostEqual(expected[0]['ArgminPoints'][i][0], result[0]['ArgminPoints'][i][0])
            self.assertAlmostEqual(expected[0]['ArgminPoints'][i][1], result[0]['ArgminPoints'][i][1])


        for i in range(len(expected[1]['UnsignedCurve2Vec'])):self.assertAlmostEqual(expected[1]['UnsignedCurve2Vec'][i], result[1]['UnsignedCurve2Vec'][i])
        for i in range(len(expected[1]['ArgminPoints'])):
            self.assertAlmostEqual(expected[1]['ArgminPoints'][i][0], result[1]['ArgminPoints'][i][0])
            self.assertAlmostEqual(expected[1]['ArgminPoints'][i][1], result[1]['ArgminPoints'][i][1])


        # segIndx=True and argPnts=True
        expected=np.array([
            {'UnsignedCurve2Vec':np.array([1,1.41421356,2.82842712,1,1,2.82842712,1.41421356,1]),
             'SelectedSegmentsIndex':np.array([0, 0, 0, 0, 0, 0, 0, 0]),
             'ArgminPoints':np.array([ [-2,2], [-2,2], [0,0], [-2,2], [2,-2], [0,0], [2,-2], [2,-2] ])
            },
            {'UnsignedCurve2Vec':np.array([1,1.41421356,1.41421356,1,2.23606798,1.41421356,2.82842712,2.12132034]),
             'SelectedSegmentsIndex':np.array([ 0,  0, 10,  0,  9,  5, 11, 12]),
             'ArgminPoints':np.array([ [-2,2], [-2,2], [-1,-1], [-2,2], [0,-2], [1,1], [1,-1], [1.5,-0.5] ])
            }
        ])

        result=curve2vec(landmarks, trajectories, segIndx=True, argPnts=True)
        
        for i in range(len(expected[0]['UnsignedCurve2Vec'])):self.assertAlmostEqual(expected[0]['UnsignedCurve2Vec'][i], result[0]['UnsignedCurve2Vec'][i])
        for i in range(len(expected[0]['SelectedSegmentsIndex'])):self.assertAlmostEqual(expected[0]['SelectedSegmentsIndex'][i], result[0]['SelectedSegmentsIndex'][i])
        for i in range(len(expected[0]['ArgminPoints'])):
            self.assertAlmostEqual(expected[0]['ArgminPoints'][i][0], result[0]['ArgminPoints'][i][0])
            self.assertAlmostEqual(expected[0]['ArgminPoints'][i][1], result[0]['ArgminPoints'][i][1])


        for i in range(len(expected[1]['UnsignedCurve2Vec'])):self.assertAlmostEqual(expected[1]['UnsignedCurve2Vec'][i], result[1]['UnsignedCurve2Vec'][i])
        for i in range(len(expected[1]['SelectedSegmentsIndex'])):self.assertAlmostEqual(expected[1]['SelectedSegmentsIndex'][i], result[1]['SelectedSegmentsIndex'][i])
        for i in range(len(expected[1]['ArgminPoints'])):
            self.assertAlmostEqual(expected[1]['ArgminPoints'][i][0], result[1]['ArgminPoints'][i][0])
            self.assertAlmostEqual(expected[1]['ArgminPoints'][i][1], result[1]['ArgminPoints'][i][1])



    def test_signed_curve2vec(self):
        
        landmarks=self.landmarks[0]
        trajectories=self.trajectories

        # default signed curve2vec
        expected=np.array([
        [-0.18393972,0,-0.00094883,0.18393972,-0.18393972,0.00094883,0,0.18393972],
        [0,0.0956965,0.19139299,0.36787944,0.01506651,0.19139299,-0.00094883,-0.02356574]
        ])
        
        result=curve2vec(landmarks, trajectories, version='signed')

        for i in range(len(expected[0])):self.assertAlmostEqual(expected[0][i],result[0][i])
        for i in range(len(expected[1])):self.assertAlmostEqual(expected[1][i],result[1][i])


        # change sigma
        expected=np.array([
        [-0.161644699,0,-0.000161426291,0.161644699,-0.161644699,0.000161426291,0,0.161644699],
        [0,0.0665135976,0.133027195,0.323289399,0.00518098527,0.133027195,-0.000161426291,-0.00911206115]
        ])

        result=curve2vec(landmarks, trajectories, version='signed', sigma=0.9)

        for i in range(len(expected[0])):self.assertAlmostEqual(expected[0][i],result[0][i])
        for i in range(len(expected[1])):self.assertAlmostEqual(expected[1][i],result[1][i])

        # segIndx=True
        expected=np.array([
            {'SignedCurve2Vec':np.array([-0.18393972,0,-0.00094883,0.18393972,-0.18393972,0.00094883,0,0.18393972]),
             'SelectedSegmentsIndex':np.array([0, 0, 0, 0, 0, 0, 0, 0]),
            },
            {'SignedCurve2Vec':np.array([0,0.0956965,0.19139299,0.36787944,0.01506651,0.19139299,-0.00094883,-0.02356574]),
             'SelectedSegmentsIndex':np.array([ 0,  0, 10,  0,  9,  5, 11, 12]),
            }
        ])

        result=curve2vec(landmarks, trajectories, version='signed', segIndx=True)

        for i in range(len(expected[0]['SignedCurve2Vec'])):self.assertAlmostEqual(expected[0]['SignedCurve2Vec'][i], result[0]['SignedCurve2Vec'][i])
        for i in range(len(expected[0]['SelectedSegmentsIndex'])):self.assertAlmostEqual(expected[0]['SelectedSegmentsIndex'][i], result[0]['SelectedSegmentsIndex'][i])

        for i in range(len(expected[1]['SignedCurve2Vec'])):self.assertAlmostEqual(expected[1]['SignedCurve2Vec'][i], result[1]['SignedCurve2Vec'][i])
        for i in range(len(expected[1]['SelectedSegmentsIndex'])):self.assertAlmostEqual(expected[1]['SelectedSegmentsIndex'][i], result[1]['SelectedSegmentsIndex'][i])


        # argPnts=True
        expected=np.array([
            {'SignedCurve2Vec':np.array([-0.18393972,0,-0.00094883,0.18393972,-0.18393972,0.00094883,0,0.18393972]),
             'ArgminPoints':np.array([ [-2,2], [-2,2], [0,0], [-2,2], [2,-2], [0,0], [2,-2], [2,-2] ])
            },
            {'SignedCurve2Vec':np.array([0,0.0956965,0.19139299,0.36787944,0.01506651,0.19139299,-0.00094883,-0.02356574]),
             'ArgminPoints':np.array([ [-2,2], [-2,2], [-1,-1], [-2,2], [0,-2], [1,1], [1,-1], [1.5,-0.5] ])
            }
        ])

        result=curve2vec(landmarks, trajectories, version='signed', argPnts=True)

        for i in range(len(expected[0]['SignedCurve2Vec'])):self.assertAlmostEqual(expected[0]['SignedCurve2Vec'][i], result[0]['SignedCurve2Vec'][i])
        for i in range(len(expected[0]['ArgminPoints'])):
            self.assertAlmostEqual(expected[0]['ArgminPoints'][i][0], result[0]['ArgminPoints'][i][0])
            self.assertAlmostEqual(expected[0]['ArgminPoints'][i][1], result[0]['ArgminPoints'][i][1])


        for i in range(len(expected[1]['SignedCurve2Vec'])):self.assertAlmostEqual(expected[1]['SignedCurve2Vec'][i], result[1]['SignedCurve2Vec'][i])
        for i in range(len(expected[1]['ArgminPoints'])):
            self.assertAlmostEqual(expected[1]['ArgminPoints'][i][0], result[1]['ArgminPoints'][i][0])
            self.assertAlmostEqual(expected[1]['ArgminPoints'][i][1], result[1]['ArgminPoints'][i][1])


        # segIndx=True and argPnts=True
        expected=np.array([
            {'SignedCurve2Vec':np.array([-0.18393972,0,-0.00094883,0.18393972,-0.18393972,0.00094883,0,0.18393972]),
             'SelectedSegmentsIndex':np.array([0, 0, 0, 0, 0, 0, 0, 0]),
             'ArgminPoints':np.array([ [-2,2], [-2,2], [0,0], [-2,2], [2,-2], [0,0], [2,-2], [2,-2] ])
            },
            {'SignedCurve2Vec':np.array([0,0.0956965,0.19139299,0.36787944,0.01506651,0.19139299,-0.00094883,-0.02356574]),
             'SelectedSegmentsIndex':np.array([ 0,  0, 10,  0,  9,  5, 11, 12]),
             'ArgminPoints':np.array([ [-2,2], [-2,2], [-1,-1], [-2,2], [0,-2], [1,1], [1,-1], [1.5,-0.5] ])
            }
        ])

        result=curve2vec(landmarks, trajectories, version='signed', segIndx=True, argPnts=True)
        
        for i in range(len(expected[0]['SignedCurve2Vec'])):self.assertAlmostEqual(expected[0]['SignedCurve2Vec'][i], result[0]['SignedCurve2Vec'][i])
        for i in range(len(expected[0]['SelectedSegmentsIndex'])):self.assertAlmostEqual(expected[0]['SelectedSegmentsIndex'][i], result[0]['SelectedSegmentsIndex'][i])
        for i in range(len(expected[0]['ArgminPoints'])):
            self.assertAlmostEqual(expected[0]['ArgminPoints'][i][0], result[0]['ArgminPoints'][i][0])
            self.assertAlmostEqual(expected[0]['ArgminPoints'][i][1], result[0]['ArgminPoints'][i][1])


        for i in range(len(expected[1]['SignedCurve2Vec'])):self.assertAlmostEqual(expected[1]['SignedCurve2Vec'][i], result[1]['SignedCurve2Vec'][i])
        for i in range(len(expected[1]['SelectedSegmentsIndex'])):self.assertAlmostEqual(expected[1]['SelectedSegmentsIndex'][i], result[1]['SelectedSegmentsIndex'][i])
        for i in range(len(expected[1]['ArgminPoints'])):
            self.assertAlmostEqual(expected[1]['ArgminPoints'][i][0], result[1]['ArgminPoints'][i][0])
            self.assertAlmostEqual(expected[1]['ArgminPoints'][i][1], result[1]['ArgminPoints'][i][1])








                         
