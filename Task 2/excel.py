import json
import os
from natsort import natsorted
from openpyxl import load_workbook
from collections import OrderedDict


dirName = './pozyxAPI_dane_pomiarowe'


def readtitles(sheet):
    titlesArray = []
    for cell in sheet[1]:
        if cell.value is not None:
            titlesArray.append(cell.value)
    return titlesArray


def readvalues(sheet, titles):
    doc = OrderedDict()
    for value in sheet.iter_rows(min_row=2, values_only=True):
        if value[0] is None:
            dictionary = {titles[0]: value[1], titles[1]: value[2],
                          titles[3]: value[4], titles[4]: value[5],
                          titles[5]: value[6], titles[6]: value[7]}
            doc[value[3]] = OrderedDict(dictionary)
    return doc


def parseandsavetojson(path, sheet, titles):
    doc = readvalues(sheet, titles)
    with open(path, 'w') as file:
        json.dump(doc, file, indent=4)


def processall():
    it = 1
    titles = []
    for filename in natsorted(os.listdir(dirName)):
        if filename.endswith(".xlsx"):
            workbook = load_workbook(filename=dirName+"/"+filename, data_only=True)
            sheet = workbook.active
            if it == 1:
                titles = readtitles(sheet)
            parseandsavetojson(f"./jsons/{it}.json", sheet, titles)
            it += 1