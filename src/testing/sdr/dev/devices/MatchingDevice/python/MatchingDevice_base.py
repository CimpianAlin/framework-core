#!/usr/bin/env python
#
# AUTO-GENERATED CODE.  DO NOT MODIFY!
#
# Source: MatchingDevice.spd.xml
from ossie.cf import CF, CF__POA
from ossie.utils import uuid

from ossie.device import Device
from ossie.properties import simple_property

import Queue, copy, time, threading

NOOP = -1
NORMAL = 0
FINISH = 1
class ProcessThread(threading.Thread):
    def __init__(self, target, pause=0.0125):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.target = target
        self.pause = pause
        self.stop_signal = threading.Event()

    def stop(self):
        self.stop_signal.set()

    def updatePause(self, pause):
        self.pause = pause

    def run(self):
        state = NORMAL
        while (state != FINISH) and (not self.stop_signal.isSet()):
            state = self.target()
            delay = 1e-6
            if (state == NOOP):
                # If there was no data to process sleep to avoid spinning
                delay = self.pause
            time.sleep(delay)

class MatchingDevice_base(CF__POA.Device, Device):
        # These values can be altered in the __init__ of your derived class

        PAUSE = 0.0125 # The amount of time to sleep if process return NOOP
        TIMEOUT = 5.0 # The amount of time to wait for the process thread to die when stop() is called
        DEFAULT_QUEUE_SIZE = 100 # The number of BulkIO packets that can be in the queue before pushPacket will block

        def __init__(self, devmgr, uuid, label, softwareProfile, compositeDevice, execparams):
            Device.__init__(self, devmgr, uuid, label, softwareProfile, compositeDevice, execparams)
            self.threadControlLock = threading.RLock()
            self.process_thread = None
            # self.auto_start is deprecated and is only kept for API compatibility
            # with 1.7.X and 1.8.0 devices.  This variable may be removed
            # in future releases
            self.auto_start = False

        def initialize(self):
            Device.initialize(self)
            
            # Instantiate the default implementations for all ports on this device

        def start(self):
            self.threadControlLock.acquire()
            try:
                Device.start(self)
                if self.process_thread == None:
                    self.process_thread = ProcessThread(target=self.process, pause=self.PAUSE)
                    self.process_thread.start()
            finally:
                self.threadControlLock.release()

        def process(self):
            """The process method should process a single "chunk" of data and then return.  This method will be called
            from the processing thread again, and again, and again until it returns FINISH or stop() is called on the
            device.  If no work is performed, then return NOOP"""
            raise NotImplementedError

        def stop(self):
            self.threadControlLock.acquire()
            try:
                process_thread = self.process_thread
                self.process_thread = None

                if process_thread != None:
                    process_thread.stop()
                    process_thread.join(self.TIMEOUT)
                    if process_thread.isAlive():
                        raise CF.Resource.StopError(CF.CF_NOTSET, "Processing thread did not die")
                Device.stop(self)
            finally:
                self.threadControlLock.release()

        def releaseObject(self):
            try:
                self.stop()
            except Exception:
                self._log.exception("Error stopping")
            self.threadControlLock.acquire()
            try:
                Device.releaseObject(self)
            finally:
                self.threadControlLock.release()

        ######################################################################
        # PORTS
        # 
        # DO NOT ADD NEW PORTS HERE.  You can add ports in your derived class, in the SCD xml file, 
        # or via the IDE.

        ######################################################################
        # PROPERTIES
        # 
        # DO NOT ADD NEW PROPERTIES HERE.  You can add properties in your derived class, in the PRF xml file
        # or by using the IDE.
        device_kind = simple_property(id_="DCE:cdc5ee18-7ceb-4ae6-bf4c-31f983179b4d",
                                      name="device_kind",
                                      type_="string",
                                      defvalue="MatchingDevice",
                                      mode="readonly",
                                      action="eq",
                                      kinds=("allocation","configure"),
                                      description="""This specifies the device kind"""
                                      )
        device_model = simple_property(id_="DCE:0f99b2e4-9903-4631-9846-ff349d18ecfb",
                                       name="device_model",
                                       type_="string",
                                       mode="readonly",
                                       action="eq",
                                       kinds=("allocation","configure"),
                                       description=""" This specifies the specific device"""
                                       )
        os_name = simple_property(id_="DCE:4a23ad60-0b25-4121-a630-68803a498f75",
                                  name="os_name",
                                  type_="string",
                                  defvalue="OS/2",
                                  mode="readonly",
                                  action="eq",
                                  kinds=("allocation",)                                 )
        test_eq = simple_property(id_="test_eq",
                                  type_="string",
                                  defvalue="default",
                                  mode="readonly",
                                  action="eq",
                                  kinds=("allocation",)                                 )
        test_ge = simple_property(id_="test_ge",
                                  type_="long",
                                  defvalue=0,
                                  mode="readonly",
                                  action="ge",
                                  kinds=("allocation",)                                 )
        test_gt = simple_property(id_="test_gt",
                                  type_="float",
                                  defvalue=0.0,
                                  mode="readonly",
                                  action="gt",
                                  kinds=("allocation",)                                 )
        test_le = simple_property(id_="test_le",
                                  type_="double",
                                  defvalue=0.0,
                                  mode="readonly",
                                  action="le",
                                  kinds=("allocation",)                                 )
        test_lt = simple_property(id_="test_lt",
                                  type_="short",
                                  defvalue=0,
                                  mode="readonly",
                                  action="lt",
                                  kinds=("allocation",)                                 )
        test_ne = simple_property(id_="test_ne",
                                  type_="ulong",
                                  defvalue=0,
                                  mode="readonly",
                                  action="ne",
                                  kinds=("allocation",)                                 )
        impl_defined = simple_property(id_="impl_defined",
                                       type_="string",
                                       defvalue="unknown",
                                       mode="readonly",
                                       action="eq",
                                       kinds=("allocation",)                                 )

