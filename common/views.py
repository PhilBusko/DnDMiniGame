"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
COMMON/VIEWS.py
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from django.shortcuts import render
from django.http import JsonResponse

import members.forms as MF
import common.central as CN
import members.models.members as MM

import logging
prog_lg = logging.getLogger('progress')
excp_lg = logging.getLogger('exception')


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
HTML PAGE REQUESTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def home(request):
    return render(request, 'common_home.html')


def store(request):
    context = {
        'moneyStore': CN.Reporter.MoneyStoreData(),
    }
    return render(request, 'store.html', context)


def notfound(request):
    return render(request, 'common_notfound.html')


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
AJAX REQUESTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def central(request, command):
    
    prog_lg.info("ajax command: " + command)
    
    if command == 'update_buyDiamonds':
        itemId = request.POST.get('itemId')
        hret = CN.Editor.PurchaseDiamonds(request.user, itemId) 
        return JsonResponse(hret.results, safe=False, status=hret.status)
    
    elif command == 'update_exchangeTokens':
        diamonds = int(request.POST.get('diamonds'))
        hret = CN.Editor.ExchangeTokens(request.user, diamonds) 
        return JsonResponse(hret.results, safe=False, status=hret.status)
    
    else:
        msg = "command invalid: " + command
        excp_lg.error(msg)
        return JsonResponse(msg, safe=False, status = 404)  






"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
END OF FILE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""