#!/usr/bin/python

## @restructure_data.py
#  This file contains methods needed to correctly reformat input data.

## Class: Restructure_Data, explicitly inherit 'new-style class
#
#  Note: this class is invoked within 'views.py'
class Restructure_Data(object):

    ## constructor
    def __init__(self, settings, files=None):
        self.settings   = settings
        self.files      = files
        self.list_error = []

    ## restructure: restructure input data
    def restructure(self):

        # local variables
        formatted_settings = {}
        formatted_files    = []

        # restructure settings
        try:
            for key, value in self.settings.items():
                for lvalue in self.settings.getlist(key):
                    if key.lower() in formatted_settings:
                        # base case
                        if type(formatted_settings[key.lower()]) == unicode:
                            formatted_settings[key.lower()] = [formatted_settings[key.lower()]]
                            formatted_settings[key.lower()].append(lvalue)
                        # step case
                        elif type(formatted_settings[key.lower()]) == list:
                            formatted_settings[key.lower()].append(lvalue)
                    formatted_settings[key.lower()] = lvalue.lower()
        except Exception as error:
            self.list_error.append(error)
            return {'data': None, 'error': self.list_error}

        # restructure files: not all sessions involve files
        if self.files:
            try:
                for file in self.files.getlist('svm_dataset[]'):
                    formatted_files.append({'filename': file.filename, 'file': file})

                dataset = {'upload_quantity': len(self.files.getlist('svm_dataset[]')), 'file_upload': formatted_files}
            except Exception as error:
                self.list_error.append(error)
                return {'data': None, 'error': self.list_error}

        else: dataset = None

        # build input structure
        data = {'settings': formatted_settings, 'dataset': dataset}
 
        # return new structured data
        return {'data': data, 'error': None}

    ## get_errors: returns all errors corresponding to this class instance
    def get_errors(self):
        if len(self.list_error) > 0: return {'error': self.list_error}
        else: return {'error': None}
