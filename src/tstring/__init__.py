import importlib.metadata 
import logging
tstring_logger = logging.getLogger(__name__)

__version__ =  importlib.metadata.version('tstring-util')

from tstring.interpolation import iformat 
from tstring.lazy import render
from tstring.cpath import path
from tstring.safe_split import safe_split 

