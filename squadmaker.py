import asyncio
import discord
import subprocess
from discord.ext import commands
from configs import checks
import json
from random import choice
from random import randint
from urllib.request import urlopen
import xmltodict
import sys
import os
from pyfiglet import figlet_format
from unidecode import unidecode
import datetime
from dateutil.relativedelta import relativedelta

# set trigger and description
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='SquadMaker')

# paths
basePath = os.path.dirname(os.path.realpath(__file__)) + "/"
configPath = basePath + 'configs/config.json'
rolesPath = basePath + 'configs/roles.json'
###


# vars for stats
totalUseDispo = 0
totalUseNDispo = 0
totalVoiceJoin = 0
totalDisconnect = 0

# voice channel for ranked
listRankedChannels = ["292740400731521024", "292740501281570817", "293711190176301066", "292741401857359872", "292741439002247170", "293710972043132928", "292741888363200513", "292741915353284608", "293710876408545280", "305689254044893184", "292745138072190976", "292745351662796801", "293711078737575936", "297099630959656971", "297100263486128128", "297100373250801665", "292745991277379584", "292746134525444106"]


# load config
with open(configPath) as data_file:    
    config = json.load(data_file)


class Administrations:
    """Administrations' related commands for owner."""
    def __init__(self, bot):
        self.bot = bot

    def is_me(self, m):
        return m.author == bot.user

    # CHECK
    @commands.command(pass_context=True, no_pm=False)
    @checks.is_owner()
    @asyncio.coroutine
    def clean(self, ctx, length : int = None):
        """Delete bot's messages."""
        if length == None:
            length = 100
        else:
            length += 1
        deleted = yield from bot.purge_from(ctx.message.channel, limit=int(length), check=self.is_me)
        yield from bot.send_message(ctx.message.channel, 'Deleted {} message(s)'.format(len(deleted)))


    @commands.command(pass_context=True, no_pm=False)
    @checks.is_owner()
    @asyncio.coroutine
    def stop(self, ctx):
        """Stop the bot."""
        yield from self.bot.delete_message(ctx.message)
        tmp = yield from self.bot.send_message(ctx.message.channel, "Bye bye... 🐘")
        yield from asyncio.sleep(3)
        yield from self.bot.delete_message(tmp)
        output = subprocess.check_output(["systemctl", "stop", "squadmaker.service"], universal_newlines=True)

    @commands.command(pass_context=True, no_pm=False)
    @checks.is_owner()
    @asyncio.coroutine
    def restart(self, ctx):
        """Restart the bot."""
        yield from self.bot.delete_message(ctx.message)
        tmp = yield from self.bot.send_message(ctx.message.channel, "Restarting now... 🐘")
        yield from asyncio.sleep(3)
        yield from self.bot.delete_message(tmp)
        output = subprocess.check_output(["systemctl", "restart", "squadmaker.service"], universal_newlines=True)

    @commands.command(pass_context=True, no_pm=False)
    @checks.is_owner()
    @asyncio.coroutine
    def path(self, ctx):
        """Use to find the path of the script."""
        yield from self.bot.send_message(ctx.message.channel, "Real path : " + os.path.dirname(os.path.realpath(__file__)))

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_role()
    @asyncio.coroutine
    def purge(self, ctx, *, args : str = None):
        """Only allowed roles can purge channel."""
        try: 
            if args is not None:
                args = int(args)
            else:
                args = 1

        except Exception:
            yield from self.bot.send_message(ctx.message.channel, 'Need to be an Number.')
            return

        try:
            if args > 10 and not checks.is_owner():
                yield from self.bot.say("Command limited to 10.")
                args = 11
                time.sleep(5)
            else:
                args += 1

            yield from self.bot.purge_from(ctx.message.channel, limit=args)


        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\nContact Kanizada#4724 if the problem persist.``` '
            yield from self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))



    # test command
    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    @asyncio.coroutine
    def createrole(self, ctx, *, datas : str = None):
        """Allow to create role."""
        arr = datas.split(";")
        name = arr[0]
        hoist = False
        mentionable = False
        if arr[1] == 'true':
            hoist = True
        if arr[2] == 'true':
            mentionable = True

        role = yield from self.bot.create_role(ctx.message.server, name=name, hoist=hoist, mentionable=mentionable)

    # test command
    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    @asyncio.coroutine
    def deleterole(self, ctx, *, name : str = None):
        """Allow to delete role."""
        for role in ctx.message.server.roles:
            if role.name.lower() == name.lower():
                yield from self.bot.delete_role(ctx.message.server, role)
                yield from self.bot.send_message(ctx.message.channel, "Done.")

    # test command
    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    @asyncio.coroutine
    def fallen(self, ctx):
        """Made to remove all roles."""
        status = yield from self.bot.send_message(ctx.message.channel, "Falling...")
        for role in ctx.message.server.roles:
            if role in ctx.message.author.roles and role.is_everyone != True:
                yield from self.bot.remove_roles(ctx.message.author, role)

        yield from self.bot.edit_message(status, "Fallen.")
        yield from self.bot.delete_message(ctx.message)


