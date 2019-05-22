from libs.utils import convert_video


basePath = "E:/Projeto Final/Projeto Petrobras/20170724_FTP83G_Petrobras/"
baseDest = "E:/Projeto Final/Projeto Petrobras/demo/"

videoName = "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 21.02.35_C1.wmv"

convert_video(basePath+videoName, baseDest, 'mp4')
