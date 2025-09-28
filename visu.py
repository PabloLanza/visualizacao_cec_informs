import streamlit as st
import pandas as pd
import func

st.markdown("""
                <style>
                h1 {color: darkblue !important;
                    text_align: center;
                }
                <style>""", unsafe_allow_html=True)

st.title("PAINEL INTERATIVO CEC INFORMS")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])


#TABELA DE ARTILHEIROS
st.title("Ranking de Artilheiros")
df_gols = func.gols(competicoes=competicao_sel, mando=mando_sel)
st.table(df_gols)

#TABELA DE ASSISTÊNCIAS
st.title("Ranking de Assistências")
df_ass = func.assistencias(competicoes=competicao_sel, mando=mando_sel)
st.table(df_ass)

#TABELA DE PARTICIPAÇÕES EM GOLS
st.title("Ranking de Participações em Gols")
df_participacoes = func.participacoes(competicoes=competicao_sel, mando=mando_sel)
st.table(df_participacoes)

#TABELA DE DOBRADINHAS
st.title("Ranking de Dobradinhas")
st.write("Dobradinha é quando um jogador x da assistencias pra um jogador y fazer o gol ou vice-versa")
df_dobradinha = func.dobradinha(competicoes=competicao_sel, mando=mando_sel)
st.table(df_dobradinha)

