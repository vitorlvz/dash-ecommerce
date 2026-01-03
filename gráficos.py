import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(r"C:\Users\Vitor Luviza\Desktop\atividade pandas\ecommerce_estatistica.csv")
import numpy as np

import dash
from dash import dcc, html
import plotly.express as px

df["Qtd_Vendidos"] = (
    df["Qtd_Vendidos"].astype(str)
    .str.replace("mil", "000", regex=False)
    .str.replace("+", "", regex=False)
    .str.replace(".", "", regex=False)
    .astype(float)
)


#histograma#

fig_hist = px.histogram(
    df, 
    x="Preço",
    nbins=40,
    title="Distribuição de Preços"
)





#df.hist(figsize=(12,8))
#plt.tight_layout()
#plt.show()


#dispersão#
fig_disp = px.scatter(
    df,
    x="Preço",
    y="Qtd_Vendidos",
    title="Preço vs Quantidade Vendida",
    opacity=0.6
)



plt.figure(figsize=(8,5))
plt.scatter(df["Preço"], df["Qtd_Vendidos_Cod"], alpha=0.6)

plt.title("Relação entre Preço e Quantidade Vendida")
plt.xlabel("Preço (R$)")
plt.ylabel("Quantidade Vendida")

plt.grid(True)
#plt.show()

#mapa de calor#

cols = ["Preço", "Nota", "N_Avaliações", "Desconto", "Qtd_Vendidos"]
corr = df[cols].corr()

fig_heatmap = px.imshow(
    corr,
    text_auto=True,
    title="Mapa de Calor das Correlações",
    color_continuous_scale="viridis"
)



df["Qtd_Vendidos"] = df["Qtd_Vendidos"].astype(str)

df["Qtd_Vendidos"] = (
    df["Qtd_Vendidos"]
    .str.replace("mil", "000", regex=False)  # transforma "10mil" em "10000"
    .str.replace("+", "", regex=False)       # remove o "+"
    .str.replace(".", "", regex=False)       # remove pontos caso existam
    .astype(float)
)

plt.figure()
cols = ["Preço", "Nota", "N_Avaliações", "Desconto", "Qtd_Vendidos"]
corr = df[cols].corr()

plt.imshow(corr, cmap="viridis", interpolation="nearest")
plt.title("Mapa de Calor das Correlações")
plt.xticks(range(len(cols)), cols, rotation=45)
plt.yticks(range(len(cols)), cols)
plt.colorbar()
#plt.show()

#gráfico de barra - Top 5 Marcas Mais Vendidas#


top_marcas = df["Marca"].value_counts().head(5).reset_index()
top_marcas.columns = ["Marca", "Quantidade"]

fig_bar = px.bar(
    top_marcas,
    x="Marca",
    y="Quantidade",
    title="Top 5 Marcas Mais Vendidas"
)



plt.figure()
top_marcas = df["Marca"].value_counts().head(5)
plt.bar(top_marcas.index, top_marcas.values)
plt.title("Top 5 Marcas Mais Vendidas")
plt.xlabel("Marca")
plt.ylabel("Quantidade")
#plt.show()

#gráfico de pizza - Distribuição de Gênero#

generos = df["Gênero"].value_counts().reset_index()
generos.columns = ["Gênero", "Quantidade"]

fig_pie = px.pie(
    generos,
    names="Gênero",
    values="Quantidade",
    title="Distribuição de Gênero"
)



plt.figure()
generos = df["Gênero"].value_counts()
plt.pie(generos.values, labels=generos.index, autopct="%1.1f%%")
plt.title("Distribuição de Gênero")
#plt.show()

#gráfico de densidade - Preço#
precos = df["Preço"].dropna().values

density, bins = np.histogram(precos, bins=40, density=True)
centers = 0.5 * (bins[1:] + bins[:-1])


plt.figure()
plt.plot(centers, density)
plt.title("Densidade dos Preços (Matplotlib + NumPy)")
plt.xlabel("Preço")
plt.ylabel("Densidade")
#plt.show()

#gráfico de regressão - Preço vs Avaliações#

fig_reg = px.scatter(
    df,
    x="Preço",
    y="N_Avaliações",
    trendline="ols",
    title="Regressão: Preço vs Nº de Avaliações"
)



plt.figure()
x = df["Preço"]
y = df["N_Avaliações"]

coef = np.polyfit(x, y, 1)  
reg_fn = np.poly1d(coef)

plt.scatter(x, y)
plt.plot(x, reg_fn(x))
plt.title("Regressão Linear: Preço vs Nº de Avaliações")
plt.xlabel("Preço")
plt.ylabel("Nº de Avaliações")
#plt.show()


app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#f5f6fa",
        "padding": "20px",
        "fontFamily": "Arial"
    },
    children=[

        html.H1(
            "Dashboard E-commerce",
            style={
                "textAlign": "center",
                "marginBottom": "30px"
            }
        ),

        html.Div(
            style={"display": "flex", "gap": "20px"},
            children=[
                html.Div(dcc.Graph(figure=fig_hist), style={"flex": 1}),
                html.Div(dcc.Graph(figure=fig_disp), style={"flex": 1}),
            ]
        ),

        html.Div(
            style={"display": "flex", "gap": "20px", "marginTop": "20px"},
            children=[
                html.Div(dcc.Graph(figure=fig_heatmap), style={"flex": 1}),
                html.Div(dcc.Graph(figure=fig_bar), style={"flex": 1}),
            ]
        ),

       
        html.Div(
            style={"display": "flex", "gap": "20px", "marginTop": "20px"},
            children=[
                html.Div(dcc.Graph(figure=fig_pie), style={"flex": 1}),
                html.Div(dcc.Graph(figure=fig_reg), style={"flex": 1}),
            ]
        ),
    ]
)



if __name__ == "__main__":
    app.run(debug=True)
