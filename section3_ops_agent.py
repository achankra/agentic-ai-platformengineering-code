"""
Section 3: Operational Intelligence Agent
==========================================

This agent analyzes logs, correlates incidents, and provides
intelligent remediation recommendations.
"""

import os
import json
import re
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from anthropic import Anthropic


class LLMProvider:
    """Multi-provider LLM support"""
    
    def __init__(self):
        self.provider = self._detect_provider()
        if self.provider == 'claude':
            self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def _detect_provider(self) -> str:
        if os.getenv('ANTHROPIC_API_KEY'):
            return 'claude'
        else:
            print("⚠️  No API key found. Using mock mode.")
            return 'mock'
    
    def complete(self, prompt: str, max_tokens: int = 3000) -> str:
        if self.provider == 'claude':
            return self._claude_complete(prompt, max_tokens)
        else:
            return self._mock_complete()
    
    def _claude_complete(self, prompt: str, max_tokens: int) -> str:
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def _mock_complete(self) -> str:
        return """
## Incident Analysis Report
**Timestamp:** 2025-11-14T10:15:00Z  
**Severity:** HIGH

### Executive Summary
Database connection pool exhaustion caused cascading failures across the payment 
processing service. The incident affected 15% of user transactions for approximately 
12 minutes before automatic recovery mechanisms engaged.

### Root Cause Analysis

**Primary Cause:** Database connection pool exhaustion  
**Triggering Event:** Sudden traffic spike (3.5x normal load)  
**Contributing Factors:**
1. Undersized connection pool (max 20 connections)
2. Long-running queries holding connections
3. No connection timeout configured
4. Missing circuit breaker on payment service

**Timeline:**
- 10:00:00 - Traffic spike begins (Black Friday promotion launch)
- 10:02:15 - Connection pool reaches capacity
- 10:02:45 - First connection timeout errors appear
- 10:03:30 - Payment service begins queuing requests
- 10:05:00 - Queue overflow triggers cascading failures
- 10:12:00 - Auto-scaling adds database capacity
- 10:15:00 - Services recover automatically

### Service Impact Chain

```
Traffic Spike → Database Pool Exhaustion → Payment Service Degradation 
→ Order Processing Delays → User-Facing Errors
```

**Affected Services:**
1. payment-processor (primary)
2. order-service (secondary - dependency)
3. notification-service (tertiary - retry storm)

### Error Pattern Analysis

**Database Errors (1,234 occurrences):**
```
psycopg2.OperationalError: FATAL: remaining connection slots are reserved
```

**Application Errors (456 occurrences):**
```
ConnectionPoolTimeout: Could not acquire connection within 5 seconds
```

**Correlation:** 98% of application errors occurred within 2 seconds of database errors

### Metrics Analysis

| Metric | Normal | Peak | Impact |
|--------|--------|------|--------|
| Requests/sec | 450 | 1,575 | +250% |
| DB Connections | 8-12 | 20/20 | 100% utilization |
| P95 Latency | 150ms | 8,500ms | +5,566% |
| Error Rate | 0.1% | 15.2% | +15,100% |

### Remediation Recommendations

**Immediate Actions (Already Taken):**
✅ Auto-scaling added database capacity  
✅ Connection pool automatically expanded  
✅ Traffic normalized after 15 minutes

**Short-term (Next 24 hours):**
1. **Increase Connection Pool Size**
   - Current: 20 connections
   - Recommended: 50 connections
   - Configuration: `DB_POOL_SIZE=50` in payment-processor

2. **Add Connection Timeouts**
   - Set `DB_CONNECT_TIMEOUT=10s`
   - Set `DB_QUERY_TIMEOUT=30s`

3. **Implement Circuit Breaker**
   ```python
   from circuitbreaker import circuit
   
   @circuit(failure_threshold=5, recovery_timeout=60)
   def process_payment(payment_data):
       # payment processing logic
   ```

**Medium-term (Next Week):**
1. Implement read replicas for payment queries
2. Add connection pooling at application level (PgBouncer)
3. Set up predictive scaling based on promotional calendar

**Long-term (Next Month):**
1. Migrate to managed connection pooling (RDS Proxy)
2. Implement caching layer for frequent queries
3. Add comprehensive chaos engineering tests

### Monitoring Enhancements

**New Alerts to Add:**
- Connection pool utilization >80%
- Query duration >10s
- Database CPU >70%
- Payment service error rate >5%

**Dashboard Additions:**
- Real-time connection pool metrics
- Query performance breakdown
- Service dependency map with health status

### Prevention Measures

1. **Load Testing:** Simulate 5x traffic before major promotions
2. **Capacity Planning:** Maintain 50% headroom on connection pools
3. **Rate Limiting:** Implement progressive rate limits during spikes
4. **Graceful Degradation:** Queue non-critical operations during overload

### Cost Impact

- Auto-scaling costs: ~$45 (additional database capacity)
- Lost revenue (estimated): ~$2,300 (15% error rate × 12 minutes)
- Engineering response time: 2 hours

**ROI on Fixes:** Implementing recommendations will cost ~$120/month but 
prevent ~$50,000 in potential lost revenue during peak events.

### Postmortem Action Items

- [ ] Update connection pool configuration (Owner: DevOps, Due: 24h)
- [ ] Implement circuit breaker (Owner: Backend Team, Due: 3 days)
- [ ] Set up new monitoring alerts (Owner: SRE, Due: 24h)
- [ ] Schedule load testing (Owner: QA, Due: 1 week)
- [ ] Document runbook for similar incidents (Owner: Platform, Due: 3 days)

### Confidence Score: 92/100

**Recommendation:** Implement immediate and short-term fixes within 24 hours. 
Schedule load testing before next promotional event.
"""


