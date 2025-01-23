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


    
def format_variables(df,interp_factor):
    # Obtém as coordenadas únicas de x e y
    x = np.sort(df['x'].unique())
    y = np.sort(df['y'].unique())

    # Construir matrizes para os valores de Ex e Ey
    Ex = df.pivot(index='y', columns='x', values='Ex').to_numpy()
    Ey = df.pivot(index='y', columns='x', values='Ey').to_numpy()
    
    xnew = np.linspace(x.min(), x.max(), len(x-1) * interp_factor + 1)
    ynew = np.linspace(y.min(), y.max(), len(y-1) * interp_factor + 1)
    
    # Criar as matrizes de coordenadas
    X, Y = np.meshgrid(x, y)
    Xnew, Ynew = np.meshgrid(xnew, ynew)
    
    return x, y, Ex, Ey, xnew, ynew, X, Y, Xnew, Ynew

    
    
def compute_rect_bivariate_spline(df,parameter=10):
    """
    Realiza a interpolação bivariada para os campos Ex e Ey usando a spline retangular.

    Parâmetros:
    - df: DataFrame contendo as colunas 'x', 'y', 'Ex' e 'Ey', onde 'Ex' e 'Ey' representam os campos elétricos.

    Retorna:
    - X, Y: Matrizes de coordenadas originais (x, y).
    - Ex, Ey: Matrizes dos valores originais de Ex e Ey.
    - Xnew, Ynew: Matrizes de coordenadas interpoladas.
    - Exnew, Eynew: Matrizes dos valores interpolados de Ex e Ey.
    """
    x, y, Ex, Ey, xnew, ynew, X, Y, Xnew, Ynew = format_variables(df, parameter)

    # Cria as splines para Ex e Ey
    spline_Ex = RectBivariateSpline(x, y, Ex)
    spline_Ey = RectBivariateSpline(x, y, Ey)

    # Realiza a interpolação nos novos pontos
    Exnew = spline_Ex(xnew, ynew)
    Eynew = spline_Ey(xnew, ynew)

    # Retorna as variáveis de interesse
    return X, Y, Ex, Ey, Xnew, Ynew, Exnew, Eynew

    

def compute_lsq_bivariate_spline(df, num_knots=30, interp_factor=10, kx=3, ky=3):
    """
    Calcula a interpolação usando LSQBivariateSpline para os componentes Ex e Ey de um campo vetorial.

    Parameters:
        df (pd.DataFrame): DataFrame contendo colunas 'x', 'y', 'Ex', 'Ey' para coordenadas e componentes do campo.
        num_knots (int): Número de nós para os splines ao longo de cada dimensão.
        interp_factor (int): Fator de refinamento para a malha interpolada.
        kx (int): Ordem do spline na direção x.
        ky (int): Ordem do spline na direção y.

    Returns:
        tuple: Dados originais (X, Y, Ex, Ey) e interpolados (Xnew, Ynew, Exnew, Eynew).
    """
    x, y, Ex, Ey, xnew, ynew, X, Y, Xnew, Ynew = format_variables(df, interp_factor)

    # Gerar nós uniformemente espaçados para os splines
    tx = np.linspace(x.min(), x.max(), num_knots)
    ty = np.linspace(y.min(), y.max(), num_knots)

    # Criar os splines LSQ para Ex e Ey
    spline_Ex = LSQBivariateSpline(X.ravel(), Y.ravel(), Ex.ravel(), tx, ty, kx=kx, ky=ky)
    spline_Ey = LSQBivariateSpline(X.ravel(), Y.ravel(), Ey.ravel(), tx, ty, kx=kx, ky=ky)

    # Interpolar os componentes do campo na nova malha
    Exnew = spline_Ex(xnew, ynew)
    Eynew = spline_Ey(xnew, ynew)

    return X, Y, Ex, Ey, Xnew, Ynew, Exnew.T, Eynew.T



