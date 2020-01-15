"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DND4E/VIEWS.py
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import json
from collections import OrderedDict

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe

import common.utility as CU
import dnd4e.models.magicitems as DG
import dnd4e.models.monsters as DM

import logging
prog_lg = logging.getLogger('progress')
excp_lg = logging.getLogger('exception')


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
HTML PAGE REQUESTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def intro(request):
    return render(request, 'intro.html')


def corerules(request):
    return render(request, 'corerules.html')


def resources(request):
    return render(request, 'resources.html')


def magicitems(request):
    return render(request, 'magicitems.html')


def encgroup(request):
    context = {
        'allyGroups': mark_safe(json.dumps(DM.Reporter.AllyGroupsList())),
    }
    return render(request, 'encgroup.html', context)


def domainraces(request):
    return render(request, 'domainraces.html')


def monst_stats(request):
    races = DM.Reporter.RacesList()
    context = {
        'monstCnt': DM.Reporter.MonsterCount(),
        'raceCnt': len(races['data']),
        'byRole': mark_safe(json.dumps(DM.Reporter.CountsByRole())),
        'byLevel': mark_safe(json.dumps(DM.Reporter.CountsByLevel())),
        'raceList': mark_safe(json.dumps(races)),
    }
    return render(request, 'monst_stats.html', context)


def miniatures(request):
    return render(request, 'miniatures.html')


def terrain(request):
    return render(request, 'terrain.html')


def database(request):
    
    results = DM.Reporter.GetTableData() 
    results += DG.Reporter.GetTableData()
    
    colFormat = OrderedDict()
    colFormat['table'] = ''
    colFormat['count'] = 'format_center'
    
    tableData = {
       'data': results,
       'colFormat': colFormat,
    }
    
    context = {
        'tableData': mark_safe(json.dumps(tableData))
    }
    
    return render(request, 'database.html', context)



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
AJAX REQUESTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def db_report(request, command):
    
    prog_lg.info("ajax report command: " + command)
    
    if command == 'table_report':
        hret = DM.Reporter.GetTableData()
        return JsonResponse(hret.results, safe=False, status=hret.status)
    
    elif command == 'rollitem':
        level = request.GET.get('level')
        hret = DG.Reporter.GetRandomItem(level)
        return JsonResponse(hret.results, safe=False, status=hret.status)
    
    elif command == 'domainRaces':
        habitat = request.GET.get('habitat')
        hret = DM.Reporter.RandomDomainRace(habitat)
        return JsonResponse(hret.results, safe=False, status=hret.status)
    
    elif command == 'encounter':
        chars = request.GET.get('chars')
        level = request.GET.get('level')
        habitat = request.GET.get('habitat')
        allyGroup = request.GET.get('allyGroup')
        origin = request.GET.get('origin')
        mtype = request.GET.get('type')
        threat = request.GET.get('threat')
        
        hret = DM.Reporter.GenerateEncounter(chars, level, habitat, allyGroup, origin, mtype, threat)
        return JsonResponse(hret.results, safe=False, status=hret.status)
    
    msg = "command invalid: " + command
    return JsonResponse(msg, safe=False, status = 404)  


def db_edit(request, command):
    
    prog_lg.info("ajax edit command: " + command)
    
    if command == 'load_tables':
        
        DM.Editor.DeleteTables()
        DG.Editor.DeleteTables()
        
        monstRes = DM.Editor.LoadTables()
        magicRes = DG.Editor.LoadTables()
                
        hret = CU.HttpReturn()
        hret.results = monstRes + " | " + magicRes
        hret.status = 201
        return JsonResponse(hret.results, safe=False, status=hret.status)
    
    msg = "command invalid: " + command
    return JsonResponse(msg, safe=False, status = 404)  



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
END-OF-FILE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""