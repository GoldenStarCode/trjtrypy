import numpy as np
import itertools
import copy


class DistsBase:
    '''
        ___________________________________Goal___________________________________
      |                                                                            |
      |   This class includes base computations for distances which are given      |
      |   in this package. Base computations consists of computing distance of     |
      |   a point from a segment. The signed localized distance of a point         |
      |   from a segment is available too. The sign in the signed version shows    |
      |   the situation of a point with respect to the segment's direction.        |
      |                                                                            |
      | * Notice that allowable curves here are composed of line segments, namely, |
      |   trajectories(also called piecewise linear curves or polygons).           |
      |                                                                            |
      | * In signed version if a point selects an endpoint of a line segment,      |
      |   then, according to the related reference, the distance will be measured  |
      |   by the local l^infinty norm.                                             |
      |                                                                            |
      | * Here landmarks and points are used interchangably.                       |                  
      |____________________________________________________________________________|

        ________Details for understanding the functionality of this class_________
      |                                                                            |
      |     In this class the vectorized form of a method introduced               |
      |     in following link is implemented:                                      |    
      |                                                                            |
      |        https://www.fundza.com/vectors/point2line/index.html                |
      |                                                                            |
      |     The approach is as follows:                                            |
      |                                                                            |
      |     1. The above method is defined for a point and a line segment.         |
      |                                                                            |
      |         point1       segment1 ---> distance(point1, segment1)--> answer    |
      |                                                                            |
      |     2. Now we generalize it to a point and a number of line segments:      |
      |        (distance of a point from a curve)                                  |
      |                                                                            |
      |                      segment1  ---> distance(point1, segment1)|            |
      |                      segment2  ---> distance(point1, segment2)|            |
      |         point1       segment3  ---> distance(point1, segment3)|--> answer is the minimum of these distances
      |                      segment4  ---> distance(point1, segment4)|            |
      |                      segment5  ---> distance(point1, segment5)|            |
      |                                                                            |
      |     3. Considering this extension, it is easy to generalize                |
      |        this method to a set of points and a set of segments as follows:    |
      |           Assume our curve has 5 segments and we want                      |
      |           to find the distance of 3 points from this curve.                |
      |                                                                            |
      |                      segment1  ---> distance(point1, segment1)|            |
      |                      segment2  ---> distance(point1, segment2)|            |
      |         point1       segment3  ---> distance(point1, segment3)|--> answer is the minimum of five distances
      |                      segment4  ---> distance(point1, segment4)|            |
      |                      segment5  ---> distance(point1, segment5)|            |
      |                                                                            |
      |                      segment1  ---> distance(point2, segment1)|            |
      |                      segment2  ---> distance(point2, segment2)|            |
      |         point2       segment3  ---> distance(point2, segment3)|--> answer is the minimum of five distances
      |                      segment4  ---> distance(point2, segment4)|            |
      |                      segment5  ---> distance(point2, segment5)|            |
      |                                                                            |
      |                      segment1  ---> distance(point3, segment1)|            |
      |                      segment2  ---> distance(point3, segment2)|            |
      |         point3       segment3  ---> distance(point3, segment3)|--> answer is the minimum of five distances
      |                      segment4  ---> distance(point3, segment4)|            |
      |                      segment5  ---> distance(point3, segment5)|            |
      |____________________________________________________________________________|

    '''
    warning=False
    def __init__(self):
        self.pnts=None
        self.sgmnts=None
        self.SgmntsSPnt=None
        self.SgmntsSPntMat=None
        self.SgmntTyp={'[1,0]':'1', '[1,1]':'2', '[0,1]':'3', '[-1,1]':'4', '[-1,0]':'5', '[-1,-1]':'6', '[0,-1]':'7', '[1,-1]':'8'}
        self.AnglTyp=np.array([np.roll(np.array(['IP', '-1', '-1', '-1', 'B', '+1', '+1', '+1']),i) for i in range(8)])

        self.crv=None
        self.SgmntsMat=None
        self.SgmntRspctdPntsVecMat=None
        self.Ts=None
        self.NstPntsVecForm=None
        self.DistsVec=None
        self.i=None
        self.j=None
        self.UnsignedDist=None
        self.SlctdSgmnts=None
        self.SlctdPntsOnSgmntsMat=None
        self.SlctdPntsOnSgmnts=None

        self.RshpdTs=None
        self.PntsIndx=None
        self.PntsRspctdSgmntIndx=None
        self.PntsRspctdSgmntPrt=None
        self.PntsRspctdDist=None
        self.SignedDistances=None


        


        

    def SetPnts(self, pnts):
        self.pnts=pnts
        return
    def SetSgmnts(self, sgmnts):
        self.sgmnts=sgmnts
        return
    def SetSgmntsSPnt(self, SgmntsSPnt, pntslen):
        self.SgmntsSPnt=SgmntsSPnt
        self.SgmntsSPntMat=np.tile(SgmntsSPnt,(pntslen, 1))
        return
    def UnsetAll(self):
        self.pnts=None
        self.sgmnts=None
        self.SgmntsSPnt=None
        self.SgmntsSPntMat=None
        self.crv=None
        self.SgmntsMat=None
        self.SgmntRspctdPntsVecMat=None
        self.Ts=None
        self.NstPntsVecForm=None
        self.DistsVec=None
        self.i=None
        self.j=None
        self.UnsignedDist=None
        self.RshpdTs=None
        self.PntsIndx=None
        self.PntsRspctdSgmntIndx=None
        self.PntsRspctdSgmntPrt=None
        self.PntsRspctdDist=None
        self.SlctdSgmnts=None
        self.SlctdPntsOnSgmntsMat=None
        self.SlctdPntsOnSgmnts=None
        self.SignedDist=None
        return



    def SgmntsPntsToMat(self, crv, pnts):
        '''

            Usage 
                   Transforms all segments of curve crv and points pnts to an array form,
                   in order to take the advantage of vectorized operations. It also
                   calls two functions "SetSgmnts" and "SetSgmntsSPnt", to pass values to
                   self.sgmnts, self.SgmntsSPnt and self.SgmntsSPntMat for maintaining
                   segments, start points of segments and array form of the start points.
            
            ------------------------------------------------------------------------------------
            Parameters
                         crv: ndarray of shape (len(crv), 2) #len(crv) = number of waypoints
                         of crv.
                              It is the curve that we would like to calculate the distance of
                              points from it.
                    
                        pnts: ndarray of shape (len(pnts), 2)
                              The points aimed to measure their distance from the curve crv.
                              
            ------------------------------------------------------------------------------------
            Returns
                                 SgmntsMat: ndarray of shape (len(crv), 2)
                                            Vertical concatination of len(pnts) times the array
                                            of curve's segments by itself.
                    
                     SgmntRspctdPntsVecMat: ndarray of shape (len(crv), 2)
                                            An array that contains points' associated vectors to
                                            the start of each segment's vector.
                                            
        '''
        SgmntsSPnt=crv[:-1]
        SgmntsEPnt=crv[1:]
        sgmnts=np.subtract(SgmntsEPnt, SgmntsSPnt)

        self.SetSgmnts(sgmnts)
        self.SetSgmntsSPnt(SgmntsSPnt, len(pnts))

        SgmntsMat=np.tile(sgmnts,(len(pnts), 1))

        
        PntsVec=np.repeat(pnts, len(SgmntsSPnt), axis=0)
        SgmntRspctdPntsVecMat=np.subtract(PntsVec, self.SgmntsSPntMat)
        return SgmntsMat,SgmntRspctdPntsVecMat





    def TsVec(self, SgmntRspctdPntsVecMat, SgmntsMat):
        '''

            Usage
                   Gives the associated t's to points and segments.
            
            ------------------------------------------------------------------------------------
            Parameters
                        SgmntRspctdPntsVecMat: ndarray of shape (len(crv), 2)
                                               An array containing points' associated vector to
                                               the start of
                                               each segment vector.
                    
                                   SgmntsMat: ndarray of shape (len(crv), 2)
                                              Vertical concatination of len(pnts) times the array
                                              of curve segments by itself.
                                              
            ------------------------------------------------------------------------------------
            Returns
                     Ts: ndarray of shape (len(points)*len(crv)-1), 1)
                         Corresponding t's of points and segments.
                    
                    
        '''
        SRPsVecDotSVec=np.array([np.einsum('ij,ij->i', SgmntRspctdPntsVecMat, SgmntsMat)]).T

        NormVec=np.array([np.linalg.norm(SgmntsMat, axis=1)]).T
        SgmntsLenVec=np.einsum('...i,...i->...i', NormVec, NormVec)

        
        SgmntsLenRvrsVec=np.divide(1, SgmntsLenVec)
        

        Ts=np.einsum('...i,...i->...i', SgmntsLenRvrsVec, SRPsVecDotSVec)

        Ts=np.clip(Ts, 0, 1)

        return Ts







    def Norm2(self, mat1, mat2):
        '''

            Usage
                   Computes row-wise 2-norm of two (n, 2) shape arrays.
            
            ------------------------------------------------------------------------
            Parameters
                        mat1: ndarray of shape (len(mat1), 2)
                              An array with coordinats of a 2d vector in each row.

                        mat2: ndarray of shape (len(mat2), 2)
                              An array with coordinats of a 2d vector in each row.

                        * len(mat1) = len(mat2)
                        
            ------------------------------------------------------------------------
            Returns
                     ndarray
                     An array of shape (len(mat1), 1), consisting of row-wise
                     2-norm of mat1 and mat2.
                
        '''
        return np.array([np.linalg.norm(np.subtract(mat1, mat2), axis=1)]).T


    def APntSetDistACrv(self, pnts, crv, ArgminPnts=False, InUse=False):
        '''

            Usage
                   Computes distance of each point in a set of points (pnts) from
                   a curve (crv) simultaneously.
            
            ------------------------------------------------------------------------------------
            Parameters   
                              pnts: ndarray of shape (len(pnts), 2)
                                    An array that contains coordinates of points in pnts in each
                                    row. 

                               crv: ndarray of shape (len(crv), 2)
                                    An array that contains the waypoints of the curve crv
                                    consecutively.

                        ArgminPnts: bool (True, False), default=False
                                    By being True or False it determines whether the nearest
                                    points on the curve crv to points pnts to be computed and
                                    outputted or not.

                             InUse: bool (True, False), default=False
                                    Setting True or False specifies if all the computed values 
                                    inside this function to be maintained or not.
                                    
            ------------------------------------------------------------------------------------
            Returns
                     UnsignedDist: ndarray of shape (1, len(pnts))
                                   An array containing the distance of each point in pnts from
                                   the input curve crv.
            
        '''
        self.crv=np.array([i[0] for i in itertools.groupby(crv.tolist())])

        self.SgmntsMat, self.SgmntRspctdPntsVecMat = self.SgmntsPntsToMat(self.crv, pnts)

        self.Ts = self.TsVec(self.SgmntRspctdPntsVecMat, self.SgmntsMat)

        self.NstPntsVecForm = np.einsum('...i,...i->...i', self.SgmntsMat, self.Ts)

        self.DistsVec = self.Norm2(self.NstPntsVecForm, self.SgmntRspctdPntsVecMat)

        self.i, self.j = len(pnts), int(len(self.DistsVec)/len(pnts))

        RshpdDistsVec=self.DistsVec.reshape(self.i, self.j)

        self.UnsignedDist=np.amin(RshpdDistsVec , axis=1)
        
        self.SlctdSgmnts=np.argmin(RshpdDistsVec , axis=1)

        if InUse:
            if ArgminPnts:
                self.SlctdPntsOnSgmntsMat=np.add(self.NstPntsVecForm, self.SgmntsSPntMat)
                self.SlctdPntsOnSgmnts=[]
                count=0
                for i in range(0, len(self.SlctdPntsOnSgmntsMat), len(self.sgmnts)):
                    self.SlctdPntsOnSgmnts.append(list(self.SlctdPntsOnSgmntsMat[i:i+len(self.sgmnts)][self.SlctdSgmnts[count]]))
                    count+=1
                return self.UnsignedDist 
            else: return self.UnsignedDist
        else:
            out=copy.copy(self.UnsignedDist)
            self.UnsetAll()
            return out

        

        
 
    def EsChozSignDist(self, PntIndx, PntRspctdSgmntIndx, PntRspctdDist):
        '''

            Usage
                   Computes signed distance of points that select an endpoint of
                   the given curve from corresponding endpoints. 
                   This process is written according to the metric introduced in 
                   the related reference.

            ------------------------------------------------------------------------------------
            Parameters          
                                   PntIndx: int
                                            The index of the point that chooses an endpoint.

                        PntRspctdSgmntIndx: int
                                            The index of a segment which is chosen by the point.
                                            It has just two possible values: the index of the  
                                            first or last segment of the curve crv.

                             PntRspctdDist: float
                                            The 2-norm distance of a point from the curve.
                                            
            ------------------------------------------------------------------------------------
            Returns
                     float
                     The signed l^infity distance of a point that 
                     chooses an endpoint of the curve from that endpoint.

                    
        '''

        LHand=[-1*self.sgmnts[PntRspctdSgmntIndx][1],self.sgmnts[PntRspctdSgmntIndx][0]]
        LHandNorm=np.linalg.norm(LHand)
            
        if PntRspctdSgmntIndx==0:
                
            SPnt=self.SgmntsSPnt[PntRspctdSgmntIndx]
                
            SgmntRspctdPntVec=self.pnts[PntIndx]-SPnt
                
            Sign=np.dot(LHand,SgmntRspctdPntVec)/LHandNorm
                
            vrtcl=np.absolute(np.dot(LHand,SgmntRspctdPntVec)/LHandNorm)
                
            hrzntl=np.sqrt(PntRspctdDist**2-vrtcl**2)
                
            if PntRspctdDist == 0: return 0
            else: return Sign*max(vrtcl,hrzntl)/(PntRspctdDist)

        else:
            SPnt=self.SgmntsSPnt[PntRspctdSgmntIndx]
                
            EPnt=SPnt+self.sgmnts[PntRspctdSgmntIndx]
                
            SgmntRspctdPntVec=self.pnts[PntIndx]-EPnt
                
            Sign=np.dot(LHand,SgmntRspctdPntVec)/LHandNorm
                
            vrtcl=np.absolute(np.dot(LHand,SgmntRspctdPntVec)/LHandNorm)
                
            hrzntl=np.sqrt(PntRspctdDist**2-vrtcl**2)
            if PntRspctdDist == 0: return 0
            else: return Sign*max(vrtcl,hrzntl)/(PntRspctdDist)
            





    def MidlChozSignDist(self, PntIndx, PntRspctdSgmntIndx, PntRspctdSgmntPrt, PntRspctdDist ):
        '''

            Usage
                   Computes signed distance of points that select a middle point
                   of a segment of the given curve as argmin point.

            ------------------------------------------------------------------------------------
            Parameters            
                                   PntIndx: int
                                            The index of the point that chooses an endpoint.

                        PntRspctdSgmntIndx: int
                                            The index of a segment which is chosen by the point.
                                            It has just two possible values: the index of  
                                            the first or last segment of the curve crv.
                                     
                         PntRspctdSgmntPrt: float
                                            The corresponding t value with respect to PntIndx
                                            and PntRspctdSgmntIndx. 

                            PntRspctdDist: float
                                           The 2-norm distance of a point from the curve.
                                           
            ------------------------------------------------------------------------------------
            Returns
                     float
                     The signed distance of a point that chooses a middle point of the
                     given curve.
                
        '''
        if PntRspctdSgmntPrt==1 or PntRspctdSgmntPrt==0: # PntRspctdSgmntPrt==0 is chosen because of approximation errors in calculations

                PntRspctdSgmntIndx=PntRspctdSgmntIndx-int(not PntRspctdSgmntPrt)

                PntRspctdSgmntTyp=self.SgmntTyp[str(list(np.sign(self.sgmnts[PntRspctdSgmntIndx]).astype(int))).replace(" ","")]

                PntNxtRspctdSgmntTyp=self.SgmntTyp[str(list(np.sign(self.sgmnts[(PntRspctdSgmntIndx+1)%len(self.sgmnts)]).astype(int))).replace(" ","")]

                AngTyp=str(self.AnglTyp[int(PntRspctdSgmntTyp)-1, int(PntNxtRspctdSgmntTyp)-1 ])

                if AngTyp=='+1' or AngTyp=='-1': return int(AngTyp)*PntRspctdDist
                elif AngTyp=='IP':
                    LHand=[-1*self.sgmnts[PntRspctdSgmntIndx][1],self.sgmnts[PntRspctdSgmntIndx][0]]
                    
                    SgmntRspctdPntVec=self.pnts[PntIndx]-self.SgmntsSPnt[PntRspctdSgmntIndx]
                    
                    dot=np.dot(LHand, SgmntRspctdPntVec)
                    
                    if dot>0:return 1*PntRspctdDist
                    else:return -1*PntRspctdDist

                else:
                    cross=np.cross(self.sgmnts[PntRspctdSgmntIndx], self.sgmnts[(PntRspctdSgmntIndx+1)%len(self.sgmnts)])

                    if not cross==0:return -1*np.sign(cross)*PntRspctdDist

                    else:

                      if not self.warning:

                          print('Warning:','Some of the landmarks have chosen overlapped segments of some trajectories')
                                            
                          DistsBase.warning=True

                          return PntRspctdDist

                      else: return PntRspctdDist

        else:
   
  
                LHand=[-1*self.sgmnts[PntRspctdSgmntIndx][1], self.sgmnts[PntRspctdSgmntIndx][0]]
  
                SgmntRspctdPntVec=self.pnts[PntIndx]-self.SgmntsSPnt[PntRspctdSgmntIndx]

                dot=np.dot(LHand, SgmntRspctdPntVec)
     
                if dot>0:return 1*PntRspctdDist
                else:return -1*PntRspctdDist





    def SignPnt(self, PntIndx, PntRspctdSgmntIndx, PntRspctdSgmntPrt, PntRspctdDist):
        '''

              Usage
                     Computes signed distance of a point from a curve.

              ------------------------------------------------------------------------------------
              Parameters              
                                     PntIndx: int
                                              The index of the point that chooses an endpoint.

                          PntRspctdSgmntIndx: int
                                              The index of a segment which is chosen by the point.
                                              It has just two possible values: the index of  
                                              the first or last segment of the curve crv.
                                         
                          PntRspctdSgmntPrt: float
                                             The corresponding t value with respect to PntIndx
                                             and PntRspctdSgmntIndx. 

                              PntRspctdDist: float
                                             The 2-norm distance of a point from the curve.

              ------------------------------------------------------------------------------------
              Return 
                      float
                      The signed distance of a point from a curve.

        '''
        
        if (PntRspctdSgmntIndx, PntRspctdSgmntPrt)==(0, 0):

            return self.EsChozSignDist(PntIndx, 0, PntRspctdDist)

        elif (PntRspctdSgmntIndx, PntRspctdSgmntPrt)==(len(self.sgmnts)-1, 1):

            return self.EsChozSignDist(PntIndx, len(self.sgmnts)-1, PntRspctdDist) 

        else:

            return self.MidlChozSignDist(PntIndx, PntRspctdSgmntIndx, PntRspctdSgmntPrt, PntRspctdDist)
            






    def APntSetSignedDistACrv(self, pnts, crv, sigma=1, ArgminPnts=False, InUse=False):
        '''

            Usage
                   Computes signed distance of each point in a set of points (pnts) from
                   a curve (crv) simultaneously.
                   
            ------------------------------------------------------------------------------------
            Parameters     
                              pnts: ndarray of shape (len(pnts), 2)
                                    An array that contains coordinates of points in
                                    pnts in each row. 

                               crv: ndarray of shape (len(crv), 2)
                                    An array that contains the waypoints of the curve crv
                                    consecutively.
                        
                             sigma: float, default=1 
                                    A positve real number specifying the Gaussian weight
                                    parameter employed in the definition of the signed
                                    feature mapping. So, it will be effective only when
                                    version='signed'.

                        ArgminPnts: bool (True, False), default=False
                                    By being True or False it determines whether the nearest
                                    points on the curve crv to points pnts to be computed and
                                    outputted or not.

                             InUse: bool (True, False), default=False
                                    Setting True or False specifies if all the computed values
                                    inside this function to be maintained or not.
                             
            ------------------------------------------------------------------------------------
            Return
                    SignedDist: ndarray of shape (1, len(pnts))
                                An array that includes the signed distance of each point 
                                from the input curve.

        '''
        Invsigma2=1/(float(sigma)**2)
          
        self.APntSetDistACrv(pnts, crv, ArgminPnts=ArgminPnts, InUse=True)
        
        self.RshpdTs=self.Ts.reshape(self.i, self.j)
                
        self.PntsIndx=np.arange(len(pnts))

        self.PntsRspctdSgmntIndx=np.argmin(self.DistsVec.reshape(self.i,self.j), axis=1)

        self.PntsRspctdSgmntPrt=np.diag(self.RshpdTs.T[self.PntsRspctdSgmntIndx])

        self.PntsRspctdDist=np.amin(self.DistsVec.reshape(self.i,self.j), axis=1)

        self.SetPnts(pnts)
        # These are setted by SetSgmntSPnt function while calling APntSetDistACrv function
        #self.SetSgmnts(self.crv[1:]-self.crv[:-1])
        #self.SetSgmntsSPnt(self.crv[:-1],len(pnts))

        if crv[0][0]==crv[-1][0] and crv[0][1]==crv[-1][1]:

            SignedDist=np.array(list(map(self.MidlChozSignDist, self.PntsIndx, self.PntsRspctdSgmntIndx, self.PntsRspctdSgmntPrt, self.PntsRspctdDist)))
           
        else:
          
           SignedDist=np.array(list(map(self.SignPnt, self.PntsIndx, self.PntsRspctdSgmntIndx, self.PntsRspctdSgmntPrt, self.PntsRspctdDist)))


        if InUse:
            q_p2=np.einsum( '...i,...i->...i', self.UnsignedDist, self.UnsignedDist )
            self.SignedDist=np.multiply(SignedDist, np.exp(np.multiply(-1*Invsigma2, q_p2)))/float(sigma)
            return self.SignedDist
        else:
            q_p2=np.einsum( '...i,...i->...i', self.UnsignedDist, self.UnsignedDist )
            out=np.multiply(SignedDist, np.exp(np.multiply(-1*Invsigma2, q_p2)))/float(sigma)
            self.UnsetAll()
            return out
