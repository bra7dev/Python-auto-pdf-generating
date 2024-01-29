from PyPDF2 import PdfReader
import os
import openai
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader
import io
import json
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import barcode
from barcode.writer import ImageWriter
from PIL import Image
from reportlab.lib.colors import white, black, lightslategray
import array
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('ProximaNova', 'doc/FontsFree-Net-proxima_nova_reg-webfont.ttf'))
load_dotenv()
page = ""
first_dna_pst = 0
dna_pst = 0
dy = [
    
    715,
    700,
    685,
    670,
    655,
    640,
    625,
    610,
    595,
    580,
    565,
    550,
    535,
    520,
    505,
    490,
    475,
    460,
    445,
    430,
    415,
    400,
    385,
    370,
    355,
    340,
    325,
    310,
    295,
    280,
    265,
    250,
    235,
    220,
    205,
    190,
    175,
    160,
    145,
    130,
    115,
    100, 
    85,
    70,
    55,
    40,
    25
]
# This function is reading PDF from the start page to final page
# given as input (if less pages exist, then it reads till this last page)
def get_pdf_text(document_path, start_page=1, final_page=999):
    page = ""
    reader = PdfReader(document_path)
    number_of_pages = len(reader.pages)

    for page_num in range(start_page - 1, min(number_of_pages, final_page)):
        page += reader.pages[page_num].extract_text()
    return page


openai.api_key = os.getenv('OPENAI_API_KEY')
def gpt_req_res(doc_text,
                prompt='answer like an experienced consultant: ',
                model='text-davinci-003',
                max_tokens=1200,
                temperature=0.8):
    AI_prompt = f"""
    I have this difficult text content that is difficult to understand.
    {doc_text}
    {prompt}
    """

    
    # https://platform.openai.com/docs/api-reference/completions/create
    response = openai.Completion.create(
        model=model,
        prompt=AI_prompt,
        temperature=temperature,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text

## PDF generation functions ##
def text_center_draw(canvas, x, y, text, font, size, dy=0):
    width = canvas.stringWidth(text=str(text), fontName="ProximaNova", fontSize=size)
    canvas.setFont("ProximaNova", size)
    canvas.drawString(x-(width/2), y, str(text))

def text_staticPnt_draw(canvas, x, y, text, font, size):
    canvas.setFont("ProximaNova", size)
    canvas.drawString(x, y, str(text))

def text_dynamic_draw(canvas, x, y, text, font, size, max_cnt):
    global dna_pst, first_dna_pst
    width = canvas.stringWidth(text=str(text), fontName="ProximaNova", fontSize=size)
    canvas.setFont("ProximaNova", size)
    text_list = text.split(" ")
    reText = ""
    ddy = 0
    for i in range(len(text_list)):
        reText += " " + str(text_list[i])
        width = canvas.stringWidth(text=str(reText), fontName="ProximaNova", fontSize=size)
        if width > 400:
            canvas.drawString(x, dy[ddy], str(reText))
            ddy += 1
            reText = ""
            width = 0
        elif i == len(text_list)-1:
            canvas.drawString(x, dy[ddy], str(reText))

def generate_new_pdf_withGPT(pageNum):
    doc_path_name = 'Traffic.pdf'
    doc_text = get_pdf_text(doc_path_name, pageNum, pageNum)
    print(doc_text)
    prompt = 'rewrite as more detail as possible about this text content in more detail based on this original content to understand well with easy language.'
    reply = gpt_req_res(doc_text, prompt)

    print("Reploy:", reply)

    c = canvas.Canvas("output.pdf")
    width, height = 600, 800  # Specify the dimensions of the PDF page




    text_center_draw(c, 300, 750, str("FOOT NOTE"),"ProximaNova", 16)
    text_dynamic_draw(c, 80, 640, str(reply), "ProximaNova", 12, 14)

    # Save the PDF
    c.save()


output = PdfWriter()

## first 117 page (order and preface)
# for i in range(117): 
#     existing_pdf = PdfReader(open("doc/Traffic.pdf", "rb"))
#     output.add_page(existing_pdf.pages[i])
# existing_pdf = PdfReader(open("Order117.pdf", "rb"))
# output.add_page(existing_pdf)
# 1090
original_pdf = PdfReader(open("Traffic.pdf", "rb"))
for i in range(117, 123, 1):
    generate_new_pdf_withGPT(i)
    new_pdf = PdfReader(open("output.pdf", "rb"))
    output.add_page(new_pdf.pages[0])
    output.add_page(original_pdf.pages[i+1])

output_stream = open("result.pdf", "wb")
output.write(output_stream)
output_stream.close()
## first 117 page (order and preface)
print("PDF generated successfully.")