# -*- coding: utf-8 -*-
"""
This is a function to make nice figures with minimum effort.
"""
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as mticker
from matplotlib.cm import ScalarMappable
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import Divider, Size

from pathlib import Path
import sys

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("Logging.log"),
        logging.StreamHandler(sys.stdout)
    ])
from warnings import filterwarnings
filterwarnings('ignore',"has a label of '_nolegend_' which cannot be automatically added to the legend.")


#%%

fontsize=70

Params={'lines.linewidth': 5,
    # 'lines.markersize': 1.5,
    'font.size': fontsize,
    'axes.linewidth': 4,
    'legend.fontsize':fontsize-5,
    'axes.titlesize': fontsize-10,
    'axes.titlepad': 20, 
    'axes.labelpad': 30,
    
    'xtick.major.size': 10, 'xtick.major.width': 4, # 'xtick.major.pad': 10,
    'xtick.minor.size': 5, 'xtick.minor.width': 2, 
    'ytick.major.size': 10, 'ytick.major.width': 4, # 'ytick.major.pad': 10
    'ytick.minor.size': 5, 'ytick.minor.width': 2,
    
    }



def MLplot( x,Y,
            label=[],label_box=False,anchor=None,
            title=None,
            xlabel=None, ylabel=None,
            ROI=None, xrange=(None,None), yrange=(None,None),
            linestyles=None,
            fill=None,fill_label='_nolegend_',
            colors=None,
            padx=0.04,pady=0.1,
            xrule=True,
            vline=[],
            xline=None,
            xscale='linear',
            yscale='linear',
            gui=False,
            figsize=(16,9),
            dpi=200
            ,rcParams={}
            ):
    
    """
    Input:
        x: x-values for x-axis
        Y: list of y-values. If x-values differ from 'x', data has to be inserted as touple (x2,y2).
        label: List of curve-labels.
        label_box: options: True, False, 'outside'
        title: title of plot,
        xlabel: x-axis label.
        ylabel: y-axis label.
        ROI: range of data to plot,
        xrange: x-range for plotting as touple (left,right).
        yrange: y-range for plotting as touple (lower,upper)
        linestyles: list with linestyles 'o' for scatter plot. Length has to be same as Y.
        fill: touple of three elements: (x-values,y-values,scaling-factor),
        fill_label: label for fill curve.
        colors: list with colors. Length has to be same as Y.
        padx: white space around data in x-direction.
        pady: white space around data in y-direction.
        xrule: horizontal line at y=0.
        vline: draws vertical line at positions [x1,x2,...]
        xscale: x-scale. options: 'linear', 'log', 'symlog'
        gui: Graphical user interface.
        dpi: resolution for figures. ~200 for quick view, ~2000 for final images.
        
    Output:
        figure instance from pyplot
        if save option is True, plots are saved in Figure folder in base path.
    
    """
    colors_list=['#515151', '#F14040', '#1A6FDF', '#37AD6B', '#B177DE', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#d62728','#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    from warnings import filterwarnings
    filterwarnings('ignore',"has a label of '_nolegend_' which cannot be automatically added to the legend.")
    
    mpl.rcParams.update(**Params)
    
    if gui:
        mpl.use('TkAgg')
        import matplotlib.pyplot as plt
    else:
        
        import matplotlib.pyplot as plt
    
    ##########################################
    # this function wants to deal with lists #  
    ##########################################
    
    if type(Y)!=list:
        Y=[Y]
    
    if linestyles==None or len(linestyles)!=len(Y):
        linestyles=[None]*len(Y)
        
    if colors==None or len(colors)!=len(Y):
        colors=colors_list[:len(Y)]
    
    ###########################################
    # if no x-values are provided, make some: #
    ###########################################
    
    if type(x).__module__ != np.__name__:
        if type(Y[0])==tuple:
            x=np.arange(0,Y[0][0].shape[0],1)
        else:
            x=np.arange(0,Y[0].shape[0],1)
     
    ################################
    #Cut Data accordingly and plot #
    ################################
    mpl.rcParams.update(**rcParams)
    fig=plt.figure(dpi=dpi)
    ax=set_size(figsize,fig)
   
    for n,y in enumerate(Y):
        if type(y)==tuple: #if you have data with different x-scales, you need to specify the dataset as (x,y) touple.
            if ROI:
                fromx=np.argmax(y[0]>ROI[0])
                tox=np.argmax(y[0]>ROI[1])
                if tox==0:
                    tox=len(y[0])  
                x0=y[0][fromx:tox]
                y0=y[1][fromx:tox]
            else:
                x0=y[0]
                y0=y[1]
        else:
            if ROI:
                fromx=np.argmax(x>ROI[0])
                tox=np.argmax(x>ROI[1])
                if tox==0:
                    tox=len(x)   
                x0=x[fromx:tox]
                y0=y[fromx:tox]
            else:
                x0=x
                y0=y
            
        if linestyles[n]=='o' or linestyles[n]=='+':
            plt.plot(x0,y0,linestyles[n],markersize=15,markeredgewidth=4,markerfacecolor='white',color=colors[n])
        else:
            plt.plot(x0,y0,linestyle=linestyles[n],color=colors[n])
    
    
    if fill:
        fromx=np.argmax(fill[0]>np.min(x0))
        tox=np.argmax(fill[0]>np.max(x0))-1
        if tox==0:
            tox=len(fill[0])
        
        plt.fill_between(fill[0][fromx:tox],fill[1][fromx:tox]*fill[2],color="#01153E",alpha=0.2)
        # if xrule:
        #     label.append('_nolegend_')
        label.append(fill_label)
    
    ################
    #Layout stuff: #
    ################
    
    # ax=plt.gca()
    if yrange:
        ax.set_ylim(bottom=yrange[0])
        ax.set_ylim(top=yrange[1])
    if xrange:
        ax.set_xlim(left=xrange[0])
        ax.set_xlim(right=xrange[1])
    
    ax.margins(padx,pady)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)

    if xrule:
        plt.axhline(y=0, color='k', linewidth=2)   
        label.append('_nolegend_')
        
    if vline:
        for i in vline:
            plt.axvline(x=i,linestyle='--')
        
    plt.title(title)#,wrap=True) #TODO: Title gets cut off if multiple lines.
    
    if len(label)==0:
         for n in range(len(Y)):
             label.append('Curve'+str(n+1))
    
    loc=None
    if anchor:
        loc='upper left'
        if type(anchor)==str:
            loc=anchor
            anchor=None
    
        
    if label_box=='outside':
        plt.legend(label,frameon=True,bbox_to_anchor=(1,1))
    else:
        if label_box:
            plt.legend(label,frameon=True,bbox_to_anchor=anchor,loc=loc)
        else:
            plt.legend(label,frameon=False,bbox_to_anchor=anchor,loc=loc)
    
    
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    
    plt.minorticks_on()    


    
    return fig
    
        

