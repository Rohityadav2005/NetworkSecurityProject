import sys
from networksecurity.loggings import loggers

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()
        
        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "The error file name is [{0}],the error line number is [{1}] the error message is [{2}]".format(self.filename,self.lineno,self.error_message)
    
if __name__ == '__main__':
            try:
                a = 1/0
                print('This will not be printed',a)
            except Exception as e:
                raise NetworkSecurityException(e,sys)
        