import discord
from discord.ext import commands
import statsapi
from baseball_id import Lookup

//I have hidden the token and channel ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def handle_user_messages(msg) ->str:
    message = msg.lower()
    if message.startswith('!help'):
        infoMessage = "Hello! I am Baseball Bot. I can help you with baseball stats.\n\nType !stats <player name> <batter/pitcher> to get all their stats\nType !stats <player name> <batter/pitcher> <name of stat> to get that stat of that player\nType !stats <player name> <name of stat> <year> to get that stat of that player for that year\n\nType !help to see this message again"
        return infoMessage
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

            G = PA = AB = R = H = _2B = _3B = HR = RBI = SB = CS = BB = SO = BA = OBP = SLG = OPS = TB = GDP = HBP = SH = SF = IBB = ""
            firstSection = "   G  |  PA   |   AB  |   R  |   H  |  2B | 3B |  HR |  RBI | SB | CS\n"
            firstLine =    "-------------------------------------------------------------------------\n"
            secondSection = " BB | SO | BA | OBP | SLG | OPS | TB | GDP | HBP | SH | SF | IBB | Pos\n"
            secondLine =    "------------------------------------------------------------------------\n"
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

            firstStats = f" {G} |  {PA} |  {AB} |  {R}  |  {H}  |  {_2B}  |  {_3B}  | {HR} | {RBI} | {SB} | {CS} \n\n"
            secondStats = f" {BB} | {SO} | {BA} | {OBP} | {SLG} | {OPS} | {TB} | {GDP} | {HBP} | {SH} | {SF} | {IBB} | {pos}\n"
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

            firstSection = " W | L | W-L%| ERA | G | GS | GC | GF | SHO | SV | IP | H | R | ER\n"
            firstLine =    "-------------------------------------------------------------------------\n"
            secondSection = "  HR | BB | IBB | SO | HPB | BK | WP | BF | WHIP | H9 | HR9 | BB9 | SO9 | SO/W\n"
            secondLine =    "------------------------------------------------------------------------\n"
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
            
            firstStats = f" {W} | {L} | {WL} | {ERA} | {G} | {GS} | {GC} | {GF} | {SHO} | {SV} | {IP} | {H} | {R} | {ER} \n\n"
            secondStats = f" {HR} | {BB} | {IBB} | {SO} | {HPB} | {BK} | {WP} | {BF} | {WHIP} | {H9} | {HR9} | {BB9} | {SO9} | {SOW}\n"
            printout += firstStats + secondSection + secondLine + secondStats + "`"

        if certainStat:
            return f"{name} has {certainStat} {statToGet}"
        else: 
            return printout
    
async def processMessage(message, user_message):
    try:
        botfeedback = handle_user_messages(user_message)
        await message.channel.send(botfeedback)
    except Exception as error:
        print(error)

def runBot():
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(channelId)
        await channel.send("Welcome to Baseball Bot! To get started, type '!help'")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await processMessage(message, message.content)
    client.run(token)
