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
from matplotlib import colormaps
from matplotlib import pyplot as plt

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

fontsize=65

Params={'lines.linewidth': 4,
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
            colors=None,cmap='autumn',
            padx=0.04,pady=0.1,
            xrule=True,
            vline=[],
            xline=None,
            xscale='linear',
            yscale='linear',
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

    mpl.rcParams.update(**Params)
    
    colors_list=['#515151', '#F14040', '#1A6FDF', '#37AD6B', '#B177DE', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#d62728','#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    colors_grad=colormaps[cmap]
    
    from warnings import filterwarnings
    filterwarnings('ignore')
    
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
        

    if colors=='grad':
        colors=colors_grad(np.linspace(0,1,len(Y)))
    elif colors==None or len(colors)!=len(Y):
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
    
    mpl.rcParams.update(**rcParams)
    
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

    mpl.rcParams.update(**Params)
    
    import matplotlib.pyplot as plt
    
    from warnings import filterwarnings
    filterwarnings('ignore',"_nolegend_")
    
    if type(x).__module__ != np.__name__:
        x=np.arange(0,Z.shape[1],1)
        
    if type(y).__module__ != np.__name__:
        y=np.arange(0,Z.shape[0],1)
    
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
            xlabel_style='scientific',
            
            title=None,
            xlabel="$\Delta$t / ps",
            ylabel="$\Delta$mOD",
            labelpad=(0.05,0.05),
            
            xrange=None,
            yrange=None,
            
            linestyles=None,
            colors=None,cmap='autumn',
            
            padx=0.04,
            pady=0.2,
            
            xrule=True,
            xline=None,
            x_break=2,
            

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
    
    from warnings import filterwarnings
    filterwarnings('ignore',"_nolegend_")
    
    mpl.rcParams.update(**Params)
    
    colors_list=['#515151', '#F14040', '#1A6FDF', '#37AD6B', '#B177DE', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#d62728' ]
    
    colors_grad=colormaps[cmap](np.arange(0.001,0.999,1/(len(Y)-0.9)))
    
    
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
    
    if colors=='grad':
        colors=colors_grad
    elif colors==None or len(colors)!=len(Y):
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
    mpl.rcParams.update(**rcParams)

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
                if xrange[0]:
                    fromx=np.argmax(y[0]>xrange[0])
                else:
                    fromx=0
                if xrange[1]:
                    tox=np.argmax(y[0]>xrange[1])
                else:
                    tox=len(x)-1               
                if tox==0:
                    tox=len(x)-1   
                    
                    
                x0=y[0][fromx:tox]
                y0=y[1][fromx:tox]
                
                ax.set_xlim(y[0][fromx]-0.2,x_break-0.001)
                ax2.set_xlim(x_break+0.001,y[0][tox]*1.2)
            else:
                x0=y[0]
                y0=y[1]
        else:
            if xrange:
                if xrange[0]:
                    fromx=np.argmax(x>xrange[0])
                else:
                    fromx=0
                if xrange[1]:
                    tox=np.argmax(x>xrange[1])
                else:
                    tox=len(x)-1               
                if tox==0:
                    tox=len(x)-1   
                x0=x[fromx:tox]
                y0=y[fromx:tox]
                
                ax.set_xlim(x[fromx]-0.2,x_break-0.001)
                ax2.set_xlim(x_break+0.001,x[tox]*1.2)
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
        
    return fig

def MLtimecontour(x,y,Z,
              x_range=[None,None],
              x_break=1,
              y_range=[None,None],
              Z_range=[None,None],
              title=None,
              zero_contour=False,
              **rcParams):
    
    mpl.rcParams.update(**Params)
    
    mpl.rcParams.update({'figure.figsize': (16,4*16/6),
                         'lines.linewidth': 4,
                        'lines.markersize': 8,
                        'font.size': 50,
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
    
    if x_range[0]==None:
        x_range[0]=np.nanmin(x)-1e-6
    if x_range[1]==None:
        x_range[1]=np.nanmax(x)-1e-6
        
    if Z_range[0]==None:
        Z_range[0]=np.nanmin(Z)-1e-6
    if Z_range[1]==None:
        Z_range[1]=np.nanmax(Z)-1e-6
    
    mpl.rcParams.update(**rcParams)           
    fig,ax=plt.subplots(1,2,gridspec_kw={'width_ratios':[1,2],'wspace':0.012})
   
    ##############
    ####Contour
    n_levels=40
    levels = np.linspace(Z_range[0],Z_range[1],n_levels)
    zero=np.argmax(levels>0)
    levels=np.concatenate((levels[:zero],[0],levels[zero:]))
    cmap_neg=[mpl.cm.get_cmap('Blues')(n/zero) for n in range(zero)]#+[mpl.cm.get_cmap('Reds')(round(n/(1*(n_levels+1)/3))) for n in range(1*(n_levels+1)/3)]#[mpl.cm.get_cmap('YlGnBu')(n/n_levels) for n in range(n_levels)].reverse()+
    cmap_pos=[mpl.cm.get_cmap('Reds')(n/(n_levels-zero)) for n in range(n_levels-zero)]
    cmap=cmap_neg[::-1]+[(1,1,1)]+ cmap_pos
    

    ax[0].contourf(x[np.argmax(x>x_range[0]):np.argmax(x>x_break)],
                   y,
                     Z[:,np.argmax(x>x_range[0]):np.argmax(x>x_break)],
                      levels=levels,colors=cmap,extend='both',
                      vmin=Z_range[0],vmax=Z_range[1],
                     )
    if zero_contour:
        ax[0].contour(x[np.argmax(x>x_range[0]):np.argmax(x>x_break)], 
                                 y, 
                                 Z[:,np.argmax(x>x_range[0]):np.argmax(x>x_break)], 
                                 levels=[0], colors='grey', linewidths=0.2)
    img=ax[1].contourf(
                   x[np.argmax(x>x_break):np.argmax(x>x_range[1])],
                   y,
                     Z[:,np.argmax(x>x_break):np.argmax(x>x_range[1])],
                      levels=levels,colors=cmap,extend='both',
                      vmin=Z_range[0],vmax=Z_range[1],
                     )
    if zero_contour:
        ax[1].contour(x[np.argmax(x>x_break):np.argmax(x>x_range[1])],
                                 y, 
                                 Z[:,np.argmax(x>x_break):np.argmax(x>x_range[1])], 
                                 levels=[0], colors='grey', linewidths=0.2)
    ax[1].set_xscale('log')
    ax[1].set_yticks([])
   
    # ax[1].xaxis.set_major_formatter(mticker.ScalarFormatter())
    # ax[0,1].ticklabel_format(style='plain',axis='y')
    # ax[0,1].title.set_text(title)
  

    ax[1].text(0.2, -0.15, '$\Delta$t', va='center',transform=ax[1].transAxes)
    ax[0].set_ylabel('$\Delta$OD')
    
    
    plt.colorbar(img)
     
    plt.title(title)
    
    plt.show()
    plt.close()
    
    return fig

#%% Auxiliary


def set_size(figsize,fig):
        
    h=[Size.Fixed(0), Size.Fixed(figsize[0])]
    v=[Size.Fixed(0),Size.Fixed(figsize[1])]
    
    divider = Divider(fig, (0,0,1,1),h,v, aspect=False)
    
    ax = fig.add_axes(divider.get_position(),axes_locator=divider.new_locator(nx=1, ny=1))
    
    return ax        