#!/usr/bin/env python3
"""Genera COLORES.pdf — referencia de colores del mockup."""

from typing import List, Optional, Tuple

from fpdf import FPDF
from fpdf.enums import XPos, YPos


def hex_to_rgb(value: str) -> Tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


class ColoresPDF(FPDF):
    MARGIN = 14
    USABLE_W = 210 - (MARGIN * 2)

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=16)
        self.set_margins(self.MARGIN, self.MARGIN, self.MARGIN)
        self.add_font("Body", "", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
        self.add_font("Body", "B", "/System/Library/Fonts/Supplemental/Arial Bold.ttf")
        self.set_font("Body", "", 9)

    def footer(self):
        self.set_y(-12)
        self.set_font("Body", "", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 6, f"Página {self.page_no()}", align="C")

    def section_title(self, title: str):
        self.ln(3)
        self.set_font("Body", "B", 12)
        self.set_text_color(15, 23, 42)
        self.multi_cell(0, 6, title)
        self.ln(1)

    def body_text(self, text: str):
        self.set_font("Body", "", 9)
        self.set_text_color(71, 85, 105)
        self.multi_cell(0, 4.8, text)
        self.ln(1.5)

    def draw_badge(self, x: float, y: float, label: str, bg: str, text: str, border: str, h: float = 6.5):
        tw = self.get_string_width(label) + 6
        tw = max(tw, 24)
        tr, tg, tb = hex_to_rgb(text)
        br, bg_c, bb = hex_to_rgb(border)
        fr, fg, fb = hex_to_rgb(bg)
        self.set_fill_color(fr, fg, fb)
        self.set_draw_color(br, bg_c, bb)
        self.set_line_width(0.25)
        self.rect(x, y, tw, h, style="DF")
        self.set_font("Body", "B", 8)
        self.set_text_color(tr, tg, tb)
        self.set_xy(x, y + 1.3)
        self.cell(tw, h - 2.6, label, align="C")

    def draw_progress_bar(self, x: float, y: float, w: float, fill: str, pct: float = 100):
        h = 4.5
        self.set_fill_color(226, 232, 240)
        self.set_draw_color(203, 213, 225)
        self.rect(x, y, w, h, style="DF")
        fr, fg, fb = hex_to_rgb(fill)
        self.set_fill_color(fr, fg, fb)
        fill_w = max(w * min(max(pct, 0), 100) / 100, 0.8 if pct > 0 else 0)
        if fill_w > 0:
            self.rect(x, y, fill_w, h, style="F")

    def table_header(self, headers: List[str], widths: List[float], aligns: Optional[List[str]] = None):
        if aligns is None:
            aligns = ["L"] * len(headers)
        self.set_font("Body", "B", 8.5)
        self.set_fill_color(226, 232, 240)
        self.set_text_color(30, 41, 59)
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.2)
        for i, (header, width) in enumerate(zip(headers, widths)):
            self.cell(width, 7, header, border=1, fill=True, align=aligns[i])
        self.ln()

    def status_table(self, rows: List[dict]):
        headers = ["Estatus", "Muestra", "Estilo PrimeNG", "Fondo", "Texto", "Borde", "Uso"]
        widths = [22, 28, 24, 18, 18, 18, self.USABLE_W - 128]
        aligns = ["L", "C", "C", "C", "C", "C", "L"]
        self.table_header(headers, widths, aligns)
        for row in rows:
            y0 = self.get_y()
            if y0 > 248:
                self.add_page()
                y0 = self.get_y()
            row_h = 11
            x0 = self.get_x()
            self.set_draw_color(203, 213, 225)
            self.rect(x0, y0, widths[0], row_h)
            self.set_xy(x0 + 1.5, y0 + 3.2)
            self.set_font("Body", "B", 8.5)
            self.set_text_color(30, 41, 59)
            self.cell(widths[0] - 3, 4, row["label"], align="L")
            badge_x = x0 + widths[0] + (widths[1] - 24) / 2
            self.draw_badge(badge_x, y0 + 2.2, row["label"], row["bg"], row["text"], row["border"])
            self.rect(x0 + widths[0], y0, widths[1], row_h)
            cells = [row["severity"], row["bg"], row["text"], row["border"], row["meaning"]]
            cell_widths = widths[2:]
            cell_aligns = aligns[2:]
            x = x0 + widths[0] + widths[1]
            self.set_font("Body", "", 8)
            self.set_text_color(51, 65, 85)
            for text, width, align in zip(cells, cell_widths, cell_aligns):
                self.rect(x, y0, width, row_h)
                self.set_xy(x, y0 + 3.5)
                self.cell(width, 4, text, align=align)
                x += width
            self.set_xy(x0, y0 + row_h)
        self.ln(2)

    def progress_table(self, rows: List[dict]):
        headers = ["Condición", "Muestra", "Estilo PrimeNG", "Color", "Uso"]
        widths = [32, 30, 24, 20, self.USABLE_W - 106]
        aligns = ["L", "C", "C", "C", "L"]
        self.table_header(headers, widths, aligns)
        for row in rows:
            y0 = self.get_y()
            if y0 > 252:
                self.add_page()
                y0 = self.get_y()
            row_h = 10
            x0 = self.get_x()
            self.set_draw_color(203, 213, 225)
            self.rect(x0, y0, widths[0], row_h)
            self.set_xy(x0 + 1.5, y0 + 3)
            self.set_font("Body", "", 8.5)
            self.set_text_color(51, 65, 85)
            self.cell(widths[0] - 3, 4, row["cond"], align="L")
            sample_x = x0 + widths[0]
            self.rect(sample_x, y0, widths[1], row_h)
            pct = row.get("pct", 55)
            bar_w = 22
            self.draw_progress_bar(sample_x + (widths[1] - bar_w) / 2, y0 + 2.8, bar_w, row["color"], pct)
            hex_x = sample_x + widths[1]
            self.rect(hex_x, y0, widths[2], row_h)
            self.set_xy(hex_x, y0 + 3)
            self.cell(widths[2], 4, row["severity"], align="C")
            color_x = hex_x + widths[2]
            self.rect(color_x, y0, widths[3], row_h)
            self.set_xy(color_x, y0 + 3)
            self.cell(widths[3], 4, row["color"], align="C")
            use_x = color_x + widths[3]
            self.rect(use_x, y0, widths[4], row_h)
            self.set_xy(use_x + 1.5, y0 + 3)
            self.multi_cell(widths[4] - 3, 4.2, row["use"])
            self.set_xy(x0, y0 + row_h)
        self.ln(2)