class Informations:
    """Informations related commands for owner."""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, no_pm=False)
    @checks.is_owner()
    @asyncio.coroutine
    def status(self, ctx):
        """Get status of the bot."""
        output = subprocess.check_output(["systemctl", "status", "squadmaker.service"], universal_newlines=True)
        fmt = '```cmd\n{}```'
        yield from self.bot.send_message(ctx.message.channel, fmt.format(output))


    @commands.command(pass_context=True, no_pm=False)
    @checks.is_owner()
    @asyncio.coroutine
    def disk_usage(self, ctx):
        """Get disk usage of the server."""
        output = subprocess.check_output(["df", "-h"], universal_newlines=True)
        fmt = '```cmd\n{}```'
        yield from self.bot.send_message(ctx.message.channel, fmt.format(output))

    # CHECK seem don't work
    @commands.command(pass_context=True, no_pm=False)
    @checks.is_owner()
    @asyncio.coroutine
    def ping(self, ctx):
        """Ping command."""
        toEdit = yield from self.bot.send_message(ctx.message.channel, "Trying to ping...")
        msdate = ctx.message.timestamp
        nwdate = datetime.datetime.now()
        c = nwdate - msdate
        d = c / 1000
        yield from self.bot.edit_message(toEdit, "Pong : " + str(d.seconds) + " ms")

