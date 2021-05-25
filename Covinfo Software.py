from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from fpdf import FPDF
import sounddevice as sd
from scipy.io.wavfile import write
import json
import numpy as np
import tensorflow.keras as keras
from tensorflow.keras.preprocessing import image
import librosa
import math
import time
import datetime as dt
from pdf_mail import sendpdf
import shutil
import subprocess
import csv


def Exit1():
    Root.destroy()


def Print():
    subprocess.Popen(["Patient Report" + "/" + report + ".pdf"], shell=True)


def mail():
    # Taking input of following values
    # ex-"abcd@gmail.com"
    sender_email_address = "your mail id"

    # ex-"xyz@gmail.com"
    receiver_email_address = str(Email)

    # ex-" abcd1412"
    sender_email_password = "your password"

    # ex-"Heading of email"
    subject_of_email = "SARS-CoV-2 Report"

    # ex-" Matter to be sent"
    body_of_email = "Respected Sir/Ma'am" + "\n"
    body_of_email += "Please find the report attachment" + "\n"
    body_of_email += "Thank You" + "\n"
    body_of_email += "Team CovInfo"

    # ex-"Name of file"
    filename = report

    location_of_file = "Patient Report"

    # Create an object of send_pdf function
    k = sendpdf(sender_email_address,
                receiver_email_address,
                sender_email_password,
                subject_of_email,
                body_of_email,
                filename,
                location_of_file)

    # sending an email
    k.email_send()


def view():
    # view details
    Frame_Login = Frame(Root, bg="white")
    Frame_Login.place(x=150, y=50, height=500, width=400)

    Label(Frame_Login, text="Covid-19 Test Details", font=("Arial", 20, "bold"), bg="white").place(x=60, y=10)
    Label(Frame_Login, text="Name :" + " " + Name, font=("Arial", 10, "bold"), bg="white").place(x=10, y=80)
    Label(Frame_Login, text="Age :" + " " + Age, font=("Arial", 10, "bold"), bg="white").place(x=10, y=110)
    Label(Frame_Login, text="Gender :" + " " + Gender, font=("Arial", 10, "bold"), bg="white").place(x=10, y=140)
    Label(Frame_Login, text="Contact Details :" + " " + Contact, font=("Arial", 10, "bold"), bg="white").place(x=10,
                                                                                                               y=170)
    Label(Frame_Login, text="Email Id :" + " " + Email, font=("Arial", 10, "bold"), bg="white").place(x=10, y=200)
    Label(Frame_Login, text="Nationality :" + " " + Nationality, font=("Arial", 10, "bold"), bg="white").place(x=10,
                                                                                                               y=230)
    Label(Frame_Login, text="Cough Status :" + " " + status, font=("Arial", 10, "bold"), bg="white").place(x=10,
                                                                                                           y=260)
    Label(Frame_Login, text="X-Ray Status :" + " " + value, font=("Arial", 10, "bold"), bg="white").place(x=10,
                                                                                                          y=290)
    Label(Frame_Login, text="Test Results :" + " " + result, font=("Arial", 10, "bold"), bg="white").place(x=10,
                                                                                                           y=320)

    Button(Frame_Login, text="Email", command=mail, height=2, width=15).place(x=50, y=350)
    Button(Frame_Login, text="Preview", command=Print, height=2, width=15).place(x=220, y=350)
    Button(Frame_Login, text="New Entry", command=Detail_Page, height=2, width=15).place(x=50, y=400)
    Button(Frame_Login, text="Log Out", command=Login, height=2, width=15).place(x=220, y=400)


def excel():
    with open('Result_Data/CovInfo.csv', 'a', newline='') as csv_file:
        detail = [{'Time': localtime, 'Name': Name, 'Age': Age, 'Gender': Gender, 'Contact': Contact,
                   'Email Id': Email, 'Nationality': Nationality, 'Status': status, 'Report': report, 'Audio': audio,
                   'SARS-CoV-2 Cough Result': status, 'X-Ray Test Result': value, 'Result': result}]
        fields = list(detail[0].keys())
        obj = csv.DictWriter(csv_file, fieldnames=fields)
        obj.writerows(detail)
        csv_file.close()


