from datetime import date

from components.calendario import Calendario
from database import (
    configuracoes,
    escalas,
    servidores
)


class EscalaService:

    # =====================================================
    # CONFIGURAÇÃO
    # =====================================================

    def __init__(self):
        self._config = None

    @property
    def config(self):

        if self._config is None:
            self._config = configuracoes.obter().data

        return self._config
    @property
    def bloqueado(self):
        return self.config["bloqueado"]

    # =====================================================
    # SERVIDORES
    # =====================================================

    def listar_servidores(self):
        return servidores.listar().data or []

    # =====================================================
    # ESCOLHAS
    # =====================================================

    def obter_escolhas(
        self,
        servidor_id: int
    ):
        return (
            escalas
            .listar_por_servidor(servidor_id)
            .data
            or []
        )

    # =====================================================
    # VALIDAÇÕES
    # =====================================================

    def validar_data(
        self,
        data: date
    ):

        cfg = self.config

        if data.year != cfg["ano"]:
            raise ValueError(
                "Ano inválido."
            )

        if data.month != cfg["mes"]:
            raise ValueError(
                "Data fora do período."
            )

        if data.weekday() >= 5:
            raise ValueError(
                "Somente dias úteis."
            )

    def validar_escolha(
        self,
        servidor_id: int,
        data: date
    ):

        if self.bloqueado:

            raise ValueError(
                "A escala está bloqueada."
            )

        self.validar_data(data)

        escolhas = self.obter_escolhas(
            servidor_id
        )

        datas = {
            escolha["data"][:10]
            for escolha in escolhas
        }

        if data.isoformat() in datas:

            raise ValueError(
                "Dia já escolhido."
            )


    # =====================================================
    # AÇÕES
    # =====================================================

    def escolher_dia(
        self,
        servidor_id: int,
        data: date
    ):

        self.validar_escolha(
            servidor_id,
            data
        )

        return escalas.inserir(
            servidor_id,
            data
        )

    def remover_dia(
        self,
        servidor_id: int,
        data: date
    ):

        if self.bloqueado:

            raise ValueError(
                "A escala está bloqueada."
            )

        return escalas.excluir_por_data(
            servidor_id,
            data
        )

    def confirmar(
        self,
        servidor_id: int
    ):

        escolhas = self.obter_escolhas(
            servidor_id
        )

        if len(escolhas) < 2:

            raise ValueError(
                "Selecione pelo menos 2 dias antes de confirmar."
            )

        for escolha in escolhas:

            if not escolha["confirmado"]:

                escalas.confirmar(
                    escolha["id"]
                )

    # =====================================================
    # CALENDÁRIO
    # =====================================================

    def eventos_calendario(
        self,
        servidor_id=None
    ):

        eventos = (
            escalas
            .listar_eventos()
            .data
            or []
        )

        return Calendario.montar_eventos(
            eventos,
            servidor_id
        )