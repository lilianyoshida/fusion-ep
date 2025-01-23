import numpy as np
import scipy as s
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import ipywidgets as widgets
import imageio
import plotly.io as pio
import imageio
import io

from scipy.interpolate import RectBivariateSpline, LSQBivariateSpline, bisplev
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import Normalize
from ipywidgets import interact
from PIL import Image

def rect(df,interp_factor):
    x = np.sort(df['x'].unique())
    y = np.sort(df['y'].unique())

    Ex_r = df.pivot(index='y', columns='x', values='Ex').to_numpy()
    Ey_r = df.pivot(index='y', columns='x', values='Ey').to_numpy()

    xnew = np.linspace(x.min(), x.max(), len(x-1) * interp_factor + 1)
    ynew = np.linspace(y.min(), y.max(), len(y-1) * interp_factor + 1)


    rect_spline_ex = RectBivariateSpline(x,y,Ex_r)
    rect_spline_ey = RectBivariateSpline(x,y,Ey_r)
    
    return rect_spline_ex, rect_spline_ey

def lsq(df,interp_factor,num_knots):
    x = df['x'].to_numpy()
    y = df['y'].to_numpy()
    
    Ex = df['Ex'].to_numpy()
    Ey = df['Ey'].to_numpy()
    
    tx = np.linspace(x.min(), x.max(), num_knots)
    ty = np.linspace(x.min(), x.max(), num_knots)
    
    xnew = np.linspace(x.min(), x.max(), (len(x-1) * interp_factor) + 1)
    ynew = np.linspace(x.min(), y.max(), (len(y-1) * interp_factor) + 1)
    
    lsq_spline_ex = LSQBivariateSpline(x,y,Ex,tx,ty)
    lsq_spline_ey = LSQBivariateSpline(x,y,Ey,tx,ty)
    
    return lsq_spline_ex, lsq_spline_ey