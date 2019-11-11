#    MICROCAR DATASETS COMPARISON
#    @filename: yu_22531975.py
#    @author: Daphne Yu
#    @for University of Western Australia CITS2401 Lab3 Part1 submission

#    @assumption:
#    There will never be a ‘missing’ instruction, all instructions are valid
#    "NA" in actual datafile means missing reading, ignore entire row for both files.
#    The number of expected and actual instructions for a microcar will always be the same.

import numpy as np
import matplotlib.pyplot as plt

#   helper function to check input argument, return -1 if bad
def sanity_check(arg):
    if not isinstance(arg,list):
        print('Both input args need to be of type `list`')
        return -1
    if len(arg)==0:
        print('Name list cannot be empty')
        return -1
    for e in arg:
        if not isinstance(e,str):
            print('Everything inside list needs to be of type `str`')
            return -1
    return 0

#   PART ONE
#   @arg1: expected_datafiles -> list of csv filenames, containing expected instructions
#   @arg2: actual_datafiles -> list of csv filenames, containing actual actions performed
#   filename should include file location path if the file is not in same dir as the python script.
#
#   @csv file format:
#   ==========      ==========      ==========
#    Angle(A)         Time(t)        Speed(s)   
#   ==========      ==========      ==========
#   wrt. East       seconds         meters per sec  
#   degree angle
#
#   @return: for each microcar csv input pair, in meters, round to 2 dec
#   np array1 -> expected horizontal displacements
#   np array2 -> expected vertical displacements
#   np array3 -> actual horizontal displacements
#   np array4 -> actual vertical displacements
#   np array5 -> expected distances travelled
#   np array6 -> actual distances travelled
#   @sample call: microcar(['expected1.csv','expected2.csv'],['actual1.csv','actual2.csv'])
def microcar(expected_datafiles,actual_datafiles):
    if sanity_check(expected_datafiles)==-1 or sanity_check(actual_datafiles)==-1:
        return None

    numOfCars = len(expected_datafiles)
    exp_h = np.array([])
    exp_v = np.array([])
    act_h = np.array([])
    act_v = np.array([])
    exp_d = np.array([])
    act_d = np.array([])

    for i in range(0,numOfCars):
        mask=[]     #bool array for filtering out missing data row
        try: 
            with open(actual_datafiles[i],'r') as infile:
                rows = []
                for row in infile:
                    rows.append(row.strip().split(",")) #get ride off \n
                act_data = np.array(rows).T #transpose and get three long rows: angle, time and speed

                b=act_data!='NA'    #bool matrix,evaluate if any entry is 'NA' 

                mask = np.tile(b[0,:] * b[1,:] * b[2,:], (3, 1))    #row-wise AND
                act_data = act_data[mask].reshape((3, -1)).astype('float64')
                A,t,s = act_data[0,:], act_data[1,:],act_data[2,:]  #A for angle t for time s for speed

                act_h = np.append(act_h,round(sum(t*s*np.cos((2*np.pi*A)/360)),2))  #trigonometry func takes radian
                act_v = np.append(act_v,round(sum(t*s*np.sin((2*np.pi*A)/360)),2))
                act_d = np.append(act_d,round(sum(t*s),2))

        except OSError:
            print('File specified in `actual_datafiles` position [' + str(i) + '] is not accessible.')
            return None

        try:  
            with open(expected_datafiles[i],'r') as infile:
                rows = []
                for row in infile:
                    rows.append(row.strip().split(","))
                exp_data = np.array(rows).T 

                exp_data = exp_data[mask].reshape((3, -1)).astype('float64')
                A,t,s = exp_data[0,:], exp_data[1,:],exp_data[2,:]

                exp_h = np.append(exp_h,round(sum(t*s*np.cos((2*np.pi*A)/360)),2))
                exp_v = np.append(exp_v,round(sum(t*s*np.sin((2*np.pi*A)/360)),2))
                exp_d = np.append(exp_d,round(sum(t*s),2))

        except OSError:
            print('File specified in `expected_datafiles` position [' + str(i) + '] is not accessible.')
            return None

    return(exp_h,exp_v,act_h,act_v,exp_d,act_d)


