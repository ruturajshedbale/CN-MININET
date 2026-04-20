from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# Initialize all 3 ports
port_status = {1: "UNKNOWN", 2: "UNKNOWN", 3: "UNKNOWN"}

def display_status():
    print("\n📊 ===== CURRENT PORT STATUS =====")
    for p in sorted(port_status):
        print(f"Port {p}: {port_status[p]}")
    print("=================================\n")

def _handle_PortStatus(event):
    port = event.ofp.desc.port_no
    reason = event.ofp.reason

    if reason == of.OFPPR_ADD:
        status = "UP"
        print(f"🟢 Port {port} UP")

    elif reason == of.OFPPR_DELETE:
        status = "REMOVED"
        print(f"🔴 Port {port} REMOVED")

    elif reason == of.OFPPR_MODIFY:
        if event.ofp.desc.config & of.OFPPC_PORT_DOWN:
            status = "DOWN"
            print(f"⚠️ ALERT: Port {port} DOWN")
        else:
            status = "UP"
            print(f"✅ Port {port} UP")

    # Update only that port
    port_status[port] = status

    # Show ALL ports every time
    display_status()

    # Log file
    with open("port_log_single.txt", "a") as f:
        f.write(f"Port {port} {status}\n")


def launch():
    core.openflow.addListenerByName("PortStatus", _handle_PortStatus)
    log.info("🔥 Enhanced Single Switch Monitor Started")
