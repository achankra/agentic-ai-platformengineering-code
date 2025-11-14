# Agentic AI in Platform Engineering - Demo Structures

## Course Overview
5-segment O'Reilly/Pearson live training with demos and exercises for each section.

---

## SECTION 1: DIAGNOSTIC AGENTS

### Demo: Infrastructure Diagnostic Agent

**Objective:** Show AI agent analyzing infrastructure configuration files and detecting issues

**Structure:**
1. **Setup Phase** (2 minutes)
   - Show buggy Terraform configuration
   - Display test failures
   - Introduce the diagnostic agent

2. **Analysis Phase** (3 minutes)
   - Trigger agent via GitHub Actions
   - Agent reads Terraform files
   - Agent runs TFLint and Trivy scans
   - Agent correlates errors

3. **Results Phase** (2 minutes)
   - Display AI-generated diagnosis
   - Show root cause analysis
   - Present recommended fixes

**GitHub Repository Structure:**
```
section1-diagnostic-agent/
├── .github/
│   └── workflows/
│       └── diagnose.yml          # GitHub Actions workflow
├── terraform/
│   ├── main.tf                   # Intentionally buggy config
│   ├── variables.tf
│   └── outputs.tf
├── tests/
│   ├── test_infrastructure.py    # Tests that expose bugs
│   └── requirements.txt
├── diagnostic_agent/
│   ├── agent.py                  # Main agent code
│   ├── analyzers/
│   │   ├── tflint_analyzer.py
│   │   ├── trivy_analyzer.py
│   │   └── log_analyzer.py
│   └── prompts/
│       └── diagnosis_prompt.txt
├── .env.example                  # API key template
└── README.md
```

**Intentional Bugs:**
1. Security group with 0.0.0.0/0 SSH access
2. Missing required tags
3. Hardcoded credentials reference
4. Deprecated resource syntax
5. Resource dependency issues

### Mini Exercise: Create Your Own Diagnostic Scenario

**Instructions:**
1. Fork the repository
2. Add a new infrastructure bug to main.tf
3. Update tests to detect the bug
4. Run the diagnostic agent
5. Review AI-generated diagnosis

---

## SECTION 2: AI-ENHANCED DEVELOPMENT LIFECYCLE

### Demo: Release Readiness Agent

**Objective:** Show AI agent evaluating deployment readiness using quality gates

**Structure:**
1. **Setup Phase** (2 minutes)
   - Show application code with tests
   - Display quality gate configuration
   - Review metrics thresholds

2. **Pipeline Execution** (3 minutes)
   - Trigger via pull request
   - Run tests and collect metrics
   - Execute security scans
   - Gather performance data

3. **AI Evaluation** (3 minutes)
   - Agent analyzes all quality gates
   - Generates release decision
   - Provides detailed rationale
   - Suggests improvements

**GitHub Repository Structure:**
```
section2-release-readiness/
├── .github/
│   └── workflows/
│       ├── quality-gates.yml     # Main pipeline
│       └── ai-evaluation.yml     # AI analysis step
├── src/
│   ├── app.py                    # Sample application
│   ├── utils.py
│   └── __init__.py
├── tests/
│   ├── test_app.py               # Unit tests
│   ├── test_integration.py
│   ├── test_performance.py
│   └── conftest.py
├── config/
│   └── quality-gates.yml         # Thresholds configuration
├── release_agent/
│   ├── evaluator.py              # Main evaluation logic
│   ├── quality_checks/
│   │   ├── coverage_check.py
│   │   ├── performance_check.py
│   │   ├── security_check.py
│   │   └── complexity_check.py
│   ├── decision_engine.py
│   └── prompts/
│       └── release_evaluation.txt
├── .env.example
└── README.md
```

**Quality Gates:**
- Test Coverage: ≥80% line coverage
- Performance: P95 latency increase ≤10%
- Security: 0 critical, <5 high severity
- Complexity: Cyclomatic complexity <10

### Mini Exercise: Adjust Quality Gates

**Instructions:**
1. Fork the demo repository
2. Edit .github/quality-gates.yml
3. Adjust thresholds (make stricter or more lenient)
4. Create pull request to trigger pipeline
5. Use Claude to analyze results
6. Write deployment decision rationale

---

## SECTION 3: OPERATIONAL INTELLIGENCE

### Demo: Log Analysis & Incident Correlation Agent

**Objective:** Show AI agent analyzing logs, correlating incidents, and suggesting remediation

**Structure:**
1. **Incident Simulation** (2 minutes)
   - Deploy application with latent bug
   - Trigger error conditions
   - Show scattered log entries

2. **Agent Analysis** (4 minutes)
   - Agent ingests logs from multiple sources
   - Correlates error patterns
   - Maps dependencies
   - Identifies root cause

3. **Remediation** (2 minutes)
   - Agent suggests fixes
   - Provides runbook
   - Estimates impact
   - Generates postmortem template

**GitHub Repository Structure:**
```
section3-operational-intelligence/
├── .github/
│   └── workflows/
│       └── incident-analysis.yml
├── app/
│   ├── microservice-a/
│   ├── microservice-b/
│   └── microservice-c/
├── logs/
│   ├── app-logs/
│   ├── infrastructure-logs/
│   └── metrics/
├── ops_agent/
│   ├── log_ingestion.py
│   ├── pattern_detection.py
│   ├── correlation_engine.py
│   ├── remediation_suggester.py
│   └── prompts/
│       ├── incident_analysis.txt
│       └── remediation_prompt.txt
├── simulations/
│   ├── generate_incident.py      # Creates realistic incidents
│   └── scenarios/
│       ├── database_slowdown.json
│       ├── memory_leak.json
│       └── cascade_failure.json
└── README.md
```

