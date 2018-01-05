# from getFrames import getFrames
import count
import dirs

# videoPath = dirs.dataset+"\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte2.mpg"
# csvPath = dirs.csv+"\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte2.csv"
#
# # videoPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\20170724_FTP83G_Petrobras\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte1.mpg"
# # csvPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\database-maker\\csv\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte1.csv"
#
# frameTotal = getFrames(videoPath, csvPath)
# # csvTotals = count.countCsv()
# # print("\nTotal potential images (classified and recorded in csv):\n")
# # print(csvTotals)
# print("{} images obtained.".format(frameTotal))

# videoList, csvList, frameTotal = count.rebuildDataset(dirs.csv, dirs.dataset)

# TODO: Use countImages instead
labels = count.listImages(dirs.images)
frameTotal = count.countImages(labels)
print("{} frames obtained.".format(frameTotal))
# print("\nDatabase rebuilt.")
