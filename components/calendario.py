from datetime import datetime

from streamlit_calendar import calendar


class Calendario:
    """
    Componente responsável por exibir o calendário.

    Não contém regras de negócio.
    Apenas renderiza eventos e devolve a interação do usuário.
    """

    def __init__(
        self,
        mes: int,
        ano: int,
        altura: int = 700
    ):

        self.mes = mes
        self.ano = ano
        self.altura = altura

    def _options(
        self,
        disabled: bool
    ):

        data_inicial = datetime(
            self.ano,
            self.mes,
            1
        ).strftime("%Y-%m-%d")

        return {

            "locale": "pt-br",

            "initialView": "dayGridMonth",

            "initialDate": data_inicial,

            "editable": False,

            "selectable": not disabled,

            "selectMirror": False,

            "dayMaxEvents": True,

            "weekends": True,

            "navLinks": False,

            "fixedWeekCount": False,

            "showNonCurrentDates": False,

            "height": self.altura,

            "headerToolbar": {

                "left": "",

                "center": "title",

                "right": ""

            }
        }

    def render(
        self,
        eventos: list,
        disabled: bool = False
    ):

        estado = calendar(

            events=eventos,

            options=self._options(disabled),

            custom_css="""
                .fc-toolbar-title{
                    font-size:24px;
                    font-weight:700;
                }

                .fc-daygrid-day-number{
                    font-weight:bold;
                }

                .fc-event{
                    border-radius:6px;
                    border:none;
                    padding:2px;
                    font-size:12px;
                }

                .fc-day-today{
                    background:#fff8dc !important;
                }
            """,

            key="calendario"

        )

        if disabled:
            return None

        return self._processar_evento(estado)

    @staticmethod
    def _processar_evento(estado):

        if not estado:
            return None

        if estado.get("dateClick"):

            return {
                "tipo": "date",
                "data": estado["dateClick"]["date"][:10]
            }

        if estado.get("eventClick"):

            evento = estado["eventClick"]["event"]

            return {
                "tipo": "event",
                "id": evento.get("id"),
                "data": evento.get("start")[:10],
                "titulo": evento.get("title")
            }

        return None

    @staticmethod
    def criar_evento(
        id_evento,
        titulo,
        data,
        confirmado=False,
        usuario=False
    ):

        if usuario:
            cor = "#2E7D32"
        elif confirmado:
            cor = "#1565C0"
        else:
            cor = "#EF6C00"

        return {

            "id": str(id_evento),

            "title": titulo,

            "start": str(data),

            "allDay": True,

            "color": cor

        }

    @classmethod
    def montar_eventos(
        cls,
        escolhas,
        servidor_id=None
    ):

        eventos = []

        for escolha in escolhas:

            eventos.append(

                cls.criar_evento(

                    id_evento=escolha["id"],

                    titulo=escolha["servidores"]["nome"],

                    data=escolha["data"],

                    confirmado=escolha["confirmado"],

                    usuario=(
                        servidor_id is not None
                        and escolha["servidor_id"] == servidor_id
                    )

                )

            )

        return eventos