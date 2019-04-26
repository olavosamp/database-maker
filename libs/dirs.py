import os

sep     = "/"       # Foward dash for Windows/Linux compatibility
# sep = "\\"        # Backwards dash for Windows specific applications

root                = "."+sep
csv                 = root+"csv"+sep
images              = root+".."+sep+"images"+sep
base_videos         = root+".."+sep+"20170724_FTP83G_Petrobras"+sep
index               = root+"csv"+sep+"main_index.csv"
dataset             = root+sep+".."+sep+"datasets"+sep
# totals              = csv+"Totals"+sep
# demo                = root+".."+sep+"demo"+sep
# converted           = root+".."+sep+"converted"+sep
# registro_de_eventos = csv+sep+"registro_de_eventos"+sep

def create_folder(path):
    try:
        os.makedirs(path)
    except OSError:
        # Folder already exists or destFolder is invalid
        pass

create_folder(images)
# create_folder(demo)
# create_folder(converted)
