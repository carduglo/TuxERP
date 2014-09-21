from distutils.core import setup
import py2exe, sys, os
import sqlite3
import ttk
from Tkinter import *
import subprocess
 
modulos = [sys.argv[1]]
sys.argv[1]="py2exe"
 
opcoes = {}
opcoes['py2exe'] = {}
opcoes['py2exe']['excludes'] = ["pywin", "pywin.debugger",
                                  "pywin.debugger.dbgcon", "pywin.dialogs",
                                  "pywin.dialogs.list"]
opcoes['py2exe']['packages'] = ["encodings"]
 
descricao = 'Programa'
versao = '1.0'
 
setup(name=descricao, console=modulos, zipfile="lib/shared.zip",
         description=descricao, version=versao)