def pdf():
    global report
    global localtime
    global result
    # creating PDF report
    localtime = time.asctime(time.localtime(time.time()))
    localtime = str(localtime)
    File = ['Images/Cover.png']
    Pdf = FPDF(orientation='P', unit='mm', format='A4')
    if status == 'Positive' and value == 'Positive':
        result = "Positive"
    elif status == 'Negative' and value == 'Negative':
        result = "Negative"
    elif status == "May be Symptomatic" and (value == "Negative" or value == "Positive"):
        result = "May be Symptomatic"
    else:
        result = "May be Symptomatic"

    # take dimension in mm

    Pdf.set_font('Arial', 'B', 20)
    for image in File:
        Pdf.add_page()
        Pdf.image(image, x=0, y=0, w=210, h=297)
    Pdf.set_xy(120, 10)
    Pdf.cell(0, 0, localtime)
    text = "Name :" + " " + Name + "\n"
    text += "Age :" + " " + Age + "\n"
    text += "Gender :" + " " + Gender + "\n"
    text += "Contact Details :" + " " + Contact + "\n"
    text += "Email :" + " " + Email + "\n"
    text += "Nationality :" + " " + Nationality + "\n"
    text += "Duration :" + " " + "10.0" + " " + "Seconds" + "\n"
    text += "Covid Cough Status :" + " " + status + "\n"
    text += "X-ray Test Status :" + " " + value + "\n"
    text += "Result :" + " " + result
    Pdf.set_xy(20, 75)
    Pdf.multi_cell(0, 15, text)
    report = Name + "_" + "report" + seconds
    Pdf.output(report + ".pdf", 'F')
    shutil.move(Name + "_" + "report" + seconds + ".pdf",
                "Patient Report")

    excel()


def predict(Model, y):
    global status
    x = np.reshape(y, (y.shape[0], y.shape[1], -1))
    count_negative = 0
    count_positive = 0
    for i in range(0, len(x)):
        y = x[i][np.newaxis, ...]
        prediction = Model.predict(y)
        prediction_index = np.argmax(prediction, axis=1)
        if prediction_index == [0]:
            count_negative += 1
        else:
            count_positive += 1
    if count_negative > count_positive:
        status = "Negative"
    elif count_positive > count_negative:
        status = "Positive"
    else:
        status = "May be Symptomatic"


def extract_features(Data, n_mfcc=40, n_fft=4096, hop_length=512):
    y = {"mfcc": []}
    Duration = 10  # measure in seconds
    SAMPLE_RATE = 22050
    num_segment = int(Duration)
    sample_track = SAMPLE_RATE * Duration
    signal, sr = librosa.load(Data, sr=SAMPLE_RATE)
    num_samples_per_segment = int(sample_track / num_segment)
    expected_num_vector_per_segment = math.ceil(num_samples_per_segment / hop_length)
    for s in range(num_segment):
        start_sample = num_samples_per_segment * s
        finish_sample = start_sample + num_samples_per_segment
        mfcc = librosa.feature.mfcc(signal[start_sample:finish_sample],
                                    sr=SAMPLE_RATE,
                                    n_mfcc=n_mfcc,
                                    n_fft=n_fft,
                                    hop_length=hop_length)
        mfcc = mfcc.T
        if len(mfcc) == expected_num_vector_per_segment:
            y["mfcc"].append(mfcc.tolist())

    JSON_PATH = "Patient Mfcc/" + Name + "_" + "mfcc" + seconds
    with open(JSON_PATH, "w") as fp:
        json.dump(y, fp, indent=4)

    Data_path = "Patient Mfcc/" + Name + "_" + "mfcc" + seconds
    with open(Data_path, "r") as fp:
        Data = json.load(fp)
    x = np.array(Data["mfcc"])
    model = keras.models.load_model('Model/covid_model.h5')
    predict(model, x)


def test(a):
    global value
    model = keras.models.load_model('Model/xray_covid_model.h5')
    Image = image.load_img(file_name)
    X = image.img_to_array(Image)
    X = np.expand_dims(X, axis=0)
    img = np.vstack([X])
    val = model.predict(img)
    if val == 1:
        value = "Negative"
    else:
        value = "Positive"


def file_opener():
    global file_name
    input = filedialog.askopenfile(initialdir="/")
    if input:
        file_name = input.name
    test(file_name)


def recording():
    global audio
    messagebox.showinfo("", "Recording Started")
    # Sampling frequency
    freq = 44100

    # Recording duration
    duration = 10

    # Start recorder with the given values
    # of duration and sample frequency
    Recording = sd.rec(int(duration * freq),
                       samplerate=freq, channels=2)

    # Record audio for the given number of seconds
    sd.wait()

    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    audio = Name + "_" + seconds + ".wav"
    write(audio, freq, Recording)
    shutil.move(Name + "_" + seconds + ".wav",
                "Patient Audio Dataset")
    messagebox.showinfo("", "Recording Completed")
    data = "Patient Audio Dataset" + "/" + audio
    extract_features(data)
    pdf()
    new_frame2 = Frame(Root, bg="white")
    new_frame2.place(x=150, y=480, width=400, height=70)
    Button(new_frame2, text="View Result", command=view, height=2, width=15).place(x=10, y=10)


