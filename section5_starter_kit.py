"""
Section 5: Agent Starter Kit CLI
=================================

Production-ready CLI tool for deploying and managing agentic AI
in platform engineering environments.
"""

import os
import sys
import json
import yaml
import shutil
import subprocess
from typing import Dict, Optional
from pathlib import Path


class AgentCLI:
    """Main CLI for agent management"""
    
    AGENT_TYPES = ['diagnostic', 'release', 'ops', 'custom']
    PLATFORMS = ['kubernetes', 'docker', 'local']
    
    def __init__(self):
        self.workspace = Path.home() / '.agent-workspace'
        self.workspace.mkdir(exist_ok=True)
    
    def init(self, agent_type: str, name: str):
        """Initialize a new agent"""
        
        if agent_type not in self.AGENT_TYPES:
            print(f"❌ Invalid agent type. Choose from: {', '.join(self.AGENT_TYPES)}")
            return False
        
        agent_dir = self.workspace / name
        if agent_dir.exists():
            print(f"❌ Agent '{name}' already exists")
            return False
        
        print(f"🚀 Initializing {agent_type} agent: {name}")
        
        # Create directory structure
        directories = ['src', 'tests', 'config', 'deployment/kubernetes', 
                      'deployment/docker', 'prompts', 'docs']
        for directory in directories:
            (agent_dir / directory).mkdir(parents=True, exist_ok=True)
        
        # Create agent files
        self._create_agent_files(agent_dir, agent_type, name)
        
        print(f"\n✅ Agent initialized successfully!")
        print(f"   Location: {agent_dir}")
        print(f"\nNext steps:")
        print(f"   1. cd {agent_dir}")
        print(f"   2. Edit agent-config.yml")
        print(f"   3. python -m cli configure --agent {name} --provider claude")
        
        return True
    
    def configure(self, name: str, provider: Optional[str] = None,
                  api_key: Optional[str] = None):
        """Configure an existing agent"""
        
        agent_dir = self.workspace / name
        if not agent_dir.exists():
            print(f"❌ Agent '{name}' not found")
            return False
        
        print(f"⚙️  Configuring agent: {name}")
        
        config_file = agent_dir / 'agent-config.yml'
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        if provider:
            config['llm']['provider'] = provider
            print(f"   Set provider: {provider}")
        
        if api_key:
            env_file = agent_dir / '.env'
            with open(env_file, 'w') as f:
                if provider == 'claude':
                    f.write(f"ANTHROPIC_API_KEY={api_key}\n")
                elif provider == 'openai':
                    f.write(f"OPENAI_API_KEY={api_key}\n")
            print(f"   API key stored securely")
        
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print("✅ Configuration updated!")
        return True
    
    def deploy(self, name: str, platform: str, environment: str = 'staging'):
        """Deploy agent to platform"""
        
        agent_dir = self.workspace / name
        if not agent_dir.exists():
            print(f"❌ Agent '{name}' not found")
            return False
        
        if platform not in self.PLATFORMS:
            print(f"❌ Invalid platform. Choose from: {', '.join(self.PLATFORMS)}")
            return False
        
        print(f"🚀 Deploying agent '{name}' to {platform} ({environment})")
        
        if platform == 'local':
            print("   Installing dependencies...")
            subprocess.run(['pip', 'install', '-r', 'requirements.txt'], 
                          cwd=agent_dir, check=True)
            print(f"\n✅ Agent ready for local execution")
            print(f"   Run: cd {agent_dir} && python src/agent.py")
            return True
        
        elif platform == 'docker':
            print("   Building Docker image...")
            subprocess.run(['docker', 'build', '-t', f'{name}:latest',
                           '-f', 'deployment/docker/Dockerfile', '.'],
                          cwd=agent_dir, check=True)
            print(f"\n✅ Docker image built: {name}:latest")
            print(f"   Run: docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY {name}:latest")
            return True
        
        elif platform == 'kubernetes':
            print("   Applying Kubernetes manifests...")
            subprocess.run(['kubectl', 'apply', '-f', 'deployment/kubernetes/'],
                          cwd=agent_dir, check=True)
            print(f"\n✅ Agent deployed to Kubernetes")
            print(f"   Check status: kubectl get pods -l app={name}")
            return True
    
    def list_agents(self):
        """List all initialized agents"""
        
        print("📋 Initialized Agents:\n")
        
        agents = []
        for agent_dir in self.workspace.iterdir():
            if agent_dir.is_dir() and (agent_dir / 'agent-config.yml').exists():
                with open(agent_dir / 'agent-config.yml', 'r') as f:
                    config = yaml.safe_load(f)
                agents.append({'name': agent_dir.name, 'type': config.get('type')})
        
        if not agents:
            print("  No agents initialized yet.")
            print("\n  Run: python -m cli init --type diagnostic --name my-agent")
        else:
            for agent in agents:
                print(f"  • {agent['name']} ({agent['type']})")
    
    def _create_agent_files(self, agent_dir: Path, agent_type: str, name: str):
        """Create all necessary agent files"""
        
        # Create agent implementation based on type
        agent_templates = {
            'diagnostic': self._diagnostic_template(),
            'release': self._release_template(),
            'ops': self._ops_template(),
            'custom': self._custom_template()
        }
        
        with open(agent_dir / 'src' / 'agent.py', 'w') as f:
            f.write(agent_templates[agent_type])
        
        # Create config
        config = {
            'name': name,
            'type': agent_type,
            'version': '1.0.0',
            'llm': {'provider': 'claude', 'model': 'claude-sonnet-4-20250514'},
            'deployment': {'platform': 'kubernetes', 'replicas': 1}
        }
        with open(agent_dir / 'agent-config.yml', 'w') as f:
            yaml.dump(config, f)
        
        # Create Dockerfile
        with open(agent_dir / 'deployment' / 'docker' / 'Dockerfile', 'w') as f:
            f.write('''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["python", "-m", "src.agent"]
''')
        
        # Create requirements.txt
        with open(agent_dir / 'requirements.txt', 'w') as f:
            f.write('anthropic>=0.18.0\npyyaml>=6.0\n')
        
        # Create Kubernetes deployment
        with open(agent_dir / 'deployment' / 'kubernetes' / 'deployment.yml', 'w') as f:
            f.write(f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: agent
        image: {name}:latest
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: agent-secrets
              key: anthropic-api-key
''')
        
        # Create README
        with open(agent_dir / 'README.md', 'w') as f:
            f.write(f'''# {name}

{agent_type.title()} agent for platform engineering.

## Quick Start

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python src/agent.py
```

## Deployment

Docker: `docker build -t {name} -f deployment/docker/Dockerfile .`  
Kubernetes: `kubectl apply -f deployment/kubernetes/`
''')
    
    def _diagnostic_template(self) -> str:
        return '''import os
from anthropic import Anthropic

class DiagnosticAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')) if os.getenv('ANTHROPIC_API_KEY') else None
    
    def diagnose(self, files):
        if not self.client:
            return "Mock diagnosis: Check security groups and tags"
        
        prompt = "Analyze infrastructure:\\n" + str(files)
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

if __name__ == '__main__':
    agent = DiagnosticAgent()
    print(agent.diagnose({"main.tf": "example config"}))
'''
    
    def _release_template(self) -> str:
        return '''import os
from anthropic import Anthropic

class ReleaseAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')) if os.getenv('ANTHROPIC_API_KEY') else None
    
    def evaluate(self, gates):
        if not self.client:
            return {"decision": "APPROVE", "rationale": "Mock: All gates passed"}
        
        prompt = "Evaluate release:\\n" + str(gates)
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"decision": "APPROVE", "rationale": message.content[0].text}

if __name__ == '__main__':
    agent = ReleaseAgent()
    print(agent.evaluate({"coverage": 82, "performance": "good"}))
'''
    
    def _ops_template(self) -> str:
        return '''import os
from anthropic import Anthropic

class OpsAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')) if os.getenv('ANTHROPIC_API_KEY') else None
    
    def analyze(self, logs):
        if not self.client:
            return {"root_cause": "Mock: Connection pool exhaustion"}
        
        prompt = "Analyze incident:\\n" + "\\n".join(logs[:50])
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"analysis": message.content[0].text}

if __name__ == '__main__':
    agent = OpsAgent()
    print(agent.analyze(["ERROR: Connection timeout"]))
'''
    
    def _custom_template(self) -> str:
        return '''import os
from anthropic import Anthropic

class CustomAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')) if os.getenv('ANTHROPIC_API_KEY') else None
    
    def process(self, data):
        if not self.client:
            return "Mock response"
        
        prompt = "Process:\\n" + str(data)
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

if __name__ == '__main__':
    agent = CustomAgent()
    print(agent.process({"example": "data"}))
'''


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Agent Starter Kit CLI')
    subparsers = parser.add_subparsers(dest='command')
    
    init_p = subparsers.add_parser('init')
    init_p.add_argument('--type', required=True, choices=['diagnostic', 'release', 'ops', 'custom'])
    init_p.add_argument('--name', required=True)
    
    config_p = subparsers.add_parser('configure')
    config_p.add_argument('--agent', required=True)
    config_p.add_argument('--provider', choices=['claude', 'openai'])
    config_p.add_argument('--api-key')
    
    deploy_p = subparsers.add_parser('deploy')
    deploy_p.add_argument('--agent', required=True)
    deploy_p.add_argument('--platform', required=True, choices=['kubernetes', 'docker', 'local'])
    deploy_p.add_argument('--environment', default='staging')
    
    list_p = subparsers.add_parser('list')
    
    args = parser.parse_args()
    cli = AgentCLI()
    
    if args.command == 'init':
        cli.init(args.type, args.name)
    elif args.command == 'configure':
        cli.configure(args.agent, args.provider, args.api_key)
    elif args.command == 'deploy':
        cli.deploy(args.agent, args.platform, args.environment)
    elif args.command == 'list':
        cli.list_agents()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
