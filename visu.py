import streamlit as st
import pandas as pd
import func



competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])


st.title("Ranking de Artilheiros")

df_gols = func.gols(competicoes=competicao_sel, mando=mando_sel)

st.table(df_gols)

st.title("Ranking de Assistências")

df_ass = func.assistencias(competicoes=competicao_sel, mando=mando_sel)

st.table(df_ass)

st.title("Ranking de Dobradinhas")
st.write("Dobradinha é quando um jogador x da assistencias pra um jogador y fazer o gol ou vice-versa")

df_dobradinha = func.dobradinha(competicoes=competicao_sel, mando=mando_sel)

st.table(df_dobradinha)