def submit():
    global Name
    global Age
    global Gender
    global Contact
    global Email
    global Nationality

    Name = e3.get()
    Age = e4.get()
    Gender = e5.get()
    Contact = e6.get()
    Email = e7.get()
    Nationality = e8.get()

    if Name == "" and Age == "" and Gender == "" and Contact == "" and Email == "" and Nationality == "":
        messagebox.showinfo("", "Blank not allowed")
        detail_page()
    else:
        messagebox.showinfo("", "Submitted")
        new_frame = Frame(Root, bg="white")
        new_frame.place(x=150, y=420, width=400, height=130)
        Button(new_frame, text="Select an X-ray File", command=file_opener, height=2, width=15).place(x=10, y=10)
        Button(new_frame, text="Start Recording", command=recording, height=2, width=15).place(x=10, y=80)


def Detail_Page():
    detail_page()


def detail_page():
    """global root
    root = Tk()
    root.title("CovInfo")
    # Adjust size
    root.geometry("1199x600+100+20")
    root.resizable(False, False)
    # Add image file
    photo = PhotoImage(file="covinfo-01.png")
    root.iconphoto(False, photo)
    bg = PhotoImage(file="Covid.png")
    Label(root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)"""
    Frame_Login = Frame(Root, bg="white")
    Frame_Login.place(x=150, y=50, height=500, width=400)
    global e3
    global e4
    global e5
    global e6
    global e7
    global e8

    Label(Frame_Login, text="Enter Patient Details", font=("Arial", 20, "bold"), bg="white").place(x=60, y=10)
    Label(Frame_Login, text="Name", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=10, y=80)
    Label(Frame_Login, text="Age", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=10, y=120)
    Label(Frame_Login, text="Gender", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=10, y=160)
    Label(Frame_Login, text="Contact Details", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=10,
                                                                                                                  y=200)
    Label(Frame_Login, text="Email Id", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=10, y=240)
    Label(Frame_Login, text="Nationality", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=10,
                                                                                                              y=280)

    e3 = Entry(Frame_Login, bg="lightgray")
    e3.place(x=150, y=80, height=30, width=200)
    e4 = Entry(Frame_Login, bg="lightgray")
    e4.place(x=150, y=120, height=30, width=200)
    e5 = Entry(Frame_Login, bg="lightgray")
    e5.place(x=150, y=160, height=30, width=200)
    e6 = Entry(Frame_Login, bg="lightgray")
    e6.place(x=150, y=200, height=30, width=200)
    e7 = Entry(Frame_Login, bg="lightgray")
    e7.place(x=150, y=240, height=30, width=200)
    e8 = Entry(Frame_Login, bg="lightgray")
    e8.place(x=150, y=280, height=30, width=200)
    Button(Frame_Login, text="Submit", command=submit, height=2, width=10).place(x=10, y=320)
    Button(Frame_Login, text="Exit", command=Exit1, height=2, width=10).place(x=270, y=320)


def ok():
    uname = e1.get()
    password = e2.get()

    if uname == " " and password == " ":
        messagebox.showinfo("", "Blank not allowed")
    elif uname == "CovInfo" and password == "123":
        messagebox.showinfo("", "Login Successful")
        # Root.destroy()
        detail_page()
    else:
        messagebox.showinfo("", "Invalid Username and Password")


def Login():
    Root.destroy()
    login()


def login():
    global Root
    Root = Tk()
    Root.title("CovInfo")
    # Adjust size
    Root.geometry("1199x600+100+20")
    Root.resizable(False, False)
    # Add image file
    photo = PhotoImage(file="Images/covinfo-01.png")
    Root.iconphoto(False, photo)
    bg = PhotoImage(file="Images/Covid.png")
    Label(Root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    global seconds
    # creating PDF report
    seconds = str(int(time.time()))
    Label(Root, text=f"{dt.datetime.now():%a, %b %d %Y}", fg="white", bg="#16d9fc", font=("helvetica", 15)).place(x=10,
                                                                                                                  y=10)
    # Label(root, text=f"{time.strftime('%H:%M:%S')}",
    # fg="white", bg="#16d9fc",
    # font=("helvetica", 20)).place(x=10, y=40)
    Frame_Login = Frame(Root, bg="white")
    Frame_Login.place(x=150, y=150, height=340, width=400)
    Label(Frame_Login, text="Login", font=("Arial", 35, "bold"), bg="white").place(x=130, y=30)

    global e1
    global e2

    Label(Frame_Login, text="Username", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=90, y=100)
    Label(Frame_Login, text="Password", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=90, y=180)

    e1 = Entry(Frame_Login, bg="lightgray")
    e1.place(x=90, y=140, height=30, width=200)

    e2 = Entry(Frame_Login, bg="lightgray")
    e2.place(x=90, y=220, height=30, width=200)
    e2.config(show="*")
    Button(Frame_Login, text="Login", command=ok, height=2, width=10).place(x=90, y=270)
    Button(Frame_Login, text="Exit", command=Exit1, height=2, width=10).place(x=210, y=270)
    # Execute tkinter
    Root.mainloop()


if __name__ == "__main__":
    login()