class Matchmaking:
    """Commandes relatives au matchmaking."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_role()
    @asyncio.coroutine
    def reset(self, ctx):
        """Commande pour enlever le grade disponible."""
        dispoRole = ""
        for role in ctx.message.server.roles:
            if role.id == "309230649691078656":
                dispoRole = role
        status = yield from self.bot.send_message(ctx.message.channel, "Reset started...")

        for member in ctx.message.server.members:
            if dispoRole in member.roles:
                yield from self.bot.remove_roles(member, dispoRole)

        yield from self.bot.edit_message(status, "Reset finished...")


    @commands.command(pass_context=True, no_pm=True)
    @checks.has_role()
    @asyncio.coroutine
    def stats(self, ctx):
        """Statistiques des disponibilités."""
        global totalUseDispo
        global totalUseNDispo
        global totalVoiceJoin
        global totalDisconnect

        dispoRole = None
        for role in ctx.message.server.roles:
            if role.id == "309230649691078656":
                dispoRole = role

        if dispoRole == None:
            yield from self.bot.send_message(ctx.message.channel, "Rôle introuvable pour faire les statistiques.")
            return False

        howmany = 0
        for member in ctx.message.server.members:
            if dispoRole in member.roles:
                howmany += 1

        fmt = 'Statistiques d\'utilisation de Squadmaker depuis le dernier redémarrage : ```diff\n + Nombre de joueurs disponible actuellement : {} joueurs \n - Nombre d\'utilisation de la commande !dispo : {} \n + Nombre d\'utilisation de la commande !ndispo : {} \n - Nombre de perte de disponibilité lié aux channels vocaux : {} \n + Nombre de perte de disponibilité lié aux déconnexions : {} ```'
        yield from self.bot.send_message(ctx.message.channel, fmt.format(howmany, totalUseDispo, totalUseNDispo, totalVoiceJoin, totalDisconnect))

    @commands.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def panneau(self, ctx):
        """Un panneau pour connaitre les joueurs disponible rapidement."""
        try:
            dispoRole = None
            bronzeRole = None
            silverRole = None
            goldRole = None
            platiniumRole = None
            diamondRole = None
            masterRole = None

            for role in ctx.message.server.roles:
                if role.id == "309230649691078656":
                    dispoRole = role
                if role.id == "292769253487149057":
                    bronzeRole = role
                if role.id == "292769216593920011":
                    silverRole = role
                if role.id == "292769167096938496":
                    goldRole = role
                if role.id == "292769335565615104":
                    platiniumRole = role
                if role.id == "292770442643767296":
                    diamondRole = role


            if dispoRole == None or bronzeRole == None or silverRole == None or goldRole == None or platiniumRole == None or diamondRole == None:
                yield from self.bot.send_message(ctx.message.channel, "Rôle introuvable pour faire le tableau.")
                return False

            bronze = []
            silver = []
            gold = []
            platinium = []
            diamond = []
            master = []
            noattr = []

            for member in ctx.message.server.members:
                if dispoRole in member.roles:
                    if diamondRole in member.roles:
                        platinium.append(member.display_name)
                    elif platiniumRole in member.roles:
                        platinium.append(member.display_name)
                    elif goldRole in member.roles:
                        gold.append(member.display_name)
                    elif silverRole in member.roles:
                        silver.append(member.display_name)
                    elif bronzeRole in member.roles:
                        bronze.append(member.display_name)
                    else:
                        noattr.append(member.display_name)



            fmt = "Liste des joueurs disponibles : ```"
            fmt += "\n ###### Bronze ######"
            for name in bronze:
                fmt += "\n - {}".format(name)

            fmt += "\n \n ###### Argent ######"
            for name in silver:
                fmt += "\n - {}".format(name)

            fmt += "\n \n ###### Or ######"
            for name in gold:
                fmt += "\n - {}".format(name)

            fmt += "\n \n ###### Platine ######"
            for name in platinium:
                fmt += "\n - {}".format(name)

            fmt += "\n \n ###### Diamant ######"
            for name in diamond:
                fmt += "\n - {}".format(name)

            fmt += "\n \n ###### Non attribué ######"
            for name in noattr:
                fmt += "\n - {}".format(name)

            fmt += "```"

            yield from self.bot.delete_message(ctx.message)
            tmp = yield from self.bot.send_message(ctx.message.channel, fmt)
            yield from asyncio.sleep(5)
            yield from self.bot.delete_message(tmp)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fmt = 'An error occurred while processing this request: ```py\n{}: {} at line : {}``` '
            yield from self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e, exc_tb.tb_lineno))

    @commands.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def dispo(self, ctx):
        """Commande pour se marquer disponible."""
        global totalUseDispo
        global totalUseNDispo
        global totalVoiceJoin
        global totalDisconnect
        try:
            dispoRole = ""
            server = self.bot.get_server("292736652143493130")
            for role in server.roles:
                if role.id == "309230649691078656":
                    dispoRole = role

            if ctx.message.author.status == discord.Status.offline:
                yield from self.bot.send_message(ctx.message.channel, ctx.message.author.mention + " Vous ne pouvez pas vous marquer disponible si votre status est invisible.")
                return False

            if ctx.message.author.voice.voice_channel != None:
                if ctx.message.author.voice_channel.id in listRankedChannels:
                    yield from self.bot.send_message(ctx.message.channel, ctx.message.author.mention + " Vous ne pouvez pas vous marquer disponible si vous êtes dans un channel vocal de partie classée.")
                    return False

            if dispoRole in ctx.message.author.roles:
                yield from self.bot.send_message(ctx.message.channel, ctx.message.author.mention + " Vous êtes déjà marqué disponible.")
                return False

            yield from self.bot.add_roles(ctx.message.author, dispoRole)
            yield from self.bot.send_message(ctx.message.channel, ctx.message.author.mention + "Vous êtes marqué disponible.")
            totalUseDispo += 1

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fmt = 'An error occurred while processing this request: ```py\n{}: {} at line : {}\nContact Kanizada#4724 if the problem persist.``` '
            yield from self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e, exc_tb.tb_lineno))

    @commands.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def ndispo(self, ctx):
        """Commande pour s'enlever le marquage."""
        global totalUseDispo
        global totalUseNDispo
        global totalVoiceJoin
        global totalDisconnect

        try:
            dispoRole = ""
            server = self.bot.get_server("292736652143493130")
            for role in server.roles:
                if role.id == "309230649691078656":
                    dispoRole = role

            if dispoRole not in ctx.message.author.roles:
                yield from self.bot.send_message(ctx.message.channel, ctx.message.author.mention + " Vous n'êtes pas marqué disponible.")
                return False

            yield from self.bot.remove_roles(ctx.message.author, dispoRole)
            yield from self.bot.send_message(ctx.message.channel, ctx.message.author.mention + "Vous n'êtes plus marqué disponible.")
            totalUseNDispo += 1

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fmt = 'An error occurred while processing this request: ```py\n{}: {} at line : {}\nContact Kanizada#4724 if the problem persist.``` '
            yield from self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e, exc_tb.tb_lineno))

