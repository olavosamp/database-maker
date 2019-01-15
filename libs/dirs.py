import os

sep     = "/"       # Foward dash for Windows/Linux compatibility
# sep = "\\"        # Backwards dash for Windows specific applications

csv                 = ".."+sep+"csv"+sep
totals              = csv+"Totals"+sep
demo                = ".."+sep+"demo"+sep
converted           = ".."+sep+"converted"+sep
images              = ".."+sep+"images"+sep
dataset             = ".."+sep+"20170724_FTP83G_Petrobras"+sep
registro_de_eventos = csv+sep+"registro_de_eventos"+sep

def create_folder(path):
    try:
        os.makedirs(path)
    except OSError:
        # Folder already exists or destFolder is invalid
        pass

create_folder(demo)
create_folder(images)
create_folder(converted)
