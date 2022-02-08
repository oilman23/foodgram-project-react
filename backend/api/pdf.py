# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# canvas = canvas.Canvas("form3.pdf", pagesize=letter)
# canvas.setLineWidth(2.6)
# canvas.setFont('Helvetica', 12)
# canvas.drawString(30, 750,'OFFICIAL COMMUNIQUE')
# canvas.drawString(30, 735,'OF ACME INDUSTRIES')
# canvas.drawString(500, 750,"12/12/2010")
# canvas.line(480,747,580,747)
# canvas.drawString(275,725,'AMOUNT OWED:')
# canvas.drawString(500,725,"$1,000.00")
# canvas.line(378,723,580,723)
# canvas.drawString(30,703,'RECEIVED BY:')
# canvas.line(120, 700, 580, 700)
# canvas.drawString(120, 703,"JOHN DOE")
# canvas.save()


import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
doc = SimpleDocTemplate("form_letter.pdf",pagesize=letter,
 rightMargin=72,leftMargin=72,
 topMargin=72,bottomMargin=18)
Story=[]
logo = "Jira_Политики.PNG"
magName = "Pythonista"
issueNum = 12
subPrice = "99.00"
limitedDate = "03/05/2010"
freeGift = "tin foil hat"
formatted_time = time.ctime()
full_name = "Mike Driscoll"
address_parts = ["411 State St.", "Marshalltown, IA 50158"]
im = Image(logo, 2*inch, 2*inch)
Story.append(im)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
ptext = '%s' % formatted_time
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
# Create return address
ptext = '%s' % full_name
Story.append(Paragraph(ptext, styles["Normal"]))
for part in address_parts:
    ptext = '%s' % part.strip()
    Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
ptext = 'Dear %s:' % full_name.split()[0].strip()
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
ptext = 'We would like to welcome you to our subscriber base for %s Magazine! \
 You will receive %s issues at the excellent introductory price of $%s. Please respond by\
 %s to start receiving your subscription and get the following free gift: %s.' % (magName,
 issueNum,
 subPrice,
 limitedDate,
 freeGift)
Story.append(Paragraph(ptext, styles["Justify"]))
Story.append(Spacer(1, 12))
ptext = 'Thank you very much and we look forward to serving you.'
Story.append(Paragraph(ptext, styles["Justify"]))
Story.append(Spacer(1, 12))
ptext = 'Sincerely,'
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 48))
ptext = 'Ima Sucker'
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
doc.build(Story)