# Agentic AI in Platform Engineering - Implementation Guide

Complete code implementations and setup instructions for all course demos.

---

## 🎯 Overview

This repository contains production-ready code for all 5 sections of the "Agentic AI in Platform Engineering" O'Reilly/Pearson live training course.

**Course Structure:**
1. Diagnostic Agents - Infrastructure analysis and debugging
2. AI-Enhanced Development Lifecycle - Release readiness evaluation
3. Operational Intelligence - Log analysis and incident response
4. Implementation Strategy - Organizational readiness assessment
5. Practical Starter Kits - End-to-end agent deployment

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
python >= 3.9
pip
git

# Optional (for full functionality)
tflint     # brew install tflint
trivy      # brew install trivy
docker     # for containerized demos
```

### Installation

```bash
# Clone repository
git clone https://github.com/your-username/agentic-platform-engineering.git
cd agentic-platform-engineering

# Install dependencies
pip install -r requirements.txt

# Set up API key (optional - demos work without it)
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run Your First Demo

```bash
# Section 1: Diagnostic Agent
python section1_diagnostic_agent.py \
    --terraform-dir ./examples/buggy-infrastructure \
    --test-dir ./examples/tests

# Output: diagnosis.md with AI-generated analysis
```

---

## 📦 What's Included

### Core Agent Implementations

| File | Description | Section |
|------|-------------|---------|
| `section1_diagnostic_agent.py` | Infrastructure diagnostic agent | 1 |
| `section2_release_agent.py` | Release readiness evaluator | 2 |
| `section3_ops_agent.py` | Operational intelligence agent | 3 |
| `section4_readiness_agent.py` | Platform readiness assessor | 4 |
| `section5_starter_kit.py` | Agent deployment CLI | 5 |

### Example Configurations

| Directory | Contents |
|-----------|----------|
| `examples/buggy-infrastructure/` | Intentionally buggy Terraform configs |
| `examples/quality-gates/` | Quality gate configurations |
| `examples/incident-logs/` | Sample log files for analysis |
| `examples/assessments/` | Readiness assessment templates |

### GitHub Actions Workflows

| Workflow | Purpose |
|----------|---------|
| `.github/workflows/diagnose.yml` | Automated infrastructure diagnosis |
| `.github/workflows/quality-gates.yml` | Release readiness pipeline |
| `.github/workflows/incident-response.yml` | Automated incident analysis |

---

## 🔧 Section 1: Diagnostic Agent

### Purpose
Analyzes infrastructure-as-code files, runs static analysis, and generates AI-powered diagnostic reports.

### Usage

```bash
python section1_diagnostic_agent.py \
    --terraform-dir ./terraform \
    --test-dir ./tests \
    --output diagnosis.md
```

### Features
- ✅ TFLint integration for Terraform linting
- ✅ Trivy security scanning
- ✅ Automated test execution
- ✅ AI-powered root cause analysis
- ✅ Prioritized remediation recommendations

### Example Output

```markdown
## Infrastructure Diagnostic Report

### Critical Issues
1. **Security Group Misconfiguration** (HIGH)
   - Location: main.tf:15
   - Issue: SSH open to 0.0.0.0/0
   - Fix: Restrict to specific CIDR blocks

2. **Hardcoded Credentials** (CRITICAL)
   - Location: main.tf:45
   - Issue: Database password in code
   - Fix: Use AWS Secrets Manager
```

### GitHub Actions Integration

```yaml
# .github/workflows/diagnose.yml
name: Infrastructure Diagnosis
on: [push, pull_request]

jobs:
  diagnose:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Diagnostic Agent
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python section1_diagnostic_agent.py \
            --terraform-dir ./terraform \
            --output diagnosis.md
      
      - name: Comment on PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const diagnosis = fs.readFileSync('diagnosis.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: diagnosis
            });
```

---

## 🎯 Section 2: Release Readiness Agent

### Purpose
Evaluates deployment readiness using quality gates (coverage, performance, security, complexity).

### Usage

```bash
python section2_release_agent.py \
    --config quality-gates.yml \
    --output release-decision.md
```

### Quality Gates

Configure thresholds in `quality-gates.yml`:

