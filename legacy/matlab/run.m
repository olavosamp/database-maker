%
%

clear

% sourceBase     = 'E:/Projeto Final/Projeto Petrobras/20170724_FTP83G_Petrobras/';
% destBase       = 'E:/Projeto Final/Projeto Petrobras/images/remake/';
sourceBase     = 'E:/Projeto Final/Projeto Petrobras/20170724_FTP83G_Petrobras/';
destBase       = 'E:/Projeto Final/Projeto Petrobras/images/remake/';

paths    = [
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 20.32.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 21.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 21.32.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 22.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 23.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 23.32.35_C1.wmv",
            "TVILL16-054_OK/DVD-2/Dive 420 16-02-25 00.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-2/Dive 420 16-02-25 00.32.35_C1.wmv",
            "TVILL16-054_OK/DVD-2/Dive 420 16-02-25 01.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-2/Dive 420 16-02-25 02.32.35_C1.wmv",
];

pathLen = length(paths);
for i = 1:pathLen
    videoName = string(paths(i));
    
 
%     videoName      = 'TVILL16-054_OK/DVD-1/Dive 420 16-02-24 19.32.32_C1.wmv';
    videoPath      = sprintf('%s%s', sourceBase, videoName);

    nameSplit      = split(videoName, '.');
    nameSplit      = string(join(nameSplit(1:end-1),'.'));

    destPath       = sprintf('%s%s', destBase, nameSplit);
    
    fprintf("%s", videoPath);

    totFrames = getFramesFixed(videoPath, destPath, 5);

    disp([num2str(totFrames) ' frames obtained in total.'])

end