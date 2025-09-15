#!/usr/bin/python3
"""
Initialization file for models package
Creates a unique FileStorage instance
"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
