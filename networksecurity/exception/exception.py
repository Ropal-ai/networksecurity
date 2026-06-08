import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message

        _, _, ext_tb = error_details.exc_info()
        self.filename = ext_tb.tb_frame.f_code.co_filename
        self.lineno = ext_tb.tb_lineno

    def __str__(self):
        return (
            "Error occured in python script name [{0}] line number [{1}] error message [{2}]"
            .format(self.filename, self.lineno, str(self.error_message))
        )

