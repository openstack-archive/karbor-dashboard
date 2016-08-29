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

TRIGGERTYPE_CHOICES = [('time', _('Time Trigger')),
                       ('event', _('Event Trigger'))]

CRONTAB = 'crontab'

DAY_CHOICES = [('1', _('Monday')),
               ('2', _('Tuesday')),
               ('3', _('Wednesday')),
               ('4', _('Thursday')),
               ('5', _('Friday')),
               ('6', _('Saturday')),
               ('0', _('Sunday'))]
DAY_DICT = collections.OrderedDict(DAY_CHOICES)

EVERYDAY = 'everyday'
EVERYWEEK = 'everyweek'
EVERYMONTH = 'everymonth'

FREQUENCE_CHOICES = [(EVERYDAY, _('Every Day')),
                     (EVERYWEEK, _('Every Week')),
                     (EVERYMONTH, _('Every Month'))]
FREQUENCE_DICT = collections.OrderedDict(FREQUENCE_CHOICES)


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
        data = {}
        if dict_crontab["format"] == CRONTAB:
            pattern = dict_crontab["pattern"]
            patterns = pattern.split(" ")
            if len(patterns) == 5:
                if patterns[2] == "*" \
                        and patterns[3] == "*" \
                        and patterns[4] == "*":
                    data["frequence"] = FREQUENCE_DICT[EVERYDAY]
                elif patterns[2] == "*" \
                        and patterns[3] == "*" \
                        and patterns[4] != "*":
                    data["frequence"] = FREQUENCE_DICT[EVERYWEEK]
                    data["day"] = DAY_DICT[patterns[4]]
                elif patterns[2] != "*" \
                        and patterns[3] == "*" \
                        and patterns[4] == "*":
                    data["frequence"] = FREQUENCE_DICT[EVERYMONTH]
                    data["date"] = patterns[2]

                data["time"] = '%s:%s' % (patterns[1].zfill(2),
                                          patterns[0].zfill(2))
        return data
