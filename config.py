# -*- coding: utf-8 -*-
from livesettings import config_register, ConfigurationGroup, PositiveIntegerValue, PercentValue, StringValue
from django.utils.translation import ugettext_lazy as _

# First, setup a grup to hold all our possible configs
MYAPP_GROUP = ConfigurationGroup(
    'MyApp',               # key: internal name of the group to be created
    u'Настройки сайта',  # name: verbose name which can be automatically translated
    ordering=0             # ordering: order of group in the list (default is 1)
    )


config_register(PositiveIntegerValue(
                                     MYAPP_GROUP,
        'SUM_START', 
        description = u'Диапазон денег. Начало.',
        help_text = u"С какой суммы начинается диапазон.",
        default = 10000
    ))

config_register(PositiveIntegerValue(
                                     MYAPP_GROUP,
        'SUM_END', 
        description = u'Диапазон денег. Конец.',
        help_text = u"На какой сумме заканчивается диапазон.",
        default = 50000
    ))

config_register(PositiveIntegerValue(
                                     MYAPP_GROUP,
        'TIME_START', 
        description = u'Диапазон времени. Начало.',
        help_text = u"С какого времени начинается диапазон.",
        default = 1
    ))

config_register(PositiveIntegerValue(
                                     MYAPP_GROUP,
        'TIME_END', 
        description = u'Диапазон времени. Конец.',
        help_text = u"Через сколько недель заканчивается диапазон.",
        default = 50
    ))

config_register(StringValue(
                                     MYAPP_GROUP,
        'EMAIL', 
        description = u'Email администратора',
        help_text = u"Почта, куда будут приходить заявки.",
        default = 'annkpx@gmail.com'
    ))

config_register(PercentValue(
                                     MYAPP_GROUP,
        'PERCENT', 
        description = u'Процентная ставка',
        help_text = u"Процентная ставка в неделю.",
        default = 0.02
    ))