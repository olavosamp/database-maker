%
%

clear

videoPath = 'F:\Program Files\Arquivos Incomuns\Relevante\UFRJ\Projeto Final\DadosPetrobras\20170724_FTP83G_Petrobras\CIMRL10-676_OK\PIDF-1 PO MRL-021_parte2.mpg';
timeFramesPath = 'F:\Program Files\Arquivos Incomuns\Relevante\UFRJ\Projeto Final\DadosPetrobras\20170724_FTP83G_Petrobras\CIMRL10-676_OK\PIDF-1 PO MRL-021_parte2.csv';
totFrames = getFrames(videoPath, timeFramesPath);

disp([num2str(totFrames) ' frames obtained in total.'])