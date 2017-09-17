function totalFrames = getFrames( videoPath, timeFramesPath)
    %
    % totalFrames = getFrames( videoPath, timeFramesPath)
    % 
    % O script lê o vídeo em videoPath e extrai os frames de acordo com os
    % tempos especificados no arquivo csv localizado em timeFramesPath. Os frames são salvos na pasta
    % '.\images\', com nome '<nome do video> ID<ID> <classe> FRAME<frame>.jpg'
    % 
    % videoPath  - caminho do arquivo de vídeo
    % timeFramesPath  - caminho do arquivo csv de referencia
    %

    table = readtable(timeFramesPath, 'TextType', 'char');
    numEntries = height(table);
    
    classes = string(['tubo'; 'nada'; 'conf' ]);
    classesCount = zeros(length(classes),1);
    
    videoObj = VideoReader(videoPath);
    frameRate = videoObj.FrameRate;     % Get video Frame Rate
    %framePeriod = 20/frameRate;         % Save one every 20 frames

    disp(['Video: ' string(table.VideoName(1))])
    disp(['Frame rate: ' num2str(frameRate)])
    
    dirPath = sprintf('.\\%s', string(table.VideoName(1)));
    mkdir(dirPath);

    totalFrames = 0;
    for i = 1:numEntries
        currentClass = string(table.Class(i));
        imagePath = sprintf('%s\\%s ID%d %s', dirPath, string(table.VideoName(i)), table.Id(i), currentClass);
        
        eventStart = table.StartTime(i);    % Start of event
        eventEnd = table.EndTime(i);        % End of event

        % Convert input time to seconds
        eventStart = timeConverter(string(eventStart));
        eventEnd = timeConverter(string(eventEnd));
        
        % Reduce capture rate if the event is very long
        tLimit = 600;       % 10 minutes
        if (eventEnd - eventStart) >= tLimit
            framePeriod = 40/frameRate;
        else
            framePeriod = 20/frameRate;
        end
        
        frameTime = eventStart;

        % Keep track of class populations
        index = (classes(:) == currentClass);
        
        disp(['Reading entry No ' num2str(table.Id(i))])
        frameCount = 0;
        while frameTime < (eventEnd - 0.5)
            videoObj.CurrentTime = frameTime;
            frame = readFrame(videoObj);

            % Advance one period
            frameTime = frameTime + framePeriod;

            % Save frame as .jpg
            filePath = sprintf('%s FRAME%d.jpg', imagePath, frameCount+1);
            imwrite(frame, filePath);

            frameCount = frameCount + 1;
            classesCount(index) = classesCount(index) + 1;
        end
        totalFrames = totalFrames + frameCount;
    end
    
    disp([''])
    disp(['Total frames: ' num2str(totalFrames)])
    disp(['Class populations: '])
    for i=1:length(classesCount)
        fprintf('%s: %d\n', classes(i), classesCount(i))
    end
end