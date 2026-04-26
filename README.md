# Closed-Loop Network Automation

Self-healing network monitoring that detects, analyzes, and fixes connectivity issues automatically.

**Author:** Israr Sadaq — CCNA, CCNP  
**Role:** Optical Networks and Automation Engineer, Fraunhofer HHI Berlin  
**Location:** Berlin, Germany

---

## Table of Contents

1. Overview
2. How It Works
3. What It Monitors
4. What It Fixes
5. Quick Start
6. Configuration
7. Project Structure
8. Real-World Scenarios
9. Logging
10. Extending the System
11. Links
12. Contact

---

## Overview

This system runs a continuous closed-loop automation cycle every 30 seconds. It monitors your network, detects failures, and executes automatic remediation without human intervention.

**The Problem:** Network issues waste time. Users lose connectivity. IT admins run manual diagnostics. Minutes become hours.

**The Solution:** Automate the entire troubleshooting workflow. When the network breaks, the system fixes itself.

---

## How It Works

The system runs four stages continuously:

| Stage | Action | Description |
|-------|--------|-------------|
| 1 DETECT | Ping and HTTP checks | Tests gateway and DNS every 30 seconds |
| 2 ANALYZE | Count consecutive failures | Triggers at 3 failures (configurable) |
| 3 DECIDE | Select remediation | Prioritizes gateway issues first |
| 4 ACT | Execute fix command | Runs flush DNS, renew DHCP, or reset adapter |
| VERIFY | Re-check target | Confirms fix worked or escalates |

---

## What It Monitors

| Layer | Target | Method |
|-------|--------|--------|
| Network | Default Gateway | ICMP ping |
| Network | Google DNS (8.8.8.8) | ICMP ping |
| Interface | Ethernet/WiFi adapter | System check |

**Expandable to:** Switches, routers, firewalls, servers, APIs, wireless APs, VPN tunnels.

---

## What It Fixes

| Failure Type | Detection Threshold | Remediation Action |
|--------------|--------------------|--------------------|
| DNS cache corruption | 3 failed pings | `ipconfig /flushdns` |
| DHCP lease expired | No IP address | `ipconfig /release && /renew` |
| Adapter driver crash | Interface down | Reset network adapter |
| ARP table stale | Gateway unreachable | `arp -d` |

All actions are logged with timestamps. Failed remediations trigger alerts.

---

## Quick Start

### Prerequisites

- Windows 10/11 or Windows Server
- Python 3.7 or higher
- Administrator privileges

### Installation

```bash
# Clone or download the project
cd D:\Israr-Projects\Closed-Loop-Network-Automation

# Install dependencies
pip install -r requirements.txt

# Run the automation
python src/main.py
