"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DND4E/MODELS/MODELS.py
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import random
from django.conf import settings

import common.utility as CU

import logging
prog_lg = logging.getLogger('progress')
excp_lg = logging.getLogger('exception')



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MODELS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def context_background(request):
    path = request.path

    if "dnd4e" in path:                                         
        imgFolder = os.path.join(settings.BASE_DIR, "dnd4e/static/images/backgrounds/")
        fileNames = CU.GetFileNames(imgFolder)
        fileName = random.choice(fileNames)
        #prog_lg.debug(fileName)
        bkgdPath = "/static/images/backgrounds/{}".format(fileName)    

    else:
        bkgdPath = None
    
    xcontext = {
        'bkgdPath': bkgdPath,
    }
    return xcontext



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
END OF FILE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""