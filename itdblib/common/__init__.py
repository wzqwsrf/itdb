# -*- coding: utf-8 -*-
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: jinlong.yang <jinlong.yang@qunar.com>
#


def sqlAttack(s):
    s = s.replace("\\", "\\\\")
    s = s.replace("'", "\\'")
    return s


def quotedSqlAttack(s):
    s = sqlAttack(s)
    return "'%s'" % s

_ = sqlAttack
_Q = quotedSqlAttack
