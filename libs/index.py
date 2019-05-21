import os
import pandas       as pd
import numpy        as np
from   datetime     import datetime
from   pathlib      import Path
from   glob         import glob

import libs.dirs    as dirs


class IndexManager:
    def __init__(self, path=dirs.index):
        self.path               = Path(path)
        self.indexExists        = False
        self.bkpFolderName      = "index_backup"

        self.duplicates_count   = 0
        self.new_entries_count  = 0
        self.originalLen        = 0

        self.validate_path()


    def validate_path(self):
        if self.path.suffix == ".csv":
            # Check for csv files matching filename in self.path
            pathList = list(self.path.parent.glob("*"+str(self.path.stem).strip()+"*.csv"))

            if len(pathList) > 0:
                try:
                    # Check if index DataFrame exists and is non-empty
                    self.index = pd.read_csv(pathList[0])
                    self.originalLen = self.index.shape[0]

                    if self.originalLen > 0:
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
        self.newEntryDf = pd.DataFrame.from_dict(newEntry)

        # Save new frame path as FramePath and the old one as OriginalFramePath
        newFramePath = "--".join([self.newEntryDf.loc[0, 'Report'], 'DVD-'+str(self.newEntryDf.loc[0, 'DVD']), self.newEntryDf.loc[0, 'FrameName']])
        self.newEntryDf['OriginalFramePath'] = self.newEntryDf['FramePath']
        self.newEntryDf['FramePath'] = newFramePath
        # print(self.newEntryDf)
        # input()

        if self.indexExists == True:
            # Append to existing df
            self.index = self.index.append(self.newEntryDf, sort=False, ignore_index=False).reset_index(drop=True)
            self.check_duplicates()
        else:
            # Create df with new entry and write to disk as the index file
            self.index = self.newEntryDf.copy()
            self.indexExists = True


    def check_duplicates(self):
        '''
            Check for duplicated index entries.

            Duplicate criteria:
                Same Report, DVD and FrameName field.

        '''
        # check1     = self.index.duplicated(['Report'], keep=False)
        # check2     = self.index.duplicated(['DVD'], keep=False)
        # check3          = self.index.duplicated(['FrameName'], keep=False)
        check3      = np.equal(self.index['FrameName'], self.newEntryDf['FrameName'])
        # print(check3)
        # input()

        # truthArray = np.array([check1, check2, check3]).T
        truthArray      = np.array([check3]).T

        mask            = np.all(truthArray, axis=1)
        dupNamesIndex   = np.squeeze(np.argwhere(mask == True))
        print("Duplicate Names: ", dupNamesIndex)


        try:   # Dirty exception escape
            len(dupNamesIndex)
        except TypeError:
            print("Index vector broke. Probably no duplicates.")
            return -1

        if len(dupNamesIndex) > 1:
            dupIndex = []
            for i in dupNamesIndex:
                # Check if other relevant fields are also duplicates
                reportCheck = np.squeeze(self.index.loc[i, 'Report'] == self.newEntryDf['Report'])
                dvdCheck    = np.squeeze(self.index.loc[i, 'DVD'] == self.newEntryDf['DVD'])
                print("reportCheck: ", reportCheck)
                print("dvdCheck: ", dvdCheck)
                print("logical: ", reportCheck and dvdCheck)

                if reportCheck and dvdCheck:
                    dupIndex.append(i)

            print("Duplicate Indexes: ", dupIndex)
            if len(dupIndex) > 1:   # Entry is duplicate
                input()
                if len(dupIndex) > 2:
                    raise ValueError("Found multiple duplicate entries. Duplicate check should only and always be run following a new addition.")
                else:
                    self.duplicates_count += len(dupIndex)-1
                    baseIndex   = dupIndex[0]
                    newIndex    = dupIndex[1]
                    # reportCheck = self.index.loc[baseIndex, 'Report'] == self.index.loc[newIndex, 'Report']
                    # dvdCheck    = self.index.loc[baseIndex, 'DVD'] == self.index.loc[newIndex, 'DVD']
                    # if reportCheck and dvdCheck:
                    print("i: ", newIndex)
                    print("Existing entry: ",   self.index.loc[[baseIndex]])
                    print("New entry: ",        self.newEntryDf)
                    # print("Existing entry: ",   self.index.loc[[baseIndex]].drop(['FrameTime', 'OriginalDataset'], axis=1))
                    # print("New entry: ",        self.newEntryDf.drop(['FrameTime', 'OriginalDataset'], axis=1))
                    input()

                    # Get duplicate and existing Tags list
                    newTags     = self.index.loc[baseIndex, 'Tags'].split("-")
                    newTags.extend(self.index.loc[newIndex, 'Tags'].split("-"))

                    # Get duplicate and existing OriginalDataset list
                    newDataset  = self.index.loc[baseIndex, 'OriginalDataset'].split("-")
                    newDataset.extend(self.index.loc[newIndex, 'OriginalDataset'].split("-"))

                    # Get unique tags and OriginalDataset
                    newTags    = list(dict.fromkeys(newTags))
                    newDataset = list(dict.fromkeys(newDataset))

                    # Save new fields with "-" as separator
                    self.index.loc[baseIndex, 'Tags'] = "-".join(newTags)
                    self.index.loc[baseIndex, 'OriginalDataset'] = "-".join(newDataset)

                    # Drop duplicate entry
                    self.index = self.index.drop(dupIndex[1]).reset_index(drop=True)

            else: # Entry is actually not duplicate
                self.new_entries_count += 1
        else:   # No duplicate candidates
            self.new_entries_count += 1


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
        self.report_changes()

    def report_changes(self):
        print(self.originalLen)
        print(self.index.shape[0])
        print("Original Index had {} entries.\nNew Index has {} entries.".format(self.originalLen, self.index.shape[0]))

        print("\nProcessed {} entries. Added {} and merged {} duplicates.\nSaved index to \n{}\
                        \n".format(self.new_entries_count+self.duplicates_count,
                            self.new_entries_count, self.duplicates_count,
                            self.indexPath))


    def get_unique_tags(self):
        self.tagList = []
        f = lambda x: self.tagList.extend(x.split('-'))

        self.index['Tags'].apply(f)
        self.tagList = list(dict.fromkeys(self.tagList))

        return self.tagList
