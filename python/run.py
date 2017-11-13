from getFrames import getFrames

videoPath = "C:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\Petrobras\\20170724_FTP83G_Petrobras\\GHmls16-263_OK\\DVD-1\\20161102000728984@DVR-SPARE_Ch1.wmv"
csvPath = "C:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\Petrobras\\database-maker\\csv\\GHmls16-263_OK\\DVD-1\\20161102000728984@DVR-SPARE_Ch1.csv"

# videoPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\20170724_FTP83G_Petrobras\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte1.mpg"
# csvPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\database-maker\\csv\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte1.csv"

frameTotal = getFrames(videoPath, csvPath) 