#   PART TWO
#   This function creates 3 subplots for each microcar input pair
#
#   Plot1 -> bar-type, comparing the expected and actual distance(array5,6)
#   Plot2 -> scatter-type, expected horizontal and vertical displacements(array1,2)
#   Plot3 -> scatter-type, actual horizontal and vertical displacements(array3,4)
#
#   @args: same as microcar() function
#   @sample call: plotmicrocar(['expected1.csv','expected2.csv'],['actual1.csv','actual2.csv'])
def plotmicrocar(expected_datafiles,actual_datafiles):
    calData = microcar(expected_datafiles,actual_datafiles)
    
    if calData is None:
        print('Invalid input, exiting...')
        return
    else:
        exp_h,exp_v,act_h,act_v,exp_d,act_d = calData[0],calData[1],calData[2],calData[3],calData[4],calData[5]
        
    numOfCars = len(expected_datafiles)
    
    xLabels = []    #contain list of string 'car0' 'car1' 'carN'
    for i in range(0,numOfCars):
        xLabels.append('car'+str(i))
    
    #use to place the scatter dot area at the fairly centre
    diameter=np.floor(1.2*np.max([abs(np.max(act_h)-np.min(act_h)),abs(np.max(act_v)-np.min(act_v)),
                                  abs(np.max(exp_h)-np.min(exp_h)),abs(np.max(exp_v)-np.min(exp_v))]))
    top = np.floor(np.mean([np.mean([np.max(act_v),np.min(act_v)]),np.mean([np.max(exp_v),np.min(exp_v)])]))+diameter
    bottom = top - 2*diameter
    right = np.floor(np.mean([np.mean([np.max(act_h),np.min(act_h)]),np.mean([np.max(exp_h),np.min(exp_h)])]))+diameter
    left = right - 2*diameter   
    
    plt.figure(figsize=(6, 6))
    plt.subplots_adjust(wspace=0.45,hspace=0.45,left=0.15,right=0.95)

    #customised colour list
    colorlst=('Tan','Maroon','Slategray','Coral','Gold','Olive','HotPink','Turquoise','Steelblue','Mediumpurple')

    #PLOT: bar
    ax1 = plt.subplot(211)
    ax1.set_title('Total Distance Travelled',fontsize=14)
    x = np.arange(numOfCars) 
    width = 0.3       
    ax1.bar(x - width/2, exp_d, width, label='Expected',color='gold')
    ax1.bar(x + width/2, act_d, width,label='Actual',color='olive')
    ax1.set_xticks(x)
    ax1.set_xticklabels(xLabels,fontsize=12)
    ax1.legend(loc='best',fontsize='small',framealpha=0.6)
    ax1.set_ylabel('Distance (Unit:metre)',fontsize=12)
    ax1.grid(axis='y',linestyle='--')
    ax1.set_ylim(0,1.25*np.max([np.max(exp_d),np.max(act_d)]))
    
    for i in range(0,numOfCars):  #add numerical figure on top of each bar
        ax1.annotate(exp_d[i],xy=(i-width/2,exp_d[i]),ha='center',va='bottom',rotation=45,color='goldenrod')
        ax1.annotate(act_d[i],xy=(i+width/2,act_d[i]),ha='center',va='bottom',rotation=45,color='darkolivegreen')
        
    #PLOT: scatter-one
    ax2 = plt.subplot(223)
    ax2.axis('equal')
    ax2.grid(True)
    ax2.set_title('Expected Final Position',fontsize=14)
    ax2.set_xlabel('X-axis (Unit:metre)',fontsize=12)
    ax2.set_ylabel('Y-axis (Unit:metre)',fontsize=12)
    ax2.set(xlim=(left,right), ylim=(bottom,top))

    for i in range(0,numOfCars):
        ax2.scatter(exp_h[i],exp_v[i],label=xLabels,color=colorlst[i%10],marker='o')
        ax2.legend(xLabels,loc='best',fontsize='x-small',framealpha=0.6)

    #PLOT: scatter-two
    ax3 = plt.subplot(224)
    ax3.axis('equal')
    ax3.grid(True)
    ax3.set_title('Actual Final Position',fontsize=14)
    ax3.set_xlabel('X-axis (Unit:metre)',fontsize=12)
    ax3.set_ylabel('Y-axis (Unit:metre)',fontsize=12)
    ax3.set(xlim=(left,right), ylim=(bottom,top))
    
    for i in range(0,numOfCars):
        ax3.scatter(act_h[i],act_v[i],label=xLabels,color=colorlst[i%10],marker='D')
        ax3.legend(xLabels,loc='best',fontsize='x-small',framealpha=0.6)

    plt.show()
    return