```yaml
quality_gates:
  coverage:
    minimum: 80.0
    severity: critical
  
  performance:
    p95_latency_increase_max: 10.0
    severity: high
  
  security:
    critical_max: 0
    high_max: 5
    severity: critical
  
  complexity:
    max_cyclomatic: 10.0
    severity: medium
```

### Features
- ✅ Test coverage analysis (pytest-cov)
- ✅ Performance benchmarking
- ✅ Security vulnerability scanning
- ✅ Complexity analysis (radon)
- ✅ AI-powered release decision with rationale

### Example Output

```markdown
## Release Decision: APPROVE WITH MONITORING

### Quality Gates Summary
✅ Test Coverage: 82% (threshold: 80%)
✅ Performance: +8% P95 (threshold: <10%)
✅ Security: 0 critical, 3 high (threshold: <5)
✅ Complexity: 7.8 avg (threshold: <10)

### Recommendation
Proceed to production with enhanced monitoring.
Watch P95 latency during rollout.
```

### GitHub Actions Integration

```yaml
# .github/workflows/quality-gates.yml
name: Release Readiness
on:
  pull_request:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Tests with Coverage
        run: |
          pip install pytest pytest-cov
          pytest --cov=src --cov-report=json
      
      - name: Run Security Scan
        run: |
          pip install safety
          safety check --json > security-results.json
      
      - name: Evaluate Release Readiness
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python section2_release_agent.py \
            --config quality-gates.yml \
            --output release-decision.md
      
      - name: Post Decision
        uses: actions/upload-artifact@v3
        with:
          name: release-decision
          path: release-decision.md
```

---

## 🔍 Section 3: Operational Intelligence Agent

### Purpose
Analyzes logs, correlates incidents, and provides intelligent remediation recommendations.

### Usage

```bash
python section3_ops_agent.py \
    logs/app-*.log logs/infra-*.log \
    --output incident-analysis.md
```

### Features
- ✅ Multi-source log ingestion (JSON, plaintext)
- ✅ Pattern detection and clustering
- ✅ Service dependency correlation
- ✅ Cascade failure detection
- ✅ AI-powered root cause analysis
- ✅ Automated remediation suggestions

### Example Output

```markdown
## Incident Analysis Report

### Root Cause
Database connection pool exhaustion caused by traffic spike.

### Service Impact Chain
Traffic Spike → DB Pool Full → Payment Service Down → Order Delays

### Immediate Actions
1. Increase connection pool: DB_POOL_SIZE=50
2. Add timeout: DB_QUERY_TIMEOUT=30s
3. Implement circuit breaker

### Timeline
- 10:00:00 - Traffic spike begins
- 10:02:15 - Connection pool saturated
- 10:05:00 - Cascading failures
- 10:12:00 - Auto-recovery engaged
```

### Conversational Operations

Use Claude conversationally during incidents:

```python
# In a Python shell or Jupyter notebook
from section3_ops_agent import OpsAgent

agent = OpsAgent()

# Interactive queries
agent.ask("Why did the deployment fail?")
agent.ask("What's the error rate trend?")
agent.ask("Compare to last week's incident")
```

---

## 📊 Section 4: Implementation Strategy Agent

### Purpose
Assesses organizational readiness for adopting agentic AI in platform engineering.

### Usage

```bash
python section4_readiness_agent.py \
    --assessment org-assessment.yml \
    --output readiness-report.md
```

### Assessment Template

```yaml
# org-assessment.yml
organization:
  name: "Acme Corp"
  size: "500 engineers"
  industry: "Fintech"

platform_maturity:
  self_service_score: 3  # 1-5
  automation_level: 4
  observability: 3
  incident_response: 4

team_capabilities:
  ai_ml_experience: 2
  platform_experience: 4
  devops_maturity: 4

infrastructure:
  cloud_native: true
  kubernetes_adoption: "80%"
  ci_cd_automation: "full"
  monitoring_tools: ["Datadog", "Grafana"]

goals:
  - "Reduce MTTR by 50%"
  - "Improve deployment frequency"
  - "Automate incident response"
```

### Features
- ✅ Maturity model assessment
- ✅ Gap analysis
- ✅ Risk identification
- ✅ Prioritized roadmap generation
- ✅ ROI estimation
- ✅ Business case template

---