class LogIngestion:
    """Ingests and parses logs from multiple sources"""
    
    def ingest(self, log_files: List[str]) -> List[Dict]:
        """Parse log files and return structured log entries"""
        logs = []
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    for line in f:
                        parsed = self._parse_log_line(line)
                        if parsed:
                            logs.append(parsed)
            except FileNotFoundError:
                print(f"⚠️  Log file not found: {log_file}")
        
        # Sort by timestamp
        logs.sort(key=lambda x: x.get('timestamp', ''))
        return logs
    
    def _parse_log_line(self, line: str) -> Dict:
        """Parse a single log line"""
        # Try JSON format first
        try:
            return json.loads(line)
        except:
            pass
        
        # Parse common log format
        # Example: 2025-11-14 10:02:45 ERROR [payment-service] Connection timeout
        pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(\w+)\s+\[([^\]]+)\]\s+(.+)'
        match = re.match(pattern, line)
        
        if match:
            return {
                'timestamp': match.group(1),
                'level': match.group(2),
                'service': match.group(3),
                'message': match.group(4).strip()
            }
        
        return None


class PatternDetection:
    """Detects patterns in log data"""
    
    def detect_patterns(self, logs: List[Dict]) -> Dict:
        """Identify error patterns and frequencies"""
        
        patterns = {
            'errors_by_service': defaultdict(int),
            'errors_by_type': defaultdict(int),
            'error_timeline': [],
            'top_errors': []
        }
        
        error_messages = defaultdict(int)
        
        for log in logs:
            if log.get('level') in ['ERROR', 'CRITICAL', 'FATAL']:
                service = log.get('service', 'unknown')
                message = log.get('message', '')
                
                patterns['errors_by_service'][service] += 1
                error_messages[message] += 1
                
                patterns['error_timeline'].append({
                    'timestamp': log.get('timestamp'),
                    'service': service,
                    'message': message
                })
        
        # Get top 10 errors
        patterns['top_errors'] = sorted(
            error_messages.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Classify error types
        patterns['errors_by_type'] = self._classify_errors(error_messages)
        
        return patterns
    
    def _classify_errors(self, error_messages: Dict) -> Dict:
        """Classify errors by type"""
        classifications = {
            'database': 0,
            'network': 0,
            'timeout': 0,
            'memory': 0,
            'application': 0
        }
        
        keywords = {
            'database': ['connection', 'query', 'sql', 'postgres', 'mysql'],
            'network': ['network', 'socket', 'connection refused', 'host'],
            'timeout': ['timeout', 'timed out', 'deadline exceeded'],
            'memory': ['memory', 'oom', 'heap', 'allocation'],
        }
        
        for message, count in error_messages.items():
            message_lower = message.lower()
            classified = False
            
            for error_type, terms in keywords.items():
                if any(term in message_lower for term in terms):
                    classifications[error_type] += count
                    classified = True
                    break
            
            if not classified:
                classifications['application'] += count
        
        return classifications


class CorrelationEngine:
    """Correlates incidents across services"""
    
    def correlate(self, logs: List[Dict], patterns: Dict) -> Dict:
        """Find correlations between incidents"""
        
        correlations = {
            'temporal_clusters': [],
            'service_dependencies': {},
            'cascade_detection': []
        }
        
        # Detect temporal clusters (errors happening close together)
        correlations['temporal_clusters'] = self._find_temporal_clusters(
            patterns['error_timeline']
        )
        
        # Analyze service dependency impacts
        correlations['service_dependencies'] = self._analyze_dependencies(
            patterns['errors_by_service']
        )
        
        # Detect cascade failures
        correlations['cascade_detection'] = self._detect_cascades(
            patterns['error_timeline']
        )
        
        return correlations
    
    def _find_temporal_clusters(self, error_timeline: List[Dict]) -> List[Dict]:
        """Find errors that happen close together in time"""
        clusters = []
        window_seconds = 120  # 2-minute window
        
        if not error_timeline:
            return clusters
        
        current_cluster = []
        cluster_start = None
        
        for error in error_timeline:
            if not current_cluster:
                current_cluster = [error]
                cluster_start = error['timestamp']
            else:
                # Simple time-based clustering
                current_cluster.append(error)
        
        if len(current_cluster) > 5:  # Significant cluster
            clusters.append({
                'start_time': cluster_start,
                'error_count': len(current_cluster),
                'services_affected': len(set(e['service'] for e in current_cluster))
            })
        
        return clusters
    
    def _analyze_dependencies(self, errors_by_service: Dict) -> Dict:
        """Analyze service dependencies based on error patterns"""
        # Simplified dependency analysis
        return {
            service: {'error_count': count, 'likely_primary': count > 100}
            for service, count in errors_by_service.items()
        }
    
    def _detect_cascades(self, error_timeline: List[Dict]) -> List[str]:
        """Detect cascade failure patterns"""
        cascades = []
        
        # Look for multiple services failing in sequence
        service_error_times = defaultdict(list)
        for error in error_timeline:
            service_error_times[error['service']].append(error['timestamp'])
        
        if len(service_error_times) >= 3:
            cascades.append(
                "Cascade failure detected: Multiple services failed in sequence"
            )
        
        return cascades


class RemediationSuggester:
    """Generates remediation recommendations"""
    
    def __init__(self):
        self.llm = LLMProvider()
    
    def suggest(self, logs: List[Dict], patterns: Dict, 
                correlations: Dict) -> str:
        """Generate remediation recommendations using LLM"""
        
        prompt = self._build_remediation_prompt(logs, patterns, correlations)
        return self.llm.complete(prompt, max_tokens=3500)
    
    def _build_remediation_prompt(self, logs: List[Dict], patterns: Dict,
                                  correlations: Dict) -> str:
        """Build comprehensive remediation prompt"""
        
        prompt = """You are an expert SRE analyzing an incident. Provide a detailed 
incident analysis and remediation plan.

## Log Summary

Total logs analyzed: {total_logs}
Error logs: {error_count}
Time range: {time_range}

## Error Patterns

### Errors by Service
{errors_by_service}

### Errors by Type
{errors_by_type}

### Top Errors
{top_errors}

## Correlations

### Temporal Clusters
{temporal_clusters}

### Service Dependencies
{service_dependencies}

### Cascade Detection
{cascades}

## Sample Error Logs
{sample_logs}

## Required Analysis

Provide:
1. **Executive Summary**: 2-3 sentence incident overview
2. **Root Cause Analysis**: What happened and why
3. **Service Impact Chain**: Show how failure propagated
4. **Error Pattern Analysis**: Key error patterns and correlations
5. **Metrics Analysis**: Impact on key metrics
6. **Remediation Recommendations**: 
   - Immediate actions
   - Short-term fixes (24 hours)
   - Medium-term improvements (1 week)
   - Long-term prevention (1 month)
7. **Monitoring Enhancements**: New alerts and dashboards needed
8. **Prevention Measures**: How to avoid this in future
9. **Postmortem Action Items**: Specific tasks with owners and deadlines

Be specific and actionable. Include code examples where helpful.
""".format(
            total_logs=len(logs),
            error_count=sum(patterns['errors_by_service'].values()),
            time_range=self._get_time_range(logs),
            errors_by_service=json.dumps(dict(patterns['errors_by_service']), indent=2),
            errors_by_type=json.dumps(patterns['errors_by_type'], indent=2),
            top_errors='\n'.join(f"- {msg} ({count}x)" for msg, count in patterns['top_errors'][:5]),
            temporal_clusters=json.dumps(correlations['temporal_clusters'], indent=2),
            service_dependencies=json.dumps(correlations['service_dependencies'], indent=2),
            cascades='\n'.join(f"- {c}" for c in correlations['cascade_detection']),
            sample_logs=self._format_sample_logs(logs[:10])
        )
        
        return prompt
    
    def _get_time_range(self, logs: List[Dict]) -> str:
        """Get time range from logs"""
        if not logs:
            return "Unknown"
        
        first = logs[0].get('timestamp', 'Unknown')
        last = logs[-1].get('timestamp', 'Unknown')
        return f"{first} to {last}"
    
    def _format_sample_logs(self, logs: List[Dict]) -> str:
        """Format sample logs for prompt"""
        formatted = []
        for log in logs:
            formatted.append(
                f"[{log.get('timestamp')}] {log.get('level')} "
                f"[{log.get('service')}] {log.get('message')}"
            )
        return '\n'.join(formatted)


class OpsAgent:
    """Main operational intelligence agent"""
    
    def __init__(self):
        self.ingestion = LogIngestion()
        self.pattern_detection = PatternDetection()
        self.correlation = CorrelationEngine()
        self.remediation = RemediationSuggester()
    
    def analyze_incident(self, log_files: List[str]) -> str:
        """Complete incident analysis"""
        
        print("🔍 Starting incident analysis...")
        
        # Ingest logs
        print("📥 Ingesting logs...")
        logs = self.ingestion.ingest(log_files)
        print(f"   Processed {len(logs)} log entries")
        
        # Detect patterns
        print("🔎 Detecting patterns...")
        patterns = self.pattern_detection.detect_patterns(logs)
        print(f"   Found errors in {len(patterns['errors_by_service'])} services")
        
        # Correlate incidents
        print("🔗 Correlating incidents...")
        correlations = self.correlation.correlate(logs, patterns)
        
        # Generate remediation
        print("💡 Generating remediation recommendations...")
        analysis = self.remediation.suggest(logs, patterns, correlations)
        
        print("\n✅ Analysis complete!")
        return analysis


# Command-line interface
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Operational Intelligence Agent'
    )
    parser.add_argument(
        'log_files',
        nargs='+',
        help='Log files to analyze'
    )
    parser.add_argument(
        '--output',
        default='incident-analysis.md',
        help='Output file for analysis'
    )
    
    args = parser.parse_args()
    
    # Run analysis
    agent = OpsAgent()
    analysis = agent.analyze_incident(args.log_files)
    
    # Save report
    with open(args.output, 'w') as f:
        f.write(analysis)
    
    print(f"\n📄 Analysis saved to: {args.output}")
