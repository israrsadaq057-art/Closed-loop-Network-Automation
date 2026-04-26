# Network Monitoring Module
# Continuously checks network health using ping and HTTP requests

import subprocess
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NetworkMonitor:
    def __init__(self, config_loader):
        self.config = config_loader
        self.failure_counts = {}
        self.status_history = {}
    
    def ping_host(self, ip_address):
        try:
            result = subprocess.run(
                ['ping', '-n', '1', '-w', '1000', ip_address],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Ping failed for {ip_address}: {e}")
            return False
    
    def monitor_target(self, target):
        target_name = target['name']
        
        if target['type'] == 'ping':
            is_healthy = self.ping_host(target['ip'])
        else:
            is_healthy = False
        
        if not is_healthy:
            self.failure_counts[target_name] = self.failure_counts.get(target_name, 0) + 1
        else:
            self.failure_counts[target_name] = 0
        
        self.status_history[target_name] = {
            'status': 'UP' if is_healthy else 'DOWN',
            'timestamp': datetime.now().isoformat(),
            'failure_count': self.failure_counts.get(target_name, 0)
        }
        
        return {
            'name': target_name,
            'healthy': is_healthy,
            'failure_count': self.failure_counts.get(target_name, 0),
            'threshold': target.get('failure_threshold', 3)
        }
    
    def run_all_checks(self):
        results = []
        targets = self.config.get_monitoring_targets()
        
        for target in targets:
            result = self.monitor_target(target)
            results.append(result)
            
            if not result['healthy']:
                logger.warning(f"Target {result['name']} is DOWN. Failure count: {result['failure_count']}")
            else:
                logger.info(f"Target {result['name']} is UP")
        
        return results
    
    def get_status_summary(self):
        return self.status_history