# CHECK class from an old script, need optimizations
class Pictures:
    """Pictures related commands."""
    def __init__(self, bot):
        self.bot = bot

    def getCat(self, typePic):
        if typePic == "gif" or typePic == "jpg" or typePic == "png":
            linkStr = "http://thecatapi.com/api/images/get?format=xml&type=" + typePic
        else:
            linkStr = "http://thecatapi.com/api/images/get?format=xml&type=jpg"

        file = urlopen(linkStr)
        data = file.read()
        file.close()

        data = json.loads(json.dumps(xmltodict.parse(data)))
        catlink = data["response"]["data"]["images"]["image"]["url"]
        return catlink

    @commands.command(pass_context=True, no_pm=False)
    @asyncio.coroutine
    def cat(self, ctx, *, pictype : str = None):
        """Envoi une photo aléatoire de chat en privé. Type available : jpg, png, gif"""
        try:
            if pictype is None:
                pictype = "jpg"

            url = self.getCat(pictype)
            yield from self.bot.send_message(ctx.message.author, url)

        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\nContact Kanizada#4724 if the problem persist.``` '
            yield from self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))

# class for debug
class Debug:
    """Others commands."""
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(pass_context=True, no_pm=False)
    @checks.has_role()
    @asyncio.coroutine
    def raw_content(self, ctx, *, content : str = None):
        """Write content raw to debug."""
        fmt = "```{}```"
        yield from self.bot.send_message(ctx.message.channel, fmt.format(content))
    @commands.command(pass_context=True, no_pm=False)
    @checks.is_owner()
    @asyncio.coroutine
    def whatsmyid(self, ctx):
        """Know your id."""
        try:
            yield from self.bot.say(ctx.message.author.id)

        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n``` '
            yield from self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.has_role()
    @asyncio.coroutine
    def whatsmyroles(self, ctx):
        """Know your roles."""
        try:
            fmt = "List of your roles : ```json\n{\n"
            roles = ctx.message.author.roles
            for role in roles:
                if role.is_everyone == False:
                    fmt += "\t" + role.name + " : \"" + role.id + "\",\n"

            fmt += "}```"
            yield from self.bot.send_message(ctx.message.channel, fmt)

        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n``` '
            yield from self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_role()
    @asyncio.coroutine
    def listallroles(self, ctx):
        """List all roles from the server."""
        try:
            fmt = "List of all roles on the server : ```json\n{\n"
            for role in ctx.message.server.roles:
                if role.is_everyone == False:
                    fmt += "\t" + role.name + " : \"" + role.id + "\",\n"

            fmt += "}```"
            yield from self.bot.send_message(ctx.message.channel, fmt)

        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n``` '
            yield from self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))

bot.add_cog(Administrations(bot))
bot.add_cog(Informations(bot))
bot.add_cog(Matchmaking(bot))
bot.add_cog(Pictures(bot))
bot.add_cog(Debug(bot))

@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
    yield from bot.change_presence(game=discord.Game(name='Tactical SquadMaker'))
    creator = yield from bot.get_user_info("156493252139286538")
    tmp = yield from bot.send_message(creator, "Bot ready !")
    yield from asyncio.sleep(10)
    yield from bot.delete_message(tmp)


@bot.event
@asyncio.coroutine
def on_member_update(before, after):
    global totalUseDispo
    global totalUseNDispo
    global totalVoiceJoin
    global totalDisconnect
    dispoRole = ""
    server = bot.get_server("292736652143493130")
    for role in server.roles:
        if role.id == "309230649691078656":
            dispoRole = role

    if dispoRole in before.roles:
        try:
            # triggered when user disconnect with the role "disponible"
            if after.status == discord.Status.offline:
                yield from bot.remove_roles(after, dispoRole)
                totalDisconnect += 1
        except Exception as e:
            print(e)

@bot.event
@asyncio.coroutine
def on_voice_state_update(before, after):
    global totalUseDispo
    global totalUseNDispo
    global totalVoiceJoin
    global totalDisconnect
    dispoRole = ""
    server = bot.get_server("292736652143493130")
    for role in server.roles:
        if role.id == "309230649691078656":
            dispoRole = role
    if dispoRole in before.roles:
        try:
            # triggered when user join ranked voice channel
            if after.voice.voice_channel != None:
                if before.voice.voice_channel != after.voice.voice_channel:
                    if after.voice.voice_channel.id in listRankedChannels:
                        yield from bot.remove_roles(after, dispoRole)
                        totalVoiceJoin += 1
        except Exception as e:
            print(e)

# CHECK debug event, maybe delete ?
@bot.event
@asyncio.coroutine
def on_server_role_create(role):
    creator = yield from bot.get_user_info("156493252139286538")
    fmt = "Role created on a server : ```\n - Server's name = {}```"
    yield from bot.send_message(creator, fmt.format(role.server.name))

# CHECK debug event, maybe delete ?
@bot.event
@asyncio.coroutine
def on_server_role_delete(role):
    creator = yield from bot.get_user_info("156493252139286538")
    fmt = "Role deleted on a server : ```\n - Server's name = {} \n - Name = {}```"
    yield from bot.send_message(creator, fmt.format(role.server.name, role.name))

# CHECK debug event, maybe delete ?
@bot.event
@asyncio.coroutine
def on_server_role_update(before, after):
    if before.permissions.value != after.permissions.value or before.name != after.name or before.position != after.position or before.hoist != after.hoist:
        creator = yield from bot.get_user_info("156493252139286538")
        messb = "Role updated on a server : ```BEFORE : \n - Server's name = {} \n - Name = {} \n - Colour = {} \n - Hoist = {} \n - Position = {} \n - Managed = {} \n - Mentionable = {} \n - Is_everyone = {} \n - Permissions_integer = {}```"
        yield from bot.send_message(creator, messb.format(before.server.name, before.name, before.colour, before.hoist, before.position, before.managed, before.mentionable, before.is_everyone, before.permissions.value))

        messa = "```AFTER : \n - Server's name = {} \n - Name = {} \n - Colour = {} \n - Hoist = {} \n - Position = {} \n - Managed = {} \n - Mentionable = {} \n - Is_everyone = {} \n - Permissions_integer = {}```"
        yield from bot.send_message(creator, messa.format(after.server.name, after.name, after.colour, after.hoist, after.position, after.managed, after.mentionable, after.is_everyone, after.permissions.value))


bot.run(config["token"])