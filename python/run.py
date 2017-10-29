from getFrames import getFrames

videoPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\20170724_FTP83G_Petrobras\\GHmls16-263_OK\\DVD-1\\20161101235105625@DVR-SPARE_Ch1.wmv"
csvPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\database-maker\\csv\\GHmls16-263_OK\\DVD-1\\20161101235105625@DVR-SPARE_Ch1.csv"
# videoPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\20170724_FTP83G_Petrobras\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte2.mpg"
# csvPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\database-maker\\csv\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte2.csv"

frameTotal = getFrames(videoPath, csvPath)