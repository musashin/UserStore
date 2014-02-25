import os
import datetime
import pickle
from prettytable.prettytable import *
import textwrap

_max_history = 3
_store_path = r'./.store'

class UserStore(object):

    def __init__(self, operator_name):
        """
        #TODO

        """
        self.operator_name = operator_name
        self.test_history = list()


        try:
            if not os.path.exists(self.get_store_file_directory()):
                os.makedirs(self.get_store_file_directory())

        except BaseException as e:
            #TODO
            print str(e)


    def add_test(self, script_file, log_file, script_result):
        """
        #TODO

        """

        #remove entry for same script name
        try:
            self.test_history = [test for test in self.test_history if not test['script']==script_file]
        except:
            pass

        self.test_history.append({'timestamp': datetime.datetime.now(), 'script': script_file, 'log': log_file, 'result': script_result})

        list.sort(self.test_history, key=lambda test: test['timestamp'], reverse=True)

        self.test_history = self.test_history[0:_max_history]


    def get_store_file_path(self):
        #TODO
        return os.path.join(self.get_store_file_directory(), self.operator_name + '.bin')


    def get_store_file_directory(self):
        #TODO
        return os.path.join(os.path.dirname(__file__), _store_path)

    def save(self):
        #TODO
        try:
            store_file = open(self.get_store_file_path(), 'wb+')

            pickle.dump(self.test_history, store_file)

        except BaseException as e:
            print str(e)

    def print_history(self,max_history=6):
        
        table = PrettyTable(field_names=('index',
                                         'time',
                                         'script',
                                         'script directory',
                                         'result'))
        index = 0
        
        for test in self.test_history:
            table.add_row([index,test['timestamp'],
                                 repr(os.path.basename(test['script'])),
                                 repr(os.path.dirname(test['script'])),
                                 test['result']])
            index += 1
            
        print table

if __name__ == '__main__':

    import time

    store = UserStore('Nico')

    store.add_test('C:/temp/X.txt','mylogg','PASS')

    time.sleep(2)

    store.add_test('C:/temp/Y.txt','mylogg','PASS')

    time.sleep(2)

    store.add_test('C:/temp/YW.txt','mylogg','PASS')

    time.sleep(2)

    store.add_test('C:/temp/tata.txt','mylogg','PASS')

    import time

    time.sleep(2)

    store.add_test('C:/temp/toto.txt','mylogg','PASS')

    store.save()

    store.print_history()



