from database.client import supabase

TABELA = "servidores"


# ==========================================================
# CONSULTAS
# ==========================================================

def listar():

    return (
        supabase
        .table(TABELA)
        .select("*")
        .eq("ativo", True)
        .order("ordem")
        .execute()
    )


def buscar_por_id(
    servidor_id: int
):

    return (
        supabase
        .table(TABELA)
        .select("*")
        .eq("id", servidor_id)
        .single()
        .execute()
    )


# ==========================================================
# INSERÇÃO
# ==========================================================

def inserir(
    nome: str
):

    return (
        supabase
        .table(TABELA)
        .insert(
            {
                "nome": nome
            }
        )
        .execute()
    )


# ==========================================================
# ATUALIZAÇÃO
# ==========================================================

def atualizar(
    servidor_id: int,
    nome: str,
    ativo: bool,
    ordem: int
):

    return (
        supabase
        .table(TABELA)
        .update(
            {
                "nome": nome,
                "ativo": ativo,
                "ordem": ordem
            }
        )
        .eq("id", servidor_id)
        .execute()
    )


# ==========================================================
# EXCLUSÃO
# ==========================================================

def excluir(
    servidor_id: int
):

    return (
        supabase
        .table(TABELA)
        .delete()
        .eq("id", servidor_id)
        .execute()
    )