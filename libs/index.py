import os
import pandas       as pd
import numpy        as np
from   datetime     import datetime
from   pathlib      import Path
from   glob         import glob

import libs.dirs    as dirs


class IndexManager:
    def __init__(self, path=dirs.index):
        self.path          = Path(path)
        self.indexExists   = False
        self.bkpFolderName = "index_backup"

        self.validate_path()


    def validate_path(self):
        if self.path.suffix == ".csv":
            # Check for csv files matching filename in self.path
            # pathList = glob(str(self.path.with_name("*"+str(self.path.stem)+"*.csv")).strip())
            pathList = list(self.path.parent.glob("*"+str(self.path.stem).strip()+"*.csv"))
            # print("PathList")
            # print(pathList)

            if len(pathList) > 0:
                try:
                    # Check if index DataFrame exists and is non-empty
                    self.index = pd.read_csv(pathList[0])

                    if self.index.shape[0] > 0:
                        self.indexExists = True
                except pd.errors.EmptyDataError:
                    pass
        else:
            raise ValueError("Invalid index path.")


    def add_entry(self, newEntry):
        '''
            Adds new entry to index by appending a line to the existing DataFrame or
            creating a new DataFrame with one line.
            newEntry: Dict of lists. Keys are data columns, values are lists containing
                      the data
        '''
        if self.indexExists == True:
            # Append to existing df
            newEntryDf = pd.DataFrame.from_dict(newEntry)

            # exit()

            self.index = self.index.append(newEntryDf, sort=False, ignore_index=False).reset_index(drop=True)
            # self.check_duplicate()
        else:
            # create df with new entry and write to disk as the index file
            self.index = pd.DataFrame.from_dict(newEntry)
            self.indexExists = True


    def check_duplicate(self):
        # print(self.index[self.index.duplicated(['VideoName'], keep=False)])
        check1 = self.index.duplicated(['Report'])
        check2 = self.index.duplicated(['DVD'])
        check3 = self.index.duplicated(['FrameName'])
        truthArray = np.array([check1, check2, check3]).T
        mask = np.all(truthArray, axis=1)

        print(check3[mask])
        print(truthArray[mask, :])
        print(self.index.loc[mask, :])
        input()
        # indexLen = self.index.shape[0]

        # for i in range(indexLen):
        #     check1 = (self.index.loc[i, 'Report']    == newEntryDf['Report']).values
        #     check2 = (self.index.loc[i, 'DVD']       == newEntryDf['DVD']).values
        #     check3 = (self.index.loc[i, 'VideoName'] == newEntryDf['VideoName']).values
        #     # print(check1)
        #     # print(check2)
        #     # print(check3)
        #     # exit()
        #     if check1 and check2 and check3:
        #         # If duplicate, return duplicate entry index
        #         return i

        # If not duplicate
        return -1


    def make_backup(self):
        '''
            Moves any index files in destination folder to a backup folder.
        '''
        # Create backup folder
        dirs.create_folder(self.path.parent / self.bkpFolderName)

        # print(str(self.path.parent.resolve()) + "\\*index*.csv")
        # existingIndex = glob((str(self.path.parent.resolve()) + "\\*index*.csv").strip())

        existingIndex = self.path.parent.glob("*index*.csv")
        for entry in existingIndex:
            entry = Path(entry)
            newPath = self.path.parent / self.bkpFolderName / entry.name
            # print(entry)
            # input()

            # Check if dest path already exists
            # If True, create a new path by appending a number at the end
            fileIndex = 2
            while newPath.is_file():
                newPath = self.path.parent / self.bkpFolderName / (entry.stem + "_" + str(fileIndex) + entry.suffix)
                fileIndex += 1

            os.rename(entry, newPath)



    def write_index(self, auto_path=True):
        '''
            Create a backup of old index and write current index DataFrame to a csv file.
            auto_path == True appends date and time to index path
        '''
        # Create destination folder
        dirs.create_folder(self.path.parent)

        self.make_backup()

        if auto_path == True:
            # Get date and time for index name
            date = datetime.now()
            newName = str(self.path.stem) +"_{}-{}-{}_{}-{}-{}".format(date.year, date.month,\
             date.day, date.hour, date.minute, date.second)

            self.indexPath = self.path.with_name( newName + str(self.path.suffix))
        else:
            self.indexPath = self.path

        # print(self.indexPath)
        # print(self.index)

        self.index.to_csv(self.indexPath, index=False)
