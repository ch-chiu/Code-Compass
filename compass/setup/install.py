#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

if __name__ == '__main__':
    # Map: Code-Developer
    os.system("sudo apt-get install clang -y")
    os.system("sudo apt-get install python-pip -y")
    os.system("sudo apt-get install python-dev -y")
    os.system("sudo apt-get install build-essential -y")
    os.system("sudo pip install --upgrade pip")
    os.system("sudo pip install --upgrade virtualenv")
    os.system("sudo pip install graphviz")
    # Map: Code-Structure
    os.system("sudo pip install gensim")
    os.system("sudo pip install nltk")
    # Web Service
    os.system("sudo pip install flask")
