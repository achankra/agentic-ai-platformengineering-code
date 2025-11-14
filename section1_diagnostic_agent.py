"""
Section 1: Infrastructure Diagnostic Agent
==========================================

This agent analyzes infrastructure-as-code files, runs static analysis tools,
and uses Claude to generate comprehensive diagnostic reports.
"""

import os
import json
import subprocess
from typing import Dict, List, Optional
from anthropic import Anthropic


class LLMProvider:
    """Multi-provider LLM support with automatic fallback"""
    
    def __init__(self):
        self.provider = self._detect_provider()
        if self.provider == 'claude':
            self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def _detect_provider(self) -> str:
        """Detect available LLM provider"""
        if os.getenv('ANTHROPIC_API_KEY'):
            return 'claude'
        elif os.getenv('OPENAI_API_KEY'):
            return 'openai'
        else:
            print("⚠️  No API key found. Using mock responses for demo.")
            return 'mock'
    
    def complete(self, prompt: str, max_tokens: int = 2000) -> str:
        """Generate completion using available provider"""
        if self.provider == 'claude':
            return self._claude_complete(prompt, max_tokens)
        elif self.provider == 'openai':
            return self._openai_complete(prompt, max_tokens)
        else:
            return self._mock_complete(prompt)
    
    def _claude_complete(self, prompt: str, max_tokens: int) -> str:
        """Use Claude API"""
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def _openai_complete(self, prompt: str, max_tokens: int) -> str:
        """Use OpenAI API (placeholder)"""
        # Implementation for OpenAI
        pass
    
    def _mock_complete(self, prompt: str) -> str:
        """Provide realistic mock response for demo without API key"""
        return """
## Infrastructure Diagnostic Report

### Critical Issues Identified

1. **Security Group Configuration (HIGH SEVERITY)**
   - Location: `main.tf:15-22`
   - Issue: Security group allows SSH (port 22) from 0.0.0.0/0
   - Impact: Exposes instances to unauthorized access from any IP
   - Recommendation: Restrict to specific CIDR blocks or use bastion host

2. **Hardcoded Credentials (CRITICAL)**
   - Location: `main.tf:45`
   - Issue: Database password appears to be hardcoded
   - Impact: Credentials exposed in version control
   - Recommendation: Use AWS Secrets Manager or Parameter Store

3. **Missing Required Tags (MEDIUM)**
   - Location: Multiple resources
   - Issue: Resources missing Environment, Owner, and CostCenter tags
   - Impact: Difficult to track costs and ownership
   - Recommendation: Add required tags to all resources

4. **Deprecated Resource Syntax (LOW)**
   - Location: `main.tf:78`
   - Issue: Using deprecated `aws_instance` argument
   - Impact: May break in future Terraform versions
   - Recommendation: Update to current syntax

### Test Failures Analysis

- 5 out of 8 tests failed
- Failure pattern: Security and compliance tests
- Root cause: Configuration does not meet security baseline

### Recommended Actions

**Immediate (Before Deployment):**
1. Remove 0.0.0.0/0 from security group ingress
2. Move credentials to secrets management
3. Add required tags

**Short-term:**
1. Update deprecated syntax
2. Implement automated compliance checking
3. Add pre-commit hooks for security scanning

**Estimated Fix Time:** 30-45 minutes
**Risk Level:** HIGH - Do not deploy until critical issues resolved
"""