def MLcontour(x,
             y,
             Z,
             xrange=None,
             yrange=None,
             zrange=None,
             separate=True,
             title=None,
             xlabel=None,
             ylabel=None,
             dpi=100,
             **rcParams
             ):
    """

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    y : TYPE
        DESCRIPTION.
    Z : TYPE
        DESCRIPTION.
    xmin : TYPE, optional
        DESCRIPTION. The default is None.
    xmax : TYPE, optional
        DESCRIPTION. The default is None.
    ymin : TYPE, optional
        DESCRIPTION. The default is None.
    ymax : TYPE, optional
        DESCRIPTION. The default is None.
    zmin : TYPE, optional
        DESCRIPTION. The default is None.
    zmax : TYPE, optional
        DESCRIPTION. The default is None.
    separate : TYPE, optional
        DESCRIPTION. The default is True.
    title : TYPE, optional
        DESCRIPTION. The default is None.
    xlabel : TYPE, optional
        DESCRIPTION. The default is None.
    ylabel : TYPE, optional
        DESCRIPTION. The default is None.
    dpi : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    fig

    """
    import matplotlib.pyplot as plt
    
    if type(x).__module__ != np.__name__:
        x=np.arange(0,Z.shape[1],1)
        
    if type(y).__module__ != np.__name__:
        y=np.arange(0,Z.shape[0],1)
    
    mpl.rcParams.update(**Params)
    
    if zrange==None:
        zrange=(np.nanmin(Z[Z!=-np.inf]),np.nanmax(Z[Z!=np.inf]))
      
    levels=20
    
    levels = np.linspace(zrange[0],zrange[1],levels+1)
    
    fig=plt.figure(dpi=dpi,figsize=(16,12))
    # ax=set_size((16,12),fig)
        
    img=plt.contourf(x,y,Z,levels=levels,cmap='rainbow')
    plt.xlim(xrange)
    plt.ylim(yrange)
        
    plt.colorbar(img,anchor=(1,1))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.tick_params(axis='x', direction='in')
    plt.tick_params(axis='y', direction='in')
    
    mpl.rcParams.update(rcParams)
    
    plt.show() 
    return fig
        


