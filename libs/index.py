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
            pathList = list(self.path.parent.glob("*"+str(self.path.stem).strip()+"*.csv"))

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

            self.index = self.index.append(newEntryDf, sort=False, ignore_index=False).reset_index(drop=True)
            self.check_duplicates()
        else:
            # Create df with new entry and write to disk as the index file
            self.index = pd.DataFrame.from_dict(newEntry)
            self.indexExists = True


    def check_duplicates(self):
        '''
            Check for duplicated index entries

            Duplicate criteria:
                Same Report, DVD and FrameName field.

        '''
        check1     = self.index.duplicated(['Report'], keep=False)
        check2     = self.index.duplicated(['DVD'], keep=False)
        check3     = self.index.duplicated(['FrameName'], keep=False)

        truthArray = np.array([check1, check2, check3]).T
        mask       = np.all(truthArray, axis=1)
        dupIndex   = np.squeeze(np.argwhere(mask == True))

        print("Duplicate Indexes: ", dupIndex)

        try:   # Dirty exception escape
            len(dupIndex)
        except TypeError:
            print("Index vector broke. Probably no duplicates.")
            return -1

        if len(dupIndex) > 0:
            newTags     = self.index.loc[dupIndex[0], 'Tags'].split("-")
            newDataset  = self.index.loc[dupIndex[0], 'OriginalDataset'].split("-")
            for i in dupIndex[-1:-1:1]:
                print("i: ", i)
                print(self.index)
                # Join duplicate and existing Tags fields
                newTags.extend(self.index.loc[i, 'Tags'].split("-"))
                # Join duplicate and existing OriginalDataset fields
                newDataset.extend(self.index.loc[i, 'OriginalDataset'].split("-"))

            # Get unique tags
            newTags = list(dict.fromkeys(newTags))
            # Save new Tag field with "-" as separator
            self.index.loc[dupIndex[0], 'Tags'] = "-".join(newTags)
            self.index.loc[dupIndex[0], 'OriginalDataset'] = "-".join(newDataset)

            # Drop duplicate entries
            self.index = self.index.drop(dupIndex).reset_index(drop=True)


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

    def get_unique_tags(self):
        self.tagList = []
        f = lambda x: self.tagList.extend(x.split('-'))

        self.index['Tags'].apply(f)
        self.tagList = list(dict.fromkeys(self.tagList))

        return self.tagList
