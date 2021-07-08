import unittest
import math
import numpy as np
from trjtrypy.basedists import distance

class TestDistance(unittest.TestCase):

   def test_unsigned_distance(self):
      point=np.array([[-0.5, -0.5], [1,1]])

      curve=np.array([[0,1], [1,0]])
      
      # default
      expected=math.sqrt(2)
      result=distance(np.array([point[0]]), np.array([curve]))[0][0]
      
      self.assertAlmostEqual(expected, result)

      # segIndx=True
      expected1=math.sqrt(2)
      expected2=0
      result1=distance(np.array([point[0]]), np.array([curve]), segIndx=True)[0]['UnsignedDistance'][0]
      result2=distance(np.array([point[0]]), np.array([curve]), segIndx=True)[0]['SelectedSegmentsIndex'][0]

      self.assertAlmostEqual(expected1, result1)
      self.assertAlmostEqual(expected2, result2)

      # argPnts=True
      expected1=math.sqrt(2)
      expected2=[0.5, 0.5]
      result1=distance(np.array([point[0]]), np.array([curve]), argPnts=True)[0]['UnsignedDistance'][0]
      result2=distance(np.array([point[0]]), np.array([curve]), argPnts=True)[0]['ArgminPoints'][0]

      self.assertAlmostEqual(expected1, result1)
      for i in range(len(expected2)):self.assertAlmostEqual(expected2[i], result2[i])
      

      # segIndx=True and argPnts=True
      expected1=math.sqrt(2)
      expected2=0
      expected3=[0.5, 0.5]
      result1=distance(np.array([point[0]]), np.array([curve]), segIndx=True, argPnts=True)[0]['UnsignedDistance'][0]
      result2=distance(np.array([point[0]]), np.array([curve]), segIndx=True, argPnts=True)[0]['SelectedSegmentsIndex'][0]
      result3=distance(np.array([point[0]]), np.array([curve]), segIndx=True, argPnts=True)[0]['ArgminPoints'][0]

      self.assertAlmostEqual(expected1, result1)
      self.assertAlmostEqual(expected2, result2)
      for i in range(len(expected3)):self.assertAlmostEqual(expected3[i], result3[i])


   def test_signed_distance(self):
      point=np.array([[-0.5, -0.5], [1,1]])

      curve=np.array([[0,1], [1,0]])
      
      # default
      expected=-1*math.sqrt(2)
      result=distance(np.array([point[0]]), np.array([curve]), version='signed')[0][0]
      
      self.assertAlmostEqual(expected, result)

      # segIndx=True
      expected1=-1*math.sqrt(2)
      expected2=0
      result1=distance(np.array([point[0]]), np.array([curve]), version='signed', segIndx=True)[0]['SignedDistance'][0]
      result2=distance(np.array([point[0]]), np.array([curve]), version='signed', segIndx=True)[0]['SelectedSegmentsIndex'][0]

      self.assertAlmostEqual(expected1, result1)
      self.assertAlmostEqual(expected2, result2)

      # argPnts=True
      expected1=-1*math.sqrt(2)
      expected2=[0.5, 0.5]
      result1=distance(np.array([point[0]]), np.array([curve]), version='signed', argPnts=True)[0]['SignedDistance'][0]
      result2=distance(np.array([point[0]]), np.array([curve]), version='signed', argPnts=True)[0]['ArgminPoints'][0]

      self.assertAlmostEqual(expected1, result1)
      for i in range(len(expected2)):self.assertAlmostEqual(expected2[i], result2[i])
      

      # segIndx=True and argPnts=True
      expected1=-1*math.sqrt(2)
      expected2=0
      expected3=[0.5, 0.5]
      result1=distance(np.array([point[0]]), np.array([curve]), version='signed', segIndx=True, argPnts=True)[0]['SignedDistance'][0]
      result2=distance(np.array([point[0]]), np.array([curve]), version='signed', segIndx=True, argPnts=True)[0]['SelectedSegmentsIndex'][0]
      result3=distance(np.array([point[0]]), np.array([curve]), version='signed', segIndx=True, argPnts=True)[0]['ArgminPoints'][0]

      self.assertAlmostEqual(expected1, result1)
      self.assertAlmostEqual(expected2, result2)
      for i in range(len(expected3)):self.assertAlmostEqual(expected3[i], result3[i])


