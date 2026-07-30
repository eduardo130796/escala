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

import re
import unicodedata

def corresponde(busca, nome):

    busca = normalizar(busca).split()
    nome = normalizar(nome).split()

    indice = 0

    for palavra_busca in busca:

        encontrado = False

        while indice < len(nome):

            if nome[indice].startswith(palavra_busca):
                encontrado = True
                indice += 1
                break

            indice += 1

        if not encontrado:
            return False

    return True
def normalizar(texto: str) -> str:

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = "".join(
        c
        for c in texto
        if not unicodedata.combining(c)
    )

    texto = texto.lower()

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()

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

nome_digitado = st.text_input(
    "👤 Digite seu nome",
    placeholder="Ex.: Eduardo Júnior"
)

servidor = None

if nome_digitado:

    busca = normalizar(nome_digitado)

    encontrados = [
        s
        for s in servidores
        if corresponde(
            nome_digitado,
            s["nome"]
        )
    ]

    if len(encontrados) == 1:

        servidor = encontrados[0]

        st.success(
            f"Bem-vindo(a), {servidor['nome']}."
        )

    elif len(encontrados) > 1:

        st.warning(
            "Encontramos mais de um servidor. Digite mais algumas letras."
        )

    else:

        st.error(
            "Servidor não encontrado."
        )

if servidor is None:
    st.stop()

servidor_id = servidor["id"]        

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
    "Selecione pelo menos 2 dias no calendário. Você pode escolher quantos dias desejar. Toque novamente em um dia seu para remover."
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
    f"{len(escolhas)} dia(s) escolhido(s)"
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