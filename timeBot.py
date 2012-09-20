import datetime, pytz
import re

# Backward compatibility
from errbot.version import VERSION
from errbot.utils import version2array
if version2array(VERSION) >= [1,6,0]:
    from errbot import botcmd, BotPlugin
else:
    from errbot.botplugin import BotPlugin
    from errbot.jabberbot import botcmd

tzs =  pytz.all_timezones_set
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

def find_tz(city):
    for x in pytz.all_timezones_set:
        if city in x:
            return x
    return None

def get_all_tznames():
    country_timezones = {}
    for (country, tzlist) in pytz.country_timezones.iteritems():
        country_name = pytz.country_names[country]
        cities = []
        for timezone in tzlist:
            city = re.sub(r'^[^/]*/', r'', timezone)
            city = re.sub(country_name + '/', '', city)
            city = re.sub(r'^([^/]*)/(.*)', r'\2, \1', city)
            city = re.sub(r'_', r' ', city)
            cities.append(city)
            country_timezones[country_name] = cities
    return country_timezones

class TimeBot(BotPlugin):
    @botcmd(split_args_with = ' ')
    def time(self, mess, args):
        """ Shows the current time for given city.
        Example: !time San Francisco
        """
        if not args:
            return 'Am I supposed to guess the location?...'
        if args == 'UTC':
            tz_name = 'UTC'
        else:
            city = '_'.join([word.capitalize() for word in args])
            tz_name = find_tz(city)
        if not tz_name:
            return 'Sorry cannot find this city, you can list them with !tzlist'
        tz = pytz.timezone(tz_name)
        local_time = datetime.datetime.now(tz)
        return 'Current time in %s : %s' % (tz_name, local_time.strftime(fmt))

    @botcmd
    def tzlist(self, mess, args):
        """ List all the known cities
        """
        country_timezones = get_all_tznames()
        answer = ''
        for country in sorted(country_timezones):
            answer+=country + ':\n'
            for city in sorted(country_timezones[country]):
                answer+='\t' + city + '\n'
        return answer
