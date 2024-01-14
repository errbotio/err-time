import datetime

import pytz
from errbot import BotPlugin, botcmd

FMT = "%Y-%m-%d %H:%M:%S %Z%z"


def find_tz(city):
    for timezone in pytz.all_timezones_set:
        if city in timezone:
            return timezone
    return None


def get_all_tznames():
    country_timezones = {}
    for country, tzlist in pytz.country_timezones.items():
        country_name = pytz.country_names[country]
        cities = []
        for timezone in tzlist:
            raw_name = timezone.rpartition("/")[2]
            name = raw_name.replace("_", " ")
            cities.append(name)
            country_timezones[country_name] = cities
    return country_timezones


class TimeBot(BotPlugin):
    @botcmd(split_args_with=" ")
    def time(self, msg, args):
        """Shows the current time for given city.
        Example: !time San Francisco
        """
        if not args:
            return "Am I supposed to guess the location?..."

        if len(args) == 1 and args[0].lower() == "utc":
            tz_name = "UTC"
        else:
            city = "_".join([word.capitalize() for word in args])
            tz_name = find_tz(city)

        if not tz_name:
            return "Sorry cannot find this city, you can list them with !tzlist"

        tz = pytz.timezone(tz_name)
        local_time = datetime.datetime.now(tz)
        return f"Current time in {tz_name}: {local_time.strftime(FMT)}"

    @botcmd
    def tzlist(self, mess, args):
        """List all the known cities"""
        country_timezones = get_all_tznames()
        answer = ""
        for country in sorted(country_timezones):
            answer += country + ":\n"
            for city in sorted(country_timezones[country]):
                answer += "\t" + city + "\n"
        return answer
