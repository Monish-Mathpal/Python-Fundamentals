# -*- coding: utf-8 -*-
"""
Created on Mon May  8 21:22:20 2017

@author: Monish Mathpal
"""
import PyPDF2
import re
from toolz import curry
from toolz import curry, compose
import itertools as it
from functools import partial
import pdb


keywords = []
report_attributes = set(keywords)
filter_dat = curry(map)
process = curry(filter)

def parsing_data(datapoints):
    str_datapoints = str(datapoints)
    cleaned_datapoints = str_datapoints.replace(',', '').strip('b').strip("''").strip('[]').strip('()').strip(' ')
    Key_string = [cleaned_datapoints if i in cleaned_datapoints else '' for i in keywords]
    return Key_string


def frb_extract(page_raw_datapoints):
    page_datapoints = list(process(lambda x: x != ' ')((list(filter_dat(parsing_data)(page_raw_datapoints)))))
    return page_datapoints








