from weasyprint import HTML
import os
path = "file://"+os.getcwd() + "/static/"
from jinja2 import Environment, FileSystemLoader

def generate_report(data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("templates/Report.html").render(data=data)
    HTML(string=template).write_pdf("static/PDF/report.pdf")

data = {
    "month" : "January",
    "year" : "2023",
    "cover1" : path + "/images/cover1.png",
    "cover2" : path + "/images/cover2.png",
    "cover_logo" : path + "/images/logo.png"
}

generate_report(data)