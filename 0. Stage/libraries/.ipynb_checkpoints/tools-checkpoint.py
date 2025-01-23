import numpy as np
import scipy as s
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.interpolate import RectBivariateSpline, LSQBivariateSpline, bisplev
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import Normalize

epsilon_0 = 8.854187817e-12
mu_0 = 4 * np.pi * 1e-7

import pandas as pd

def load_df(path):
    """
    Carrega um arquivo CSV no formato de dados espaçados e renomeia as colunas 'W' e 'Z' para 'Ex' e 'Ey'.

    Parâmetros:
    - path: Caminho para o arquivo CSV a ser carregado.

    Retorna:
    - df: DataFrame com os dados carregados e as colunas renomeadas.
    """
    # Carrega o arquivo CSV usando o delimitador de espaços
    raw_data = pd.read_csv(path, delimiter=r'\s+')

    # Renomeia as colunas conforme solicitado
    raw_data.rename(columns={"W": "Ex", "Z": "Ey"}, inplace=True)

    # Retorna o DataFrame com os dados e as colunas renomeadas
    return raw_data



def slice_df(df, x_min, x_max, y_min, y_max):
    """
    Filtra o DataFrame para incluir apenas as linhas onde as colunas 'x' e 'y' estão dentro dos limites fornecidos.

    Parâmetros:
    - df: DataFrame contendo as colunas 'x' e 'y'.
    - x_min: Valor mínimo para a coluna 'x'.
    - x_max: Valor máximo para a coluna 'x'.
    - y_min: Valor mínimo para a coluna 'y'.
    - y_max: Valor máximo para a coluna 'y'.

    Retorna:
    - DataFrame filtrado com as linhas dentro dos limites especificados para 'x' e 'y'.
    """
    # Filtra o DataFrame com base nos limites fornecidos
    filtered_df = df[(df['x'] > x_min) & (df['x'] < x_max) & (df['y'] > y_min) & (df['y'] < y_max)]
    return filtered_df




def plot_heatmap_fields(df):
    """
    Plota dois heatmaps lado a lado: um para Ex(x, y) e outro para Ey(x, y).

    Parâmetros:
    - df: DataFrame contendo as colunas 'x', 'y', 'Ex', e 'Ey' com os dados a serem visualizados
    """
    # Cria a figura e os eixos para os heatmaps
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

    # Heatmap para Ex(x, y)
    sc1 = axes[0].scatter(df['x'], df['y'], c=df['Ex'], cmap='viridis', s=10)
    axes[0].set_title('$E_x(x, y)$', fontsize=14)
    axes[0].set_xlabel('x', fontsize=12)
    axes[0].set_ylabel('y', fontsize=12)
    axes[0].grid(True)
    plt.colorbar(sc1, ax=axes[0], label='$E_x$', fraction=0.046, pad=0.04)

    # Heatmap para Ey(x, y)
    sc2 = axes[1].scatter(df['x'], df['y'], c=df['Ey'], cmap='plasma', s=10)
    axes[1].set_title('$E_y(x, y)$', fontsize=14)
    axes[1].set_xlabel('x', fontsize=12)
    axes[1].grid(True)
    plt.colorbar(sc2, ax=axes[1], label='$E_y$', fraction=0.046, pad=0.04)

    # Ajusta o layout e exibe o gráfico
    plt.tight_layout()
    plt.show()


    
def plot_3d_fields(df):
    """
    Plota dois gráficos 3D interativos lado a lado: um para Ex(x, y) e outro para Ey(x, y).

    Parâmetros:
    - df: DataFrame contendo as colunas 'x', 'y', 'Ex', e 'Ey' com os dados a serem plotados
    """
    # Inicializa a figura com o tamanho desejado
    fig = plt.figure(figsize=(14, 6))

    # Gráfico para Ex(x, y)
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(df['x'], df['y'], df['Ex'], c=df['Ex'], cmap='viridis', marker='o', s=20, label='Ex(x, y)')
    ax1.set_title('Distribuição de Ex(x, y)', fontsize=14)
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)
    ax1.set_zlabel('Ex', fontsize=12)
    ax1.legend()

    # Gráfico para Ey(x, y)
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(df['x'], df['y'], df['Ey'], c=df['Ey'], cmap='plasma', marker='^', s=20, label='Ey(x, y)')
    ax2.set_title('Distribuição de Ey(x, y)', fontsize=14)
    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel('y', fontsize=12)
    ax2.set_zlabel('Ey', fontsize=12)
    ax2.legend()

    # Ajusta o layout para melhor visualização
    plt.tight_layout()
    plt.show()
    
    

def plot_3d_interactive_fields(df, campo='Ex'):
    """
    Função para plotar uma visualização 3D interativa de Ex ou Ey.

    Parâmetros:
    - df: DataFrame contendo as colunas 'x', 'y', 'Ex', e 'Ey'
    - campo: 'Ex' ou 'Ey', para escolher o campo a ser plotado (default 'Ex')
    """
    if campo not in ['Ex', 'Ey']:
        raise ValueError("O parâmetro 'campo' deve ser 'Ex' ou 'Ey'.")

    fig_e = go.Figure()

    fig_e.add_trace(go.Scatter3d(
        x=df['x'],
        y=df['y'],
        z=df[campo],
        mode='markers',
        marker=dict(
            size=3,
            color=df[campo],  # Cor baseada nos valores do campo
            colorscale='Plasma',  # Escala de cores do dourado ao laranja escuro
            cmin=df[campo].min(),
            cmax=df[campo].max(),
            colorbar=dict(title=f'{campo}'),  # Barra de cores dinâmica
        ),
        name=f'{campo}(x, y)'
    ))

    fig_e.update_layout(
        title=f'{campo}(x, y)',
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title=campo
        )
    )

    fig_e.show()
    
    

def plot_3d_int_general(x,y,z):
    # Create a 3D surface plot
    fig = go.Figure(
        data=[go.Surface(
            z=z,
            x=x,  # x-coordinates
            y=y,  # y-coordinates
            colorscale='Plasma',  # Color scheme
        )]
    )

    # Add labels and title
    fig.update_layout(
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z'
        ),
    )

    # Show the interactive plot
    fig.show()