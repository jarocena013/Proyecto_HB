#SQL
import sqlite3
# Pandas
import pandas as pd
# Graph
import community
import networkx as nx
# Plot
import matplotlib.pyplot as plt
import seaborn as sns
# Combinations
import itertools
from pathlib import Path
# Visualizar comunidades 3D
import random
import gravis


def crear_grafo(sql):
    # Leer datos
    # TODO 8 lineas
    connect = sqlite3.connect(sql)
    query = """
            SELECT pa.paper_id, pa.author_id, a.name
            FROM paper_authors AS pa \
                     JOIN papers AS p ON pa.paper_id = p.id \
                     JOIN authors as a ON pa.author_id = a.id
            WHERE p.Year BETWEEN '2014' AND '2015' \
            """
    df = pd.read_sql(query, connect)

    # Crear grafo
    # TODO 7-10 lineas
    G = nx.Graph()

    # Transform
    for p, a in df.groupby('paper_id')['name']:
        for u, v in itertools.combinations(a, 2):
            if G.has_edge(u, v):
                G[u][v]['weight'] += 1
            else:
                G.add_edge(u, v, weight=1)

    return G


def visualizar_grafo(G):
    # TODO 6 lineas
    plt.figure(figsize=(13, 9))
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color='0.75')
    nx.draw_networkx_edges(G, pos, alpha=0.5, width=1)
    plt.show()

    plt.axis('off')
    plt.show()



def visualizar_comunidades(G, particion):
    vista = G.copy()
    comunidades = sorted({particion[n] for n in vista.nodes})

    # Generar colores aleatorios sin repetir
    tonos = random.sample(range(0x1000000), len(comunidades))
    colores = {
        comunidad: f"#{tono:06x}"
        for comunidad, tono in zip(comunidades, tonos)
    }

    # Colorear los nodos
    for nodo in vista.nodes:
        vista.nodes[nodo]["color"] = colores[particion[nodo]]
        vista.nodes[nodo]["label"] = ""

    # Una etiqueta por comunidad
    for comunidad in comunidades:
        representante = next(
            n for n in vista.nodes if particion[n] == comunidad
        )
        vista.nodes[representante]["label"] = f"Comunidad {comunidad}"

    vista.graph["background_color"] = "white"
    vista.graph["node_label_color"] = "black"

    gravis.three(
        vista,
        graph_height=600,
        node_label_data_source="label",
        show_node_label=True
    ).display(inline=True)