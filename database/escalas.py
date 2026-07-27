from datetime import date

from database.client import supabase

TABELA = "escalas"


# ==========================================================
# CONSULTAS
# ==========================================================

def listar():

    return (
        supabase
        .table(TABELA)
        .select("""
            *,
            servidores (
                id,
                nome
            )
        """)
        .order("data")
        .execute()
    )


def listar_eventos():

    return (
        supabase
        .table(TABELA)
        .select("""
            id,
            servidor_id,
            data,
            confirmado,
            servidores (
                id,
                nome
            )
        """)
        .order("data")
        .execute()
    )


def listar_por_servidor(
    servidor_id: int
):

    return (
        supabase
        .table(TABELA)
        .select("""
            id,
            servidor_id,
            data,
            confirmado
        """)
        .eq("servidor_id", servidor_id)
        .order("data")
        .execute()
    )


def listar_por_data(
    data: date
):

    return (
        supabase
        .table(TABELA)
        .select("""
            *,
            servidores (
                id,
                nome
            )
        """)
        .eq("data", data.isoformat())
        .order("created_at")
        .execute()
    )


def listar_confirmadas():

    return (
        supabase
        .table(TABELA)
        .select("""
            *,
            servidores (
                id,
                nome
            )
        """)
        .eq("confirmado", True)
        .order("data")
        .execute()
    )


def listar_em_edicao():

    return (
        supabase
        .table(TABELA)
        .select("""
            *,
            servidores (
                id,
                nome
            )
        """)
        .eq("confirmado", False)
        .order("data")
        .execute()
    )


# ==========================================================
# INSERÇÃO
# ==========================================================

def inserir(
    servidor_id: int,
    data: date
):

    return (
        supabase
        .table(TABELA)
        .insert(
            {
                "servidor_id": servidor_id,
                "data": data.isoformat(),
                "confirmado": False
            }
        )
        .execute()
    )


# ==========================================================
# ATUALIZAÇÃO
# ==========================================================

def confirmar(
    id_escala: int
):

    return (
        supabase
        .table(TABELA)
        .update(
            {
                "confirmado": True
            }
        )
        .eq("id", id_escala)
        .execute()
    )


def desconfirmar(
    id_escala: int
):

    return (
        supabase
        .table(TABELA)
        .update(
            {
                "confirmado": False
            }
        )
        .eq("id", id_escala)
        .execute()
    )


# ==========================================================
# EXCLUSÃO
# ==========================================================

def excluir(
    id_escala: int
):

    return (
        supabase
        .table(TABELA)
        .delete()
        .eq("id", id_escala)
        .execute()
    )


def excluir_por_data(
    servidor_id: int,
    data: date
):

    return (
        supabase
        .table(TABELA)
        .delete()
        .eq("servidor_id", servidor_id)
        .eq("data", data.isoformat())
        .execute()
    )


def excluir_por_servidor(
    servidor_id: int
):

    return (
        supabase
        .table(TABELA)
        .delete()
        .eq("servidor_id", servidor_id)
        .execute()
    )


def excluir_todas():

    return (
        supabase
        .table(TABELA)
        .delete()
        .neq("id", 0)
        .execute()
    )

# ==========================================================
# ESTATÍSTICAS
# ==========================================================

# ==========================================================
# ESTATÍSTICAS
# ==========================================================

def quantidade():

    response = (
        supabase
        .table(TABELA)
        .select(
            "id",
            count="exact"
        )
        .execute()
    )

    return response.count or 0