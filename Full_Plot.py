# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:52:34 2023

@author: work
"""

from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import colormaps
import matplotlib.ticker as mticker
import numpy as np
import GIF

"""
WL0: wl slices
t0: time slices
"""
#%%


def full_plot(t,WL,TA,WL0,t0,fromdt=None,dt_break=1,todt=None,fromI=-2.3,toI=1.2,hlines=True,vlines=True,title=None):
    
    mpl.rcParams.update({'figure.figsize': (16,4*16/6),
                         'lines.linewidth': 4,
                        'lines.markersize': 8,
                        'font.size': 32,
                        'axes.linewidth': 3,
                        # 'legend.fontsize':15,
    #                     'axes.titlesize': fontsize-10,
    #                     'axes.titlepad': 20, 
                        'axes.labelpad': 5,
                        
                        'xtick.major.size': 10, 'xtick.major.width': 2, # 'xtick.major.pad': 10,
                        'xtick.minor.size': 5, 'xtick.minor.width': 2, 
                        'ytick.major.size': 10, 'ytick.major.width': 2, # 'ytick.major.pad': 10
                        'ytick.minor.size': 5, 'ytick.minor.width': 2,
                        
                        })
    
    if fromdt==None:
        fromdt=np.nanmin(t)-1e-6
    if todt==None:
        todt=np.nanmax(t)-1e-6
        
        
        
    fig,ax=plt.subplots(3,2,gridspec_kw={'width_ratios':[2,1],'height_ratios':[2,1.3,1.8],'hspace':0.028,'wspace':0.012})
    
    fig.delaxes(ax[2,1])
   
    ##############
    ####Contour
    n_levels=20
    levels = np.linspace(fromI,toI-0.2,n_levels)
    cmap_neg=[mpl.cm.get_cmap('Blues')(n/(3*(n_levels)/4)) for n in range(round(3*(n_levels)/4))]#+[mpl.cm.get_cmap('Reds')(round(n/(1*(n_levels+1)/3))) for n in range(1*(n_levels+1)/3)]#[mpl.cm.get_cmap('YlGnBu')(n/n_levels) for n in range(n_levels)].reverse()+
    cmap_pos=[mpl.cm.get_cmap('Reds')(n/(1*(n_levels)/4)) for n in range(round(1*(n_levels)/4))]
    cmap=cmap_neg[::-1] + cmap_pos
    
    ax[0,0].contourf(WL,
                     t[np.argmax(t>dt_break):np.argmax(t>todt)],
                     TA[np.argmax(t>dt_break):np.argmax(t>todt),:],
                     levels=levels,colors=cmap)
    ax[0,0].set_xticks([])
    ax[0,0].set_yscale('log')
    ax[0,0].yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax[0,0].ticklabel_format(style='plain',axis='y')
    ax[0,0].title.set_text(title)
    # ax[1,0].text(np.max(WL)+17, 10, '$\Delta$t / ps', va='center', rotation='vertical')
    #Lines
    if hlines:
        for i in WL0:
            ax[0,0].axvline(x=i,linestyle='--',linewidth=mpl.rcParams['axes.linewidth']*0.75,color='k')
    if vlines:
        for i in t0:
            if i<todt and i>dt_break:
                ax[0,0].axhline(y=i,linestyle='--',linewidth=mpl.rcParams['axes.linewidth']*0.75,color='k')
    
    ax[1,0].contourf(WL,t[np.argmax(t>fromdt):np.argmax(t>dt_break)],TA[np.argmax(t>fromdt):np.argmax(t>dt_break),:],levels=levels,colors=cmap)
    ax[1,0].set_xticks([])
    #Lines
    if vlines:
        for i in WL0:
            ax[1,0].axvline(x=i,linestyle='--',linewidth=mpl.rcParams['axes.linewidth']*0.75,color='k')
    if hlines:
        for i in t0:
            if i>fromdt and i<dt_break:
                ax[1,0].axhline(y=i,linestyle='--',linewidth=mpl.rcParams['axes.linewidth']*0.75,color='k')
    
    ######
    ####Timeplot
    base = ax[0,1].transData
    rot = mpl.transforms.Affine2D().rotate_deg(90)
    ax[0,1].margins(0)
    for n,i in enumerate(WL0):
        ax[0,1].plot(t[np.argmax(t>dt_break):np.argmax(t>todt)],
                 -1*TA[np.argmax(t>dt_break):np.argmax(t>todt),np.argmax(WL>i)],transform=rot+base,
                 color=colormaps['hot'](np.arange(0.001,1,1/(len(t0)-0.9))[n]))
    ax[0,1].axvline(x=0,color='k',linewidth=mpl.rcParams['axes.linewidth'])
    ax[0,1].set_yscale('log')
    ax[0,1].set_xlim((fromI,toI))
    ax[0,1].set_yticks([])
    #Lines
    if hlines:
        for i in t0:
            if i<todt and i>dt_break:
                ax[0,1].axhline(y=i,linestyle='--',linewidth=mpl.rcParams['axes.linewidth']*0.75,color='k')
    #
    base = ax[1,1].transData
    rot = mpl.transforms.Affine2D().rotate_deg(90)
    ax[1,1].margins(0)
    for n,i in enumerate(WL0):
        ax[1,1].plot(t[np.argmax(t>fromdt):np.argmax(t>dt_break)],
                 -1*TA[np.argmax(t>fromdt):np.argmax(t>dt_break),np.argmax(WL>i)],transform=rot+base,
                 color=colormaps['hot'](np.linspace(0,1,len(t0)))[n])
    ax[1,1].axvline(x=0,color='k',linewidth=mpl.rcParams['axes.linewidth'])
    # ax[1,1].set_xticks([-2,-1,0,1])
    ax[1,1].set_xlim((fromI,toI))
    ax[1,1].set_yticks([])
    ax[1,1].set_xlabel('$\Delta$OD x 100')
    #lines
    if hlines:
        for i in t0:
            if i>fromdt and i<dt_break:
                ax[1,1].axhline(y=i,linestyle='--',linewidth=mpl.rcParams['axes.linewidth']*0.75,color='k')
    ########
    
    ####Spectrum
    ax[2,0].margins(0)
    colors=[mpl.cm.get_cmap('winter')(i) for i in np.linspace(0,1,len(t0))]
    for n,i in enumerate(t0):
        ax[2,0].plot(WL,TA[np.argmax(t>i),:],color=colors[n])
    ax[2,0].axhline(y=0,color='k',linewidth=mpl.rcParams['axes.linewidth'])
    ax[2,0].set_xlabel('Wavelength / nm')
    ax[2,0].set_ylabel('$\Delta$OD x 100')
    ax[2,0].set_ylim((fromI,toI))
    # ax[2,0].set_yticks([-2,-1,0,1])
    #lines
    if vlines:
        for i in WL0:
            ax[2,0].axvline(x=i,linestyle='--',linewidth=mpl.rcParams['axes.linewidth']*0.75,color='k')
    ######
    plt.show()
    plt.close()
    

