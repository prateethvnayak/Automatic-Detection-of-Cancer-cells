import os

def img_list(path):
    dirListing = sorted(os.listdir(path))
    CroppedFiles = []
    for item in dirListing:
        if ".jpeg" in item:
            CroppedFiles.append(item)

    return CroppedFiles
