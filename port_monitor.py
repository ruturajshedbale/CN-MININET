from ryu.base import app_manager
from ryu.controller import dpset
from ryu.controller.handler import set_ev_cls
import logging
import datetime

logging.basicConfig(
    filename='port_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class PortMonitor(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(PortMonitor, self).__init__(*args, **kwargs)
        self.port_status = {}

    @set_ev_cls(dpset.EventPortAdd)
    def port_add(self, ev):
        port = ev.port.port_no
        msg = f"Port {port} ADDED/UP"
        print("🟢", msg)
        logging.info(msg)
        self.port_status[port] = "UP"
        print("Current Status:", self.port_status)

    @set_ev_cls(dpset.EventPortDelete)
    def port_delete(self, ev):
        port = ev.port.port_no
        msg = f"Port {port} REMOVED"
        print("🔴", msg)
        logging.info(msg)
        self.port_status[port] = "REMOVED"
        print("Current Status:", self.port_status)

    @set_ev_cls(dpset.EventPortModify)
    def port_modify(self, ev):
        port = ev.port.port_no
        state = ev.port.state

        if state == 1:
            status = "DOWN"
            print("⚠️ ALERT: Port", port, "DOWN")
        else:
            status = "UP"
            print("✅ Port", port, "UP")

        msg = f"Port {port} {status}"
        logging.info(msg)
        self.port_status[port] = status
        print("Current Status:", self.port_status)
