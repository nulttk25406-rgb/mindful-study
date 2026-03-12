import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


def export_report(sessions):

    if not sessions:
        print("Chưa có dữ liệu để xuất!")
        return

    x = range(1, len(sessions)+1)

    plt.figure()
    plt.plot(x, sessions)

    plt.xticks(range(1, len(sessions)+1))
    plt.xlabel("Phiên học")
    plt.ylabel("Số phút")
    plt.title("Biểu đồ năng suất")

    base_path = os.path.dirname(__file__)

    chart_path = os.path.join(base_path, "chart.png")
    plt.savefig(chart_path)
    plt.close()

    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))

    pdf_path = os.path.join(base_path, "report.pdf")
    pdf = SimpleDocTemplate(pdf_path)
    elements = []

    styles = getSampleStyleSheet()
    styles["Title"].fontName = "DejaVu"
    styles["Normal"].fontName = "DejaVu"

    elements.append(
        Paragraph("BÁO CÁO NĂNG SUẤT HỌC TẬP", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    total_minutes = sum(sessions)
    total_seconds = int(total_minutes * 60)
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    elements.append(
        Paragraph(f"Tổng thời gian học: {minutes} phút {seconds} giây", styles["Normal"]))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Image(chart_path, width=4*inch, height=3*inch))

    pdf.build(elements)
    os.startfile(pdf_path)

    print("Đã xuất report.pdf thành công!")
