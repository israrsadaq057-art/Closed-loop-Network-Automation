# Main Closed-Loop Automation Script
# Entry point for the entire system

import logging
import time
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_loader import ConfigLoader
from monitor import NetworkMonitor
from analyzer import FailureAnalyzer
from remediator import RemediationEngine
from alert import AlertSystem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ClosedLoopAutomation:
    def __init__(self):
        logger.info("=" * 60)
        logger.info("Closed-Loop Network Automation System")
        logger.info("Author: Israr Sadaq - CCNA, CCNP")
        logger.info("=" * 60)
        
        os.makedirs('logs', exist_ok=True)
        
        self.config = ConfigLoader()
        self.monitor = NetworkMonitor(self.config)
        self.analyzer = FailureAnalyzer()
        self.remediator = RemediationEngine(self.config)
        self.alert = AlertSystem(self.config)
        
        self.loop_count = 0
        self.running = True
    
    def run_once(self):
        self.loop_count += 1
        logger.info(f"=== Closed-Loop Cycle {self.loop_count} ===")
        
        print(f"\n[Cycle {self.loop_count}] DETECT - Checking network...")
        monitoring_results = self.monitor.run_all_checks()
        
        print(f"[Cycle {self.loop_count}] ANALYZE - Evaluating failures...")
        actions_needed = self.analyzer.analyze(monitoring_results)
        
        if not actions_needed:
            print(f"[Cycle {self.loop_count}] System is HEALTHY. No action needed.")
            return
        
        print(f"[Cycle {self.loop_count}] DECIDE - {len(actions_needed)} remediation actions needed")
        
        for action in actions_needed:
            print(f"[Cycle {self.loop_count}] ACT - Remediating {action['target']}")
            remediation_result = self.remediator.apply_remediation(action)
            
            if remediation_result.get('success', False):
                print(f"[Cycle {self.loop_count}] SUCCESS - {action['target']} fixed")
                self.alert.info_alert(f"Fixed: {action['target']}")
            else:
                print(f"[Cycle {self.loop_count}] FAILED - Could not fix {action['target']}")
                self.alert.critical_alert(f"Manual intervention needed for {action['target']}")
    
    def run_continuous(self):
        logger.info("Starting continuous monitoring")
        interval = self.config.get_monitoring_interval()
        print(f"\nMonitoring every {interval} seconds. Press Ctrl+C to stop.\n")
        
        while self.running:
            try:
                self.run_once()
                print(f"\nWaiting {interval} seconds until next check...\n")
                time.sleep(interval)
            except KeyboardInterrupt:
                self.shutdown()
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(10)
    
    def shutdown(self):
        self.running = False
        logger.info("System shutdown")
        print(f"\nTotal cycles completed: {self.loop_count}")
        print(f"Remediations performed: {len(self.remediator.get_history())}")

def main():
    automation = ClosedLoopAutomation()
    automation.run_continuous()

if __name__ == "__main__":
    main()