import os, signal, argparse, sys, re, shutil
import time
from datetime import datetime, timezone
import datetime as dt
import subprocess

import requests,urllib
import csv
import pysftp as sftp
import json
import pandas as pd
import numpy as np

import logging
import util_rpa
from util_rpa import Configuration
import cv2

###
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.ie.options import Options as OptionsIE
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

from fpdf import FPDF
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

import urllib3
import base64
import fitz
import mysql.connector

# Definicion de Carpetas
dir_path = os.path.dirname(__file__)
dir_in = os.path.join(dir_path,"input")
dir_out = os.path.join(dir_path,"output")
dir_log = os.path.join(dir_path,"log")
dir_sql = os.path.join(dir_path,"sql")
dir_res = os.path.join(dir_path,"resource")
dir_temp = os.path.join(dir_path,"temp")

util_rpa.create_folder_env(dir_path)

# Definicion de Variables
today = datetime.now()
#today = datetime.strptime("09/07/2021 23:45:00", "%d/%m/%Y %H:%M:%S")

today_line=str(today.strftime("%Y%m%d%H%M%S"))
today_format=str(today.strftime("%d/%m/%Y %H:%M:%S"))

#file_download=os.path.join(dir_in,"fase2_" + today_line + ".txt")
urllib3.disable_warnings()
inicio=time.time()

# log.info("## Convirtiendo PDF a Imagen PNG")

# log.info("Archivo PDF: " + mensaje["ARCHIVO_LOCAL"])
doc = fitz.open("061696464PEhpKbcY.pdf")
page = doc.loadPage(0)

pix = page.getPixmap(matrix=fitz.Matrix(150/72,150/72))
archivo_png = os.path.join(dir_temp, str("061696464PEhpKbcY.pdf").replace(".pdf", ".png"))
#archivo_png = os.path.join(dir_temp, "test.png")

# log.info("Archivo PNG: " + archivo_png)
pix.writePNG(archivo_png)

# log.info("## Conviertiendo Imagen a texto - OCR")

with open(archivo_png, "rb") as image_file:
    data = base64.b64encode(image_file.read())
    base = data.decode("utf-8")

data = {"base64"   : base,
        "languages": "spa"}

try:
    url = "http://172.30.250.106:8081/base64"
    # log.info ("URL: " + url)
    # log.info ("Request Body: " + str(data)[0:15])

    img = cv2.imread(archivo_png)
    crop_img = img[922:109, 1240:1755]
    cv2.imwrite(os.path.join(dir_temp, "test.png"), crop_img)

    response = requests.post(url = url, json = cv2, verify = False, timeout=60, proxies={})
    # log.info("Response StatusCode: " + str(response.status_code))
    # log.info("Response Header: " + str(response.headers))
    # log.info("Response Body: " + str(response.text)[0:15])

    resultado_json = json.loads(response.text)

    r_j = resultado_json["result"]

    print(r_j)


except Exception as e:
    # log.info("Ocurrio un error en la lectura OCR")
    raise Exception(e)

# log.info("## Analizando texto")
# log.info(mensaje["ARCHIVO_CONTENIDO"])
