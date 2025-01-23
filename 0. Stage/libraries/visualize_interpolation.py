import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import os
import imageio




def vis_slice(X, Y, E, Xnew, Ynew, Enew, ponto=0, parametro=10, fixar='y', salvar_imagens=False):
    """
    Visualiza a comparação entre os pontos originais e a interpolação para Ex ou Ey, 
    fixando um dos eixos (x ou y). Retorna a figura gerada e, opcionalmente, salva as imagens.

    Parâmetros:
    - X, Y: Arrays 2D com as coordenadas originais.
    - E: Array 2D com os valores originais do campo Ex ou Ey.
    - Xnew, Ynew: Arrays 2D com as coordenadas interpoladas.
    - Enew: Array 2D com os valores interpolados dos campos Ex ou Ey.
    - ponto: Índice do ponto no eixo fixado (default é 38).
    - parametro: Fator de interpolação para definir a densidade do índice interpolado (default é 100).
    - fixar: 'x' ou 'y' para indicar qual eixo será fixado (default é 'y').
    - salvar_imagens: Se True, salva as imagens para gerar o GIF (default é False).
    - tamanho_marker: Tamanho dos pontos no gráfico (default é 8).

    Retorna:
    - A figura gerada.
    """
    if fixar == 'y':
        eixo_original = X[ponto, :]
        valores_originais = E[ponto, :]
        eixo_interpolado = Xnew[ponto * parametro, :]
        valores_interpolados = Enew[ponto * parametro, :]
        titulo = f'Comparação de E para $y = {Y[ponto, 0]:.4f}$'
        eixo_label = 'x'
    elif fixar == 'x':
        eixo_original = Y[:, ponto]
        valores_originais = E[:, ponto]
        eixo_interpolado = Ynew[:, ponto * parametro]
        valores_interpolados = Enew[:, ponto * parametro]
        titulo = f'Comparação de {campo} para $x = {X[0, ponto]:.4f}$'
        eixo_label = 'y'
    else:
        raise ValueError("O parâmetro 'fixar' deve ser 'x' ou 'y'.")

    # Criando a figura com plotly
    fig = go.Figure()

    # Adicionando as curvas de dispersão
    fig.add_trace(go.Scatter(x=eixo_original, y=valores_originais, mode='markers', name='Original', marker=dict(color='#2A9D8F', size=6)))  
    fig.add_trace(go.Scatter(x=eixo_interpolado, y=valores_interpolados, mode='markers', name='Interpolado', marker=dict(color='#E76F51', size=2)))  

    # Título e labels
    fig.update_layout(
        title='Interpolation Slice Visualization',
        xaxis_title='x',
        yaxis_title='y',
        template='ggplot2'
    )
    fig.update_yaxes(range=[1.3*E.min(), 1.3*E.max()])

    if salvar_imagens:
        # Salva a imagem
        nome_imagem = f"imagens/imagem_{ponto}.png"
        fig.write_image(nome_imagem)

    return fig









def gerar_gif(X, Y, Ex, Xnew, Ynew, Exnew, output_gif="output.gif", parametro=10, fixar='y'):
    """
    Gera um GIF a partir das visualizações de slices do campo Ex ou Ey.

    Parâmetros:
    - X, Y: Arrays 2D com as coordenadas originais.
    - Ex, Xnew, Ynew, Exnew: Arrays 2D com os valores dos campos e coordenadas.
    - output_gif: Nome do arquivo GIF de saída (default é 'output.gif').
    - parametro: Fator de interpolação (default é 10).
    - fixar: Eixo a ser fixado, 'x' ou 'y' (default é 'y').
    """
    figuras = []
    for i in range(len(Y)):
        # Gerando as figuras para cada ponto
        fig = vis_slice(X, Y, Ex, Xnew, Ynew, Exnew, ponto=i, parametro=parametro, fixar=fixar)
        
        # Capturando a imagem em formato PNG
        img_bytes = fig.to_image(format="png", width=1600, height=1200)
        img = imageio.imread(img_bytes)
        figuras.append(img)

    # Salvando o GIF
    imageio.mimsave(output_gif, figuras, duration=0.5)  # Ajuste o duration conforme necessário

    print(f"GIF gerado com sucesso! Salvo como: {output_gif}")

