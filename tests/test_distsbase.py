import unittest
import numpy as np
import math
from trjtrypy.distsbase import DistsBase

class TestDistssBase(unittest.TestCase):


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

    def setUp(self):
        self.d=DistsBase()


    def test_SetPnts(self):
        
        pnts=self.landmarks[0]
        expected=pnts
        
        self.d.SetPnts(pnts)
        result=self.d.pnts

        self.assertCountEqual(expected[:,0], result[:,0])
        self.assertCountEqual(expected[:,1], result[:,1])


    def test_SetSgmnts(self):

        sgmnts=self.trajectories[0]
        expected=sgmnts

        self.d.SetSgmnts(sgmnts)
        result=self.d.sgmnts

        self.assertCountEqual(expected[:,0], result[:,0])
        self.assertCountEqual(expected[:,1], result[:,1])


    def test_SetSgmntsSPnt(self):

        SgmntsSPnt=self.trajectories[0][:-1]
        pntslen=len(self.landmarks[0])
        expected1=SgmntsSPnt
        expected2=np.array(list(SgmntsSPnt)*pntslen)

        
        self.d.SetSgmntsSPnt(SgmntsSPnt, pntslen)
        result1=self.d.SgmntsSPnt
        result2=self.d.SgmntsSPntMat


        self.assertCountEqual(expected1[:,0], result1[:,0])
        self.assertCountEqual(expected1[:,1], result1[:,1])

        self.assertCountEqual(expected2[:,0], result2[:,0])
        self.assertCountEqual(expected2[:,1], result2[:,1])
        

    def test_UnsetAll(self):
        
        self.d.pnts=self.landmarks[0]
        self.d.sgmnts=self.trajectories[0]
        self.d.SgmntsSPnt=self.trajectories[0]
        self.d.SgmntsSPntMat=self.trajectories[0]
        self.d.crv=self.trajectories[0]
        self.d.SgmntsMat=self.trajectories[0]
        self.d.SgmntRspctdPntsVecMat=self.trajectories[0]
        self.d.Ts=self.trajectories[0][:,0]
        self.d.NstPntsVecForm=self.landmarks[0]
        self.d.DistsVec=self.trajectories[0][:,0]
        self.d.i=1
        self.d.j=1
        self.d.UnsignedDist=self.trajectories[0][:,0]
        self.d.RshpdTs=self.trajectories[0][:,0]
        self.d.PntsIndx=[3,5,1,7,43,234,45,768,89,34,324,45,2,34,76,4,23,5,7,5,4,324,2]
        self.d.PntsRspctdSgmntIndx=[3,5,1,7,43,234,45,768,89,34,324,45,2,34,76,4,23,5,7,5,4,324,2]
        self.d.PntsRspctdSgmntPrt=self.trajectories[0][:,0]
        self.d.PntsRspctdDist=self.trajectories[0][:,0]
        self.d.SlctdSgmnts=[3,5,1,7,43,234,45,768,89,34,324,45,2,34,76,4,23,5,7,5,4,324,2]
        self.d.SlctdPntsOnSgmntsMat=self.trajectories[0]
        self.d.SlctdPntsOnSgmnts=self.trajectories[0]
        self.d.SignedDist=self.trajectories[0][:,0]


        self.d.UnsetAll()
        
        self.assertIsNone(self.d.pnts)
        self.assertIsNone(self.d.sgmnts)
        self.assertIsNone(self.d.SgmntsSPnt)
        self.assertIsNone(self.d.crv)
        self.assertIsNone(self.d.SgmntsMat)
        self.assertIsNone(self.d.SgmntRspctdPntsVecMat)
        self.assertIsNone(self.d.Ts)
        self.assertIsNone(self.d.NstPntsVecForm)
        self.assertIsNone(self.d.DistsVec)
        self.assertIsNone(self.d.i)
        self.assertIsNone(self.d.j)
        self.assertIsNone(self.d.UnsignedDist)
        self.assertIsNone(self.d.RshpdTs)
        self.assertIsNone(self.d.PntsIndx)
        self.assertIsNone(self.d.PntsRspctdSgmntIndx)
        self.assertIsNone(self.d.PntsRspctdSgmntPrt)
        self.assertIsNone(self.d.PntsRspctdDist)
        self.assertIsNone(self.d.SlctdSgmnts)
        self.assertIsNone(self.d.SlctdPntsOnSgmntsMat)
        self.assertIsNone(self.d.SlctdPntsOnSgmnts)
        self.assertIsNone(self.d.SignedDist)



    def test_SgmntsPntsToMat(self):

        crv=self.trajectories[1]
        pnts=self.landmarks[0]
        
        
        
        expected1=np.array([
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1]
        ])

        expected2=np.array([
        [-1,0], [-2,1], [0,-3], [-1,3], [3,-4], [2,0], [2,-4], [3,-3], [-3,2], [-3,4], [-2,0], [-1,4], [1,-2],
        [ 4,0], [4,-5], [5,-3], [-2,2], [-2,2], [-2,-4], [-3,2], [2,-4], [2,2], [3,-2], [3,0], [-2,3], [-4,4],
        [0,-4], [-1,1], [ 4,-4], [3,2], [4,-4], [3,-4], [-4,1], [-3,2], [-2,-2], [-2,4], [2,-1], [3,3], [2,-2],
        [5,-4], [-2,0], [-1,2], [-1,-2], [-1,2], [2,-5], [1,1], [3,-4], [3,-2], [-3,3], [-3,5], [-1,-1], [-3,4],
        [ 4,-5], [3,0], [5,-4], [4,-2], [-2,1], [-3,1], [-3,-3], [-2,2], [2,-3], [2,3], [3,-1], [4,-1], [-4,3],
        [-1,1], [-1,-4], [0,2], [3,-3], [3,1], [3,-5], [2,-3], [-3,1], [-3,3], [-2,-1], [-2,5], [3,-2], [1,3],
        [5,-5], [4,-4], [-1,1], [-2,3], [-1,-3], [-2,1], [1,-4], [2,1], [3,-3], [ 3,-1], [-3,4], [-2,4], [-3,-1],
        [ 0,1], [ 3,-5], [4,1], [4,-3], [4,-3], [-3,0], [-4,2], [-2,-3], [-2,3], [2,-2], [2,4], [4,-2], [2,-1],
        ])

        result1,result2=self.d.SgmntsPntsToMat(crv, pnts)

        self.assertCountEqual(expected1[:,0], result1[:,0])
        self.assertCountEqual(expected1[:,1], result1[:,1])

        self.assertCountEqual(expected2[:,0], result2[:,0])
        self.assertCountEqual(expected2[:,1], result2[:,1])

    
        expected3=np.array([
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        ])
        expected4=crv[:-1]
        expected5=np.array(
        8*list(crv[:-1])
        )

        result3=self.d.sgmnts
        result4=self.d.SgmntsSPnt
        result5=self.d.SgmntsSPntMat


        self.assertCountEqual(expected3[:,0], result3[:,0])
        self.assertCountEqual(expected3[:,1], result3[:,1])

        self.assertCountEqual(expected4[:,0], result4[:,0])
        self.assertCountEqual(expected4[:,1], result4[:,1])

        self.assertCountEqual(expected5[:,0], result5[:,0])
        self.assertCountEqual(expected5[:,1], result5[:,1])


    def test_TsVec(self):
        
        SgmntRspctdPntsVecMat=np.array([
        [-1,0], [-2,1], [0,-3], [-1,3], [3,-4], [2,0], [2,-4], [3,-3], [-3,2], [-3,4], [-2,0], [-1,4], [1,-2],
        [ 4,0], [4,-5], [5,-3], [-2,2], [-2,2], [-2,-4], [-3,2], [2,-4], [2,2], [3,-2], [3,0], [-2,3], [-4,4],
        [0,-4], [-1,1], [ 4,-4], [3,2], [4,-4], [3,-4], [-4,1], [-3,2], [-2,-2], [-2,4], [2,-1], [3,3], [2,-2],
        [5,-4], [-2,0], [-1,2], [-1,-2], [-1,2], [2,-5], [1,1], [3,-4], [3,-2], [-3,3], [-3,5], [-1,-1], [-3,4],
        [ 4,-5], [3,0], [5,-4], [4,-2], [-2,1], [-3,1], [-3,-3], [-2,2], [2,-3], [2,3], [3,-1], [4,-1], [-4,3],
        [-1,1], [-1,-4], [0,2], [3,-3], [3,1], [3,-5], [2,-3], [-3,1], [-3,3], [-2,-1], [-2,5], [3,-2], [1,3],
        [5,-5], [4,-4], [-1,1], [-2,3], [-1,-3], [-2,1], [1,-4], [2,1], [3,-3], [ 3,-1], [-3,4], [-2,4], [-3,-1],
        [ 0,1], [ 3,-5], [4,1], [4,-3], [4,-3], [-3,0], [-4,2], [-2,-3], [-2,3], [2,-2], [2,4], [4,-2], [2,-1],
        ])
        SgmntsMat=np.array([
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1],
        [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1]
        ])

        expected=np.array([
        [0], [0.5], [1], [1], [0], [1], [0], [1], [0], [0], [1], [0], [0],
        [1], [0.5], [1], [1], [0], [1], [1], [1], [0], [1], [0], [0], [0],
        [0], [0], [1], [1], [0], [1], [1], [0], [1], [0], [0], [1], [0],
        [1], [1], [0], [0], [0.5], [1], [0], [1], [1], [0], [1], [0], [0.5],
        [1], [0], [1], [0], [0], [0], [1], [0], [1], [0], [0], [1], [0],
        [0], [1], [0], [0], [1], [1], [0], [0], [0], [1], [1], [1], [1],
        [1], [0], [0], [1], [0], [0], [0], [0], [1], [1], [1], [0], [0],
        [0], [1], [1], [0], [0.5], [0], [1], [1], [0], [1], [1], [1], [0.5]
        ])

        result=self.d.TsVec(SgmntRspctdPntsVecMat, SgmntsMat)


        for i in range(len(expected)):self.assertAlmostEqual(expected[i][0], result[i][0])
          
    def test_Norm2(self):
        
        mat1=np.array([
            [3,4],
            [2,3],
            [5,8],
            [1,2],
            [7,8]
        ])

        mat2=np.array([
            [1,1],
            [0,2],
            [4,3],
            [6,9],
            [8,2]
        ])

        expected=np.array([
            [3.6055512755],
            [2.2360679775],
            [5.0990195136],
            [8.602325267],
            [6.0827625303]
        ])

        result=self.d.Norm2(mat1, mat2)

        
        for i in range(len(expected)):self.assertAlmostEqual(expected[i][0], result[i][0])

    def test_APntSetDistACrv(self):

        pnts=self.landmarks[1]
        crv=self.trajectories[1]

        # default APntSetDistACrv
        expected1=np.array([0.7071067812,0.5,0.7071067812,0.7071067812,0.3535533906,0.5,0.5,0.5,0.3535533906,0.3535533906,0.5,0,0.7071067812,0.5,0.5,0.7071067812])

        result1=self.d.APntSetDistACrv(pnts, crv)

        for i in range(len(expected1)):self.assertAlmostEqual(expected1[i], result1[i])

        # InUse=True
        expected2=expected1

        result2=self.d.APntSetDistACrv(pnts, crv, InUse=True)
        
        for i in range(len(expected2)):self.assertAlmostEqual(expected2[i], result2[i])

   
        self.assertIsNotNone(self.d.sgmnts)
        self.assertIsNotNone(self.d.SgmntsSPnt)
        self.assertIsNotNone(self.d.crv)
        self.assertIsNotNone(self.d.SgmntsMat)
        self.assertIsNotNone(self.d.SgmntRspctdPntsVecMat)
        self.assertIsNotNone(self.d.Ts)
        self.assertIsNotNone(self.d.NstPntsVecForm)
        self.assertIsNotNone(self.d.DistsVec)
        self.assertIsNotNone(self.d.i)
        self.assertIsNotNone(self.d.j)
        self.assertIsNotNone(self.d.UnsignedDist)
        self.assertIsNotNone(self.d.SlctdSgmnts)

        # InUse=True and ArgminPnts=True
        self.d.UnsetAll()

        expected3=expected1
        expected4=np.array([
        [-2,2],[-2,2],[-2,2],[-1.5,0.5],[-1.75,1.25],[-1.5,2],
        [0,-0.5],[-1,0.5],[-0.75,1.25],[-0.25,1.75],[0,-0.5],
        [0.5,1.5],[1.5,-0.5],[2,0],[2,0],[2,0]
        ])

        result3=self.d.APntSetDistACrv(pnts, crv, ArgminPnts=True, InUse=True)
        result4=self.d.SlctdPntsOnSgmnts

        for i in range(len(expected3)):self.assertAlmostEqual(expected3[i], result3[i])
        
        for i in range(len(expected4)):self.assertAlmostEqual(expected4[i][0], result4[i][0])
        for i in range(len(expected4)):self.assertAlmostEqual(expected4[i][1], result4[i][1])


        
        self.assertIsNotNone(self.d.sgmnts)
        self.assertIsNotNone(self.d.SgmntsSPnt)
        self.assertIsNotNone(self.d.crv)
        self.assertIsNotNone(self.d.SgmntsMat)
        self.assertIsNotNone(self.d.SgmntRspctdPntsVecMat)
        self.assertIsNotNone(self.d.Ts)
        self.assertIsNotNone(self.d.NstPntsVecForm)
        self.assertIsNotNone(self.d.DistsVec)
        self.assertIsNotNone(self.d.i)
        self.assertIsNotNone(self.d.j)
        self.assertIsNotNone(self.d.UnsignedDist)
        self.assertIsNone(self.d.PntsIndx)
        self.assertIsNone(self.d.PntsRspctdSgmntIndx)
        self.assertIsNone(self.d.PntsRspctdSgmntPrt)
        self.assertIsNone(self.d.PntsRspctdDist)
        self.assertIsNotNone(self.d.SlctdSgmnts)
        self.assertIsNotNone(self.d.SlctdPntsOnSgmntsMat)
        self.assertIsNotNone(self.d.SlctdPntsOnSgmnts)


    def test_EsChozSignDist(self):
        # when choses start point
        PntIndx=0
        PntRspctdSgmntIndx=0
        PntRspctdDist=0.7071067812
        expected=-0.3535533906
        self.d.SetSgmnts(np.array([
            [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1]
        ]))
        self.d.SetSgmntsSPnt(self.trajectories[1][:-1], len(self.landmarks[1]))
        self.d.SetPnts(self.landmarks[1])
        result=self.d.EsChozSignDist(PntIndx, PntRspctdSgmntIndx, PntRspctdDist)
        self.assertAlmostEqual(expected, result)


        PntIndx=1
        PntRspctdSgmntIndx=0
        PntRspctdDist=0.5
        expected=0
        result=self.d.EsChozSignDist(PntIndx, PntRspctdSgmntIndx, PntRspctdDist)
        self.assertAlmostEqual(expected, result)



        PntIndx=2
        PntRspctdSgmntIndx=0
        PntRspctdDist=0.7071067812
        expected=0.3535533906
        result=self.d.EsChozSignDist(PntIndx, PntRspctdSgmntIndx, PntRspctdDist)
        self.assertAlmostEqual(expected, result)

        # when choses end point
        PntIndx=15
        PntRspctdSgmntIndx=12
        PntRspctdDist=0.7071067812
        expected=0
        result=self.d.EsChozSignDist(PntIndx, PntRspctdSgmntIndx, PntRspctdDist)
        self.assertAlmostEqual(expected, result)

        PntIndx=14
        PntRspctdSgmntIndx=12
        PntRspctdDist=0.5
        expected=-0.25
        result=self.d.EsChozSignDist(PntIndx, PntRspctdSgmntIndx, PntRspctdDist)
        self.assertAlmostEqual(expected, result)


    def test_MidlChozSignDist(self):
        
        PntIndx=6
        PntRspctdSgmntIndx=8
        PntRspctdSgmntPrt=0.5
        PntRspctdDist=0.5
        expected=-0.5
        self.d.SetSgmnts(np.array([
            [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1]
        ]))
        self.d.SetSgmntsSPnt(self.trajectories[1][:-1], len(self.landmarks[1]))
        self.d.SetPnts(self.landmarks[1])
        result=self.d.MidlChozSignDist(PntIndx, PntRspctdSgmntIndx, PntRspctdSgmntPrt, PntRspctdDist)
        self.assertAlmostEqual(expected, result)



        

    def test_SignPnt(self):
        
        PntIndx=7
        PntRspctdSgmntIndx=12
        PntRspctdSgmntPrt=0.5
        PntRspctdDist=2.121320343559643
        expected=-2.121320343559643

        self.d.SetSgmnts(np.array([
            [1,0], [-1,-1], [1,-1], [0,1], [1,1], [1,-1], [-1,0], [0,-1], [0,-1], [0,-1], [-1,1], [2,0], [1,1]
        ]))
        self.d.SetSgmntsSPnt(self.trajectories[1][:-1],len(self.landmarks[0]))
        self.d.SetPnts(self.landmarks[0])

        result=self.d.SignPnt(PntIndx, PntRspctdSgmntIndx, PntRspctdSgmntPrt, PntRspctdDist)

        self.assertAlmostEqual(expected, result)
        


    def test_APntSetSignedDistACrv(self):

        pnts=self.landmarks[1]
        crv=self.trajectories[1]

        # default APntSetSignedDistACrv
        expected=np.array([-0.2144409712,0,0.2144409712,-0.4288819424,0.3120097720,0.3894003915,-0.3894003915,-0.3894003915,-0.3120097720,-0.3120097720,0.3894003915,0,-0.4288819424,0.1947001957,-0.1947001957,0])
        
        result=self.d.APntSetSignedDistACrv(pnts, crv)
        
        for i in range(len(expected)):self.assertAlmostEqual(expected[i], result[i])


        # change sigma and ArgminPnts=True and InUse=True
        sigma=0.5
        
        expected1=np.array([
        -0.095696496,0,0.0956964965,-0.191392993,0.428881942,
        0.367879441,-0.367879441,-0.367879441,-0.428881942,
        -0.428881942,0.367879441,0,-0.191392993,0.183939721,-0.183939721,0
        ])
        expected2=np.array([
        [-2,2],[-2,2],[-2,2],[-1.5,0.5],[-1.75,1.25],[-1.5,2],
        [0,-0.5],[-1,0.5],[-0.75,1.25],[-0.25,1.75],[0,-0.5],
        [0.5,1.5],[1.5,-0.5],[2,0],[2,0],[2,0]
        ])

        result1=self.d.APntSetSignedDistACrv(pnts, crv, sigma=sigma, ArgminPnts=True, InUse=True)
        result2=self.d.SlctdPntsOnSgmnts
     
        for i in range(len(expected1)):self.assertAlmostEqual(expected1[i], result1[i])
        for i in range(len(expected2)):
            self.assertAlmostEqual(expected2[i][0], result2[i][0])
            self.assertAlmostEqual(expected2[i][1], result2[i][1])



        self.assertIsNotNone(self.d.pnts)
        self.assertIsNotNone(self.d.sgmnts)
        self.assertIsNotNone(self.d.SgmntsSPnt)
        self.assertIsNotNone(self.d.crv)
        self.assertIsNotNone(self.d.SgmntsMat)
        self.assertIsNotNone(self.d.SgmntRspctdPntsVecMat)
        self.assertIsNotNone(self.d.Ts)
        self.assertIsNotNone(self.d.NstPntsVecForm)
        self.assertIsNotNone(self.d.DistsVec)
        self.assertIsNotNone(self.d.i)
        self.assertIsNotNone(self.d.j)
        self.assertIsNotNone(self.d.UnsignedDist)
        self.assertIsNotNone(self.d.RshpdTs)
        self.assertIsNotNone(self.d.PntsIndx)
        self.assertIsNotNone(self.d.PntsRspctdSgmntIndx)
        self.assertIsNotNone(self.d.PntsRspctdSgmntPrt)
        self.assertIsNotNone(self.d.PntsRspctdDist)
        self.assertIsNotNone(self.d.SlctdSgmnts)
        self.assertIsNotNone(self.d.SlctdPntsOnSgmntsMat)
        self.assertIsNotNone(self.d.SlctdPntsOnSgmnts)
        self.assertIsNotNone(self.d.SignedDist)


        # close curve
        crv=np.array([
        [0,0], [1,0], [1,1], [0,0]
        ])
        pnts=np.array([
        [-1,-1]
        ])
        expected=-0.19139299
        result=self.d.APntSetSignedDistACrv(pnts, crv)[0]
        self.assertAlmostEqual(expected, result)

        # straight curve
        crv=np.array([
        [0,0], [1,0], [2,0]
        ])
        pnts=np.array([
        [1,1]
        ])
        expected=0.36787944
        result=self.d.APntSetSignedDistACrv(pnts, crv)[0]
        self.assertAlmostEqual(expected, result)


        pnts=np.array([
        [1,-1]
        ])
        expected=-0.36787944
        result=self.d.APntSetSignedDistACrv(pnts, crv)[0]
        self.assertAlmostEqual(expected, result)
        

        # problem curve
        crv=np.array([
        [0,0], [1,0], [1,-1], [1,0], [2,0]
        ])
        pnts=np.array([
        [1,-2]
        ])
        expected=0.36787944
        result=self.d.APntSetSignedDistACrv(pnts, crv)[0]
        self.assertAlmostEqual(expected, result)


        pnts=np.array([
        [1,-2], [0,-1]
        ])
        expected=[0.36787944, -0.36787944]
        result=self.d.APntSetSignedDistACrv(pnts, crv)
        for i in range(len(expected)): self.assertAlmostEqual(expected[i], result[i])
        