def comparison_surface(X, Y, E, Xnew, Ynew, Enew):
    """
    Plota as superfícies 3D para os campos Ex ou Ey originais e interpolados.

    Parâmetros:
    - X, Y: Matrizes de coordenadas originais (x, y).
    - Ex or Ey: Matrizes dos valores originais dos campos Ex e Ey.
    - Xnew, Ynew: Matrizes de coordenadas interpoladas.
    - Exnew or Eynew: Matrizes dos valores interpolados dos campos Ex e Ey.
    """
    # Cria a figura para os subgráficos
    fig = plt.figure(figsize=(14, 6))

    # Subgráfico 1: Superfície para o campo original (Ex ou Ey)
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, E, cmap='viridis', edgecolor='k')
    ax1.set_title("Original E(x, y)")
    ax1.set_zlabel('E')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')

    # Subgráfico 2: Superfície para o campo interpolado (Ex ou Ey)
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(Xnew, Ynew, Enew, cmap='viridis', edgecolor='k')
    ax2.set_title("Interpolated Enew(x, y)")
    ax2.set_zlabel('E')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')

    # Ajusta o layout para melhor visualização
    plt.tight_layout()
    plt.show()
    

    
def comparison_scatter(X, Y, E, Xnew, Ynew, Enew):
    """
    Plota gráficos comparativos em 3D para a superfície original e a superfície ajustada.

    Parâmetros:
    - X, Y: Matrizes 2D de coordenadas originais.
    - Z_original: Valores da superfície original.
    - Xnew, Ynew: Matrizes 2D de coordenadas ajustadas (interpoladas).
    - Z_interpolated: Valores da superfície ajustada (interpolada).
    """
    fig = plt.figure(figsize=(14, 6))

    # Superfície original
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(X, Y, E, c=E, cmap='viridis', edgecolor='k', alpha=0.8)
    ax1.set_title("Superfície Original")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_zlabel("E")

    # Superfície ajustada pelo spline
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(Xnew, Ynew, Enew, c=Enew, cmap='plasma', edgecolor='k', alpha=0.8)
    ax2.set_title("Superfície Ajustada (Spline)")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.set_zlabel("Enew")

    plt.tight_layout()
    plt.show()
    
    
    
    
from scipy.interpolate import RectBivariateSpline

def compute_rect_bivariate_spline_with_methods(df, parameter=10, s=0):
    """
    Realiza a interpolação bivariada para os campos Ex e Ey e explora métodos da spline.
    """
    x, y, Ex, Ey, xnew, ynew, X, Y, Xnew, Ynew = format_variables(df, parameter)

    # Cria as splines para Ex e Ey
    spline_Ex = RectBivariateSpline(x, y, Ex, s=s)
    spline_Ey = RectBivariateSpline(x, y, Ey, s=s)

    # Usando __call__ para interpolação
    Exnew = spline_Ex(xnew, ynew)

    # Obtendo valores de nós e coeficientes
    knots_x, knots_y = spline_Ex.get_knots()
    coeffs = spline_Ex.get_coeffs()

    # Calculando derivadas parciais usando __call__
    dEx_dx = spline_Ex(xnew, ynew, dx=1, dy=0)
    dEx_dy = spline_Ex(xnew, ynew, dx=0, dy=1)

    # Calculando as derivadas parciais usando o método partial_derivative
    partial_dEx_dx = spline_Ex.partial_derivative(dx=1, dy=0)
    partial_dEx_dy = spline_Ex.partial_derivative(dx=0, dy=1)

    # Avaliando valores com ev
    example_value = spline_Ex.ev(2.5, 3.5)

    # Calculando a integral sobre toda a região de interesse
    total_integral = spline_Ex.integral(x.min(), x.max(), y.min(), y.max())

    # Calculando uma integral definida específica
    partial_integral = spline_Ex.integral(x[0], x[-1] / 2, y[0], y[-1] / 2)

    # Residual da spline
    residual = spline_Ex.get_residual()

    # Retornando todas as informações
    return {
        "Exnew": Exnew,
        "knots": (knots_x, knots_y),
        "coeffs": coeffs,
        "dEx_dx": dEx_dx,
        "dEx_dy": dEx_dy,
        "partial_dEx_dx": partial_dEx_dx,
        "partial_dEx_dy": partial_dEx_dy,
        "example_value": example_value,
        "total_integral": total_integral,
        "partial_integral": partial_integral,
        "residual": residual
    }