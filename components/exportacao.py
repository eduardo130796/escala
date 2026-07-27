from io import BytesIO

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


class Exportacao:

    @staticmethod
    def gerar_excel(escolhas):
        """
        Gera um arquivo Excel em memória.

        Parâmetro:
            escolhas -> lista retornada pelo banco.

        Retorno:
            BytesIO
        """

        dados = []

        for escolha in escolhas:

            dados.append(
                {
                    "Servidor": escolha["servidores"]["nome"],
                    "Data": escolha["data"],
                    "Confirmado": (
                        "Sim"
                        if escolha["confirmado"]
                        else "Não"
                    )
                }
            )

        df = pd.DataFrame(dados)

        arquivo = BytesIO()

        with pd.ExcelWriter(
            arquivo,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                sheet_name="Escala",
                index=False
            )

        arquivo.seek(0)

        return arquivo
    
    @staticmethod
    def gerar_pdf(
        escolhas,
        mes,
        ano
    ):
        """
        Gera um PDF da escala.

        Retorno:
            BytesIO
        """

        arquivo = BytesIO()

        doc = SimpleDocTemplate(
            arquivo,
            pagesize=A4
        )

        estilos = getSampleStyleSheet()

        elementos = []

        elementos.append(
            Paragraph(
                "<b>ESCALA DE TRABALHO</b>",
                estilos["Title"]
            )
        )

        elementos.append(
            Paragraph(
                f"{mes:02d}/{ano}",
                estilos["Heading2"]
            )
        )

        elementos.append(
            Spacer(
                1,
                0.5 * cm
            )
        )

        tabela = [
            [
                "Servidor",
                "Data",
                "Confirmado"
            ]
        ]

        for escolha in escolhas:

            tabela.append(
                [
                    escolha["servidores"]["nome"],
                    escolha["data"],
                    "Sim"
                    if escolha["confirmado"]
                    else "Não"
                ]
            )

        tabela_pdf = Table(tabela)

        tabela_pdf.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.black,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER",
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        8,
                    ),
                ]
            )
        )

        elementos.append(
            tabela_pdf
        )

        doc.build(
            elementos
        )

        arquivo.seek(0)

        return arquivo