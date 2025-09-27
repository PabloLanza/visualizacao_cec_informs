import streamlit as st
import plotly_express as px
import pandas as pd
from func import gols


st.title("Painel de Artilheiros")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])


competicao_sel = tuple(competicao_sel)
mando_sel = tuple(mando_sel)

if len(competicao_sel) == 1:
    competicao_sel = competicao_sel + ('',)

if len(mando_sel) == 1:
    mando_sel = mando_sel + ('',)

df = gols(competicoes=competicao_sel, mando=mando_sel)

st.table(df)