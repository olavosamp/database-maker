function [ seconds ] = timeConverter( strTime )
% seconds = timeConverter( strTime )
% Converts HHMMSS input string to numeric seconds
%


len = length(strTime);

if len > 6
    seconds = 0;
else
    strTime = char(pad(strTime, 6, 'left', num2str(0)));

    h = str2num(strTime(1:2));
    m = str2num(strTime(3:4));
    s = str2num(strTime(5:6));

    seconds = s + m*60 + h*3600;
end
end

