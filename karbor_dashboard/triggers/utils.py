#    Copyright (c) 2016 Huawei, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import collections
from django.utils.translation import ugettext_lazy as _
from icalendar.cal import Component
from icalendar import Event
from oslo_serialization import jsonutils

TRIGGERTYPE_CHOICES = [('time', _('Time Trigger')),
                       ('event', _('Event Trigger'))]

CRONTAB = 'crontab'

CRONTAB_DAY_CHOICES = [('1', _('Monday')),
                       ('2', _('Tuesday')),
                       ('3', _('Wednesday')),
                       ('4', _('Thursday')),
                       ('5', _('Friday')),
                       ('6', _('Saturday')),
                       ('0', _('Sunday'))]
CRONTAB_DAY_DICT = collections.OrderedDict(CRONTAB_DAY_CHOICES)

EVERYDAY = 'everyday'
EVERYWEEK = 'everyweek'
EVERYMONTH = 'everymonth'

CRONTAB_FREQUENCE_CHOICES = [(EVERYDAY, _('Every Day')),
                             (EVERYWEEK, _('Every Week')),
                             (EVERYMONTH, _('Every Month'))]
CRONTAB_FREQUENCE_DICT = collections.OrderedDict(CRONTAB_FREQUENCE_CHOICES)


class CrontabUtil(object):
    """Convert to or from Crontab format.

    pattern: * * * * *
    first * is stand for minute 0~59
    second * is stand for hour 0~23
    third * is stand for day 1~31
    fouth * is stand for month 1~12
    fifth * is stand for week 0~6 (0 is Sunday)
    """

    @staticmethod
    def convert_to_crontab(data):
        dict_crontab = {
            "format": CRONTAB,
            "pattern": "* * * * *"
        }

        data_day = data["day"]
        data_date = data["date"]
        data_time = data["time"]

        if data['frequence'] == EVERYDAY:
            dict_crontab["pattern"] = '%s %s * * *' \
                                      % (data_time.minute,
                                         data_time.hour)
        elif data['frequence'] == EVERYWEEK:
            dict_crontab["pattern"] = '%s %s * * %s' \
                                      % (data_time.minute,
                                         data_time.hour, data_day)
        elif data['frequence'] == EVERYMONTH:
            dict_crontab["pattern"] = '%s %s %s * *' \
                                      % (data_time.minute,
                                         data_time.hour, data_date)

        return dict_crontab

    @staticmethod
    def convert_from_crontab(dict_crontab):
        data = {
            'format': dict_crontab['format']
        }
        if dict_crontab["format"] == CRONTAB:
            pattern = dict_crontab["pattern"]
            patterns = pattern.split(" ")
            if len(patterns) == 5:
                if patterns[2] == "*" \
                        and patterns[3] == "*" \
                        and patterns[4] == "*":
                    data["frequence"] = CRONTAB_FREQUENCE_DICT[EVERYDAY]
                elif patterns[2] == "*" \
                        and patterns[3] == "*" \
                        and patterns[4] != "*":
                    data["frequence"] = CRONTAB_FREQUENCE_DICT[EVERYWEEK]
                    data["day"] = CRONTAB_DAY_DICT[patterns[4]]
                elif patterns[2] != "*" \
                        and patterns[3] == "*" \
                        and patterns[4] == "*":
                    data["frequence"] = CRONTAB_FREQUENCE_DICT[EVERYMONTH]
                    data["date"] = patterns[2]

                data["time"] = '%s:%s' % (patterns[1].zfill(2),
                                          patterns[0].zfill(2))
        return data

CALENDAR = 'calendar'
CALENDAR_DAY_CHOICES = [('1', _('MO')),
                        ('2', _('TU')),
                        ('3', _('WE')),
                        ('4', _('TH')),
                        ('5', _('FR')),
                        ('6', _('SA')),
                        ('0', _('SU'))]
CALENDAR_DAY_DICT = collections.OrderedDict(CALENDAR_DAY_CHOICES)
CALENDAR_DAY_MAPPING = [('MO', _('Monday')),
                        ('TU', _('Tuesday')),
                        ('WE', _('Wednesday')),
                        ('TH', _('Thursday')),
                        ('FR', _('Friday')),
                        ('SA', _('Saturday')),
                        ('SU', _('Sunday'))]
CALENDAR_DAY_MAPPING_DICT = collections.OrderedDict(CALENDAR_DAY_MAPPING)
MINUTELY = 'MINUTELY'
HOURLY = 'HOURLY'
DAILY = 'DAILY'
WEEKLY = 'WEEKLY'
MONTHLY = 'MONTHLY'


class CalendarUtil(object):
    """Convert to or from calendar format."""
    @staticmethod
    def convert_to_calendar(data):
        dict_calendar = {
            "format": CALENDAR,
        }

        pattern_frequence = ''
        if data['frequence'] == EVERYMONTH:
            pattern_frequence = MONTHLY
        elif data['frequence'] == EVERYWEEK:
            pattern_frequence = WEEKLY
        elif data['frequence'] == EVERYDAY:
            pattern_frequence = DAILY
        calendar_event = Event()
        rule_pattern = {
            'freq': pattern_frequence,
            'byhour': data["time"].hour,
            'byminute': data["time"].minute,
        }

        if pattern_frequence == MONTHLY:
            rule_pattern['bymonthday'] = data["date"]
        elif pattern_frequence == WEEKLY:
            rule_pattern['byday'] = CALENDAR_DAY_DICT[data["day"]]

        calendar_event.add('rrule', rule_pattern)
        dict_calendar['pattern'] = calendar_event.to_ical()
        return dict_calendar

    @staticmethod
    def decode_calendar_pattern(pattern):
        try:
            pattern.index('\\')
            pattern_dict = jsonutils.loads('{"pattern": "%s"}' % pattern)
            return pattern_dict["pattern"]
        except Exception:
            return pattern

    @staticmethod
    def convert_from_calendar(dict_calendar):
        data = {
            'format': dict_calendar['format']
        }
        if dict_calendar["format"] == CALENDAR:
            pattern = dict_calendar["pattern"]
            calendar_event = Component.from_ical(
                CalendarUtil.decode_calendar_pattern(pattern)
            )
            if isinstance(calendar_event, Event):
                calendar_event_rule = calendar_event['RRULE']
                data['frequence'] = calendar_event_rule['FREQ'][0]

                if data['frequence'] == MONTHLY and not (
                        'INTERVAL' in calendar_event['RRULE']):
                    data['date'] = ' '.join(
                        str(date)
                        for date in calendar_event_rule['BYMONTHDAY'])

                if data['frequence'] == WEEKLY and not (
                        'INTERVAL' in calendar_event['RRULE']):
                    data['day'] = ' '.join(
                        str(CALENDAR_DAY_MAPPING_DICT[day])
                        for day in calendar_event_rule['BYDAY'])

                if 'BYHOUR' in calendar_event['RRULE']:
                    data['hour'] = ' '.join(
                        str(hour) for hour in calendar_event_rule['BYHOUR'])

                if 'BYMINUTE' in calendar_event['RRULE']:
                    data['minute'] = ' '.join(
                        str(minute)
                        for minute in calendar_event_rule['BYMINUTE'])

                if 'INTERVAL' in calendar_event['RRULE']:
                    data['interval'] = ' '.join(
                        str(interval)
                        for interval in calendar_event_rule['INTERVAL'])

        return data