def build_pdf(output_path: str):
    pdf = ColoresPDF()
    pdf.add_page()

    pdf.set_font("Body", "B", 17)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "Códigos de color", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Body", "B", 13)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 7, "Reporte detallado de olas", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    pdf.body_text(
        "Referencia de colores del mockup reporte-detallado-olas.html. "
        "Tema PrimeNG Lara Light Blue. Los estatus usan Tag (severity); "
        "la barra de avance usa ProgressBar con severity secondary, danger o success."
    )

    pdf.section_title("1. Estatus de ola (HU.01)")
    pdf.body_text(
        "Columna Estatus de ola en el listado y badge en Información de la ola (HU.02). "
        "Componente PrimeNG: Tag (severity)."
    )
    pdf.status_table(
        [
            {
                "label": "En progreso",
                "severity": "warn",
                "bg": "#ffedd5",
                "text": "#c2410c",
                "border": "#fed7aa",
                "meaning": "Ola en progreso",
            },
            {
                "label": "Liberada",
                "severity": "success",
                "bg": "#dcfce7",
                "text": "#15803d",
                "border": "#bbf7d0",
                "meaning": "Ola liberada",
            },
            {
                "label": "Cancelada",
                "severity": "danger",
                "bg": "#fee2e2",
                "text": "#b91c1c",
                "border": "#fecaca",
                "meaning": "Ola cancelada",
            },
            {
                "label": "Pendiente",
                "severity": "secondary",
                "bg": "#f1f5f9",
                "text": "#64748b",
                "border": "#e2e8f0",
                "meaning": "Ola pendiente",
            },
        ]
    )

    pdf.section_title("2. Estatus de tarea (HU.02)")
    pdf.body_text("Columna Estatus en la tabla de tareas. Componente PrimeNG: Tag (severity).")
    pdf.status_table(
        [
            {
                "label": "Asignada",
                "severity": "info",
                "bg": "#dbeafe",
                "text": "#1d4ed8",
                "border": "#bfdbfe",
                "meaning": "Asignada a usuario",
            },
            {
                "label": "Cancelada",
                "severity": "danger",
                "bg": "#fee2e2",
                "text": "#b91c1c",
                "border": "#fecaca",
                "meaning": "Tarea cancelada",
            },
            {
                "label": "Disponible",
                "severity": "secondary",
                "bg": "#f1f5f9",
                "text": "#64748b",
                "border": "#e2e8f0",
                "meaning": "Disponible para asignación",
            },
            {
                "label": "En progreso",
                "severity": "warn",
                "bg": "#ffedd5",
                "text": "#c2410c",
                "border": "#fed7aa",
                "meaning": "Tarea en ejecución",
            },
            {
                "label": "Realizado",
                "severity": "success",
                "bg": "#dcfce7",
                "text": "#15803d",
                "border": "#bbf7d0",
                "meaning": "Tarea finalizada",
            },
        ]
    )

    pdf.section_title("3. Barra de porcentaje surtido vs. planeado")
    pdf.body_text(
        "Listado HU.01 y panel de progreso HU.02. Fórmula: (surtida ÷ planeada) × 100. "
        "Formato: NN.NN%. Componente PrimeNG: ProgressBar con severity según avance. "
        "Fondo de pista: #d1d5db (--p-progressbar-background)."
    )
    pdf.progress_table(
        [
            {
                "cond": "Porcentaje ≤ 0",
                "severity": "secondary",
                "color": "#64748b",
                "pct": 0,
                "use": "Sin avance",
            },
            {
                "cond": "0 < % < 50",
                "severity": "danger",
                "color": "#ef4444",
                "pct": 25,
                "use": "Avance bajo",
            },
            {
                "cond": "Porcentaje ≥ 50",
                "severity": "success",
                "color": "#22c55e",
                "pct": 75,
                "use": "Avance aceptable / alto",
            },
        ]
    )

    pdf.body_text(
        "Ejemplos mock: 677440 → 10.02% danger (#ef4444); "
        "677441 → 0.00% secondary (#64748b); "
        "677443 → 100.00% success (#22c55e)."
    )

    pdf.output(output_path)


if __name__ == "__main__":
    build_pdf("COLORES.pdf")
    print("Generado: COLORES.pdf")
