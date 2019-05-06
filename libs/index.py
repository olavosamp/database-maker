import os
import pandas       as pd
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
            if self.path.exists() == True:
                try:
                    # Check if index DataFrame exists and is non-empty
                    self.index = pd.read_csv(self.path)
                    # print(self.index)
                    # input()
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
        else:
            # create df with new entry and write to disk as the index file
            self.index = pd.DataFrame.from_dict(newEntry)
            self.indexExists = True


    def make_backup(self):
        '''
            Moves any index files in destination folder to a backup folder.
        '''
        # Create backup folder
        dirs.create_folder(self.path.parent / self.bkpFolderName)

        existingIndex = glob(str(self.path.parent / "*index*.csv"))
        for entry in existingIndex:
            entry = Path(entry)
            newPath = self.path.parent / self.bkpFolderName / entry.name

            # Check if dest path already exists
            # If True, create a new path by appending a number at the end
            fileIndex = 2
            while newPath.is_file():
                newPath = self.path.parent / self.bkpFolderName / (entry.stem + "_" + str(fileIndex) + entry.suffix)
                fileIndex += 1

            os.rename(entry, newPath)


    def write_index(self, auto_path=True):
        '''
            Writes current index DataFrame to a csv file.
        '''
        # Create destination folder
        dirs.create_folder(self.path.parent)

        self.make_backup()
        self.index.to_csv(self.path, index=False)
