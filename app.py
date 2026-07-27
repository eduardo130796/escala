from datetime import datetime

import streamlit as st

from components.calendario import Calendario
from services.escala_service import EscalaService


# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Escala de Trabalho",
    page_icon="📅",
    layout="wide"
)

service = EscalaService()
config = service.config

MESES = [
    "",
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
    "Dezembro",
]


# =====================================================
# SESSION
# =====================================================

if "salvo" not in st.session_state:
    st.session_state.salvo = False

if "ultimo_servidor" not in st.session_state:
    st.session_state.ultimo_servidor = None


# =====================================================
# CABEÇALHO
# =====================================================

st.title("📅 Escala de Trabalho")
st.caption(f"{MESES[config['mes']]} de {config['ano']}")

if config["bloqueado"]:

    st.info(
        "🔒 A escala está encerrada. As escolhas podem ser consultadas, mas não alteradas."
    )


# =====================================================
# SERVIDORES
# =====================================================

servidores = service.listar_servidores()

if not servidores:

    st.error(
        "Nenhum servidor cadastrado."
    )

    st.stop()

opcoes = {
    servidor["nome"]: servidor["id"]
    for servidor in servidores
}

nomes = list(opcoes.keys())

if "servidor" not in st.session_state:

    st.session_state.servidor = nomes[0]

nome_servidor = st.selectbox(
    "👤 Servidor",
    options=nomes,
    key="servidor"
)

servidor_id = opcoes[nome_servidor]


# =====================================================
# RESET AO TROCAR SERVIDOR
# =====================================================

if st.session_state.ultimo_servidor != servidor_id:

    st.session_state.salvo = False
    st.session_state.ultimo_servidor = servidor_id


# =====================================================
# INSTRUÇÕES
# =====================================================

st.caption(
    f"Selecione até {config['max_dias_por_servidor']} dias no calendário. Toque novamente em um dia seu para remover."
)


# =====================================================
# CALENDÁRIO
# =====================================================

calendario = Calendario(
    mes=config["mes"],
    ano=config["ano"]
)

eventos = service.eventos_calendario(
    servidor_id
)

# Quando a escala estiver bloqueada o calendário fica somente leitura.
if config["bloqueado"]:

    calendario.render(eventos)
    clique = None

else:

    clique = calendario.render(eventos)


# =====================================================
# AÇÕES DO CALENDÁRIO
# =====================================================

if clique:

    data = datetime.strptime(
        clique["data"],
        "%Y-%m-%d"
    ).date()

    try:

        if clique["tipo"] == "date":

            service.escolher_dia(
                servidor_id,
                data
            )

        else:

            service.remover_dia(
                servidor_id,
                data
            )

        # Sempre que houver alteração,
        # o botão salvar volta a ficar disponível.
        st.session_state.salvo = False

        st.rerun()

    except ValueError as erro:

        st.error(str(erro))


# =====================================================
# LEGENDA
# =====================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🟢 Seu dia")

with col2:
    st.caption("🔵 Outro servidor")

with col3:
    st.caption("🟠 Selecionado (não confirmado)")


# =====================================================
# ESCOLHAS
# =====================================================

escolhas = service.obter_escolhas(
    servidor_id
)

st.subheader("📅 Dias escolhidos")

if escolhas:

    dias = [
        datetime.strptime(
            escolha["data"][:10],
            "%Y-%m-%d"
        ).strftime("%d/%m")
        for escolha in escolhas
    ]

    st.write(" • ".join(dias))

else:

    st.caption(
        "Nenhum dia selecionado."
    )

st.caption(
    f"{len(escolhas)} de {config['max_dias_por_servidor']} dias escolhidos"
)

st.divider()


# =====================================================
# SALVAR
# =====================================================

if config["bloqueado"]:

    st.info(
        "A escala está bloqueada. Não é possível alterar ou confirmar escolhas."
    )

else:

    if all(escolha["confirmado"] for escolha in escolhas):

        st.session_state.salvo = True

    if st.button(
        "✅ Salvar escolhas",
        use_container_width=True,
        disabled=(
            st.session_state.salvo
            or not escolhas
        )
    ):

        try:

            with st.spinner(
                "Salvando escolhas..."
            ):

                service.confirmar(
                    servidor_id
                )

            st.session_state.salvo = True

            st.success(
                "✅ Escolhas salvas com sucesso."
            )

            st.rerun()

        except ValueError as erro:

            st.error(str(erro))