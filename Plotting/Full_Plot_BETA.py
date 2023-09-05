# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:57:56 2023

@author: work
"""

from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mticker
import numpy as np

import sys
sys.path.append('Z:/Nutzer/Lang/privat/04_Software/Python/MLModules')
import MLBasic_GUI as GUI
import MLPumpProbe as pp
import GIF

#%%

data=pp.fitData(folderpath='Z:/Nutzer/Lang/privat/08_Messdaten/U21_TA/20220816_Fe-PD196/07_ma/',
                Abspath='Z:/Nutzer/Lang/privat/08_Messdaten/U21_TA/20220816_Fe-PD196/Absorption/05_Fe-PD196_after_TA.csv')


#%%


def full_plot(x,y,Z,x0=[],y0=[],xrange=(400,750),yrange=(-0.25,200),y_break=1,zrange=(-2.3,1.2),
              data_factor=1,
              xlabel='Wavelength / nm',ylabel='$\Delta$t / ps',zlabel='$\Delta$OD'):
    

    
    zlabel=zlabel+' x '+str(data_factor)
    Z=Z*data_factor
    
    fig,ax=plt.subplots(3,2,gridspec_kw={'width_ratios':[2,1],'height_ratios':[2,1.3,1.8],'hspace':0.028,'wspace':0.012})
    
    fig.delaxes(ax[2,1])
    
    
    ####Contour
    levels = np.linspace(zrange[0],zrange[1]-0.2,20)
    ax[0,0].contourf(x[np.argmax(x>xrange[0]):np.argmax(x>xrange[1])],
                     y[np.argmax(y>y_break):np.argmax(y>yrange[1])],
                     Z[np.argmax(y>y_break):np.argmax(y>yrange[1]),np.argmax(x>xrange[0]):np.argmax(x>xrange[1])],
                     levels=levels,cmap='rainbow')
    ax[0,0].set_xticks([])
    ax[0,0].set_yscale('log')
    ax[0,0].yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax[0,0].ticklabel_format(style='plain',axis='y')
    ax[1,0].text(350, 1, ylabel, va='center', rotation='vertical')
    #Lines
    for i in x0:
        ax[0,0].axvline(x=i,linestyle='--',linewidth=0.5,color='k')
    for i in y0:
        if i<yrange[1] and i>y_break:
            ax[0,0].axhline(y=i,linestyle='--',linewidth=0.5,color='k')
    
    ax[1,0].contourf(x[np.argmax(x>xrange[0]):np.argmax(x>xrange[1])],
                     y[np.argmax(y>yrange[0]):np.argmax(y>y_break)],
                     Z[np.argmax(y>yrange[0]):np.argmax(y>y_break),np.argmax(x>xrange[0]):np.argmax(x>xrange[1])],
                     levels=levels,cmap='rainbow')
    ax[1,0].set_xticks([])
    ax[1,0].set_yticks([0,0.5,1])
    #lines
    for i in x0:
        ax[1,0].axvline(x=i,linestyle='--',linewidth=0.5,color='k')
    for i in y0:
        if i>yrange[0] and i<y_break:
            ax[1,0].axhline(y=i,linestyle='--',linewidth=0.5,color='k')
    ######
    
    ####Timeplot
    base = ax[0,1].transData
    rot = mpl.transforms.Affine2D().rotate_deg(90)
    ax[0,1].margins(0)
    for i in x0:
        ax[0,1].plot(y[np.argmax(y>y_break):np.argmax(y>yrange[1])],
                 -1*Z[np.argmax(y>y_break):np.argmax(y>yrange[1]),np.argmax(x>i)],transform=rot+base)
    ax[0,1].axvline(x=0,color='k',linewidth=0.75)
    ax[0,1].set_yscale('log')
    ax[0,1].set_xlim(zrange)
    ax[0,1].set_yticks([])
    #Lines
    for i in y0:
        if i<yrange[1] and i>y_break:
            ax[0,1].axhline(y=i,linestyle='--',linewidth=0.5,color='k')
    #
    base = ax[1,1].transData
    rot = mpl.transforms.Affine2D().rotate_deg(90)
    ax[1,1].margins(0)
    for i in x0:
        ax[1,1].plot(y[np.argmax(y>yrange[0]):np.argmax(y>y_break)],
                 -1*Z[np.argmax(y>yrange[0]):np.argmax(y>y_break),np.argmax(x>i)],transform=rot+base)
    ax[1,1].axvline(x=0,color='k',linewidth=0.75)
    ax[1,1].set_xlim(zrange)
    ax[1,1].set_xticks([-2,-1,0,1])
    ax[1,1].set_yticks([])
    ax[1,1].set_xlabel(zlabel)
    #lines
    for i in y0:
        if i>yrange[0] and i<y_break:
            ax[1,1].axhline(y=i,linestyle='--',linewidth=0.5,color='k')
    ########
    
    ####Spectrum
    colors=plt.cm.get_cmap('rainbow')(np.linspace(0,1,len(y0)))
    colors=[mpl.colors.to_hex(i) for i in colors]
    
    ax[2,0].margins(0)
    for n,i in enumerate(y0):
        ax[2,0].plot(x[np.argmax(x>xrange[0]):np.argmax(x>xrange[1])],
                     Z[np.argmax(y>i),np.argmax(x>xrange[0]):np.argmax(x>xrange[1])],
                     color=colors[n])
    ax[2,0].axhline(y=0,color='k',linewidth=0.75)
    ax[2,0].set_xlabel(xlabel)
    ax[2,0].set_ylabel(zlabel)
    ax[2,0].set_ylim(zrange)
    ax[2,0].set_yticks([-2,-1,0,1])
    #lines
    for i in x0:
        ax[2,0].axvline(x=i,linestyle='--',linewidth=0.5,color='k')
    ######
    plt.show()
    plt.close()
#%%
   
full_plot(data.WL,data.dt,data.TA,data_factor=100,x0=[460,520],y0=[0.1,5,20,100],
          xrange=(400,700),yrange=(-0.25,200))