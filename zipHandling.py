# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 21:35:38 2023

@author: dforc
"""


import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout


'''Zip'''
class ZipCodeDialog(QDialog):    
    
    
    ## Initializes ZipCode GUI
    def __init__(self):
        super().__init__()
        self.zipCode = ""                                       ## Zip Init
        self.setWindowTitle("Zip Code Entry")                   ## Window Title
        self.zip_label = QLabel("Enter Your 5 Digit Zip Code")  ## Prompt Label
        self.zip_entry = QLineEdit()
        self.submit_button = QPushButton("Submit")              ## Button Label
        self.submit_button.clicked.connect(self.onSubmit)      ## Click Condit
        layout = QVBoxLayout()                                  ## Box Layout
        layout.addWidget(self.zip_label)
        layout.addWidget(self.zip_entry)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)
        
    
    ## Checks Proper Zip Code
    def checkZip(self, zipCode):
        
        if len(zipCode) != 5:
            return False
        if not zipCode.isdigit():
            return False
        
        return True
    

    ## Checks Zip Code and Closes GUI if Correct
    def onSubmit(self):
        
        zipCode = self.zip_entry.text()
        if self.checkZip(zipCode):
            self.zipCode = zipCode
            self.accept()
            
        ## If Zip is Invalid    
        else:
            ## Resets Text Field
            self.zip_entry.setText("")    
            ## Displays Invalid Zip Code Text
            self.zip_entry.setPlaceholderText("Invalid zip code")



app = QApplication(sys.argv)
dialog = ZipCodeDialog()
dialog.exec_()
zipCode = dialog.zipCode