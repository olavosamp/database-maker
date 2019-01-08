import os

sep     = "/"       # Foward dash for Windows/Linux compatibility
# sep = "\\"        # Backwards dash for Windows specific applications

csv                 = ".."+sep+"csv"+sep
totals              = csv+"Totals"+sep
demo                = ".."+sep+"demo"+sep
images              = ".."+sep+".."+sep+"images"+sep
dataset             = ".."+sep+".."+sep+"20170724_FTP83G_Petrobras"+sep
registro_de_eventos = csv+sep+"registro_de_eventos"+sep

new_images          = ".."+sep+".."+sep+"new_images"+sep
trim                = new_images+"trim"+sep

def create_folder(path):
    try:
        os.makedirs(path)
    except OSError:
        # Folder already exists or destFolder is invalid
        pass

create_folder(demo)
create_folder(images)
create_folder(new_images)