## 🛠️ Section 5: Practical Starter Kit

### Purpose
CLI tool for deploying production-ready agents to your infrastructure.

### Usage

```bash
# Initialize new agent
python section5_starter_kit.py init \
    --type diagnostic \
    --name my-diagnostic-agent

# Configure agent
python section5_starter_kit.py configure \
    --agent my-diagnostic-agent \
    --provider claude \
    --api-key $ANTHROPIC_API_KEY

# Deploy agent
python section5_starter_kit.py deploy \
    --agent my-diagnostic-agent \
    --platform kubernetes

# Monitor agent
python section5_starter_kit.py monitor \
    --agent my-diagnostic-agent
```

### Agent Templates

Available templates:
- `diagnostic` - Infrastructure analysis agent
- `release` - Release readiness evaluator
- `ops` - Operational intelligence agent
- `custom` - Build your own

### Features
- ✅ Multi-provider LLM support (Claude, OpenAI, mock)
- ✅ Kubernetes deployment manifests
- ✅ GitHub Actions integration
- ✅ Built-in observability
- ✅ Cost tracking
- ✅ Prompt version control

---

## 🔑 API Key Setup

### Claude API (Recommended)

```bash
# Get API key from https://console.anthropic.com/
export ANTHROPIC_API_KEY="sk-ant-..."

# Or add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
```

### OpenAI API (Alternative)

```bash
export OPENAI_API_KEY="sk-..."
```

### Mock Mode (No API Key Required)

All demos work without an API key using realistic mock responses. Perfect for:
- Testing the workflow
- Learning the concepts
- Budget-conscious workshops (< $2 per participant)

---

## 💰 Cost Considerations

### With Claude API
- **Section 1 Demo**: ~$0.10 per run
- **Section 2 Demo**: ~$0.15 per run
- **Section 3 Demo**: ~$0.20 per run
- **Total per student**: < $2 for all exercises

### Mock Mode
- **Cost**: $0
- **Functionality**: 90% of features work
- **Use case**: Testing, learning, budget workshops

---

## 🎓 Workshop Guide

### Timing

| Section | Presentation | Demo | Exercise | Total |
|---------|-------------|------|----------|-------|
| 1. Diagnostic Agents | 30 min | 7 min | 5 min | 42 min |
| 2. CI/CD Enhancement | 30 min | 8 min | 5 min | 43 min |
| 3. Ops Intelligence | 30 min | 8 min | 5 min | 43 min |
| 4. Implementation | 30 min | 8 min | 5 min | 43 min |
| 5. Starter Kits | 30 min | 8 min | 7 min | 45 min |

**Total**: ~216 minutes (3.6 hours) + breaks

### Teaching Tips

1. **Start with mock mode** - Let participants see the workflow first
2. **Add API keys gradually** - After concepts are understood
3. **Use live debugging** - Show real errors and fixes
4. **Encourage customization** - Have participants modify prompts
5. **Facilitate discussion** - Ask "How would you use this in your org?"

---

## 📚 Dependencies

```txt
# requirements.txt
anthropic>=0.18.0
openai>=1.0.0
pytest>=7.4.0
pytest-cov>=4.1.0
pyyaml>=6.0
requests>=2.31.0

# Optional tools (install via brew/apt)
# tflint - Terraform linting
# trivy - Security scanning
# radon - Complexity analysis
```

---

## 🤝 Contributing

This is course material for "Agentic AI in Platform Engineering". Contributions welcome:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🆘 Troubleshooting

### "Module 'anthropic' not found"
```bash
pip install -r requirements.txt
```

### "TFLint not found"
```bash
brew install tflint  # macOS
# or download from https://github.com/terraform-linters/tflint
```

### API Rate Limits
- Use mock mode during development
- Cache responses where possible
- Implement retry logic with exponential backoff

### Performance Issues
- Process logs in batches
- Use streaming for large files
- Implement async processing for parallel analysis

---

## 📞 Support

- **Course Questions**: Contact through O'Reilly platform
- **Technical Issues**: Open GitHub issue
- **Feature Requests**: Open GitHub discussion

---

## 🌟 Acknowledgments

Based on "Effective Platform Engineering" by Ajay Chankramath
Course developed for O'Reilly/Pearson Live Training Platform