# Exemplo de chamada da função
# Supondo que X, Y, Ex, Xnew, Ynew, Exnew sejam os dados fornecidos:
# gerar_gif(X, Y, Ex, Xnew, Ynew, Exnew)




def vis_slice_com_slider(X, Y, E, Xnew, Ynew, Enew, parametro=10, fixar='y'):
    """
    Visualiza os slices das imagens com interpolação usando um slider interativo.

    Parâmetros:
    - X, Y: Arrays 2D com as coordenadas originais.
    - E: Array 2D com os valores originais do campo Ex ou Ey.
    - Xnew, Ynew: Arrays 2D com as coordenadas interpoladas.
    - Enew: Array 2D com os valores interpolados dos campos Ex ou Ey.
    - parametro: Fator de interpolação para definir a densidade do índice interpolado (default é 10).
    - fixar: 'x' ou 'y' para indicar qual eixo será fixado (default é 'y').

    Retorna:
    - A figura interativa com slider.
    """
    frames = []  # Lista para armazenar os frames
    steps = []   # Lista para os passos do slider

    for ponto in range(len(Y)):
        if fixar == 'y':
            eixo_original = X[ponto, :]
            valores_originais = E[ponto, :]
            eixo_interpolado = Xnew[ponto * parametro, :]
            valores_interpolados = Enew[ponto * parametro, :]
            titulo = f"Slice para $y = {Y[ponto, 0]:.4f}$"
            eixo_label = 'x'
        elif fixar == 'x':
            eixo_original = Y[:, ponto]
            valores_originais = E[:, ponto]
            eixo_interpolado = Ynew[:, ponto * parametro]
            valores_interpolados = Enew[:, ponto * parametro]
            titulo = f"Slice para $x = {X[0, ponto]:.4f}$"
            eixo_label = 'y'
        else:
            raise ValueError("O parâmetro 'fixar' deve ser 'x' ou 'y'.")

        # Criação do frame para o slider
        frame = go.Frame(
            data=[
                go.Scatter(x=eixo_original, y=valores_originais, mode='markers', 
                           marker=dict(color='#2A9D8F', size=6), name='Original'),
                go.Scatter(x=eixo_interpolado, y=valores_interpolados, mode='markers', 
                           marker=dict(color='#E76F51', size=3), name='Interpolado'),
            ],
            name=str(ponto),
            layout=go.Layout(title=titulo)
        )
        frames.append(frame)

        # Adicionando um passo no slider
        steps.append({
            "args": [[str(ponto)], {"frame": {"duration": 300, "redraw": True}, "mode": "immediate"}],
            "label": f"{ponto}",
            "method": "animate",
        })

    # Figura principal
    fig = go.Figure(
        data=[
            go.Scatter(x=X[0, :], y=E[0, :], mode='markers', marker=dict(color='#2A9D8F', size=6), name='Original'),
            go.Scatter(x=Xnew[0, :], y=Enew[0, :], mode='markers', marker=dict(color='#E76F51', size=3), name='Interpolado'),
        ],
        layout=go.Layout(
            title="Visualização Interativa com Slider",
            xaxis_title=eixo_label,
            yaxis_title="E",
            template="ggplot2",
            updatemenus=[{
                "buttons": [
                    {"args": [None, {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True}],
                     "label": "Play", "method": "animate"},
                    {"args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                     "label": "Pause", "method": "animate"}
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }],
            sliders=[{
                "active": 0,
                "steps": steps,
                "x": 0.1,
                "len": 0.9,
                "xanchor": "left",
                "yanchor": "top",
                "pad": {"b": 10, "t": 50},
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Frame: ",
                    "visible": True,
                    "xanchor": "right"
                },
                "transition": {"duration": 300, "easing": "cubic-in-out"}
            }]
        ),
        frames=frames
    )
    fig.update_yaxes(range=[1.3*E.min(), 1.3*E.max()])

    return fig

# Exemplo de chamada
# Supondo que X, Y, Ex, Xnew, Ynew, Exnew sejam seus arrays:
# fig = vis_slice_com_slider(X, Y, Ex, Xnew, Ynew, Exnew)
# fig.show()