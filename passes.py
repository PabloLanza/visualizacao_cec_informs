import streamlit as st
import pandas as pd
import func

st.markdown("""
                <style>
                h1 {color: darkblue !important;
                    text_align: center;
                }
                <style>""", unsafe_allow_html=True)

st.title("CEC INFORMS - PAINEL DE PASSES")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])


fig1, fig2 = func.passes_trocados(competicoes=competicao_sel, mando=mando_sel)

st.pyplot(fig1)
st.pyplot(fig2)