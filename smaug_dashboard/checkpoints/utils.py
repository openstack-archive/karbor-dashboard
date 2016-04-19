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

FILTER_LIST = ['provider_filter', 'plan_filter', 'date_filter']

TODAY = 'today'
LASTESTONEWEEK = 'lastestoneweek'
LASTESTTWOWEEKS = 'lastesttwoweeks'
LASTESTONEMONTH = 'lastestonemonth'
LASTESTTHREEMONTHS = 'lastestthreemonths'

DATE_CHOICES = [(TODAY, _('Today')),
                (LASTESTONEWEEK, _('Lastest one week')),
                (LASTESTTWOWEEKS, _('Lastest two weeks')),
                (LASTESTONEMONTH, _('Lastest one month')),
                (LASTESTTHREEMONTHS, _('Lastest three months'))]
DATE_DICT = collections.OrderedDict(DATE_CHOICES)
