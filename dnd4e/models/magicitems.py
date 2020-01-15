"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DND4E/MODELS/MAGICITEMS.py
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import csv
from collections import OrderedDict
from random import randint

from django.db import models
from django.db.models import Count, F, Q 

import common.utility as CU

import logging
prog_lg = logging.getLogger('progress')
excp_lg = logging.getLogger('exception')


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MODEL DECLARATIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class MagicItem(models.Model):
    Name = models.TextField()
    Slot = models.TextField()
    SubSlot = models.TextField()
    Level = models.IntegerField(default=0)
    Book = models.TextField(null=True)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MAGIC ITEM METHODS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Reporter(object):
    
    
    @staticmethod
    def GetTableData():
        
        results = []
        
        newRow = OrderedDict()
        newRow['Table'] = "MagicItem"
        newRow['Count'] = MagicItem.objects.all().count()
        results.append(newRow)
        
        return results
        
        
    @staticmethod
    def GetRandomItem(p_level):
        
        levelMin = int(p_level) -2
        levelMax = int(p_level) +2
        item_mdls = MagicItem.objects.filter(Level__gte=levelMin, Level__lte=levelMax)
        
        levelItems = []
        for item_m in item_mdls:
            newRow = OrderedDict()
            newRow['Name'] = item_m.Name
            newRow['Slot'] = item_m.Slot
            newRow['SubSlot'] = item_m.SubSlot
            newRow['Level'] = item_m.Level
            newRow['Book'] = item_m.Book
            levelItems.append(newRow)
        
        rolledIndex = randint(0, len(levelItems)-1)
        
        colFormat = OrderedDict()
        colFormat['Level'] = 'format_center'        
        
        record = {
            'data': levelItems,
            'colFormat': {'level': 'format_center', 'book': 'format_fixline'},
            'rolledIndex': rolledIndex,
        }
        
        hret = CU.HttpReturn()
        hret.results = record
        hret.status = 201
        return hret


class Editor(object):
    
    
    @staticmethod
    def DeleteTables():
        magics = MagicItem.objects.all().delete()[0]
        results = "Magics Deleted: " + str(magics)
        return results
    
    
    @staticmethod
    def LoadTables():
        
        path = "dnd4e/static/data/magicitems.csv"
        with open(path) as fhandle:
            reader = csv.reader(fhandle)
            next(reader)  # skip header row
            for row in reader:
                if not row[3]:
                    continue
                levels = row[3].strip().split()     # splits on whitespace by default
                for level in levels:
                    created = MagicItem.objects.get_or_create(
                        Name = row[0].title(),
                        Slot = row[1].title(),
                        SubSlot = row[2].title(),
                        Level = level,
                        Book = row[4],
                    )
        
        return "Magic Items Loaded."


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
END OF FILE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""