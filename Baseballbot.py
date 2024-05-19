import discord
from discord.ext import commands
import statsapi
from baseball_id import Lookup
from datetime import date
import requests
import json
from random import randrange
from quotes import quoteboard

keys = open("keys.txt", "r")
token = keys.readline().strip()
channelId = int(keys.readline().strip())
keys.close()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def handle_user_messages(msg, id) ->str:
    if msg == 'Thank you for your suggestion! If I like it, I will add it to the bot!':
        return msg
    elif msg.startswith('The current results of the question'):
        return msg
    
    message = msg.lower()
    if message.startswith('!help'):
        infoMessage = "Hello! I am Baseball Bot. I can help you with baseball stats and select other things.\n\n"
        baseballtext = "Baseball Commands:\n\t\t`!stats <player name> <batter/pitcher>`: Get all stats for the specified player.\n\t\t`!stats <player name> <batter/pitcher> <name of stat>`: Get a specific stat for the player.\n\t\t`!stats <player name> <batter/pitcher> <year>`: Get the stats for the player for a specific year.\n\t\t`!standings <American/National>`: See the current standings for the specified league.\n\t\t`!score <Team Name>`: Get the most recent score for the specified team.\n\n"
        otherfeatures = "Other Features:\n\t\t`!poll <question ending in ?> <options split by ', '>`: Create a poll with up to 12 options.\n\t\t`!meme`: Get a random meme.\n\t\t`!ping`: Get a pong back.\n\t\t`!weather <city name>`: Get the weather for the specified city.\n\t\t`!roll <'d'Number>`: Roll a die with the specified number of sides.\n\n"
        quoteText = "Quote Board:\n\t\t`!quote add <quote> <name>`: Adds 'quote' by 'name' to the quoteboard\n\t\t`!quote remove <quote> <name>`: Removes 'quote' by 'name' from the quoteboard\n\t\t`!quote get <name>`: Gets a random quote by 'name'\n\t\t`!quote get`: Gets a random quote\n\n"
        help = "Use `!help` to see this message again."
        infoMessage += baseballtext + quoteText + otherfeatures + help
        return infoMessage
    elif message.startswith('!quote'):
        splitMsg = message.split(' ')
        splitMsg.pop(0)

        if splitMsg[0] == 'add':
            splitMsg.pop(0)
            rest = " ".join(splitMsg)

            quote = rest.split('"')
            quote.pop(0)

            name = quote[-1].strip().capitalize()

            quote = f"{quote[0].capitalize()} - {name}"

            if quote in quoteboard:
                return "Quote already exists for this person"
            else:
                quoteboard.append(quote)

            f = open("quotes.py", "w")
            f.write("quoteboard = " + str(quoteboard))
            f.close()

            return "Quote Added!"
        elif splitMsg[0] == 'remove':
            splitMsg.pop(0)
            rest = " ".join(splitMsg)

            quote = rest.split('"')
            quote.pop(0)

            name = quote[-1].strip().capitalize()

            quote = f"{quote[0].capitalize()} - {name}"
            if quote not in quoteboard:
                return "Quote does not exist for this person"
            else:
                quoteboard.remove(quote)

            f = open("quotes.py", "w")
            f.write("quoteboard = " + str(quoteboard))
            f.close()

            return "Quote Removed!"
        elif splitMsg[0] == 'get':
            splitMsg.pop(0)
            name = " ".join(splitMsg).capitalize()

            if name == 'Random':
                quote = quoteboard[randrange(len(quoteboard))]
                return str(quote)
            quotes = []

            for i in range(len(quoteboard)):
                if name in quoteboard[i]:
                    quotes.append(quoteboard[i].split(' - ')[0])

            output = ""
            output += f"{name}'s Quotes:\n"

            for i in quotes:
                output += f"{i}\n"
            return output
        else:
            return "Please enter a valid quote command"
    elif message.startswith('!roll'):
        splitMsg = message.split(' ')
        splitMsg.pop(0)
        if len(splitMsg) > 1:
            return "Please enter a die to roll"
        if splitMsg[0][0] != 'd':
            return "Please enter a valid die to roll"
        else:
            die = splitMsg[0][1:]
            return f"You rolled a {splitMsg[0]} and got a {randrange(int(die) + 1)}"
    elif message.startswith('!weather'):
        apiKey = 'a12cc50ea3a50599451ea185977a2bb2'
        baseUrl = "http://api.openweathermap.org/data/2.5/weather?"
        splitMsg = message.split(' ')
        splitMsg.pop(0)
        for i in range(len(splitMsg)):
            splitMsg[i] = splitMsg[i].capitalize()
        city = " ".join(splitMsg)

        complete_url = baseUrl + "appid=" + apiKey + "&q=" + city
        response = requests.get(complete_url)
        data = response.json()

        weatherType = data['weather'][0]['main']
        tempMin = data['main']['temp_min']
        tempMax = data['main']['temp_max']

        # Convert Kelvin to Fahrenheit
        tempMin = round((float(tempMin) - 273.15) * 9/5 + 32, ndigits=1)
        tempMax = round((float(tempMax) - 273.15) * 9/5 + 32, ndigits=1)

        return f"The weather in {city} is {weatherType} with temperatures ranging from {tempMin} to {tempMax} Fahrenheit"
    elif message.startswith('!ping'):
        return f"<@{id}> Pong!"
    elif message.startswith('!meme'):
        content = requests.get("https://meme-api.com/gimme").text
        content = json.loads(content)
        return content["url"]
    elif message.startswith('!poll'):
        splitMsg = message.split('?')

        question = splitMsg[0].split(' ')
        question.pop(0)

        splitMsg.pop(0)
        questionText = " ".join(question).capitalize()

        options = splitMsg[0].split(', ')

        options[0] = options[0].strip()
        for i in range(len(options)):
            options[i] = options[i].capitalize()

        if len(options) < 2:
            return "Please enter a valid poll question with at least two options"
        elif len(options) > 12:
            return "Please enter a valid poll question with at most twelve options"
        
        outputMsg = ""
        outputMsg += f"{questionText}?\n\n"

        numStr = [':heart:', ':pink_heart:', ':orange_heart:', ':yellow_heart:', ':green_heart:', ':blue_heart:', ':light_blue_heart:', ':purple_heart:', ':brown_heart:', ':black_heart:', ':grey_heart:', ':white_heart:']

        for i in range(len(options)):
            outputMsg += f"React with {numStr[i]} for {options[i]}\n"

        return outputMsg
    elif message.startswith('!score'):
        splitMsg = message.split(' ')
        splitMsg.pop(0)

        splitMsg[0] = splitMsg[0].capitalize()
        teamIds = {'Angels': 108, 'Diamondbacks': 109, 'Orioles': 110, 'Red Sox': 111, 'Cubs': 112, 'Reds': 113, 'Indians': 114, 'Rockies': 115, 'Tigers': 116, 'Astros': 117, 'Royals': 118, 'Dodgers': 119, 'Nationals': 120, 'Mets': 121, 'Atheletics': 133, 'Pirates': 134, 'Padres': 135, 'Mariners': 136, 'Giants': 137, 'Cardinals': 138, 'Rays': 139, 'Rangers': 140, 'Blue Jays': 141, 'Twins': 142, 'Phillies': 143, 'Braves': 144, 'White Sox': 145, 'Marlins': 146, 'Yankees': 147, 'Brewers': 158}
        currentTeamId = teamIds.get(splitMsg[0])

        gameID = statsapi.last_game(currentTeamId)
        lineScore = statsapi.linescore(gameID)
        return '`' + lineScore + '`'
    elif message.startswith('!standings'):
        splitMsg = message.split(' ')
        splitMsg.pop(0)

        today = date.today()
        todayStr = today.strftime("%m/%d/%Y")

        standings = statsapi.standings(date=todayStr)
        splitLeagues = standings.split('National League East')

        if 'american' in splitMsg or 'American' in splitMsg:
            return '`' + splitLeagues[0] + '`'
        elif 'national' in splitMsg or 'National' in splitMsg:
            return '`' + 'National League East' + splitLeagues[1] + '`'

        return splitLeagues[0]
    elif message.startswith('!stats'):
        splitMsg = message.split(' ')
        
        splitMsg.pop(0)
        for i in range(len(splitMsg)):
            if splitMsg[i] != 'batter' or splitMsg[i] != 'pitcher':
                splitMsg[i] = splitMsg[i].capitalize()
        
        if (len(splitMsg) < 2):
            return "Please enter a player's full name"
        
        name = splitMsg[0] + ' ' + splitMsg[1]
        try:
            mlbID = Lookup.from_names([name])['mlb_id'].to_string().split(' ')[4]
            mlbID = int(float(mlbID))
        except:
            return "Player not found. Please check the spelling and try again"

        category = ""
        if 'Batter' in splitMsg or 'batter' in splitMsg or 'Hitter' in splitMsg or 'hitter' in splitMsg: 
            category = 'hitting'
        elif 'Pitcher' in splitMsg or 'pitcher' in splitMsg:
            category = 'pitching'
        else:
            return "Please follow the format <player name> <pitcher/batter>"
        
        statToGet = None
        if splitMsg[-1].upper() in ['W', 'L', 'W-L%', 'ERA', 'G', 'GS', 'GC', 'GF', 'SHO', 'SV', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'IBB', 'SO', 'HPB', 'BK', 'WP', 'BF', 'WHIP', 'H9', 'HR9', 'BB9', 'SO9', 'SO/W'] or splitMsg[-1].upper() in ['G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'CS', 'BB', 'SB','SO', 'BA', 'OBP', 'SLG', 'OPS', 'TB', 'GDP', 'HBP', 'SH', 'SF', 'IBB', 'POS']:
            statToGet = splitMsg[-1].upper()
        elif splitMsg[-2].upper() in ['W', 'L', 'W-L%', 'ERA', 'G', 'GS', 'GC', 'GF', 'SHO', 'SV', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'IBB', 'SO', 'HPB', 'BK', 'WP', 'BF', 'WHIP', 'H9', 'HR9', 'BB9', 'SO9', 'SO/W'] or splitMsg[-2].upper() in ['G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'CS', 'BB', 'SB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', 'TB', 'GDP', 'HBP', 'SH', 'SF', 'IBB', 'POS']:
            statToGet = splitMsg[-2].upper()

        printout = ""
        certainStat = None

        year = None
        try:
            year = int(splitMsg[-1])
        except ValueError:
            pass

        pos = None
        if year:
            foundYear = False
            year = str(year)
            stats = statsapi.player_stat_data(mlbID, category, 'yearByYear', sportId=1)
            name = stats['first_name'] + ' ' + stats['nickname'] + ' ' + stats['last_name']
            pos = stats['position']
            for i in range(len(stats['stats'])):
                if stats['stats'][i]['season'] == year:
                    stats = stats['stats'][i]
                    foundYear = True
                    break
            
            if not foundYear:
                return f"{name} was not in the league in {year}"
        else:
            stats = statsapi.player_stats(mlbID, category, 'career')

        if category == 'hitting':  
            statsSplit = None
            try:
                statsSplit = stats.split('\n')
                namePos = statsSplit[0].split(',')
                name = namePos[0]
                pos = namePos[1].split(' ')[1]

                statsSplit.pop(0)
                statsSplit.pop(0)
                statsSplit.pop(0)
            except:
                pass

            # ╔ ═ ║ ╚ ╗ ╝

            G = PA = AB = R = H = _2B = _3B = HR = RBI = SB = CS = BB = SO = BA = OBP = SLG = OPS = TB = GDP = HBP = SH = SF = IBB = ""
            firstSection =  "   G  ║  PA  ║  AB  ║   R  ║   H  ║  2B  ║  3B  ║  HR  ║  RBI ║  SB  ║   CS \n"
            firstLine =     "══════════════════════════════════════════════════════════════════════════════\n"
            secondSection = "   BB ║  SO  ║  BA  ║  OBP ║  SLG ║  OPS ║  TB  ║  GDP ║  HBP ║   SH ║  SF  ║  IBB ║ Pos\n"
            secondLine =    "══════════════════════════════════════════════════════════════════════════════════════════\n"
            printout += "`" + name + '\n\n' + firstSection + firstLine

            if statsSplit:
                G = statsSplit[0].split(' ')[1]
                R = statsSplit[3].split(' ')[1]
                _2B = statsSplit[4].split(' ')[1]
                _3B = statsSplit[5].split(' ')[1]
                HR = statsSplit[6].split(' ')[1]
                SO = statsSplit[7].split(' ')[1]
                BB = statsSplit[8].split(' ')[1]
                IBB = statsSplit[9].split(' ')[1]
                H = statsSplit[10].split(' ')[1]
                HBP = statsSplit[11].split(' ')[1]
                BA = statsSplit[12].split(' ')[1]
                AB = statsSplit[13].split(' ')[1]
                OBP = statsSplit[14].split(' ')[1]
                SLG = statsSplit[15].split(' ')[1]
                OPS = statsSplit[16].split(' ')[1]
                CS = statsSplit[17].split(' ')[1]
                SB = statsSplit[18].split(' ')[1]
                GDP = statsSplit[20].split(' ')[1]
                PA = statsSplit[22].split(' ')[1]
                TB = statsSplit[23].split(' ')[1]
                RBI = statsSplit[24].split(' ')[1]
                SH = statsSplit[26].split(' ')[1]
                SF = statsSplit[27].split(' ')[1]
            else:
                G = stats['stats']['gamesPlayed']
                R = stats['stats']['runs']
                _2B = stats['stats']['doubles']
                _3B = stats['stats']['triples']
                HR = stats['stats']['homeRuns']
                SO = stats['stats']['strikeOuts']
                BB = stats['stats']['baseOnBalls']
                IBB = stats['stats']['intentionalWalks']
                H =  stats['stats']['hits']
                HBP =  stats['stats']['hitByPitch']
                BA =  stats['stats']['avg']
                AB =  stats['stats']['atBats']
                OBP =  stats['stats']['obp']
                SLG =  stats['stats']['slg']
                OPS =  stats['stats']['ops']
                CS =  stats['stats']['caughtStealing']
                SB =  stats['stats']['stolenBases']
                GDP =  stats['stats']['groundIntoDoublePlay']
                PA =  stats['stats']['plateAppearances']
                TB =  stats['stats']['totalBases']
                RBI =  stats['stats']['rbi']
                SH =  stats['stats']['sacBunts']
                SF =  stats['stats']['sacFlies']

            statDict = {'G': G, 'PA': PA, 'AB': AB, 'R': R, 'H': H, '2B':_2B, '3B':_3B, 'HR': HR, 'RBI': RBI, 'SB': SB, 'CS': CS, 'BB': BB, 'SO': SO, 'BA': BA, 'OBP': OBP, 'SLG': SLG, 'OPS': OPS, 'TB': TB, 'GDP': GDP, 'HBP': HBP, 'SH': SH, 'SF': SF, 'IBB': IBB, 'POS': pos}
            if statToGet:
                certainStat = statDict.get(statToGet)

            firstStats = f" {G:>4} ║ {PA:>4} ║ {AB:>4} ║ {R:>4} ║ {H:>4} ║ {_2B:>4} ║ {_3B:>4} ║ {HR:>4} ║ {RBI:>4} ║ {SB:>4} ║ {CS:>4} \n\n"
            secondStats = f" {BB:>4} ║ {SO:>4} ║ {BA:>4} ║ {OBP:>4} ║ {SLG:>4} ║ {OPS:>4} ║ {TB:>4} ║ {GDP:>4} ║ {HBP:>4} ║ {SH:>4} ║ {SF:>4} ║ {IBB:>4} ║ {pos}\n"
            printout += firstStats + secondSection + secondLine + secondStats + "`"

        elif category == 'pitching':
            statsSplit = None
            try:
                statsSplit = stats.split('\n')
                namePos = statsSplit[0].split(',')
                name = namePos[0]
                pos = namePos[1].split(' ')[1]

                statsSplit.pop(0)
                statsSplit.pop(0)
                statsSplit.pop(0)
            except:
                pass

            W = L = WL = ERA = G = GS = GC = GF = SHO = SV = IP = H = R = ER = HR = BB = IBB = SO = HPB = BK = WP = BF = WHIP = H9 = HR9 = BB9 = SO9 = SOW = ""

            firstSection = "   W  ║   L  ║ W-L% ║ ERA  ║   G  ║  GS  ║  GC  ║  GF  ║  SHO ║  SV  ║   IP  ║   H  ║   R  ║  ER\n"
            firstLine =    "═══════════════════════════════════════════════════════════════════════════════════════════════════\n"
            secondSection = "   HR ║  BB  ║  IBB ║  SO  ║  HPB ║   BK ║   WP ║  BF  ║ WHIP ║  H9  ║  HR9 ║  BB9 ║  SO9 ║ SO/W\n"
            secondLine =    "══════════════════════════════════════════════════════════════════════════════════════════════════\n"
            printout += "`" + name + '\n\n' + firstSection + firstLine

            if statsSplit:
                G = statsSplit[0].split(' ')[1]
                GS = statsSplit[1].split(' ')[1]
                R = statsSplit[4].split(' ')[1]
                HR = statsSplit[7].split(' ')[1]
                SO = statsSplit[8].split(' ')[1]
                BB = statsSplit[9].split(' ')[1]
                IBB = statsSplit[10].split(' ')[1]
                H = statsSplit[11].split(' ')[1]
                HPB = statsSplit[12].split(' ')[1]
                ERA = statsSplit[23].split(' ')[1]
                IP = statsSplit[24].split(' ')[1]
                W = statsSplit[25].split(' ')[1]
                L = statsSplit[26].split(' ')[1]
                SV = statsSplit[27].split(' ')[1]
                ER = statsSplit[31].split(' ')[1]
                WHIP = statsSplit[32].split(' ')[1]
                BF = statsSplit[33].split(' ')[1]
                GC = statsSplit[36].split(' ')[1]
                SHO = statsSplit[37].split(' ')[1]
                BK = statsSplit[41].split(' ')[1]
                WP = statsSplit[42].split(' ')[1]
                WL = statsSplit[46].split(' ')[1]
                GF = statsSplit[48].split(' ')[1]
                SOW = statsSplit[49].split(' ')[1]
                SO9 = statsSplit[50].split(' ')[1]
                BB9 = statsSplit[51].split(' ')[1]
                H9 = statsSplit[52].split(' ')[1]
                HR9 = statsSplit[54].split(' ')[1]
            else:
                G = stats['stats']['gamesPlayed']
                GS = stats['stats']['gamesStarted']
                R = stats['stats']['runs']
                HR = stats['stats']['homeRuns']
                SO = stats['stats']['strikeOuts']
                BB = stats['stats']['baseOnBalls']
                IBB =  stats['stats']['intentionalWalks']
                H =  stats['stats']['hits']
                HPB =  stats['stats']['hitByPitch']
                ERA =  stats['stats']['era']
                IP =  stats['stats']['inningsPitched']
                W =  stats['stats']['wins']
                L =  stats['stats']['losses']
                SV =  stats['stats']['saves']
                ER =  stats['stats']['earnedRuns']
                WHIP =  stats['stats']['whip']
                BF =  stats['stats']['battersFaced']
                GC =  stats['stats']['completeGames']
                SHO =  stats['stats']['shutouts']
                BK =  stats['stats']['balks']
                WP =  stats['stats']['wildPitches']
                WL =  stats['stats']['winPercentage']
                GF =  stats['stats']['gamesFinished']
                SOW =  stats['stats']['strikeoutWalkRatio']
                SO9 =  stats['stats']['strikeoutsPer9Inn']
                BB9 =  stats['stats']['walksPer9Inn']
                H9 =  stats['stats']['hitsPer9Inn']
                HR9 =  stats['stats']['homeRunsPer9']

            statDict = {'W': W, 'L': L, 'WL': WL, 'ERA': ERA, 'G': G, 'GS': GS, 'GC': GC, 'GF': GF, 'SHO': SHO, 'SV': SV, 'IP': IP, 'H': H, 'R': R, 'ER': ER, 'HR': HR, 'BB': BB, 'IBB': IBB, 'SO': SO, 'HPB': HPB, 'BK': BK, 'WP': WP, 'BF': BF, 'WHIP': WHIP, 'H9': H9, 'HR9': HR9, 'BB9': BB9, 'SO9': SO9, 'SOW': SOW}
            if statToGet:
                certainStat = statDict.get(statToGet)
            
            firstStats = f" {W:>4} ║ {L:>4} ║ {WL:>4} ║ {ERA:>4} ║ {G:>4} ║ {GS:>4} ║ {GC:>4} ║ {GF:>4} ║ {SHO:>4} ║ {SV:>4} ║ {IP:>4} ║ {H:>4} ║ {R:>4} ║ {ER:>4} \n\n"
            secondStats = f" {HR:>4} ║ {BB:>4} ║ {IBB:>4} ║ {SO:>4} ║ {HPB:>4} ║ {BK:>4} ║ {WP:>4} ║ {BF:>4} ║ {WHIP:>4} ║ {H9:>4} ║ {HR9:>4} ║ {BB9:>4} ║ {SO9:>4} ║ {SOW:>4}\n"
            printout += firstStats + secondSection + secondLine + secondStats + "`"

        if certainStat:
            return f"{name} has {certainStat} {statToGet}"
        else: 
            return printout
    else:
        return "Invalid command. Type !help to see all available commands"
    
async def processMessage(message, user_message):
    try:
        botfeedback = handle_user_messages(user_message, message.author.id)
        await message.channel.send(botfeedback)
    except Exception as error:
        print(error)

def runBot():
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(channelId)
        await channel.send("Welcome to Baseball Bot+! To get started, type '!help'")
    
    @client.event
    async def on_reaction_add(reaction, user):
        if user == client.user:
            return
        if ':heart:' in reaction.message.content:
            votes = {}
            counter = 0
            for i in reaction.message.reactions:
                if i.count == 1:
                    votes[counter] = 0
                else:
                    votes[counter] = i.count - 1
                counter += 1
                

            poll = reaction.message.content.split('\n')
            question = poll.pop(0)
            poll.pop(0)

            resultStr = f"The current results of the question {question} are:\n"
            for i in range(len(poll)):
                resultStr += f"{poll[i].split(' ')[-1]} has {votes[i]} votes\n"
            await processMessage(reaction.message, resultStr)    
        return

    @client.event
    async def on_message(message):
        if message.author == client.user:
            if ':heart:' not in message.content:
                return
            else:
                splitMsg = message.content.split('\n')
                splitMsg.pop(0)
                splitMsg.pop(0)                

                hearts = ["\U00002764", "\U0001FA77", "\U0001F9E1", "\U0001F49B", "\U0001F49A", "\U0001F499", "\U0001FA75", "\U0001F49C", "\U0001F90E", "\U0001F5A4", "\U0001FA76", "\U0001F90D"]

                for i in range(len(splitMsg)):
                    await message.add_reaction(hearts[i])
                
        else:
            if message.content.startswith('!'):
                if message.content.startswith('!suggestion'):
                    splitMsg = message.content.split(' ')
                    splitMsg.pop(0)
                    suggestion = " ".join(splitMsg)

                    devID = 272834628346445824
                    dev = await client.fetch_user(devID)
                    await dev.send(f"{message.author} has a suggestion: {suggestion}")

                    await processMessage(message, "Thank you for your suggestion! If I like it, I will add it to the bot!")
                    return
                else:
                    await processMessage(message, message.content)

    client.run(token)