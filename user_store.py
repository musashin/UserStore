import os
import datetime
import pickle
from prettytable.prettytable import *
import textwrap

_max_history = 3
_store_path = r'./.store'

class UserStore(object):
    """
    Purpose:
        A class to store operator test history.

    Additionally, this class permits:
        - Printing history in human readable format.
        - Exporting/Import History.
    """

    def __init__(self, operator_name):
        """
        Purpose:
            Initialize user history instance

        Parameters:
            operator_name: string used to identify the test operator

        Implementation:
            1. Create the directory used to store data if required.
            2. Load user history.

        """
        self.operator_name = operator_name
        self.test_history = list()

        try:
            if not os.path.exists(self.get_store_file_directory()):
                os.makedirs(self.get_store_file_directory())

        except BaseException as e:
            #TODO
            print 'Cannot create directory {0!s} [{1!s}]'.format(self.get_store_file_directory(), str(e))

        self.load()

    def add_test(self, script_file, log_file, script_result):
        """
        Purpose:
            Add a new test to the user history and save the data.

        Parameters:
            - script_file: fully qualified file to the script file.
            - log_file: fully qualified path to the log file
            - script_result: string identifying the script result.

        Implementation:
            1. Remove any existing test with exact same script from history.
            2. Add new test to history.
            3. Reorder history with the more recent test first.
            4. Limit history size to max_history.
            5. Save the new history.

        """

        try:
            #remove entry for same script name
            self.test_history = [test for test in self.test_history if not test['script']==script_file]

            self.test_history.append({'timestamp': datetime.datetime.now(), 'script': script_file, 'log': log_file, 'result': script_result})

            list.sort(self.test_history, key=lambda test_entry: test_entry['timestamp'], reverse=True)

            self.test_history = self.test_history[0:_max_history]

            self.save()

        except BaseException as e:
            #TODO
            print 'Cannot add test to history [{0!s}]'.format(str(e))

    def get_test(self, test_index):

        try:

            test_entry = self.test_history[test_index]
            return test_entry['script'], test_entry['log']

        except:
            #TODO
            print 'Cannot retrieve test from history: no test at index {0!s}'.format(test_index)


    def get_store_file_path(self):
        return os.path.join(self.get_store_file_directory(), self.operator_name + '.bin')

    @staticmethod
    def get_store_file_directory():
        return os.path.join(os.path.dirname(__file__), _store_path)

    def save(self, directory=None):
        #TODO

        try:

            file_name = os.path.join(directory, self.operator_name + '.bin') if directory else self.get_store_file_path()

            with open(file_name, 'wb+') as store_file:

                pickle.dump(self.test_history, store_file)

        except BaseException as e:
            print 'Cannot save history [{0!s}]'.format(str(e)) #TODO

    def load(self, file=None):

        #TODO
        try:

            loaded_file = file if file else self.get_store_file_path()

            with open(loaded_file, 'rb') as store_file:

                self.test_history.extend(pickle.load(store_file))

                #remove duplicates
                self.test_history = [entry for (index, entry) in enumerate(self.test_history) if entry not in self.test_history[index+1:]]

                #sort
                list.sort(self.test_history, key=lambda test_entry: test_entry['timestamp'], reverse=True)

                #limit size
                self.test_history = self.test_history[0:_max_history]

        except BaseException as e:
            print 'Cannot load history [{0!s}]'.format(str(e)) #TODO




    def print_history(self, max_history=None):
        
        table = PrettyTable(field_names=('index',
                                         'time',
                                         'script',
                                         'script directory',
                                         'result'))
        index = len(self.test_history[0:max_history])-1
        
        for test in reversed(self.test_history[0:max_history]):
            table.add_row([index, '\n'.join(textwrap.wrap(test['timestamp'].strftime('%m/%d/%y-%H:%M'), 16)),
                                  '\n'.join(textwrap.wrap(repr(os.path.basename(test['script'])), 16)),
                                  '\n'.join(textwrap.wrap(repr(os.path.dirname(test['script'])), 60)),
                                  '\n'.join(textwrap.wrap(test['result'], 16))])
            index -= 1
            
        print table

    def export(self):

        import Tkinter,tkFileDialog

        root = Tkinter.Tk()
        root.withdraw()

        export_directory = tkFileDialog.askdirectory()

        if export_directory:
            try:
                self.save(export_directory)
            except BaseException as e:
                 #TODO
                 print 'Cannot save file in directory {0!s} [{1!s}]'.format(export_directory, e)

    def import_store(self):

        import Tkinter,tkFileDialog

        root = Tkinter.Tk()
        root.withdraw()

        file_to_import = tkFileDialog.askopenfilename()

        if file_to_import:
            try:
                self.load(file_to_import)
            except BaseException as e:
                 #TODO
                 print 'Cannot load file {0!s} [{1!s}]'.format(file_to_import, e)


###################### New Stuff #########################################################

    @staticmethod
    def store_exist(operator_name):
        """
        Purpose:
            return TRUE if a store exist for this operator,FALSE otherwise.

        Parameters:
            operator_name: string used to identify the test operator

        """
        return os.path.isfile(os.path.join(os.path.join(os.path.dirname(__file__), _store_path),
                                            operator_name + '.bin'))

    @staticmethod
    def get_similar_operators(operator_name):
        """
        Purpose:
            Get a list of operator names with similar names that already have s tore

        Parameters:
            operator_name: string used to identify the test operator.

        Implementation:
            1. Get a list of store files.
            2. Use get_close_matches() to determine which file are closed enougth to the queried operator name,
            and return it

        """

        from os import listdir
        from os.path import isfile, join
        from difflib import get_close_matches


        files = [f for f in listdir(os.path.join(os.path.dirname(__file__), _store_path))
                 if isfile(join(os.path.join(os.path.dirname(__file__), _store_path), f))]


        return get_close_matches(operator_name, [os.path.splitext(name)[0] for name in files], cutoff=0.8)


if __name__ == '__main__':

    print UserStore.store_exist('ulysse ')

    print UserStore.get_similar_operators('N. ulysse')




