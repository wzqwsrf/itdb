# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


import basedal
from itdblib.models.dt_device_state import DeviceState
from sqlalchemy import func
from qg.core import log as logging
LOG = logging.getLogger(__name__)


class DeviceStateDal(basedal.BaseDal):

    def __init__(self):
        self.session = self._getSession()

    def get_all_device_state(self):
        """ query all device state
        """
        hQuery = self.session.query(DeviceState)
        return hQuery.all()

    def add_device_state(self, stateType):
        """ add device state type
        """
        try:
            ds = DeviceState()
            ds.ch_name = stateType
            self.session.add(ds)
        except Exception, _ex:
            LOG.warning("add state status is exception : %s" % str(_ex))
            return False
        return True

    def del_device_state(self, stateType):
        """ delete device state type
        """
        try:
            self.session.delete(stateType)
        except Exception, _ex:
            LOG.warning("delete state type is exception : %s" % str(_ex))
            return False
        return True

    def update_device_state(self, stateType):
        """ update device state type
        """
        try:
            deviceType = self.session.query(DeviceState())\
                    .filter_by(DeviceState.ch_name == stateType)\
                    .first()
            if deviceType is not None:
                self.session.delete(stateType)
            else:
                LOG.warning("the device state is not existed")
        except Exception, _ex:
            LOG.error("error occured while update %s device type,Error :\
                                                        %s" % str(_ex))
            return False
        return True

    def get_device_state_id_by_ch_name(self, ch_name):
        try:
            return self.session.query(DeviceState).filter(
                        func.lower(DeviceState.ch_name) == func.lower(ch_name)).first()
        except Exception as e:
            LOG.error('get_device_state_id_by_ch_name error:%s' % str(e))
            return None

    def get_device_state_name_by_id(self, device_state_id):
        try:
            return self.session.query(DeviceState).filter(
                        DeviceState.id == device_state_id).first()
        except Exception as e:
            LOG.error('get_device_state_name_by_id error:%s' % str(e))
            return None