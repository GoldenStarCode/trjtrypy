from trjtrypy.distsbase import DistsBase
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def draw_landmarks_trajectory(landmarks, trajectory, version='unsigned', trj=True, lndmarks=True, dists=True, argminpnts=True, zoom=None, figsize=(10,10)):
    '''

      Usage
      
             An interactive visualization tool that allows the user to draw landmarks, 
             trajectory, distances and nearest points of trajectory to the landmarks.

      -----------------------------------------------------------------------------------------------
      Parameters        
                   landmarks: ndarray of shape (len(landmarks), 2)
                              An array containing coordinates of landmarks in each row. 
                            
                  trajectory: ndarray of shape (len(trajectory), 2)
                              An array that contains the waypoints of the trajectory
                              consecutively.

                     version: str ('signed', 'unsigned'), default='unsigned'
                              Determines which version of the feature mappings is utilized.


                         trj: bool (True, False), default=True
                              Being True or False specifies whether the trajectory should be drawn
                              or not.

                    lndmarks: bool (True, False), default=True
                              Setting True or False determines whether landmarks should be drawn 
                              or not.

                       dists: bool (True, False), default=True
                              Setting True or False determines whether distances (segments connecting
                              a landmark to the nearest point on trajectory to that landmark) should
                              be drawn or not.

                  argminpnts: bool (True, False), default=True
                              Setting True or False specifies if the nearest points on 
                              trajectory to landmarks should be drawn or not.

                        zoom: float
                              A positive float number which determines zooming in or out in 
                              a fixed figure size.

                     figsize: tuple
                              A tuple consisting of horizontal and vertical lengths of the 
                              output figure.
                              
        -----------------------------------------------------------------------------------------------
        Returns
                 A figure that can include the trajectory, landmarks, distances, argmin points according
                 to the selected properties by the user.
                 
                
    '''

    color={'-1':'red','1':'blue','0':'black'}
    D=DistsBase()
    fig, ax = plt.subplots()
    fig.set_figwidth(figsize[0])
    fig.set_figheight(figsize[1])
    
    
    if version=='unsigned':
        D.APntSetDistACrv(landmarks, trajectory, ArgminPnts=True, InUse=True)
        SlctdPntsOnSgmnts=D.SlctdPntsOnSgmnts
        SgmntsSPnt=D.SgmntsSPnt
        SgmntsEPnt=D.SgmntsSPnt+D.sgmnts
        if trj:
            for i in range(len(D.sgmnts)):
                plt.plot([SgmntsSPnt[i][0], SgmntsEPnt[i][0]], [SgmntsSPnt[i][1], SgmntsEPnt[i][1]], color='black', alpha=.8, linewidth=.5)

        LndmarksLabeled,DistsLabeled,ArgminpntsLabeled=False,False,False
        for i in range(len(landmarks)):
            if lndmarks:
                
                if LndmarksLabeled:
                    plt.scatter(landmarks[i][0], landmarks[i][1], color='black', s=5)
                else:
                    plt.scatter(landmarks[i][0], landmarks[i][1] ,color='black', s=5, label='Landmark')
                    LndmarksLabeled=True
                    
            if dists:
                
                if DistsLabeled:
                    plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1], SlctdPntsOnSgmnts[i][1]], color='red', linewidth=.5)
                else:
                    plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1], SlctdPntsOnSgmnts[i][1]], color='red', linewidth=.5, label='Landmark distance from trajectory')
                    DistsLabeled=True
                    
            if argminpnts:

                if ArgminpntsLabeled:
                    plt.scatter(SlctdPntsOnSgmnts[i][0], SlctdPntsOnSgmnts[i][1], color='blue', s=5)
                else:
                    plt.scatter(SlctdPntsOnSgmnts[i][0], SlctdPntsOnSgmnts[i][1], color='blue', s=5, label='Chosen nearest point on trajectory')
                    ArgminpntsLabeled=True

    else:
        out=D.APntSetSignedDistACrv(landmarks, trajectory, ArgminPnts=True, InUse=True)
        SlctdPntsOnSgmnts=D.SlctdPntsOnSgmnts
        signs=np.sign(out)
        SgmntsSPnt=D.SgmntsSPnt
        SgmntsEPnt=D.SgmntsSPnt+D.sgmnts
        count,RspctdTs=0,[]
        for i in range(0,len(D.Ts),len(D.sgmnts)):
            RspctdTs.append(list(D.Ts[i:i+len(D.sgmnts)][D.SlctdSgmnts[count]]))
            count+=1
        if trj:
            for i in range(len(D.sgmnts)):
                ax.add_patch(mpatches.FancyArrowPatch(posA=(SgmntsSPnt[i][0], SgmntsSPnt[i][1]), posB=(SgmntsEPnt[i][0], SgmntsEPnt[i][1]), shrinkA=0, shrinkB=0, arrowstyle='->', mutation_scale=10, alpha=.8))

        LndmarksLabeled, PosEndsLabeled, PosMidLabeled, NegMidLabeled, NegEndsLabeled, ArgminpntsLabeled=False, False, False, False, False, False
        for i in range(len(landmarks)):

            if lndmarks:
                
                if LndmarksLabeled:
                    plt.scatter(landmarks[i][0], landmarks[i][1], color='black', s=5)
                else:
                    plt.scatter(landmarks[i][0], landmarks[i][1], color='black', s=5, label='Landmark')
                    LndmarksLabeled=True
                    
            if dists:

                if signs[i]>0:

                    if ((D.SlctdSgmnts[i], RspctdTs[i][0])==(0, 0) or (D.SlctdSgmnts[i], RspctdTs[i][0])==(len(D.sgmnts)-1, 1)):
                        if PosEndsLabeled:
                            plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1], SlctdPntsOnSgmnts[i][1]], color=color[str(signs[i].astype(int))], linestyle=':', linewidth=.5)
                        else:
                            plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1], SlctdPntsOnSgmnts[i][1]], color=color[str(signs[i].astype(int))], linestyle=':', linewidth=.5, label='Positive landmark l^∞-distance from trajectory')
                            PosEndsLabeled=True

                    else:#Middles
                        if PosMidLabeled:
                            plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1], SlctdPntsOnSgmnts[i][1]], color=color[str(signs[i].astype(int))], linewidth=.5)
                        else:
                            plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1], SlctdPntsOnSgmnts[i][1]], color=color[str(signs[i].astype(int))], linewidth=.5, label='Positive landmark l\u00B2-distance from trajectory')
                            PosMidLabeled=True
                    
                else:#NegDist
                    if ((D.SlctdSgmnts[i], RspctdTs[i][0])==(0, 0) or (D.SlctdSgmnts[i], RspctdTs[i][0])==(len(D.sgmnts)-1, 1)):
                        if NegEndsLabeled:
                            plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1], SlctdPntsOnSgmnts[i][1]], color=color[str(signs[i].astype(int))], linestyle=':', linewidth=.5)
                        else:
                            plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1], SlctdPntsOnSgmnts[i][1]], color=color[str(signs[i].astype(int))], linestyle=':', linewidth=.5, label='Negative landmark l^∞-distance from trajectory')
                            NegEndsLabeled=True
                    else:
                        if NegMidLabeled:
                            plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1],SlctdPntsOnSgmnts[i][1]], color=color[str(signs[i].astype(int))], linewidth=.5)
                        else:
                            plt.plot([landmarks[i][0], SlctdPntsOnSgmnts[i][0]], [landmarks[i][1],SlctdPntsOnSgmnts[i][1]], color=color[str(signs[i].astype(int))], linewidth=.5, label='Negative landmark l\u00B2-distance from trajectory')
                            NegMidLabeled=True
                

            if argminpnts:
                if ArgminpntsLabeled:
                    plt.scatter(SlctdPntsOnSgmnts[i][0], SlctdPntsOnSgmnts[i][1], color='blue',s=5)
                else:
                    plt.scatter(SlctdPntsOnSgmnts[i][0], SlctdPntsOnSgmnts[i][1], color='blue', s=5, label='Chosen nearest point on trajectory')
                    ArgminpntsLabeled=True

    
    xmin=min(min(SgmntsSPnt[:,0]), SgmntsEPnt[-1][0])
    xmax=max(max(SgmntsSPnt[:,0]), SgmntsEPnt[-1][0])
    ymin=min(min(SgmntsSPnt[:,1]), SgmntsEPnt[-1][1])
    ymax=max(max(SgmntsSPnt[:,1]), SgmntsEPnt[-1][1])
    if not zoom is None:
        if zoom<=0:
            raise ValueError('Zoom value must not be negative or zero')
        else:
            zoom=1/zoom
            ax.set_xlim([xmin-zoom, xmax+zoom])
            ax.set_ylim([ymin-zoom, ymax+zoom])
    if (True in [lndmarks, dists, argminpnts]):
      ax.legend(loc='upper left', shadow=False)

    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.show()
    D.UnsetAll()
        
