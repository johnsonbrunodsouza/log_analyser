import json
from collections import namedtuple
from datetime import datetime,time
import logging
import sys
import re
import os

START_STRING = 'start_string'
END_STRING = 'end_string'
FIELDS_TO_EXTRACT = 'fields_to_extract'

class log_analyser:
    def __init__(self,configuration_file):
        self._config = log_analyser.load_configurations(configuration_file)
        self._files_to_analyze = []

    def setup(self):
        """
        
        Parameters:

        Returns:

        """
        for path in self._config.data_files_directory:
            for log_file in os.listdir(path):
                self._files_to_analyze.append(os.path.join(path,log_file))

    @staticmethod
    def load_configurations(config_file):
        """
        Loads application configuration 
        
        Parameters:
        config_file(str): Path of application configuration file

        Returns:
        config: configurations
        """

        def json2class(c_dict):
            return namedtuple('config',c_dict.keys())(*c_dict.values())

        with open(config_file) as c_file:
            json_file_str = ''.join(c_file.readlines())

        config = json.loads(json_file_str,object_hook=json2class)
        return config
    
    @staticmethod
    def help():
        """
        
        
        Parameters:

        Returns:
        """
        return "Usage: python log_generator.py configuration.json"

    def main(self):
        """
        
        
        Parameters:

        Returns:
        """

        self.setup()
        for seach_text_dict in self._config.Search_parameters:
            print(seach_text_dict)

            if len(seach_text_dict) == 3:
                self.get_start_end_time_with_additional_fields(seach_text_dict[0],seach_text_dict[1],log_file,seach_text_dict[2])
                pass ## call 
            elif len(seach_text_dict) == 2:
                for log_file in self._files_to_analyze:
                    #self.get_transformation_time(seach_text_dict[START_STRING],seach_text_dict[END_STRING],log_file)
                    self.get_start_end_time(seach_text_dict[0],seach_text_dict[1],log_file)
            

    def get_start_end_time(self,start_string,end_string,file_name):
        """
        
        
        Parameters:

        Returns:
        """
        found_start_string = False

        with open(file_name) as f: 
            for line in f:
                if start_string.upper() in line.upper():
                    if re.match(r"\d{4}-\d{2}-\d{2}",line):
                        st1=line.split(" :")[0]
                        found_start_string = True
                        logging.info(file_name + "|" + line)
                if end_string.upper() in line.upper():
                    if re.match(r"\d{4}-\d{2}-\d{2}",line):
                        st2=line.split(" :")[0]
                        if found_start_string:
                            d1=datetime.strptime(st1,"%Y-%m-%d %H:%M:%S")
                            d2=datetime.strptime(st2,"%Y-%m-%d %H:%M:%S")
                            logging.info(file_name + "|" + line)
                            logging.info("Time taken" + str(d2-d1))
                            found_start_string = False

    def get_start_end_time_with_additional_fields(self,start_string,end_string,file_name,fields_to_extract):
        """
        
        
        Parameters:

        Returns:
        """
        found_start_string = False
        found_end_string = False
        additional_field_values = {}

        with open( file_name) as f: 
            for line in f:
                if start_string.upper() in line.upper():
                    if re.match(r"\d{4}-\d{2}-\d{2}",line):
                        st1=line.split(" :")[0]
                        found_start_string = True
                        logging.info(file_name + "|" + line)
                if end_string.upper() in line.upper():
                    if found_start_string:
                        found_end_string = True
                
                if found_end_string:
                    for item in fields_to_extract:
                        if item in line:
                            additional_field_values[item] = line

                if found_end_string and len(additional_field_values) == len(fields_to_extract):
                    if re.match(r"\d{4}-\d{2}-\d{2}",line):
                        st2=line.split(" :")[0]
                        d1=datetime.strptime(st1,"%Y-%m-%d %H:%M:%S")
                        d2=datetime.strptime(st2,"%Y-%m-%d %H:%M:%S")
                        logging.info(file_name + "|" + line)
                        logging.info("Time taken" + str(d2-d1))
                        for key,value in additional_field_values.items():
                            logging.info(key + ":->" + value)
                        found_start_string = False
                        found_end_string = False

if __name__ == "__main__":
    logging.basicConfig(filename='log_analyser.log',level=logging.INFO,format='%(asctime)s %(message)s')
    logging.info("********************************************")
    start = time()

    if len(sys.argv) != 2:
        print(help())
        exit(1)

    log_analyser = log_analyser(sys.argv[1])
    log_analyser.main()