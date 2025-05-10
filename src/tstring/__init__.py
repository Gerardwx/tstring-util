import importlib.metadata 
import logging
tstring_logger = logging.getLogger(__name__)

__version__ =  importlib.metadata.version('tstring-util')
from tstring.lazy import render

