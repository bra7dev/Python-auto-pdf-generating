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


output = PdfWriter()
## first 117 page (order and preface)
# for i in range(117): 
existing_pdf = PdfReader(open("doc/Traffic.pdf", "rb"))
existing_pdf.add_page(existing_pdf.pages[3])

output_stream = open("Order.pdf", "wb")
existing_pdf.write(output_stream)
output_stream.close()
