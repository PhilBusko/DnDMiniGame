"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
NAME SYSTEM
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import re
import random
import os

from django.conf import settings

import common.utility as CU

 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class NameSystem(object):


    @staticmethod
    def StandardizeName(p_artname):

        newname = p_artname
        newname = newname.replace("_cosplay", "")


        # anime

        if any(x in newname for x in ["attack_", "ymir", "mikasa"]): 
            newname = "attack.titan"

        if "accel_world" in newname: newname = "accel.world"
        if "black_rock_" in newname: newname = "black.rock"
        if "dragon_ball" in newname: newname = "dragon.ball"

        if any(x in newname for x in ["asuka", "evangelion"]): 
            newname = "evangelion"

        if "erza_" in newname: newname = "fairy.tail"
        if "yoko_" in newname: newname = "gurren.lagann"
		
        if "karoku" in newname: newname = "karneval"

        if any(x in newname for x in ["kill_la_kill", "matoi_ryuko", "satsuki_kiryuin"]): 
            newname = "kill.la.kill"
			
        if "kuroshitsuji" in newname: newname = "kuroshitsuji"
		
        if "macross" in newname: newname = "macross"
		
        if any(x in newname for x in ["madoka_magica", "homucifer"]): 
            newname = "madoka.magica"
		
        if "naruto" in newname: newname = "naruto"
        
        if "one_piece" in newname: newname = "one.piece"
		
        if any(x in newname for x in ["pokemon", "umbreon"]):
            newname = "pokemon"
		
        if any(x in newname for x in ["sailor", "serena"]):
            newname = "sailor.moon"

        if any(x in newname for x in ["saint_seya", "saint_seiya"]):
            newname = "saint.seiya"
		
        if "taiga_aisaka" in newname: newname = "toradora"

        if any(x in newname for x in ["trinityblood", "trinity_blood"]):
            newname = "trinity.blood"


        # cartoon

        if any(x in newname for x in ["avatar_", "korra_", "zuko_"]):
            newname = "avatar"

        if "flintstones" in newname: newname = "flintstones"

        if any(x in newname for x in ["rainbow_dash"]):
            newname = "my.little.pony"
		
		
        if "alice_" in newname: newname = "alice"
        if "elsa" in newname: newname = "frozen"
        if "ariel_" in newname: newname = "little.mm"
		
        if any(x in newname for x in ["maleficent", "aurora"]):
            newname = "sleeping.bt"

        if "snow_white" in newname: newname = "snow.white"



        # comics
		
        if any(x in newname for x in ["thor", "loki_"]):
            newname = "thor"
		
        if "x_23" in newname: newname = "x.twth"
		

        if any(x in newname for x in ["catwoman", "cat_woman"]):
            newname = "catwoman"

        if "wonder_woman" in newname: newname = "wonder.woman"

        if any(x in newname for x in ["batman", "joker"]):
            newname = "batman"

        if "harley_quinn" in newname: newname = "harley.quinn"

        if "teen_titans" in newname: newname = "teen.titans"

        if any(x in newname for x in ["justice_league", "injustice", "suicide_squad"]):
            newname = "dcu"

        if "supergirl" in newname: newname = "supergirl"

        if "powergirl" in newname: newname = "dcu"


        if "lady_death" in newname: newname = "chaos.cmx"


		
        # movies
		
        if "addams" in newname: newname = "addams.family"

        if any(x in newname for x in ["alien_", "ripley"]):
            newname = "alien"

        if "merida" in newname: newname = "brave"

        if "daenerys" in newname: newname = "game.thrones"

        if any(x in newname for x in ["legolas", "thranduil", "arwen"]):
            newname = "lord.ot.rings"

        if "jessica_rabbit" in newname: newname = "jessica.rabbit"
        if "oz_" in newname: newname = "legend.oz"

        if "star_wars" in newname: newname = "star.wars"

        if any(x in newname for x in ["van_helsing", "aleera", "marishka"]):
            newname = "van.helsing"

        if any(x in newname for x in ["warhammer", "howling_banshee", "40k"]):
            newname = "wrhm_fortyk"

        if "x_files" in newname: newname = "x.files"



        # videogames

        if "atlantica_online" in newname: newname = "atlantica.online"

        if any(x in newname for x in ["bioshock", "elizabeth"]):
            newname = "bioshock"

        if "borderlands" in newname: newname = "borderlands"

        if "munakata" in newname: newname = "danganronpa"
        if "dark_souls" in newname: newname = "dark.souls"

        if any(x in newname for x in ["darkstalker", "aensland"]):
            newname = "darkstalkers"

        if "dead_or_alive" in newname: newname = "dead.alive"

        if any(x in newname for x in ["dmc", "devil_may_cry"]):
            newname = "devil.may.cry"

        if "diablo_" in newname: newname = "diablo"
        if "merrill" in newname: newname = "dragon.age"
        if "dota_2" in newname: newname = "dota"

        if any(x in newname for x in ["catherine", "katherine"]):
            newname = "catherine"

        if "elsword" in newname: newname = "elsword"

        if any(x in newname for x in ["fallout", "piper_wright"]):
            newname = "fallout"

        if "fate_" in newname: newname = "fate.series"

        if any(x in newname for x in ["sephiroth", "tifa_"]):
            newname = "finalfnts_vii"

        if any(x in newname for x in ["ff_x_", "rikku_"]):
            newname = "finalfnts_x"
            
        if any(x in newname for x in ["ff_xiii", "lightning"]):
            newname = "finalfnts_xiii"

        if any(x in newname for x in ["noctis"]):
            newname = "finalfnts_xv"

        if "granado" in newname: newname = "granado.sp"
        if "heroes_of_the_storm" in newname: newname = "heroes.storm"

        if "shiranui" in newname: newname = "king.fighters"
        if "kingdom_hearts" in newname: newname = "kingdom.hearts"

        if "ahri" in newname: newname = "ahri.fox"
        if "jinx" in newname: newname = "jinx"
        if "dj_sona" in newname: newname = "dj.sona"
        if any(x in newname for x in ["league_of_legends", "katarina"]):
            newname = "league.legends"

        if "lineage" in newname: newname = "lineage"
        if "lollipop_chainsaw" in newname: newname = "lollipop.ch"


        if any(x in newname for x in ["mass_effect", "shepard"]):
            newname = "mass.effect"

        if any(x in newname for x in ["monster_hunter", "rathalos_", "jinouga_"]):
            newname = "monster.hunter"

        if any(x in newname for x in ["mortal_combat", "mortal_kombat", "mileena", "mk9_", 
            "mkx_", "kitana", "skarlet", "cassie_cage"]):
            newname = "mortal.kombat"

        if "overwatch" in newname: newname = "overwatch"

        if "ragnarok" in newname: newname = "ragnarok"

        if any(x in newname for x in ["resident_", "jill_valentine", "claire_redfield"]):
            newname = "resident.evil"


        if "soul_calibur" in newname: newname = "soulcalibur"

        if any(x in newname for x in ["starcraft", "kerrigan"]):
            newname = "starcraft"

        if any(x in newname for x in ["street_fighter", "chun_li", "chunli"]):
            newname = "street.fighter"

        if "tera_" in newname: newname = "tera.online"
        if "tomb_raider" in newname: newname = "tomb.raider"

        if any(x in newname for x in ["tekken", "christie_monteiro", "jaycee"]):
            newname = "tekken"

        if any(x in newname for x in ["velvet_crowe", "zestiria", "besteria"]):
            newname = "talesof.series"


        if "alexstrasza" in newname: newname = "dragonkin"

        if any(x in newname for x in ["blood_elf", "sylvanas"]):
            newname = "blood.elf"

        if any(x in newname for x in ["night_elf", "tyrande"]):
            newname = "night.elf"

        if any(x in newname for x in ["arthas", "jaina"]):
            newname = "human_wcft"

        if "warcraft" in newname: newname = "_warcraft"


        if any(x in newname for x in ["witcher", "ciri_", "yennefer"]):
            newname = "the.witcher"

        if any(x in newname for x in ["zelda", "hyrule"]):
            newname = "zelda"


        # fantasy

        if "sorceress" in newname or "sorcerer" in newname : newname = "hmd_arcane"


        return newname


    @staticmethod
    def GetFileNo(p_artist):

        letter_rx = (r"^([a-zA-Z0-9])")
        match = re.match(letter_rx, p_artist)
        letter = match.groups()[0].lower()

        if letter in ['a', 'b', 'c', 'd']:
            sortNo = 4
        elif letter in ['e', 'f', 'g', 'h']:
            sortNo = 5
        elif letter in ['i', 'j', 'k', 'l']:
            sortNo = 6
        elif letter in ['m', 'n', 'o', 'p']:
            sortNo = 7
        elif letter in ['q', 'r', 's', 't', 'u']:
            sortNo = 8
        elif letter in ['v', 'w', 'x', 'y', 'z']:
            sortNo = 9
        else:
            sortNo = 3

        randNo = random.randint(0, 99999)
        fileNo = str(sortNo) + CU.Pad5(randNo)

        return fileNo


class MediaStorage(object):


    # returns dict with info about files in media folder
    @staticmethod
    def GetCurrentZips():
        mediaPath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT)

        media_ls = []
        fileNames_ls = CU.GetFileNames(mediaPath)

        for fileName in fileNames_ls:
            newMedia = {}
            newMedia['url'] = os.path.join("/media", fileName)
            newMedia['name'] = fileName
            media_ls.append(newMedia)

        return media_ls


    # removes all folders and files from media root
    @staticmethod
    def ClearMedia():

        import shutil
        mediaPath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT)

        for the_file in os.listdir(mediaPath):
            file_path = os.path.join(mediaPath, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)



