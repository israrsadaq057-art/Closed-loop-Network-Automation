# Configuration Loader Module
# Loads YAML configuration files for the automation system

import yaml
import os

class ConfigLoader:
    def __init__(self, config_path="config/settings.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def get_monitoring_targets(self):
        return self.config.get('monitoring', {}).get('targets', [])
    
    def get_monitoring_interval(self):
        return self.config.get('monitoring', {}).get('interval_seconds', 30)
    
    def get_remediation_config(self):
        return self.config.get('remediation', {})
    
    def get_alert_config(self):
        return self.config.get('alerting', {})