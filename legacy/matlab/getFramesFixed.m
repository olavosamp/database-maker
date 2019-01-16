function currentFrame = getFramesFixed( videoPath, destPath, interval)
    %
    % totalFrames = getFrames( videoPath, timeFramesPath)
    % 
    % O script lê o vídeo em videoPath e extrai os frames de acordo com os
    % tempos especificados no arquivo csv localizado em timeFramesPath. Os frames são salvos na pasta
    % './images/', com nome '<nome do video> ID<ID> <classe> FRAME<frame>.jpg'
    % 
    % videoPath  - caminho do arquivo de vídeo
    %


    videoObj = VideoReader(videoPath);
    
    
%     frameRate   = ceil(videoObj.FrameRate);     % Get video Frame Rate
    %interval   = 20/frameRate;               % Save one every 20 frames
    
    videoTime = videoObj.Duration;
    
    videoName = videoObj.Name;
    
%     disp(['Video: ' string(table.VideoName(1))])
%     disp(['Frame rate: ' num2str(frameRate)])
%     disp(['Frame period: ' num2str(interval)])
    
%     dirPath = sprintf('./%s', string(table.VideoName(1)));

    

    mkdir(destPath);
    
    fprintf('\nStarting capture of video \n%s\nTotal duration: %ds\n', videoPath, videoTime)

    
    currentFrame= 1;
    currentTime = 0;
    while currentTime < videoTime
        fprintf('Frame %d\n', currentFrame)
        imagePath = sprintf('%s/%s', destPath, videoName);
        

        videoObj.CurrentTime = currentTime;
        frame = readFrame(videoObj);

        
        % Save frame as .jpg
        filePath = sprintf('%s_FRAME_%d.jpg', imagePath, currentFrame);
        imwrite(frame, filePath);

        % Advance one period
        currentTime = currentTime + interval;
        
        currentFrame = currentFrame + 1;
    end
    
    disp([''])
    disp(['Total frames: ' num2str(currentFrame)])
end