class TFLintAnalyzer:
    """Runs TFLint static analysis on Terraform files"""
    
    def analyze(self, terraform_dir: str) -> Dict:
        """Run TFLint and return results"""
        try:
            result = subprocess.run(
                ['tflint', '--format=json', terraform_dir],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                return json.loads(result.stdout)
            else:
                return {'issues': []}
                
        except subprocess.TimeoutExpired:
            return {'error': 'TFLint analysis timed out'}
        except FileNotFoundError:
            print("⚠️  TFLint not installed. Install with: brew install tflint")
            return {'error': 'TFLint not found'}
        except Exception as e:
            return {'error': str(e)}


class TrivyAnalyzer:
    """Runs Trivy security scanner"""
    
    def analyze(self, terraform_dir: str) -> Dict:
        """Run Trivy security scan"""
        try:
            result = subprocess.run(
                ['trivy', 'config', '--format=json', terraform_dir],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.stdout:
                return json.loads(result.stdout)
            else:
                return {'results': []}
                
        except subprocess.TimeoutExpired:
            return {'error': 'Trivy scan timed out'}
        except FileNotFoundError:
            print("⚠️  Trivy not installed. Install with: brew install trivy")
            return {'error': 'Trivy not found'}
        except Exception as e:
            return {'error': str(e)}


class TestRunner:
    """Runs infrastructure tests"""
    
    def run_tests(self, test_dir: str) -> Dict:
        """Execute pytest tests and return results"""
        try:
            result = subprocess.run(
                ['pytest', test_dir, '--json-report', '--json-report-file=/tmp/test-results.json'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            try:
                with open('/tmp/test-results.json', 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                # Fallback: parse pytest output
                return {
                    'passed': result.stdout.count(' PASSED'),
                    'failed': result.stdout.count(' FAILED'),
                    'output': result.stdout
                }
                
        except Exception as e:
            return {'error': str(e)}


class DiagnosticAgent:
    """Main diagnostic agent that coordinates analysis"""
    
    def __init__(self):
        self.llm = LLMProvider()
        self.tflint = TFLintAnalyzer()
        self.trivy = TrivyAnalyzer()
        self.test_runner = TestRunner()
    
    def diagnose(self, terraform_dir: str, test_dir: str) -> str:
        """Run complete diagnostic analysis"""
        
        print("🔍 Starting infrastructure diagnosis...")
        print(f"   Terraform directory: {terraform_dir}")
        print(f"   Test directory: {test_dir}")
        
        # Collect data from all sources
        print("\n📊 Running static analysis...")
        tflint_results = self.tflint.analyze(terraform_dir)
        
        print("🔒 Running security scan...")
        trivy_results = self.trivy.analyze(terraform_dir)
        
        print("🧪 Running tests...")
        test_results = self.test_runner.run_tests(test_dir)
        
        # Read Terraform files
        print("📖 Reading configuration files...")
        tf_files = self._read_terraform_files(terraform_dir)
        
        # Generate diagnostic prompt
        prompt = self._build_diagnostic_prompt(
            tf_files, tflint_results, trivy_results, test_results
        )
        
        # Get AI analysis
        print("\n🤖 Generating AI diagnosis...")
        diagnosis = self.llm.complete(prompt, max_tokens=3000)
        
        print("\n✅ Diagnosis complete!")
        return diagnosis
    
    def _read_terraform_files(self, terraform_dir: str) -> Dict[str, str]:
        """Read all .tf files from directory"""
        tf_files = {}
        
        if not os.path.exists(terraform_dir):
            return {}
        
        for filename in os.listdir(terraform_dir):
            if filename.endswith('.tf'):
                filepath = os.path.join(terraform_dir, filename)
                with open(filepath, 'r') as f:
                    tf_files[filename] = f.read()
        
        return tf_files
    
    def _build_diagnostic_prompt(self, tf_files: Dict, tflint: Dict, 
                                  trivy: Dict, tests: Dict) -> str:
        """Build comprehensive diagnostic prompt for LLM"""
        
        prompt = """You are an expert platform engineer analyzing infrastructure-as-code.

Review the following information and provide a comprehensive diagnostic report:

## Terraform Configuration Files

"""
        
        for filename, content in tf_files.items():
            prompt += f"\n### {filename}\n```hcl\n{content}\n```\n"
        
        prompt += f"""

## TFLint Static Analysis Results

```json
{json.dumps(tflint, indent=2)}
```

## Trivy Security Scan Results

```json
{json.dumps(trivy, indent=2)}
```

## Test Results

```json
{json.dumps(tests, indent=2)}
```

## Required Output

Generate a diagnostic report with:

1. **Critical Issues**: Security vulnerabilities, compliance violations
2. **Medium Issues**: Best practice violations, deprecations
3. **Low Issues**: Style issues, optimization opportunities
4. **Root Cause Analysis**: Why tests are failing
5. **Remediation Steps**: Specific fixes with code examples
6. **Priority Order**: What to fix first
7. **Estimated Fix Time**: How long repairs will take

Focus on actionable recommendations that can be implemented immediately.
Format the report in clear Markdown with code examples where helpful.
"""
        
        return prompt


# Command-line interface
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Infrastructure Diagnostic Agent'
    )
    parser.add_argument(
        '--terraform-dir',
        default='./terraform',
        help='Directory containing Terraform files'
    )
    parser.add_argument(
        '--test-dir',
        default='./tests',
        help='Directory containing tests'
    )
    parser.add_argument(
        '--output',
        default='diagnosis.md',
        help='Output file for diagnosis report'
    )
    
    args = parser.parse_args()
    
    # Run diagnosis
    agent = DiagnosticAgent()
    diagnosis = agent.diagnose(args.terraform_dir, args.test_dir)
    
    # Save report
    with open(args.output, 'w') as f:
        f.write(diagnosis)
    
    print(f"\n📄 Report saved to: {args.output}")
    print("\nDiagnosis Summary:")
    print("=" * 60)
    print(diagnosis[:500] + "...\n")
