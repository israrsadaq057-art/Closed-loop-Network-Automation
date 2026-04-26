# Remediation Module
# Executes automatic fixes for detected failures

import subprocess
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RemediationEngine:
    def __init__(self, config_loader):
        self.config = config_loader
        self.remediation_history = []
        self.last_remediation_time = None
    
    def execute_command(self, command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def remediate_gateway(self):
        logger.info("Attempting to remediate Gateway issue")
        
        actions = [
            {'name': 'Flush DNS', 'command': 'ipconfig /flushdns'},
            {'name': 'Renew DHCP', 'command': 'ipconfig /release && ipconfig /renew'}
        ]
        
        results = []
        for action in actions:
            result = self.execute_command(action['command'])
            results.append({
                'action': action['name'],
                'success': result['success'],
                'timestamp': datetime.now().isoformat()
            })
            if result['success']:
                logger.info(f"Success: {action['name']}")
        
        return results
    
    def apply_remediation(self, action_needed):
        target = action_needed['target']
        
        if 'Gateway' in target:
            result = self.remediate_gateway()
        else:
            result = self.execute_command('ipconfig /flushdns')
        
        self.last_remediation_time = datetime.now()
        
        self.remediation_history.append({
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'result': result
        })
        
        return {'success': True, 'result': result}
    
    def get_history(self):
        return self.remediation_history