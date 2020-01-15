"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DND4E/MODELS/MONSTERS.py
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import csv
from collections import OrderedDict
import re
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


class Monsters(models.Model):
    Race = models.TextField()
    SubRace = models.TextField()
    Book = models.TextField()
    Origin = models.TextField()
    Type = models.TextField()
    Keyword = models.TextField()
    Level = models.IntegerField(default=0)
    Class = models.TextField()
    Threat = models.TextField()
    Habitat = models.TextField()
    Social = models.TextField()
    AllyGroups = models.TextField()


class LevelXP(models.Model):
    Level = models.IntegerField()
    XPAward = models.IntegerField()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MONSTERS REPORTER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Reporter(object):
    
    
    @staticmethod
    def GetTableData():
        
        results = []
        
        newRow = OrderedDict()
        newRow['Table'] = "Monsters"
        newRow['Count'] = Monsters.objects.all().count()
        results.append(newRow)
        
        newRow = OrderedDict()
        newRow['Table'] = "Level-XP"
        newRow['Count'] = LevelXP.objects.all().count()
        results.append(newRow)
        
        return results

    
    @staticmethod
    def MonsterCount():
        monstCnt = Monsters.objects.all().count()
        return monstCnt
    
    
    @staticmethod
    def CountsByRole():
        
        monst_q = Monsters.objects.values_list('Class').annotate(cnt=Count('id'))
        byrole_dx = dict(monst_q)
        monstCnt = Reporter.MonsterCount()
        
        order_dx = OrderedDict()
        order_dx['Skirmisher'] = "{0:.1f}".format(byrole_dx['Skirmisher'] / monstCnt * 100) + "%"
        order_dx['Lurker'] = "{0:.1f}".format(byrole_dx['Lurker'] / monstCnt * 100) + "%"
        order_dx['Soldier'] = "{0:.1f}".format(byrole_dx['Soldier'] / monstCnt * 100) + "%"
        order_dx['Brute'] = "{0:.1f}".format(byrole_dx['Brute'] / monstCnt * 100) + "%"
        order_dx['Controller'] = "{0:.1f}".format(byrole_dx['Controller'] / monstCnt * 100) + "%"
        order_dx['Artillery'] = "{0:.1f}".format(byrole_dx['Artillery'] / monstCnt * 100) + "%"
        
        return order_dx


    @staticmethod
    def CountsByLevel():
        monst_q = Monsters.objects.values_list('Level'
                    ).annotate(cnt=Count('id'))
        bylevel_dx = dict(monst_q)
        
        results = []
        for key, value in bylevel_dx.items():
            newRow = OrderedDict()
            newRow['Level'] = key
            newRow['Count'] = value
            results.append(newRow)
        
        colFormat = {}
        colFormat['level'] = 'format_center'
        colFormat['count'] = 'format_center'
        
        record = {
            'data': results,
            'colFormat': colFormat,
        }
        
        return record


    @staticmethod
    def RacesList():
        monst_q = Monsters.objects.values_list('Race').distinct()
        monstRaces = list(monst_q)
        
        results = []
        for race in monstRaces:
            
            raceName = race[0]
            
            race_mdls = Monsters.objects.filter(Race=raceName)
            
            newRow = OrderedDict()
            newRow['race'] = race[0]
            newRow['freq'] = len(race_mdls)
            newRow['levelRange'] = ""
            newRow['habitats'] = ""
            newRow['allyGroups'] = ""
            
            level_min = 99
            level_max = 0
            
            for entry_m in race_mdls:
                if entry_m.Level < level_min:
                    level_min = entry_m.Level
                if entry_m.Level > level_max:
                    level_max = entry_m.Level
                
                currHabs_ls = entry_m.Habitat.split(", ")
                for hab in currHabs_ls:
                    if hab not in newRow['habitats']:
                        newRow['habitats'] += hab + ", "
                
                currGroups_ls = entry_m.AllyGroups.split(", ")
                for group in currGroups_ls:
                    if group not in newRow['allyGroups']:
                        newRow['allyGroups'] += group + ", "
                
            level_ave = round((level_max+level_min)/2)
            newRow['levelRange'] = CU.Pad2(level_ave) + " (" + str(level_min) + "-" + str(level_max) + ")"
            newRow['habitats'] = newRow['habitats'][:-2]
            newRow['allyGroups'] = newRow['allyGroups'][:-2]
            results.append(newRow)
            
        colFormat = {}
        colFormat['freq'] = 'format_center'
        colFormat['levelRange'] = 'format_center'
        
        record = {
            'data': results,
            'colFormat': colFormat,
        }
        
        return record
    
    
    @staticmethod
    def AllyGroupsList():
        allies_q = Monsters.objects.values_list('AllyGroups', flat=True).distinct().order_by('AllyGroups')
        allies_raw = list(allies_q)
        
        allies_ls = []
        for allies in allies_raw:
            currAllies_ls = allies.split(", ")
            for ally in currAllies_ls:
                if ally and ally not in allies_ls:
                    allies_ls.append(ally) 
        
        allies_ls.sort()
        allies_ls.insert(0, "Any")
        
        return allies_ls
    
    
    @staticmethod
    def RandomDomainRace(habitat):
        
        
        hret = CU.HttpReturn()
        hret.results = None
        hret.status = 201
        return hret
    
    
    @staticmethod
    def GenerateEncounter(p_chars, p_level, p_habitat, p_allyGroup, p_origin, p_type, p_threat):
        
        levelMin = int(p_level) -2
        levelMax = int(p_level) +2
        
        prim_mdls = Monsters.objects.filter(Level__gte=levelMin, Level__lte=levelMax
                        ).filter(Habitat__contains=p_habitat
                        ).order_by('Race')
        
        if p_origin != 'Any':
            prim_mdls = prim_mdls.filter(Origin=p_origin)
        
        if p_type != 'Any':
            prim_mdls = prim_mdls.filter(Type=p_type)
        
        if p_threat != 'Any':
            prim_mdls = prim_mdls.filter(Threat=p_threat)
        
        if p_allyGroup != 'Any':
            prim_mdls = prim_mdls.filter(AllyGroups__contains=p_allyGroup)
        
        prim_dict = prim_mdls.values('Race', 'SubRace', 'Class', 'Level', 'Threat', 'Habitat', 'AllyGroups', 'Book'
                        ).filter(Level__gte=levelMin, Level__lte=levelMax
                        ).filter(Habitat__contains=p_habitat
                        ).order_by('Race')
        
        if len(prim_dict) > 0:
            rolledIndex = randint(0, len(prim_dict)-1)
            primary = prim_dict[rolledIndex]
        else:
            primary = {}
        
        if not primary:
            records = {
                'primary': primary,
            }
            hret = CU.HttpReturn()
            hret.results = records
            hret.status = 201
            return hret
     
        
        # get secondaries 
        
        levelMin = primary['Level'] -2
        levelMax = primary['Level'] +2
        
        if primary['Class'] in ['Lurker', 'Skirmisher']:
            excludeClass = ['Lurker', 'Skirmisher']
        elif primary['Class'] in ['Soldier', 'Brute']:
            excludeClass = ['Soldier', 'Brute']
        elif primary['Class'] in ['Controller', 'Artillery']:
            excludeClass = ['Controller', 'Artillery']
        
        allies_ls = primary['AllyGroups'].split(", ")
        regex = re.compile(r'_Civ')
        filter_ls = [i for i in allies_ls if not regex.search(i)]
        
        rolledIndex = randint(0, len(filter_ls)-1)
        allyRand = filter_ls[rolledIndex]
        if not allyRand: allyRand = "none"
        
        secRace_mdls = Monsters.objects.filter(Level__gte=levelMin, Level__lte=levelMax
                                    ).exclude(Class__in=excludeClass
                                    ).filter(Race=primary['Race'])
        
        secAlly_mdls = Monsters.objects.filter(Level__gte=levelMin, Level__lte=levelMax
                                    ).exclude(Class__in=excludeClass
                                    ).exclude(Race=primary['Race']
                                    ).filter(AllyGroups__contains=allyRand)
        
        secHabt_mdls = Monsters.objects.filter(Level__gte=levelMin, Level__lte=levelMax
                                    ).exclude(Class__in=excludeClass
                                    ).exclude(Race=primary['Race']
                                    ).filter(Habitat__contains=p_habitat)
        
        secRace_dict = secRace_mdls.values('Race', 'SubRace', 'Class', 'Level', 'Threat', 'Book')
        secAlly_dict = secAlly_mdls.values('Race', 'SubRace', 'Class', 'Level', 'Threat', 'Book')
        secHabt_dict = secHabt_mdls.values('Race', 'SubRace', 'Class', 'Level', 'Threat', 'Book')
        
        
        # create encounter groups
        
        levelXP = LevelXP.objects.filter(Level=p_level).values_list('XPAward', flat=True)[0]
        targetXP = int(p_chars) * levelXP
        levelXPn = LevelXP.objects.filter(Level=(int(p_level)+1)).values_list('XPAward', flat=True)[0]
        nextXP = int(p_chars) * levelXPn
        
        enc1_enc = Reporter.CreateEncGroup(primary, secRace_dict, p_level, targetXP, nextXP)
        enc2_enc = Reporter.CreateEncGroup(primary, secRace_dict, p_level, targetXP, nextXP)
        enc3_enc = Reporter.CreateEncGroup(primary, secAlly_dict, p_level, targetXP, nextXP)
        enc4_enc = Reporter.CreateEncGroup(primary, secAlly_dict, p_level, targetXP, nextXP)
        enc5_enc = Reporter.CreateEncGroup(primary, secHabt_dict, p_level, targetXP, nextXP)
        enc6_enc = Reporter.CreateEncGroup(primary, secHabt_dict, p_level, targetXP, nextXP)
        
        
        # format data structures to return
        
        primOrder_dict = []
        for currPrim in prim_dict:
            newRow = OrderedDict()
            newRow['Race'] = currPrim['Race']
            newRow['Class'] = currPrim['Class']
            newRow['Level'] = currPrim['Level']
            newRow['Threat'] = currPrim['Threat']
            newRow['Habitat'] = currPrim['Habitat']
            newRow['AllyGroups'] = currPrim['AllyGroups']
            primOrder_dict.append(newRow)
        
        secRace_ordc = []
        for currSec in secRace_dict:
            newRow = OrderedDict()
            newRow['Race'] = currSec['Race']
            newRow['Class'] = currSec['Class']
            newRow['Level'] = currSec['Level']
            newRow['Threat'] = currSec['Threat']
            secRace_ordc.append(newRow)
        
        secAlly_ordc = []
        for currSec in secAlly_dict:
            newRow = OrderedDict()
            newRow['Race'] = currSec['Race']
            newRow['Class'] = currSec['Class']
            newRow['Level'] = currSec['Level']
            newRow['Threat'] = currSec['Threat']
            secAlly_ordc.append(newRow)
        
        secHabt_ordc = []
        for currSec in secHabt_dict:
            newRow = OrderedDict()
            newRow['Race'] = currSec['Race']
            newRow['Class'] = currSec['Class']
            newRow['Level'] = currSec['Level']
            newRow['Threat'] = currSec['Threat']
            secHabt_ordc.append(newRow)
        
        records = {
            'targetXP': targetXP,
            'levelXP': levelXP,
            'primaries': primOrder_dict,
            'primary': primary,
            'secRace': secRace_ordc,
            'secAlly': secAlly_ordc,
            'secHabt': secHabt_ordc,
            'enc1': enc1_enc,
            'enc2': enc2_enc,
            'enc3': enc3_enc,
            'enc4': enc4_enc,
            'enc5': enc5_enc,
            'enc6': enc6_enc,
            'colFormat': {'Level': 'format_center'},
            'encColFormat': {'Quant': 'format_center'},
        }
        
        hret = CU.HttpReturn()
        hret.results = records
        hret.status = 201
        return hret
        
    
    # helper for GenerateEncounter
    @staticmethod
    def CreateEncGroup(p_primary, secTable_dict, p_level, targetXP, nextXP):
        
        prim_dx = p_primary.copy()
        prim_dx['Quant'] = 0
        
        if secTable_dict:
            rolledIndex = randint(0, len(secTable_dict)-1)
            sec_dx = secTable_dict[rolledIndex]
            sec_dx['Quant'] = 0
        else:
            sec_dx = None
        
        # add in priority order to encounter monster entries 
        
        encMonst_dict = []
        if prim_dx['Class'] in ['Soldier', 'Brute']:
            encMonst_dict.append(prim_dx)
        if sec_dx and sec_dx['Class'] in ['Lurker', 'Skirmisher']:
            encMonst_dict.append(sec_dx)
        if prim_dx['Class'] in ['Lurker', 'Skirmisher']:
            encMonst_dict.append(prim_dx)
        if sec_dx and sec_dx['Class'] in ['Soldier', 'Brute']:
            encMonst_dict.append(sec_dx)
        if prim_dx['Class'] in ['Controller', 'Artillery']:
            encMonst_dict.append(prim_dx)
        if sec_dx and sec_dx['Class'] in ['Controller', 'Artillery']:
            encMonst_dict.append(sec_dx)
        
        # increment quantities in order
        
        if randint(0, 1) == 1:
            encMonst_dict[0]['Quant'] = 1
        
        incr = 0
        while (Reporter.GetEncounterXP(encMonst_dict) < targetXP):
            currMonst = encMonst_dict[incr % len(encMonst_dict)]
            currMonst['Quant'] += 1
            incr += 1
            
        xpTotal = Reporter.GetEncounterXP(encMonst_dict)
        levelEff = int(p_level) + (xpTotal - targetXP) / (nextXP - targetXP)
        levelEff = str(round(levelEff, 2))

        results = {
            'monsters': encMonst_dict,
            'xpTotal': xpTotal,
            'levelEff': levelEff,
        }
        
        return results


    # helper for CreateEncGroup
    @staticmethod
    def GetEncounterXP(encMonst_dict):
        points = 0
        for monst_dx in encMonst_dict:
            baseXP = LevelXP.objects.filter(Level=monst_dx['Level']).values_list('XPAward', flat=True)[0]
            threat = 1
            if monst_dx['Threat'] == 'Elite': threat = 2
            if monst_dx['Threat'] == 'Solo': threat = 5
            points += baseXP * threat * monst_dx['Quant']
        return points


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MONSTERS EDITOR
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Editor(object):
    
    
    @staticmethod
    def DeleteTables():
        monsts = Monsters.objects.all().delete()[0]
        levels = LevelXP.objects.all().delete()[0]
        results = "Deleted: Monst " + str(monsts) + ", Levels " + str(levels) + "."
        return results
    
    
    @staticmethod
    def LoadTables():
        
        path = "dnd4e/static/data/monsters.csv"
        with open(path) as fhandle:
            reader = csv.reader(fhandle)
            for row in reader:
                
                if not row[8] or row[8] == 'Habitat':
                    continue
                
                if row[4] == "n": origin = "Natural"
                elif row[4] == "f": origin = "Fey"
                elif row[4] == "s": origin = "Shadow"
                elif row[4] == "a": origin = "Aberrant"
                elif row[4] == "e": origin = "Elemental"
                elif row[4] == "i": origin = "Immortal"
                else: origin = "Unknown";
                
                if row[5] == "h": mtype = "Humanoid"
                elif row[5] == "b": mtype = "Beast"
                elif row[5] == "m": mtype = "MBeast"
                elif row[5] == "a": mtype = "Animate"
                else: mtype = "Unknown"
                
                habitat = row[8]
                habitat = habitat.replace("al sf", "Nat Srf, Fwd Srf, Shf Srf")
                habitat = habitat.replace("al ug", "Nat Und, Fwd Und, Shf Und")                    
                habitat = habitat.replace("nt", "Nat")
                habitat = habitat.replace("fw", "Fwd")
                habitat = habitat.replace("sh", "Shf")
                habitat = habitat.replace("sf", "Srf")
                habitat = habitat.replace("ug", "Und")
                habitat = habitat.replace("aq", "Aqu")    
                habitat = habitat.replace("as", "Ast")
                habitat = habitat.replace("ec", "ElC")
                
                levels = row[7].strip().split()     # splits on whitespace by default
                
                for levelCode in levels:
                    
                    p = re.compile("([0-9]{1,2})([a-z])([a-z]{0,1})")
                    matches = p.search(levelCode)
                    level = matches.group(1)
                    mclass = matches.group(2)
                    threat = matches.group(3)
                                        
                    if mclass == "u": mclass = "Lurker"
                    elif mclass == "k": mclass = "Skirmisher"
                    elif mclass == "s": mclass = "Soldier"
                    elif mclass == "b": mclass = "Brute"
                    elif mclass == "c": mclass = "Controller"
                    elif mclass == "a": mclass = "Artillery"
                    else: mclass = "Unknown"
                    
                    if threat == "": threat = ""
                    elif threat == "m": threat = "Minion"
                    elif threat == "e": threat = "Elite"
                    elif threat == "s": threat = "Solo"
                    else: threat = "Unknown"
                    
                    created = Monsters.objects.get_or_create(
                        Race = row[1].title(),
                        SubRace = row[2].title(),
                        Book = row[3],
                        Origin = origin,
                        Type = mtype,
                        Keyword = row[6],
                        Level = int(level),
                        Class = mclass,
                        Threat = threat,
                        Habitat = habitat,
                        Social = row[9].title(),
                        AllyGroups = row[10].title(),
                    )
                # end for-loop
        
        path = "dnd4e/static/data/levelsXP.csv"
        with open(path) as fhandle:
            reader = csv.reader(fhandle)
            for row in reader:
                
                created = LevelXP.objects.get_or_create(
                    Level = row[0],
                    XPAward = row[1]
                )
        
        return "Monsters, Levels loaded."






"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
END OF FILE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""