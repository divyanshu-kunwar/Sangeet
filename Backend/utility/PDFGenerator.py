from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from controller.c_analytics import prepareReport
from utility.mailer import Mail
from flask import current_app
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def generate_chart(path, date, plays, likes = None):
    x = date
    y = plays
    if likes:
        y2 = likes
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    if likes:
        ax.plot(x, y2)

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

    # create file and save
    plt.savefig(path , transparent=True)
    plt.close()


def generate_report(id , email):
    
    data_ = prepareReport(id)

    path = "file://"+os.getcwd() + "/static/"
    data_["cover1"] = path + "images/cover1.png"
    data_["cover2"] = path + "images/cover2.png"
    data_["cover_logo"] = path + "images/logo.png"
    data_["font1"] = path + "font/Kalam-Regular.ttf"
    data_["font2"] = path + "font/Raleway-VariableFont_wght.ttf"

    # for each song in data_["songs"]
    # generate chart using plotly and then add it as image
    for song_key in data_["songs"]:
        data_["songs"][song_key]["chart"] = path + "images/chartSong" + str(song_key) + ".png"
        relative_path = "static/images/chartSong" + str(song_key) + ".png"
        generate_chart(relative_path, data_["songs"][song_key]["date"], 
                    data_["songs"][song_key]["play_count"], data_["songs"][song_key]["like_count"])
    
    for album_key in data_["albums"]:
        data_["albums"][album_key]["chart"] = path + "images/chartAlbum" + str(album_key) + ".png"
        relative_path = "static/images/chartAlbum" + str(album_key) + ".png"
        generate_chart(relative_path, data_["albums"][album_key]["date"], 
                    data_["albums"][album_key]["play_count"])


    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("templates/Report.html").render(data=data_)

    HTML(string=template).write_pdf("static/PDF/report.pdf")

    print("Report Generated ====== > Sending Mail to user")

    mail = Mail(current_app)
    result = mail.send(subject="Monthly Report", to_email=email, htmlbody="Report", pdf_file_path="static/PDF/report.pdf")
    if(result == True):
        print("Mail Sent to ===> " + email)
    else:
        print("Could Not Sent Mail to ===> " + email)
