from components.calendario import Calendario
from database import (
    configuracoes,
    escalas,
    servidores
)


class AdminService:

    def __init__(self):
        self._config = None

    # ==========================================================
    # CONFIGURAÇÃO
    # ==========================================================

    @property
    def config(self):

        if self._config is None:
            self._config = configuracoes.obter().data

        return self._config

    def atualizar_config(self):
        self._config = configuracoes.obter().data
        return self._config

    def existem_escolhas(self) -> bool:
        return escalas.quantidade() > 0

    def salvar_configuracao(
        self,
        mes: int,
        ano: int,
        max_dias: int
    ):

        if self.existem_escolhas():
            raise ValueError(
                "Não é possível alterar o período porque já existem escolhas cadastradas."
            )

        configuracoes.atualizar(
            mes=mes,
            ano=ano,
            max_dias_por_servidor=max_dias,
            bloqueado=self.config["bloqueado"]
        )

        self.atualizar_config()

    def alterar_status_edicao(
        self,
        permitir: bool
    ):

        cfg = self.config

        configuracoes.atualizar(
            mes=cfg["mes"],
            ano=cfg["ano"],
            max_dias_por_servidor=cfg["max_dias_por_servidor"],
            bloqueado=not permitir
        )

        self.atualizar_config()

    # ==========================================================
    # CALENDÁRIO
    # ==========================================================

    def eventos_calendario(self):

        eventos = (
            escalas
            .listar_eventos()
            .data
            or []
        )

        return Calendario.montar_eventos(eventos)

    # ==========================================================
    # SERVIDORES
    # ==========================================================

    def listar_servidores(self):

        return (
            servidores
            .listar()
            .data
            or []
        )

    # ==========================================================
    # RESUMO
    # ==========================================================

    def listar_resumo(self):

        servidores_lista = self.listar_servidores()

        escolhas = self.listar_escolhas()

        resumo = {}

        for escolha in escolhas:

            servidor = escolha["servidor_id"]

            if servidor not in resumo:

                resumo[servidor] = {
                    "dias": 0,
                    "confirmado": True
                }

            resumo[servidor]["dias"] += 1

            resumo[servidor]["confirmado"] &= escolha["confirmado"]

        resultado = []

        for servidor in servidores_lista:

            dados = resumo.get(
                servidor["id"],
                {
                    "dias": 0,
                    "confirmado": False
                }
            )

            resultado.append(
                {
                    "id": servidor["id"],
                    "nome": servidor["nome"],
                    "dias": dados["dias"],
                    "confirmado": (
                        dados["dias"] > 0
                        and dados["confirmado"]
                    )
                }
            )

        return resultado

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def escolhas_por_data(
        self,
        data
    ):

        return (
            escalas
            .listar_por_data(data)
            .data
            or []
        )

    def listar_escolhas(self):

        return (
            escalas
            .listar()
            .data
            or []
        )

    # ==========================================================
    # EXCLUSÕES
    # ==========================================================

    def excluir_escolhas_servidor(
        self,
        servidor_id: int
    ):

        return escalas.excluir_por_servidor(
            servidor_id
        )

    def limpar_escala(self):

        return escalas.excluir_todas()