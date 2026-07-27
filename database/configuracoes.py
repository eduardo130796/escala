from database.client import supabase

TABELA = "configuracoes"


# ==========================================================
# CONSULTAS
# ==========================================================

def obter():

    return (
        supabase
        .table(TABELA)
        .select("*")
        .eq("id", 1)
        .single()
        .execute()
    )


# ==========================================================
# ATUALIZAÇÃO
# ==========================================================

def atualizar(
    mes: int,
    ano: int,
    max_dias_por_servidor: int,
    bloqueado: bool
):

    return (
        supabase
        .table(TABELA)
        .update(
            {
                "mes": mes,
                "ano": ano,
                "max_dias_por_servidor": max_dias_por_servidor,
                "bloqueado": bloqueado
            }
        )
        .eq("id", 1)
        .execute()
    )