def colorcoding(vectorizedfunc, trajectory, version='unsigned', zoom=None, dpi=50, figsize=(10,10)):
    '''

      Usage
             Visualizing the specified feature mapping by color considering every point 
             on a rectangular region, that includs the trajectory, as a potential landmark. 

      -----------------------------------------------------------------------------------------------
      Parameters        
                  vectorizedfunc: A vectorized function
                                  Vectorized form of the function that is used to get the
                                  feature mapping.

                      trajectory: ndarray of shape (len(trajectory), 2)
                                  An array that contains the waypoints of the trajectory
                                  consecutively.

                         version: str ('signed', 'unsigned'), default='unsigned'
                                  Determines which version of the feature mappings is utilized.
                                  For unsigned version the sequential colormap is used but for
                                  signed version the diverging colormap is employed.

                            zoom: float
                                  A positive float number which determines zooming in or out in 
                                  a fixed figure size.

                             dpi: int, defult=50
                                  Specifies the resolution of the figure.

                         figsize: tuple
                                  A tuple consisting of horizontal and vertical lengths of the 
                                  output figure.
                          
      -----------------------------------------------------------------------------------------------
      Returns
               The color-coded visualization of a specified feature mapping.
               
          
    '''

    colors={'signed':'RdBu','unsigned':'gist_heat_r'}
    trjcolor={'signed':'black', 'unsigned':'blue'}
    xmin, ymin = np.min(trajectory, axis=0)
    xmax, ymax = np.max(trajectory, axis=0)
    if dpi<=0: raise ValueError('dpi must be positive')
    if zoom is None:
        xdiff=xmax-xmin
        xzoom=.5*xdiff
        ydiff=ymax-ymin
        yzoom=.5*ydiff
        x = np.linspace(xmin-xzoom, xmax+xzoom, dpi)
        y = np.linspace(ymin-yzoom, ymax+yzoom, dpi)
    else:  
        if zoom<=0:
            raise ValueError('Zoom value must not be negative or zero')
        else:
            zoom=1/zoom
            x = np.linspace(xmin- zoom, xmax+ zoom, dpi)
            y = np.linspace(ymin- zoom, ymax+ zoom, dpi)  
       
    
    X, Y = np.meshgrid(x, y)
    Z = vectorizedfunc(X, Y)
    fig, ax = plt.subplots()
    fig.set_figwidth(figsize[0])
    fig.set_figheight(figsize[1])
    plt.contourf(X, Y, Z, 20, cmap=colors[version])
    if version=='signed':
      xs=trajectory[:,0]
      ys=trajectory[:,1]
      plt.plot(xs[:-1], ys[:-1], color = trjcolor[version])
      ax.add_patch(mpatches.FancyArrowPatch(posA=(xs[-2], ys[-2]), posB=(xs[-1], ys[-1]), shrinkA=0, shrinkB=0, arrowstyle='->', mutation_scale=10, color = trjcolor[version]))
    else:
      plt.plot(trajectory[:,0], trajectory[:,1], color = trjcolor[version])
    plt.colorbar()
    
    plt.show()
