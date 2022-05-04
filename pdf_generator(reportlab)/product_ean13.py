# base
from reportlab.lib.pagesizes import A10, A4  # A4,
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget
from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas

# size
from reportlab.lib.units import inch

# ru lang
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# json
import os
import json



"""
Adjust pagesize, number of labels, barcode size and
positions of barcode and description to your needs.
"""

# ------------------------------------ config -----------------------------------------

pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))

PAGE_SIZE = (2.9 * inch, 2 * inch)  # configurate pdf page size here( A4,A10, etc, or custom(example: 2.5*ich,2*ich)
# PAGE_SIZE = A4
NUM_LABELS_X = 1 # for A4 max ==3 # cards per line
NUM_LABELS_Y = 1 # for A4 max ==4 # line per page
# PRODUCT_ON_PAGE = NUM_LABELS_X*NUM_LABELS_Y
BAR_WIDTH = 1.5
BAR_HEIGHT = 51.0
TEXT_Y = 80
BARCODE_Y = 17

MAX_LINE_LEN = 40 # symbols count
MAX_NAME_LINES = 2 # example text == [line1,line2,line3] MAX_NAME_LINES==2 => text be line1+line2+'...'
TEXT_CONFIG = {"MARGIN_TEXT": 12, "TEXT_SIZE": 10}
LONG_TEXT_CONFIG = {"MARGIN_TEXT": 10, "TEXT_SIZE": 8} # if some text so long, we use this config

LABEL_WIDTH = PAGE_SIZE[0] / NUM_LABELS_X
LABEL_HEIGHT = PAGE_SIZE[1] / NUM_LABELS_Y
SHEET_TOP = PAGE_SIZE[1]

# -----------------------------------------------------------------------------


def generate_text_lines(text_list: list, max_line_len: int) -> list[str, ...]:
    lines = []
    line = ''
    for word in text_list:
        if len(line) + len(word) < max_line_len:
            line += word + ' '
        else:
            lines.append(line + '  ')
            line = word + ' '
    lines.append(line+'  ')
    if len(lines) > MAX_NAME_LINES:
        lines = lines[:MAX_NAME_LINES]
        last_line = lines[len(lines)-1]
        lines[len(lines)-1] = last_line[:len(last_line)-3] + '...' # remove '   ' and add '...'
    return lines


def length_handler(text: str) -> list[str, ...]:
    max_line_len = MAX_LINE_LEN
    if len(text) > max_line_len:
        text_list = text.split(' ')
        text_lines = generate_text_lines(text_list=text_list, max_line_len=max_line_len)
        return text_lines
    return [text]


def description_handler(description: list[str, ...], label_drawing):
    default_lines = 3
    if len(description) > default_lines:
        text_margin, font_size = LONG_TEXT_CONFIG['MARGIN_TEXT'], LONG_TEXT_CONFIG['TEXT_SIZE']
    else:
        text_margin, font_size = TEXT_CONFIG['MARGIN_TEXT'], TEXT_CONFIG['TEXT_SIZE']

    text_y = TEXT_Y + (len(description)-1) * text_margin
    for d in description:
        text = String(0, text_y, d, fontName="FreeSans",
                      fontSize=font_size, textAnchor="middle")
        text.x = LABEL_WIDTH / 2  # center text (anchor is in the middle)
        label_drawing.add(text)
        text_y -= text_margin


def label(card_context: dict[str, str]) -> Drawing:
    """
    Generate a drawing with EAN-13 barcode and descriptive text.
    """
    text_lines = length_handler(card_context['product_name'])
    description: list[str, ...] = [line for line in text_lines] + [
        f"Article:{card_context['article']}"] + [f"Color:{card_context['color']}"]

    ean13 = card_context['ean13']

    barcode = Ean13BarcodeWidget(ean13)
    barcode.barWidth = BAR_WIDTH
    barcode.barHeight = BAR_HEIGHT
    x0, y0, bw, bh = barcode.getBounds()
    barcode.x = (LABEL_WIDTH - bw) / 2  # center barcode
    barcode.y = BARCODE_Y  # spacing from label bottom (pt)

    label_drawing = Drawing(LABEL_WIDTH, LABEL_HEIGHT)
    description_handler(description, label_drawing)
    label_drawing.add(barcode)

    return label_drawing


def fill_sheet(canvas: Canvas, label_drawing: Drawing):
    """
    Simply fill the given ReportLab canvas with label drawings.
    :param canvas: The ReportLab canvas
    :type canvas: Canvas
    :param label_drawing: Contains Drawing of configured size
    :type label_drawing: Drawing
    """
    for u in range(0, NUM_LABELS_Y):
        for i in range(0, NUM_LABELS_X):
            x = i * LABEL_WIDTH
            y = SHEET_TOP - LABEL_HEIGHT - u * LABEL_HEIGHT
            renderPDF.draw(label_drawing, canvas, x, y)



def json_test(canvas: Canvas) -> Canvas:
    pwd = os.path.dirname(__file__)
    products_json = open(pwd+'/products.json', mode='r', encoding='utf-8')
    products_array = json.load(products_json)
    products_json.close()
    for p in products_array:
        card_context = {'product_name': f"{p['title']} {p['description']}", 'article': p['article'],
                        'color': p['color'], 'ean13': p['ean13']}
        sticker = label(card_context)
        fill_sheet(canvas, sticker)
        canvas.showPage()
    return canvas


if __name__ == '__main__':
    text = "Abstract citrus fruits bouquet on blue background Abstract citrus fruits bouquet on blue background Abstract citrus fruits bouquet on blue background1"
    canvas = Canvas("product_ean13.pdf", pagesize=PAGE_SIZE)
    card_context = {'product_name': text, 'article': 'w990342',
                    'color': 'black', 'ean13': '123456789101'}
    sticker = label(card_context)
    # fill_sheet(canvas, sticker)
    canvas = json_test(canvas)
    canvas.save()