**Simulated Incidents:**
1. Database connection pool exhaustion
2. Memory leak in microservice
3. Cascading failure across services
4. API rate limit exceeded
5. Disk space issue causing failures

### Mini Exercise: Conversational Operations

**Instructions:**
1. Use the incident simulation tool
2. Generate a realistic incident scenario
3. Use Claude conversationally to:
   - "Why did the deployment fail?"
   - "What's the error rate trend?"
   - "Explain this metric spike"
   - "Compare to last release"
4. Review agent's analysis and recommendations

---

## SECTION 4: IMPLEMENTATION STRATEGY

### Demo: Platform Readiness Assessment Agent

**Objective:** Show AI agent evaluating organizational readiness for agentic AI adoption

**Structure:**
1. **Assessment Phase** (3 minutes)
   - Review organization inputs
   - Current platform maturity
   - Team capabilities
   - Infrastructure state

2. **Analysis Phase** (3 minutes)
   - Agent evaluates readiness
   - Identifies gaps
   - Assesses risks
   - Maps to book framework

3. **Recommendations** (2 minutes)
   - Prioritized roadmap
   - Quick wins identified
   - Resource requirements
   - Success metrics

**GitHub Repository Structure:**
```
section4-implementation-strategy/
├── assessments/
│   ├── assessment_form.yml       # Input template
│   ├── examples/
│   │   ├── startup.yml
│   │   ├── enterprise.yml
│   │   └── mid_market.yml
│   └── results/
├── readiness_agent/
│   ├── assessment_engine.py
│   ├── gap_analyzer.py
│   ├── roadmap_generator.py
│   ├── frameworks/
│   │   ├── effective_platform_eng.py  # From your book
│   │   └── maturity_model.py
│   └── prompts/
│       ├── readiness_assessment.txt
│       └── roadmap_generation.txt
├── templates/
│   ├── roadmap_template.md
│   ├── business_case_template.md
│   └── metrics_dashboard.md
└── README.md
```

**Assessment Dimensions:**
- Platform maturity level (1-5)
- Team AI/ML experience
- Infrastructure automation degree
- Monitoring & observability
- Self-service capabilities
- Security & compliance posture

### Mini Exercise: Assess Your Organization

**Instructions:**
1. Fill out assessment form for your organization
2. Run the readiness agent
3. Review gap analysis
4. Use Claude to refine the roadmap
5. Generate business case presentation

---

## SECTION 5: PRACTICAL STARTER KITS

### Demo: End-to-End Agent Deployment

**Objective:** Show complete deployment of a production-ready agent

**Structure:**
1. **Architecture Overview** (2 minutes)
   - Agent components
   - Integration points
   - Deployment model

2. **Deployment** (3 minutes)
   - Use starter kit CLI
   - Configure agent
   - Deploy to infrastructure
   - Verify operation

3. **Operation** (3 minutes)
   - Trigger agent workflows
   - Monitor agent performance
   - Review agent decisions
   - Iterate on prompts

**GitHub Repository Structure:**
```
section5-starter-kits/
├── cli/
│   ├── agent_cli.py              # Command-line tool
│   └── commands/
│       ├── init.py
│       ├── deploy.py
│       ├── configure.py
│       └── monitor.py
├── templates/
│   ├── diagnostic_agent/
│   ├── release_agent/
│   ├── ops_agent/
│   └── custom_agent/
├── deployment/
│   ├── kubernetes/
│   │   ├── agent-deployment.yml
│   │   ├── configmap.yml
│   │   └── secrets.yml
│   ├── docker/
│   │   └── Dockerfile
│   └── terraform/
│       ├── main.tf
│       └── modules/
├── examples/
│   ├── getting_started.md
│   ├── customization_guide.md
│   └── production_checklist.md
└── README.md
```

**Starter Kit Features:**
- Multi-provider LLM support (Claude, OpenAI, with mocks)
- GitHub Actions integration
- Kubernetes-ready
- Observability built-in
- Cost tracking
- Prompt version control

### Mini Exercise: Deploy Your First Agent

**Instructions:**
1. Choose an agent template
2. Customize for your use case
3. Deploy using the CLI
4. Connect to your infrastructure
5. Trigger first agent run
6. Review and iterate

---

## Cross-Cutting Concerns

### Multi-Provider LLM Support

All demos include:
```python
class LLMProvider:
    def __init__(self):
        self.provider = self._detect_provider()
    
    def _detect_provider(self):
        if os.getenv('ANTHROPIC_API_KEY'):
            return 'claude'
        elif os.getenv('OPENAI_API_KEY'):
            return 'openai'
        else:
            return 'mock'  # Realistic fallback
    
    def complete(self, prompt):
        if self.provider == 'claude':
            return self._claude_complete(prompt)
        elif self.provider == 'openai':
            return self._openai_complete(prompt)
        else:
            return self._mock_complete(prompt)
```

### Accessibility Features

- Works on Mac (all demos tested)
- Free tier friendly (<$2 per participant)
- Mock responses when no API key
- Comprehensive README for each repo
- Video walkthroughs available

### Documentation Standards

Each repository includes:
- Clear README with setup instructions
- Architecture diagrams
- Troubleshooting guide
- API key setup instructions
- Expected outputs/screenshots

---

## Demo Timing

| Section | Demo Duration | Exercise Duration | Total |
|---------|---------------|-------------------|-------|
| Section 1 | 7 min | 5 min | 12 min |
| Section 2 | 8 min | 5 min | 13 min |
| Section 3 | 8 min | 5 min | 13 min |
| Section 4 | 8 min | 5 min | 13 min |
| Section 5 | 8 min | 7 min | 15 min |

Total demo/exercise time: ~66 minutes across 5 sections