def MLtimeplot( x,
            Y,
            label=[],label_frame=False,label_anchor=None,
            title=None,
            xlabel="$\Delta$t / ps",
            ylabel="$\Delta$OD",labelpad=(0,0),
            xrange=None,
            yrange=None,
            linestyles=None,
            colors=None,
            padx=0.02,
            pady=0.1,
            xrule=True,
            xline=None,
            x_break=2,
            xlabel_style='scientific',
            gui=False,
            figsize=(16,9),
            dpi=200,
            **rcParams
            ):
    
    """
    Input:
        x: x-values for x-axis
        Y: list of y-values. If x-values differ from 'x', data has to be inserted as touple (x2,y2).
        label: List of curve-labels.
        title: title of plot,
        xlabel: x-axis label.
        ylabel: y-axis label.
        labelpad: padding between label and ticklabel
        xrange: x-range for plotting as touple (left,right).
        yrange: y-range for plotting as touple (lower,upper)
        linestyles: list with linestyles 'o' for scatter plot. Length has to be same as Y.
        colors: list with colors. Length has to be same as Y.
        padx: white space around data in x-direction.
        pady: white space around data in y-direction.
        xrule: horizontal line at y=0.
        xline: plot vertical line at x='xline'
        x_break: has to be specified for 'symlog'. Determines where to switch from linear to log.
        gui: Graphical user interface.
        dpi: resolution for figures. ~200 for quick view, ~2000 for final images.
        
    Output:
        figure instance from pyplot
        if save option is True, plots are saved in Figure folder in base path.
    
    """
    colors_list=['#515151', '#F14040', '#1A6FDF', '#37AD6B', '#B177DE', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#d62728' ]
    
    if gui:
        mpl.use('TkAgg')
        import matplotlib.pyplot as plt
    else:
        
        import matplotlib.pyplot as plt
    
    
    # fontsize=15

    # Params={'lines.linewidth': 2,
    #     'lines.markersize': 1.5,
    #     'font.size': fontsize,
    #     'axes.linewidth': 2,
    #     'legend.fontsize':fontsize,
    #     'axes.titlesize': fontsize-7,
    #     'axes.titlepad': 20, 
        
    #     'xtick.major.size': 5, 'xtick.major.width': 2, # 'xtick.major.pad': 10,
    #     'xtick.minor.size': 2, 'xtick.minor.width': 1, 
    #     'ytick.major.size': 5, 'ytick.major.width': 2, # 'ytick.major.pad': 10
    #     'ytick.minor.size': 2, 'ytick.minor.width': 1,
        
    #     }    
          
    mpl.rcParams.update(**Params)
        
    ##########################################    
    # this function wants to deal with lists # 
    ##########################################
    
    if type(Y)!=list:
        Y=[Y]
    
    if linestyles==None or len(linestyles)!=len(Y):
        linestyles=[None]*len(Y)
        
    if colors==None or len(colors)!=len(Y):
        colors=colors_list[:len(Y)]
    
    # if no x-values are provided, make some:
        
    if type(x).__module__ != np.__name__:
        if type(Y[0])==tuple:
            x=np.arange(0,Y[0][0].shape[0],1)
        else:
            x=np.arange(0,Y[0].shape[0],1)
    
    ############
    #plot data #
    ############

    fig=plt.figure(dpi=dpi,figsize=figsize)
    
    gs = gridspec.GridSpec(1, 2,width_ratios=[2,3],wspace=0.02)
     
    ax=plt.subplot(gs[0])
    ax2=plt.subplot(gs[1])
 
    ax.set_xlim(np.min(x)-0.2,x_break-0.001)
    ax2.set_xlim(x_break+0.001,np.max(x)*1.2)

    ax2.set_xscale('log')

    for n,y in enumerate(Y):
        if type(y)==tuple: #if you have data with different x-scales, you need to specify the dataset as (x,y) touple.
            if xrange:
                fromx=np.argmax(y[0]>xrange[0])
                tox=np.argmax(y[0]>xrange[1])
                if tox==0:
                    tox=len(y[0])  
                x0=y[0][fromx:tox]
                y0=y[1][fromx:tox]
                
                ax.set_xlim(xrange[0]-0.2,x_break-0.001)
                ax2.set_xlim(x_break+0.001,xrange[1]*1.2)
            else:
                x0=y[0]
                y0=y[1]
        else:
            if xrange:
                fromx=np.argmax(x>xrange[0])
                tox=np.argmax(x>xrange[1])
                if tox==0:
                    tox=len(x)   
                x0=x[fromx:tox]
                y0=y[fromx:tox]
                
                ax.set_xlim(xrange[0]-0.2,x_break-0.001)
                ax2.set_xlim(x_break+0.001,xrange[1]*1.2)
            else:
                x0=x
                y0=y
        if linestyles[n]=='o':
            ax.scatter(x0,y0,s=150,facecolors='none',edgecolors=colors[n],linewidth=2)
            ax2.scatter(x0,y0,s=150,facecolors='none',edgecolors=colors[n],linewidth=2)
        else:
            ax.plot(x0,y0,linestyle=linestyles[n],color=colors[n])
            ax2.plot(x0,y0,linestyle=linestyles[n],color=colors[n])

    ################
    #Layout stuff: #
    ################
    
    if yrange:
        
        ax.set_ylim(bottom=yrange[0])
        ax.set_ylim(top=yrange[1])
        ax.margins(padx,pady)
    
        ax2.set_ylim(bottom=yrange[0])
        ax2.set_ylim(top=yrange[1])
        ax2.margins(padx,pady)
        
    # else:
        
    #     ax.set_ylim(bottom=yrange[0])
    #     ax.set_ylim(top=yrange[1])
    #     ax.margins(padx,pady)
    
    #     ax2.set_ylim(bottom=yrange[0])
    #     ax2.set_ylim(top=yrange[1])
    #     ax2.margins(padx,pady)
    
    #############################
    #And some layout adjustment:#
    #############################
    
    if xrule:
        ax.axhline(y=0, color='k', linewidth=2)  
        ax2.axhline(y=0, color='k', linewidth=2) 
        label.append('_nolegend_')

    ax.set_title(title, loc='left')
    
    if len(label)==0:
         for n in range(len(Y)):
             label.append('Curve'+str(n+1))       
    plt.legend(label,frameon=label_frame,bbox_to_anchor=label_anchor)
    
    # hide the spines between ax and ax2
    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    ######################
    ##little break lines #
    ##################################################################################
                                                                                     #
    d = .015  # how big to make the diagonal lines in axes coordinates               #
    # arguments to pass to plot, just so we don't keep repeating them                #
    kwargs = dict(transform=ax.transAxes, color='k', linewidth=2, clip_on=False)     #
    ax.plot((1-d, 1+d), (-d, +d), **kwargs)        # top-left diagonal               #
    ax.plot((1- d, 1 + d), (1-d, 1+d), **kwargs)  # top-right diagonal               #
                                                                                     #
    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes              #
    ax2.plot((-2/3*d, +2/3*d), (- d, + d), **kwargs)  # bottom-left diagonal         #
    ax2.plot((- 2/3*d, + 2/3*d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal  #
    ##################################################################################    
    
    ax.minorticks_on()    
    ax2.minorticks_on()    

    #no scientific notation
    if xlabel_style=='plain':
        ax2.xaxis.set_minor_formatter(mticker.ScalarFormatter())
        ax2.xaxis.set_major_formatter(mticker.ScalarFormatter())
        ax2.ticklabel_format(style=xlabel_style,axis='x')

    ax.tick_params(labelright=False)
    ax2.tick_params(labelleft=False,which='major',left=False,right=True)
    ax2.tick_params(which='minor',left=False)
    
    if xline:
        ax.axvline(x=xline,linestyle='...')
    
    ###
    #Axis label
    ###
    fig.text(0.5, 0-labelpad[0], xlabel, ha='center')
    fig.text(0-labelpad[1], 0.5, ylabel, va='center', rotation='vertical')
    ####
    
    plt.tight_layout()
    
    mpl.rcParams.update(rcParams)
    
    return fig

#%% Auxiliary


def set_size(figsize,fig):
        
    h=[Size.Fixed(0), Size.Fixed(figsize[0])]
    v=[Size.Fixed(0),Size.Fixed(figsize[1])]
    
    divider = Divider(fig, (0,0,1,1),h,v, aspect=False)
    
    ax = fig.add_axes(divider.get_position(),axes_locator=divider.new_locator(nx=1, ny=1))
    
    return ax        