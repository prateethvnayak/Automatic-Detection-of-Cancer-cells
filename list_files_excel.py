import os


def Main_imgbmp(path):
    dirListing = sorted(os.listdir(path))
    BMPFiles = []
    for item in dirListing:
        if ".BMP" in item:
            BMPFiles.append(item)

    bmpFiles = []

    for item in dirListing:
        if "-d.bmp" in item:
            bmpFiles.append(item)

    return BMPFiles, bmpFiles

def Main_imgxml(path):
    dirListing = sorted(os.listdir(path))
    bmpFiles = []
    for item in dirListing:
        if ".bmp" in item:
            bmpFiles.append(item)

    xmlFiles = []

    for item in dirListing:
        if ".xml" in item:
            xmlFiles.append(item)

    return bmpFiles, xmlFiles

