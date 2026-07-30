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
import calendar
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import (
    black,
    lightgrey,
    darkgreen,
    darkblue,
    orange
)

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

        import calendar
        from collections import defaultdict
        from datetime import datetime

        from reportlab.lib.colors import (
            Color,
            white,
            black
        )

        from reportlab.lib.pagesizes import (
            A4,
            landscape
        )

        from reportlab.pdfbase.pdfmetrics import stringWidth

        from reportlab.pdfgen import canvas

        arquivo = BytesIO()

        pdf = canvas.Canvas(
            arquivo,
            pagesize=landscape(A4)
        )

        largura, altura = landscape(A4)

        pdf.setTitle("Escala")

        # =====================================================
        # CORES
        # =====================================================

        VERDE = Color(
            0.84,
            0.95,
            0.86
        )

        VERDE_BORDA = Color(
            0.16,
            0.63,
            0.29
        )

        LARANJA = Color(
            1.00,
            0.91,
            0.78
        )

        LARANJA_BORDA = Color(
            0.94,
            0.42,
            0.00
        )

        CINZA = Color(
            0.96,
            0.96,
            0.96
        )

        CINZA_HEADER = Color(
            0.88,
            0.88,
            0.88
        )

        BORDA = Color(
            0.80,
            0.80,
            0.80
        )

        # =====================================================
        # AGRUPA ESCOLHAS
        # =====================================================

        agenda = defaultdict(list)

        for escolha in escolhas:

            dia = int(
                escolha["data"][-2:]
            )

            agenda[dia].append(
                {
                    "nome": escolha["servidores"]["nome"],
                    "confirmado": escolha["confirmado"]
                }
            )

        # =====================================================
        # CABEÇALHO
        # =====================================================

        meses = [
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
            "Dezembro"
        ]

        pdf.setFont(
            "Helvetica-Bold",
            24
        )

        pdf.drawCentredString(
            largura / 2,
            altura - 35,
            "ESCALA DE SERVIÇO"
        )

        pdf.setFont(
            "Helvetica",
            14
        )

        pdf.drawCentredString(
            largura / 2,
            altura - 55,
            f"Competência: {meses[mes]}/{ano}"
        )

        # =====================================================
        # TAMANHOS
        # =====================================================

        margem = 20

        topo = altura - 85

        rodape = 30

        largura_util = largura - margem * 2

        calendario = calendar.Calendar(
            firstweekday=0
        )

        semanas = calendario.monthdayscalendar(
            ano,
            mes
        )

        qtd_semanas = len(
            semanas
        )

        largura_coluna = largura_util / 7

        altura_header = 24

        altura_util = (
            topo
            - rodape
        )

        altura_linha = (
            altura_util
            - altura_header
        ) / qtd_semanas

        # =====================================================
        # DIAS DA SEMANA
        # =====================================================

        dias = [
            "SEG",
            "TER",
            "QUA",
            "QUI",
            "SEX",
            "SÁB",
            "DOM"
        ]

        y = topo

        pdf.setFont(
            "Helvetica-Bold",
            10
        )

        for coluna, dia in enumerate(dias):

            x = margem + (
                coluna
                * largura_coluna
            )

            pdf.setFillColor(
                CINZA_HEADER
            )

            pdf.setStrokeColor(
                BORDA
            )

            pdf.roundRect(
                x,
                y,
                largura_coluna,
                altura_header,
                4,
                fill=1
            )

            pdf.setFillColor(
                black
            )

            pdf.drawCentredString(
                x + largura_coluna / 2,
                y + 7,
                dia
            )

        # =====================================================
        # PREPARA DESENHO DAS SEMANAS
        # =====================================================

        y -= altura_linha

        pdf.setStrokeColor(
            BORDA
        )

        pdf.setLineWidth(
            0.5
        )

        # -----------------------------------------------------
        # DAQUI CONTINUA NA PARTE 2
        # -----------------------------------------------------
            # =====================================================
        # DESENHA AS SEMANAS
        # =====================================================

        for semana in semanas:

            for coluna, dia in enumerate(semana):

                x = margem + coluna * largura_coluna

                # Fundo da célula

                if coluna >= 5:
                    pdf.setFillColor(CINZA)
                else:
                    pdf.setFillColor(white)

                pdf.roundRect(
                    x,
                    y,
                    largura_coluna,
                    altura_linha,
                    4,
                    fill=1,
                    stroke=1
                )

                if dia == 0:
                    continue

                # ------------------------------------------
                # Número do dia
                # ------------------------------------------

                tamanho_box = 18

                pdf.setFillColor(CINZA_HEADER)

                pdf.roundRect(
                    x + largura_coluna - tamanho_box - 5,
                    y + altura_linha - tamanho_box - 5,
                    tamanho_box,
                    tamanho_box,
                    3,
                    fill=1,
                    stroke=0
                )

                pdf.setFillColor(black)

                pdf.setFont(
                    "Helvetica-Bold",
                    9
                )

                pdf.drawCentredString(
                    x + largura_coluna - tamanho_box / 2 - 5,
                    y + altura_linha - 17,
                    str(dia)
                )

                # ------------------------------------------
                # Área dos servidores
                # ------------------------------------------

               
                
                registros = agenda.get(dia, [])

                qtd = len(registros)
                
                if qtd <= 2:
                    fonte = 7
                elif qtd <= 4:
                    fonte = 6
                elif qtd <= 6:
                    fonte = 5.5
                else:
                    fonte = 5
                
                yy = y + altura_linha - 28
                
                limite = y + 5
                
                exibidos = 0

                for registro in registros:

                   if yy - fonte < limite:
                       break

                    nome = registro["nome"]

                    confirmado = registro["confirmado"]

                    # ------------------------------
                    # Quebra automática
                    # ------------------------------

                    largura_texto = largura_coluna - 16

                    pdf.setFillColor(black)

                    if confirmado:
                        marcador = "✓"
                    else:
                        marcador = "○"
                    
                    pdf.setFont("Helvetica", fonte)
                    
                    pdf.drawString(
                        x + 6,
                        yy - fonte,
                        f"{marcador} {texto}"
                    )

                    yy -= fonte + 2

                    exibidos += 1

                # ------------------------------------------
                # Há mais registros?
                # ------------------------------------------

                restantes = (
                    len(registros)
                    - exibidos
                )

                if restantes > 0:

                    pdf.setFillColor(
                        black
                    )

                    pdf.setFont(
                        "Helvetica-Oblique",
                        7
                    )

                    pdf.drawString(
                        x + 8,
                        yy - 8,
                        f"(+{restantes})"
                    )

            y -= altura_linha

        # =====================================================
        # CONTINUA NA PARTE 3
        # =====================================================
            # =====================================================
        # LEGENDA
        # =====================================================

        legenda_y = 18

        # Confirmado

        pdf.setFillColor(VERDE)
        pdf.setStrokeColor(VERDE_BORDA)

        pdf.roundRect(
            margem,
            legenda_y,
            18,
            10,
            2,
            fill=1,
            stroke=1
        )

        pdf.setFillColor(black)

        pdf.setFont(
            "Helvetica",
            9
        )

        pdf.drawString(
            margem + 25,
            legenda_y + 2,
            "Confirmado"
        )

        # Não confirmado

        x_legenda = margem + 120

        pdf.setFillColor(LARANJA)
        pdf.setStrokeColor(LARANJA_BORDA)

        pdf.roundRect(
            x_legenda,
            legenda_y,
            18,
            10,
            2,
            fill=1,
            stroke=1
        )

        pdf.setFillColor(black)

        pdf.drawString(
            x_legenda + 25,
            legenda_y + 2,
            "Não confirmado"
        )

        # =====================================================
        # DATA DE EMISSÃO
        # =====================================================

        pdf.setFont(
            "Helvetica",
            8
        )

        pdf.drawRightString(
            largura - margem,
            legenda_y + 2,
            "Emitido em "
            + datetime.now().strftime(
                "%d/%m/%Y às %H:%M"
            )
        )

        # =====================================================
        # MOLDURA DA PÁGINA
        # =====================================================

        pdf.setStrokeColor(BORDA)

        pdf.roundRect(
            10,
            10,
            largura - 20,
            altura - 20,
            6,
            fill=0,
            stroke=1
        )

        # =====================================================
        # FINALIZA
        # =====================================================

        pdf.save()

        arquivo.seek(0)

        return arquivo
