from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# Store status as: {dpid: {port: status}}
network_status = {}

def _handle_PortStatus(event):
    dpid = event.dpid          # Switch ID
    port = event.ofp.desc.port_no
    reason = event.ofp.reason

    # Initialize switch entry
    if dpid not in network_status:
        network_status[dpid] = {}

    if reason == of.OFPPR_ADD:
        status = "UP"
        print(f"🟢 Switch {dpid} - Port {port} UP")

    elif reason == of.OFPPR_DELETE:
        status = "REMOVED"
        print(f"🔴 Switch {dpid} - Port {port} REMOVED")

    elif reason == of.OFPPR_MODIFY:
        if event.ofp.desc.config & of.OFPPC_PORT_DOWN:
            status = "DOWN"
            print(f"⚠️ ALERT: Switch {dpid} - Port {port} DOWN")
        else:
            status = "UP"
            print(f"✅ Switch {dpid} - Port {port} UP")

    # Update dictionary
    network_status[dpid][port] = status

    print("📊 Current Network Status:")
    for sw in network_status:
        print(f"Switch {sw}: {network_status[sw]}")

    # Log to file
    with open("port_log.txt", "a") as f:
        f.write(f"Switch {dpid} - Port {port} {status}\n")


def launch():
    core.openflow.addListenerByName("PortStatus", _handle_PortStatus)
    log.info("🔥 Multi-Switch Port Monitor Started...")
