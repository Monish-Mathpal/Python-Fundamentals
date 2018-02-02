# -*- coding: utf-8 -*-
"""
Created on Mon May  8 21:22:20 2017

@author: XBBNJTW
"""
import PyPDF2
import re
from toolz import curry
from collections import defaultdict
import pdb
from itertools import chain


keywords = []
report_attributes = set(keywords)
filter_dat = curry(map)
process = curry(filter)


def update(words, type):
    pass


def parsing_data(x):
    y = str(x)
    z = y.replace(',', '').strip('b').strip("''").strip('[]').strip('()').strip(' ').replace('\\', '').replace('(', '').replace(')', '')
    Key_string = z if z in report_attributes or z.replace('.', '').isdigit() or z.startswith(
        'Business Date:') or z.startswith('Deposit Account:') or z.startswith('TOTAL CLEARING FUND REQUIREMENT') or \
        z.startswith('Your minimum required Cash deposit is') or z.startswith('Cash') or z.startswith('Opening Balance')\
         else ' '

    # print(z)
    return Key_string

def frb_extract(rc_page_raw_datapoints):

    rc_page_datapoints = list(process(lambda x: x != ' ')((list(filter_dat(parsing_data)(rc_page_raw_datapoints)))))
    return rc_page_datapoints




def gpl(rc_page_data):
    reg_gpl = re.compile(rb"[Tf\n,Tw\n,TD\n](.*)Tj\n")
    return reg_gpl.findall(rc_page_data)


def acrobat(rc_page_data):
    reg_acrobat = re.compile(rb"[Tf\n,Tw\n,TD\n](.*)Tj\n")
    return reg_acrobat.findall(rc_page_data)


def itext(rc_page_data):
    reg_itext = re.compile(rb"[TD\n,Tf\n, T*\n](.*)Tj\n")
    return reg_itext.findall(rc_page_data)


def faceless(rc_page_data):
    reg_itext = re.compile(rb"Td\n(.*)TJ\n")

    return reg_itext.findall(rc_page_data)


def pdf_read(pdfName, pagenum=0):
    # pdb.set_trace()
    with open(pdfName, 'rb') as pdfobj:
        pdfReader = PyPDF2.PdfFileReader(pdfobj)
        rc_page = pdfReader.getPage(pagenum)
        rc_page_content = rc_page.getContents()
        rc_page_data = rc_page_content.getData()
        # print(rc_page_data)

        if pdfReader.documentInfo['/Producer'].find('Acrobat Distiller')!= -1:
            return acrobat(rc_page_data)

        # elif pdfReader.documentInfo['/Producer'].find('GPL') != -1:
        #     return gpl(rc_page_data)

        elif pdfReader.documentInfo['/Producer'].find('iText') != -1:
            return itext(rc_page_data)

        elif pdfReader.documentInfo['/Producer'].find("faceless") != -1:
            return faceless(rc_page_data)

        else:
            rc_page_data = rc_page.extractText()
            return rc_page_data.split("\n")






