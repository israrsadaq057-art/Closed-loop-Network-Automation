# Failure Analysis Module
# Determines if remediation is needed based on thresholds

import logging

logger = logging.getLogger(__name__)

class FailureAnalyzer:
    def __init__(self):
        self.remediation_needed = {}
    
    def analyze(self, monitoring_results):
        actions_needed = []
        
        for result in monitoring_results:
            if not result['healthy']:
                if result['failure_count'] >= result['threshold']:
                    actions_needed.append({
                        'target': result['name'],
                        'action': 'remediate',
                        'reason': f"Failed {result['failure_count']} times, threshold is {result['threshold']}"
                    })
                    
                    logger.warning(f"REMEDIATION NEEDED for {result['name']}")
                else:
                    logger.info(f"Monitoring {result['name']}: {result['failure_count']}/{result['threshold']} failures")
        
        return actions_needed
    
    def determine_priority(self, actions_needed):
        priority_map = {
            'Default Gateway': 1,
            'Google DNS': 2,
        }
        
        for action in actions_needed:
            action['priority'] = priority_map.get(action['target'], 10)
        
        return sorted(actions_needed, key=lambda x: x['priority'])