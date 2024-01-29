import io
import json
import math
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
#### import Font ####
pdfmetrics.registerFont(TTFont('ProximaNova', 'doc/FontsFree-Net-proxima_nova_reg-webfont.ttf'))

class MedicalPDFGenerator:
    def __init__(self, data_path, destination):
        #### Font settings ####
        self.font = "ProximaNova"
        self.sec_fts = 13
        self.col_fts = 12
        self.des_fts = 9

        #### Prevent over of text line ####
        self.client_page_des_split = 22
        self.result_page_des_split = 11

        #### import and output file Path ####
        self.data_path = data_path
        self.output_pdf_path = destination

        #### Page count for generating ####
        self.page_cnt = 2
        
        #### Dynamic text line position to draw #### 
        self.first_dna_pst = 0
        self.second_dna_pst = 0

        # static position on first page
        self.draw_page =     {
            ## static position on first page
            "page_one": [
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
                    25,
            ],
            "demographics": {
                "patient_name": {
                    "x1": 42,
                    "y1": 695,
                    "x2": 120,
                    "y2": 695
                },
                "dob": {
                    "x1": 42,
                    "y1": 680,
                    "x2": 72,
                    "y2": 680
                },
                "age": {
                    "x1": 42,
                    "y1": 665,
                    "x2": 72,
                    "y2": 665
                },
                "weight": {
                    "x1": 42,
                    "y1": 650,
                    "x2": 85,
                    "y2": 650
                },
                "height": {
                    "x1": 545,
                    "y1": 695,
                    "x2": 490,
                    "y2": 695
                },
                "gender": {
                    "x1": 545,
                    "y1": 680,
                    "x2": 510,
                    "y2": 680
                },
            },
            "incident_dict": {
                "date": {
                    "x1": 72,
                    "y1": 590,
                    "x2": 72,
                    "y2": 575
                },
                "incident": {
                    "x1": 30,
                    "y1": 550,
                    "x2": 310,
                    "y2": 535
                },
                "reference_incident": {
                    "x1": 300,
                    "y1": 590,
                    "x2": 300,
                    "y2": 575
                },
                "temp_date": {
                    "x1": 502,
                    "y1": 590,
                    "x2": 502,
                    "y2": 575
                }
            },
            "medical_conditions": {
                "date": {
                    "x1": 72,
                    "x2": 72,
                },
                "incident": {
                    "x1": 60,
                    "x2": 66,
                },
                "reference_incident": {
                    "x1": 300,
                    "x2": 300,
                },
                "temp_date": {
                    "x1": 502,
                    "x2": 502,
                },
                "rows": [
                    480,
                    465,
                    450,
                    435,
                    400,
                    385,
                    370,
                    355,
                    340,
                    315,
                    300,
                    285,
                    270,
                    245,
                    230,
                    215,
                    200,
                    175,
                    160
                ]
            },
            "executive_summary": {
                "x1": 30,
                "y1": 150
            },
            "parametrized_summary": {
                "x1": 30,
                "y1": 150
            },

            ## Next page position ##
            "results": {
                "date": {
                    "x1": 35,
                    "y1": 680,
                },
                "center": {
                    "x1": 130,
                    "y1": 680,
                },
                
                "summary": {
                    "x1": 255,
                    "y1": 680,
                },
                
                "rows": [
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
                    25,
                ]       
            }
        }
        self.page_one = ["demographics", "incident_dict", "medical_conditions", "executive_summary", "parametrized_summary"]
        self.packet = io.BytesIO()
        self.pdf_canvas = canvas.Canvas(self.packet, pagesize=letter)
        self.pdf_canvas.setFont("ProximaNova", 8)

    ## Drawing title on center position.
    def text_center_draw(self, canvas, x, y, text, font, size, dy=0):
        width = canvas.stringWidth(text=str(text), fontName="ProximaNova", fontSize=size)
        canvas.setFont("ProximaNova", size)
        canvas.drawString(x-(width/2), y, str(text))
    
    ## Drawing title on static position.
    def text_staticPnt_draw(self, canvas, x, y, text, font, size):
        canvas.setFont("ProximaNova", size)
        canvas.drawString(x, y, str(text))

    ## Drawing description(long) without overflow. 
    def text_dynamic_draw(self, canvas, x, y, text, font, size, max_cnt):
        global dna_pst, page_cnt, first_dna_pst
        width = canvas.stringWidth(text=str(text), fontName="ProximaNova", fontSize=size)
        canvas.setFont("ProximaNova", size)
        text_list = text.split(" ")
        
        if max_cnt > 20:
            line_cnt = math.ceil(len(text_list)/max_cnt)
            for i in range(line_cnt): 
                reText = ""
                if 0<=i<line_cnt-1:
                    boundry = i*max_cnt+max_cnt
                else:
                    boundry = len(text_list)
                for k in range(i*max_cnt, boundry):
                    reText += " " + str(text_list[k])
                    
                if i == 0:
                    self.first_dna_pst += 2
                y = self.draw_page["page_one"][i+self.first_dna_pst]
                canvas.setFont("ProximaNova", size)
                canvas.drawString(x, y, str(reText)) 
            
            self.first_dna_pst = self.first_dna_pst + line_cnt + 1
        elif max_cnt < 20:
            if 10 > len(text_list) > 0:
                y = self.draw_page["results"]["rows"][self.second_dna_pst]
                center1 = " ".join(str(element) for element in text_list[:4])
                canvas.drawString(x, y, str(center1))
                center2 = " ".join(str(element) for element in text_list[4:])
                canvas.drawString(x, y-15, str(center2))

            else:
                line_cnt = math.ceil(len(text_list)/max_cnt)
                #short content line
                if line_cnt == 1:
                    pass
                #long content line
                else:
                    for i in range(line_cnt): 
                        reText = ""
                        if 0<=i<line_cnt-1:
                            boundry = i*max_cnt+max_cnt
                        else:
                            boundry = len(text_list)
                        for k in range(i*max_cnt, boundry):
                            reText += " " + str(text_list[k])
            
                        if i + self.second_dna_pst > 40:
                            self.second_dna_pst = 0 - i
                            self.page_cnt += 1
                            self.page_number(canvas, 10, self.page_cnt-1)
                            canvas.showPage() 
                        y = self.draw_page["results"]["rows"][i+self.second_dna_pst]
                        canvas.setFont("ProximaNova", size)
                        canvas.drawString(x, y, str(reText)) 
                    self.page_number(canvas, 10, self.page_cnt)
                    self.second_dna_pst = self.second_dna_pst + line_cnt + 1
                    self.draw_bottom_line(canvas, y-10)

    ## Drawing bottom line.
    def draw_bottom_line(self, pdf_canvas, y):
        pdf_canvas.line(32, y, 570, y)

    ## Page number to display.
    def page_number(self, pdf_canvas, size, number):
        pdf_canvas.setFont("ProximaNova", size)
        pdf_canvas.drawString(300, 30, str(number))   

    ## loading json data to use. 
    def loading_json_data(self):
        with open(self.data_path) as file:
            data = json.load(file)

        json_data = json.dumps(data)
        data = json.loads(json_data)
        return data

    ## generating the PDF after drawing
    def generate_pdf(self):
        self.pdf_canvas.save()
        self.packet.seek(0)
        canvas_page_pdf = PdfReader(self.packet)
        output = PdfWriter()
        for i in range(self.page_cnt): 
            existing_pdf = PdfReader(open("doc/template.pdf", "rb"))
            self.packet.seek(0)
            canvas_page_pdf = PdfReader(self.packet)
            existing_page = existing_pdf.pages[0]
            existing_page.merge_page(canvas_page_pdf.pages[i])
            output.add_page(existing_page)
        output_stream = open(self.output_pdf_path, "wb")
        output.write(output_stream)
        output_stream.close()