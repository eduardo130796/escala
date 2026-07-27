from datetime import datetime

import streamlit as st
import pandas as pd

from services.admin_service import AdminService
from components.calendario import Calendario
from components.exportacao import Exportacao


st.set_page_config(
    page_title="Administrador",
    page_icon="⚙️",
    layout="wide"
)

service = AdminService()
config = service.config

MESES = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"
]

st.title("⚙️ Administração")

# ==========================================================
# COMPETÊNCIA
# ==========================================================

st.subheader("📅 Competência")

escala_iniciada = service.existem_escolhas()

col1, col2 = st.columns(2)

with col1:

    mes = st.selectbox(
        "Mês",
        options=range(1, 13),
        index=config["mes"] - 1,
        format_func=lambda x: MESES[x - 1],
        disabled=escala_iniciada
    )

with col2:

    ano = st.number_input(
        "Ano",
        min_value=2024,
        max_value=2100,
        value=config["ano"],
        disabled=escala_iniciada
    )

max_dias = st.number_input(
    "Máximo de dias por servidor",
    min_value=1,
    max_value=31,
    value=config["max_dias_por_servidor"]
)

if escala_iniciada:

    st.info(
        "A competência já foi iniciada. Para alterar mês ou ano limpe a escala primeiro."
    )

col1, col2 = st.columns([2,1])

with col1:

    if st.button(
        "💾 Salvar configuração",
        use_container_width=True,
        disabled=escala_iniciada
    ):

        try:

            with st.spinner("Salvando..."):

                service.salvar_configuracao(
                    mes,
                    ano,
                    max_dias
                )

            st.success(
                "Configuração salva com sucesso."
            )

        except ValueError as e:

            st.error(str(e))

with col2:

    permitir = st.toggle(
        "Receber escolhas",
        value=not config["bloqueado"]
    )

    if permitir != (not config["bloqueado"]):

        service.alterar_status_edicao(
            permitir
        )

        st.rerun()

st.divider()

# ==========================================================
# CALENDÁRIO
# ==========================================================

st.subheader("📅 Calendário")

eventos = service.eventos_calendario()

calendario = Calendario(
    mes=config["mes"],
    ano=config["ano"]
)

clique = calendario.render(eventos)

st.caption(
    "🟢 Disponível   🔵 Escolhido   ✔ Confirmado"
)

st.divider()

# ==========================================================
# ESCOLHAS DO DIA
# ==========================================================

if clique and clique["tipo"] == "date":

    data = datetime.strptime(
        clique["data"],
        "%Y-%m-%d"
    ).date()

    escolhas = service.escolhas_por_data(
        data
    )

    st.subheader(
        f"👥 Escolhas de {data.strftime('%d/%m/%Y')}"
    )

    if escolhas:

        for escolha in escolhas:

            status = (
                "✅ Confirmado"
                if escolha["confirmado"]
                else "⏳ Em edição"
            )

            st.write(
                f"• {escolha['servidores']['nome']} — {status}"
            )

    else:

        st.info(
            "Nenhuma escolha cadastrada para esta data."
        )

st.divider()

# ==========================================================
# RESUMO
# ==========================================================

st.subheader("📋 Resumo")

resumo = service.listar_resumo()

if resumo:

    st.dataframe(
        resumo,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": None,
            "nome": st.column_config.TextColumn(
                "Servidor"
            ),
            "dias": st.column_config.NumberColumn(
                "Dias"
            ),
            "confirmado": st.column_config.CheckboxColumn(
                "Confirmado"
            ),
        }
    )

else:

    st.info(
        "Nenhum servidor cadastrado."
    )

st.divider()

# ==========================================================
# EXPORTAÇÃO
# ==========================================================

st.subheader("📤 Exportação")

escolhas = service.listar_escolhas()

pdf = Exportacao.gerar_pdf(
    escolhas,
    config["mes"],
    config["ano"]
)

excel = Exportacao.gerar_excel(
    escolhas
)

col1, col2 = st.columns(2)

with col1:

    st.download_button(
        "📄 Baixar PDF",
        data=pdf,
        file_name=f"escala_{config['mes']:02d}_{config['ano']}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

with col2:

    st.download_button(
        "📊 Baixar Excel",
        data=excel,
        file_name=f"escala_{config['mes']:02d}_{config['ano']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.divider()

# ==========================================================
# ZONA DE PERIGO
# ==========================================================

st.subheader("⚠️ Zona de perigo")

st.caption(
    "Apaga todas as escolhas da competência atual."
)

if "confirmar_limpeza" not in st.session_state:

    st.session_state.confirmar_limpeza = False

if not st.session_state.confirmar_limpeza:

    if st.button(
        "🗑 Limpar escala",
        type="primary",
        use_container_width=True
    ):

        st.session_state.confirmar_limpeza = True
        st.rerun()

else:

    st.warning(
        "Esta ação apagará TODAS as escolhas da escala.\n\n"
        "Ela não poderá ser desfeita."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Cancelar",
            use_container_width=True
        ):

            st.session_state.confirmar_limpeza = False
            st.rerun()

    with col2:

        if st.button(
            "Confirmar exclusão",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "Apagando escala..."
            ):

                service.limpar_escala()

            st.session_state.confirmar_limpeza = False

            st.success(
                "Escala apagada com sucesso."
            )

            st.rerun()