import libs.dirs    as dirs
import pandas       as pd
from pathlib        import Path


class IndexManager:
    def __init__(self, path=dirs.index):
        self.path        = Path(path)
        self.indexExists = False

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
            newEntry: Dict of lists. Keys are data columns, values are lists containing
                      the data
        '''
        if self.indexExists == True:
            # Append to existing df
            newEntryDf = pd.DataFrame.from_dict(newEntry)
            # print("New entry DF:")
            # print(newEntryDf)
            print("Columns newEntry:")
            for col in newEntryDf.columns:
                print(col)
            print("\nColumns index:")
            for col in self.index.columns:
                print(col)
            # input()
            self.index = self.index.append(newEntryDf, sort=False, ignore_index=False).reset_index(drop=True)
        else:
            # create df with new entry and write to disk as the index file
            self.index = pd.DataFrame.from_dict(newEntry)
            self.indexExists = True

        self.index.to_csv(self.path, index=False)
