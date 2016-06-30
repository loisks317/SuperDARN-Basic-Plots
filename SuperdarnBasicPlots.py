# SuperdarnBasicPlots.py
#
# set up so it's easy to plot SuperDARN data for the various dates we
# have. Note that this is only for case studies in 2015 and 2016. Modifications
# are necessary for dates outside that range
#
# LKS, March 2016, 2 days before 26th birthday in Ethiopia, written
# outside on a porch overlooking Addis Ababa :) 
#
# imports
# the usual for processing and plotting
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
import matplotlib.dates as dt
from matplotlib.dates import HourLocator, DayLocator, DateFormatter, MinuteLocator
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
#
#
class SuperDATADisplay(object):
    #
    # Class to read in and display SuperDARN velocity, spectral widths, and
    # power. Modifications can be made to do number density too. 
    #
    # module to read SuperDARN data 
    def readAllSUPERDARN(self):
        #  self.date and self.pType used here 
        #  date is in format '20130317' 
        #  pType should be either 'power', 'spectral', or 'vel'
        # 'power' = power of reflected signal
        # 'spectral' = spectral widths of velocity
        # 'vel' = velocity
        #
         os.chdir('/Users/loisks/Documents/ResearchProjects/SANSAproject/CUTLASS/Data')
         #
         # set up the right types and appropriate strings
         if self.pType=='power':
             nameStr='f_pwr_l'
         elif self.pType=='spectral':
             nameStr='f_width_l'
         elif self.pType=='vel':
             nameStr='f_vel'
               
         if self.date[0:4]=='2016':
              # for 2016 data there are 2 'channels' the
              # date are read in. Tim did this just to screw with me
              # (but actually, he said that) 
              file1=open(self.date+nameStr+'_chA.ascii','rb')
              file2=open(self.date+nameStr+'_chB.ascii','rb')
              lines1=file1.readlines()[2:]
              lines2=file2.readlines()[2:]
              #
              # flags are for the channels 
              flag1=np.ones(len(lines1))
              flag0=np.zeros(len(lines2))
              lines=list(lines1)+list(lines2)
              flag=list(flag1)+list(flag0)
              #
              # set the limits on the plots here 
              self.xlimLow=dt.date2num(datetime.datetime(2016,3,3,14,0,0))
              self.xlimHigh=dt.date2num(datetime.datetime(2016,3,3,18,0,0))
         elif self.date[0:4]=='2015':
              file=open(self.date+nameStr+'.ascii','rb')
              lines=file.readlines()[2:]
              #
              # no flag really necessary here because Tim didn't
              # want to screw with me yet
              flag=np.zeros(len(lines))
              #
              # set the x limits on the plots here 
              self.xlimLow=dt.date2num(datetime.datetime(2015,3,12,10,0,0))
              self.xlimHigh=dt.date2num(datetime.datetime(2015,3,12,12,0,0))
         os.chdir('..')
         
         # empty lists for filling in data 
         Times=[] # n points, where n = 75 here 
         Freqs=[] # n points             
         tLen=len(lines)/3 + 1 # just how the files are read in 
         Data=np.zeros((tLen, 75))   # n x range gates 
         # set a counter
         count=0
         dataCount=0
         #
         # read the lines 
         for iLine in range(len(lines)):
              # check the flags
              if ((flag[iLine]==0) and (flag[iLine-1]==1)):
                   print ('switch to B')
                   count=0
              #
              # header 
              if count == 0: # get the header info
                   temp=lines[iLine].split()
                   HrMn=str(temp[0])
                   try:
                             # parse out hour minute second 
                             Hr=int(HrMn[0:2])
                             Mn=int(HrMn[2:])
                             Ss=int(str(temp[1])[:-1])
                             if Ss > 59:
                                  Ss=59
                             dT=datetime.datetime(int(self.date[0:4]),int(self.date[4:6]),int(self.date[6:8]),Hr,Mn,Ss)
                             # put into datetime and frequency list
                             # use append because the lists are of unknown length
                             Times.append(dT)
                             Freqs.append(int(temp[3]))
                   except(ValueError):
                             Times.append(np.nan)
                             Freqs.append(np.nan)
                             print 'Error in reading in'
                   count+=1
              #
              # data 
              elif count ==1:
                        temp=lines[iLine].split()
                        if self.pType == 'spectral':
                            # spectral has some weird glitch where
                            # the data files have **** randomly in them
                            # # of *'s is not consistent
                            # I am going to assume this means bad data, other
                            # wise, wtf
                            for iTemp in range(len(temp)):
                                # go element by element
                                try:
                                    Data[dataCount][iTemp] = int(temp[iTemp])
                                except(ValueError): # for that glitch
                                    Data[dataCount][iTemp] = np.nan
                            # for consistency 
                            Data[dataCount]=np.array(Data[dataCount])    
                        else:
                            # 10000 = nan in this dataset
                            # but we screen for these later before plot
                            t1=np.array(temp)
                            Data[dataCount]=t1
                        # count up for the empty line that
                        # follows the data 
                        dataCount+=1
                        count+=1
              elif count ==2:
                 # skip this and reset the count
                 count=0
         # fill the arrays
         Times=np.array(Times)
         Data=np.array(Data)
         Freqs=np.array(Freqs)
         # sort into the appropriate frequency, data and time bins
         f13time=Times[Freqs<14800] 
         f15time=Times[(Freqs<15800) & (Freqs>= 14800)]
         f16time=Times[(Freqs<16800) & (Freqs>= 15800)]
         f17time=Times[(Freqs<18000) & (Freqs>= 16800)]
         f18time=Times[(Freqs<18500) & (Freqs>= 18000)]
         f19time=Times[Freqs>18500]
         #
         # sort the data 
         f13band=Data[Freqs< 14800][:]
         f15band=Data[(Freqs<15800) & (Freqs>= 14800)][:]
         f16band=Data[(Freqs<16800) & (Freqs>= 15800)][:]
         f17band=Data[(Freqs<18000) & (Freqs>= 16800)][:]
         f18band=Data[(Freqs<18500) & (Freqs>= 18000)][:]
         f19band=Data[Freqs>18500][:]
         
         # sort the frequencies 
         f13F = Freqs[Freqs<14800]
         f15F=Freqs[(Freqs<15800) & (Freqs>= 14800)]
         f16F=Freqs[(Freqs<16800) & (Freqs>= 15800)]
         f17F=Freqs[(Freqs<18000) & (Freqs>= 16800)]
         f18F=Freqs[(Freqs<18500) & (Freqs>= 18000)]
         f19F=Freqs[Freqs>18500]

         # put in accessible arrays 
         pTimes=[f13time,f15time,f16time,f17time,f18time,f19time]
         pF=[f13F, f15F, f16F, f17F, f18F, f19F]
         pFband=[f13band, f15band, f16band, f17band, f18band, f19band]
         os.chdir(self.path) 
         
         return pTimes, pF, pFband

    #
    # Plot the data you just read in 
    def plotAllSUPERDARN(self):
        # make a plot of the results
        # type is what we are plotting here
        #
        # get the current variables 
        date=self.date
        type=self.pType
        pdata=self.pFband
        times=self.pTimes
        freq=self.pF
        #
        # set here the parameters for power, spectral width, and velocity
        # no log parameters here, but will need to implement that if this
        # changes 
        if self.pType == 'power':
            cblabel = 'Power [dB]'
            vmin = 0
            vmax = 20
        elif self.pType == 'spectral':
            cblabel = 'Spectral Width [m/s]'
            vmin = 0
            vmax = 50
        elif self.pType == 'vel':
            cblabel = 'L-o-s Velocity [m/s]'
            vmin = -200
            vmax = 50        
        #
        # labels for the plots 
        labels=['13 MHz', '15 MHz', '16 MHz', '17 MHz', '18 MHz', '19 MHz']
        #
        # iterate through the potential frequencies 
        for i in range(len(labels)): # number of elements in data arrays
            # start by opening a figure 
            fig=plt.figure()
            #
            # get the necessary plotting imports 
            from numpy import ma
            os.chdir('/Users/loisks/Desktop/Functions/')
            import colormaps as cmaps
            os.chdir(self.path)
            # this is a colormap I like a lot but I have to load it extra special because of the python version I have :) 
            plt.register_cmap(name='viridis', cmap=cmaps.viridis) 

            # for time parameters on plot
            # go with time labels every hour and ticks every 10 minutes
            days = DayLocator(interval=1) 
            hours = MinuteLocator(interval=30) 
            hours2 = MinuteLocator(interval=10) 
            daysFmt = DateFormatter('%H:%M')
            fig.gca().xaxis.set_major_locator(hours)
            fig.gca().xaxis.set_major_formatter(daysFmt)
            fig.gca().xaxis.set_minor_locator(hours2)
            #
            # big font to make things easy to read 
            font = {'family' : 'normal',
                    'weight' : 'bold',
                    'size'   : 22}
            plt.rc('font', **font)
            ax=fig.add_subplot(111)
            plt.subplots_adjust(right=0.70, top=0.92, bottom=0.28, left=0.11)
            ax.set_ylabel('Range Gate Number', fontsize=22, fontweight='bold')
            time=dt.date2num(self.pTimes[i])
            Altitudes = range(75) # for 75 range gates 
            X,Y=np.meshgrid(time, Altitudes)
            dtemp=np.array(self.pFband[i])
            #
            # nan the 10000 data, which are nans in this data set 
            dtemp[dtemp==10000]=np.nan
            data=ma.masked_invalid(dtemp).transpose()
            ax.set_ylim(25,38) # relevant range gates here
            ax.plot(time, np.ones(len(time))*32, lw=3, ls='--', c='k')
            ax.set_xlabel("UT Time on " + self.date, fontsize=20, fontweight='bold')
            ax.set_xlim(self.xlimLow, self.xlimHigh)
            # plot! 
            try:
                col=ax.pcolormesh(X,Y,data, cmap='viridis', vmin=vmin, vmax=vmax)
                font = {'family' : 'normal',
                  'weight' : 'bold',
                  'size'   : 22}
                plt.rc('font', **font)
                #
                # add a colorbar
                cbaxes = fig.add_axes([0.8, 0.27, 0.03, 0.65])
                cb = plt.colorbar(col, cax = cbaxes,ticks=np.linspace(vmin,vmax,5))
                cb.set_label(cblabel, fontsize=25)

                fig.set_size_inches(13,9)
                #
                # save in new directory if directory doesn't already exist
                os.chdir(self.path)
                subdir_name='CUTLASS_All_Spectrograms'
                if not os.path.exists(subdir_name):
                    os.umask(0) # unmask if necessary
                    os.makedirs(subdir_name) 
                os.chdir(subdir_name)#
                plt.savefig(labels[i]+self.date+'_'+self.pType+'.png')
            except: # if there is no data in this frequency band 
                print "No data for " + labels[i]
            #os.chdir('..')
            plt.close()
        # PLOT ALL ON SAME
        fig=plt.figure()
        for i in range(len(labels)): # number of elements in data arrays
            from numpy import ma
            os.chdir('/Users/loisks/Desktop/Functions/')
            import colormaps as cmaps
            os.chdir(self.path)
            # this is a colormap I like a lot but I have to load it extra special because of the python version I have :) 
            plt.register_cmap(name='viridis', cmap=cmaps.viridis) 

            # for time parameters on plot
            # go with time labels every hour and ticks every 10 minutes
            days = DayLocator(interval=1) 
            hours = MinuteLocator(interval=30) 
            hours2 = MinuteLocator(interval=10) 
            daysFmt = DateFormatter('%H:%M')
            fig.gca().xaxis.set_major_locator(hours)
            fig.gca().xaxis.set_major_formatter(daysFmt)
            fig.gca().xaxis.set_minor_locator(hours2)
            #
            # big font to make things easy to read 
            font = {'family' : 'normal',
                    'weight' : 'bold',
                    'size'   : 22}
            plt.rc('font', **font)
            ax=fig.add_subplot(111)
            plt.subplots_adjust(right=0.70, top=0.92, bottom=0.28, left=0.11)
            ax.set_ylabel('Range Gate Number', fontsize=22, fontweight='bold')
            time=dt.date2num(self.pTimes[i])
            Altitudes = range(75) # for 75 range gates 
            X,Y=np.meshgrid(time, Altitudes)
            dtemp=np.array(self.pFband[i])
            #
            # nan the 10000 data, which are nans in this data set 
            dtemp[dtemp==10000]=np.nan
            data=ma.masked_invalid(dtemp).transpose()
            ax.set_ylim(25,38) # relevant range gates here
            ax.plot(time, np.ones(len(time))*32, lw=3, ls='--', c='k')
            ax.set_xlabel("UT Time on " + self.date, fontsize=20, fontweight='bold')
            ax.set_xlim(self.xlimLow, self.xlimHigh)
            # plot! 
            try:
                col=ax.pcolormesh(X,Y,data, cmap='viridis', vmin=vmin, vmax=vmax)
                font = {'family' : 'normal',
                  'weight' : 'bold',
                  'size'   : 22}
                plt.rc('font', **font)
                #
                # add a colorbar
                cbaxes = fig.add_axes([0.8, 0.27, 0.03, 0.65])
                cb = plt.colorbar(col, cax = cbaxes,ticks=np.linspace(vmin,vmax,5))
                cb.set_label(cblabel, fontsize=25)


            except: # if there is no data in this frequency band 
                print "No data for " + labels[i]
            #os.chdir('..')
        fig.set_size_inches(13,9)
        #
        # save in new directory if directory doesn't already exist
        os.chdir(self.path)
        subdir_name='CUTLASS_All_Spectrograms'
        if not os.path.exists(subdir_name):
           os.umask(0) # unmask if necessary
           os.makedirs(subdir_name) 
        os.chdir(subdir_name)#
        plt.savefig('All_'+self.date+'_'+self.pType+'.png')
        plt.close()

        
    #
    # initialize the data 
    def __init__(self, dateList, pathName):
        #
        # dateList should be a list of dates in form ['20130317', '20140317']
        #
        # typeList are the 3 types of plots we'll make from our superDARN data
        typeList = ['power', 'spectral', 'vel']
        self.path=pathName # for saving files
        for iDate in dateList:
            for iType in typeList:
                self.date=iDate
                self.pType=iType
                self.pTimes,self.pF, self.pFband = self.readAllSUPERDARN()
                #
                # plot everything
                self.plotAllSUPERDARN()
        
        
#
# initialize, just for quick access
pathName=os.getcwd()
SuperDATADisplay(['20150312', '20160303'], pathName)
