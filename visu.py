import streamlit as st
import pandas as pd
import func




st.title("Painel de Artilheiros")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])


df = func.gols(competicoes=competicao_sel, mando=mando_sel)

st.table(df)