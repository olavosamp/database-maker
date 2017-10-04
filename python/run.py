from getFrames import getFrames

videoPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\20170724_FTP83G_Petrobras\\GHmls16-263_OK\\DVD-1\\20161101212059250@DVR-SPARE_Ch1.wmv"
csvPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\database-maker\\csv\\GHmls16-263_OK\\DVD-1\\20161101212059250@DVR-SPARE_Ch1.csv"

frameTotal = getFrames(videoPath, csvPath)