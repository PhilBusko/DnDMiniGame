"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
WEBSCRAPER/VIEWS.py
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import json

from django.shortcuts import render
from django.http import JsonResponse
from django.utils.safestring import mark_safe

from django.views.decorators.csrf import csrf_exempt

import common.utility as CU
import webscraper.models.dagr as WD
import webscraper.models.name_system as NS


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
SCRAPER MAIN
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def scraper(request):    
    scrapeSites = ["DeviantArt", "Hentai Foundry"]
    currMedia = NS.MediaStorage.GetCurrentZips()

    context = {
        'scrapeSites': mark_safe(json.dumps(scrapeSites)),
        'currMedia': mark_safe(json.dumps(currMedia))
    }
    return render(request, 'scraper.html', context)


@csrf_exempt
def scraper_jx(request, command):
    
    CU.prog_lg.info("ajax command: " + command)
    
    if command == 'deviant_scrape':

        gallName = request.POST.get('gallName')
        colxName = request.POST.get('colxName')

        ripper = WD.Dagr()
        ripper.Initialize(gallName, colxName)

        pages_ls = ripper.GetArtPages(gallName)

        results = {}
        results['pages'] = len(pages_ls)
        
        print( "art pages: " + str(results['pages']) )

        rip = ripper.GetArtFromPages(pages_ls)
        results = {**results, **rip}

        return JsonResponse(results, safe=False, status=201)

    elif command == 'clear_media':
        NS.MediaStorage.ClearMedia()

        results = {
            'results': 'cleared',
        }

        return JsonResponse(results, safe=False, status=201)

    else:
        msg = "command invalid: " + command
        CU.excp_lg.error(msg)
        return JsonResponse(msg, safe=False, status=404)

