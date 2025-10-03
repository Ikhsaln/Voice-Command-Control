# 🛠️ Development Guide - Voice Control Relay System

Panduan lengkap untuk developer yang ingin berkontribusi atau mengembangkan sistem voice control relay.

## 🚀 Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tools
- Code editor (VSCode recommended)

### Initial Setup
```bash
# Clone repository
git clone <repository-url>
cd voice-control-relay

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Install pre-commit hooks
pre-commit install

# Setup development database (if using)
# Copy and modify configuration files
cp .env.example .env
```

### Development Dependencies
```txt
# requirements-dev.txt
pytest==7.4.0
pytest-cov==4.1.0
black==23.7.0
flake8==6.0.0
mypy==1.5.1
pre-commit==3.4.0
sphinx==7.1.2
```

## 🏗️ Project Structure

```
voice-control-relay/
├── app.py                      # Main Flask application
├── voice_control.py            # Voice recognition engine
├── AutomationVoice.py          # Device management service
├── middleware/
│   ├── mqtt_handler.py         # MQTT communication
│   ├── logging.py              # Logging utilities
│   └── network_utils.py        # Network utilities
├── templates/
│   ├── index.html              # Main web interface
│   └── index_modern.html       # Alternative interface
├── static/                     # Static assets (CSS, JS, images)
├── JSON/
│   └── automationVoiceConfig.json  # Device configurations
├── logs/                       # Application logs
├── tests/                      # Unit and integration tests
│   ├── test_voice_control.py
│   ├── test_api.py
│   ├── test_mqtt.py
│   └── conftest.py
├── docs/                       # Documentation
├── scripts/                    # Development scripts
├── .env.example               # Environment template
├── .pre-commit-config.yaml    # Pre-commit hooks
├── pyproject.toml            # Python project configuration
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── README.md
```

## 🔧 Development Workflow

### 1. Create Feature Branch
```bash
# Create and switch to feature branch
git checkout -b feature/new-feature-name

# Or for bug fixes
git checkout -b bugfix/issue-description
```

### 2. Code Development
```bash
# Run development server
FLASK_DEBUG=True python app.py

# Run tests continuously
pytest-watch tests/

# Check code quality
black .                    # Format code
flake8 .                   # Lint code
mypy .                     # Type check
```

### 3. Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_voice_control.py

# Run tests matching pattern
pytest -k "voice" -v
```

### 4. Commit Changes
```bash
# Stage changes
git add .

# Commit with conventional format
git commit -m "feat: add new voice command support

- Add support for toggle commands
- Improve speech recognition accuracy
- Add unit tests for new functionality"

# Pre-commit hooks will run automatically
```

### 5. Push and Create PR
```bash
# Push branch
git push origin feature/new-feature-name

# Create Pull Request on GitHub
# Add description, link to issues, add reviewers
```

## 🧪 Testing Strategy

### Unit Tests
```python
# tests/test_voice_control.py
import pytest
from voice_control import VoiceControl

class TestVoiceControl:
    def test_command_analysis_on(self):
        vc = VoiceControl()
        action = vc.analyze_command_action("nyalakan lampu")
        assert action == "on"

    def test_object_extraction(self):
        vc = VoiceControl()
        text = "nyalakan lampu utama"
        action = vc.analyze_command_action(text)
        object_name = vc.extract_object_name(text, action)
        assert object_name == "lampu utama"

    def test_invalid_command(self):
        vc = VoiceControl()
        action = vc.analyze_command_action("invalid command")
        assert action is None
```

### Integration Tests
```python
# tests/test_api.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_configurations(client):
    response = client.get('/api/configurations')
    assert response.status_code == 200
    data = response.get_json()
    assert 'success' in data
    assert 'configurations' in data

def test_create_configuration(client):
    config_data = {
        'device_name': 'RelayMini1',
        'object_name': 'test lamp',
        'pin': 1
    }
    response = client.post('/api/configurations',
                          json=config_data,
                          content_type='application/json')
    assert response.status_code == 201
```

### End-to-End Tests
```python
# tests/test_e2e.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_voice_control_workflow(browser):
    browser.get('http://localhost:8000')

    # Test configuration creation
    new_config_btn = browser.find_element(By.ID, 'new-config-btn')
    new_config_btn.click()

    # Fill form
    browser.find_element(By.ID, 'device-select').send_keys('RelayMini1')
    browser.find_element(By.ID, 'object-name').send_keys('test lamp')
    browser.find_element(By.ID, 'pin-select').send_keys('1')

    # Submit
    browser.find_element(By.ID, 'create-config').click()

    # Verify success
    success_msg = browser.find_element(By.CLASS_NAME, 'success-message')
    assert 'created successfully' in success_msg.text
```

## 📝 Code Quality

### Code Formatting
```bash
# Format all Python files
black .

# Check formatting without changes
black --check .

# Format specific file
black voice_control.py
```

### Linting
```bash
# Run flake8
flake8 .

# Run with specific rules
flake8 --select=E9,F63,F7,F82 --show-source --statistics

# Exclude files
flake8 --exclude=.git,__pycache__,venv
```

### Type Checking
```bash
# Run mypy
mypy .

# Check specific file
mypy voice_control.py

# Strict mode
mypy --strict app.py
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mypy
    rev: 1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## 🔧 Core Components

### Voice Control Engine

#### Architecture
```python
class VoiceControl:
    def __init__(self, config_file="JSON/automationVoiceConfig.json"):
        self.recognizer = sr.Recognizer()
        self.mqtt = MQTTHandler()
        self.logger = setup_logging()

    def process_voice_command(self, text):
        # 1. Analyze command action
        action = self.analyze_command_action(text)

        # 2. Extract object name
        object_name = self.extract_object_name(text, action)

        # 3. Find configuration
        config = self.find_configuration_by_object_name(object_name)

        # 4. Control device
        return self.control_relay(config, action)
```

#### Key Methods
- `analyze_command_action()`: Parse voice commands
- `extract_object_name()`: Extract device names
- `find_configuration_by_object_name()`: Match configurations
- `control_relay()`: Send MQTT commands

### Flask Application

#### Route Structure
```python
# app.py
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/configurations', methods=['GET', 'POST'])
def configurations():
    if request.method == 'POST':
        # Create new configuration
        pass
    else:
        # Return all configurations
        pass

@app.route('/api/voice/test', methods=['POST'])
def test_voice_command():
    # Test voice command processing
    pass
```

#### Error Handling
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
```

### MQTT Handler

#### Connection Management
```python
class MQTTHandler:
    def __init__(self, broker='localhost', port=1883):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.connected = False

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            self.connected = True
            return True
        except Exception as e:
            log_simple(f"MQTT connection failed: {e}", "ERROR")
            return False

    def publish(self, topic, payload):
        if not self.connected:
            return False
        try:
            self.client.publish(topic, json.dumps(payload))
            return True
        except Exception as e:
            log_simple(f"MQTT publish failed: {e}", "ERROR")
            return False
```

## 🎨 Frontend Development

### HTML Templates
```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Control System</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div id="app" class="container mx-auto px-4 py-8">
        <!-- Vue.js or vanilla JS components -->
    </div>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
```

### JavaScript Architecture
```javascript
// static/js/app.js
class VoiceControlApp {
    constructor() {
        this.configurations = [];
        this.init();
    }

    async init() {
        await this.loadConfigurations();
        this.setupEventListeners();
        this.startStatusUpdates();
    }

    async loadConfigurations() {
        const response = await fetch('/api/configurations');
        const data = await response.json();
        this.configurations = data.configurations;
        this.renderConfigurations();
    }

    setupEventListeners() {
        // Voice control buttons
        document.getElementById('start-voice').addEventListener('click', () => {
            this.startVoiceControl();
        });

        // Configuration form
        document.getElementById('config-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.createConfiguration();
        });
    }

    async startVoiceControl() {
        const response = await fetch('/api/voice/start', { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            this.showNotification('Voice control started', 'success');
        }
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    new VoiceControlApp();
});
```

## 🔄 API Development

### Adding New Endpoints
```python
# In app.py
@app.route('/api/devices/<device_name>/status', methods=['GET'])
def get_device_status(device_name):
    """Get real-time status of specific device"""
    # Implementation
    pass

@app.route('/api/voice/commands', methods=['GET'])
def get_supported_commands():
    """Get list of supported voice commands"""
    commands = {
        'indonesian': [
            {'command': 'nyalakan [nama]', 'action': 'on'},
            {'command': 'matikan [nama]', 'action': 'off'},
            {'command': 'toggle [nama]', 'action': 'toggle'}
        ],
        'english': [
            {'command': 'turn on [name]', 'action': 'on'},
            {'command': 'turn off [name]', 'action': 'off'}
        ]
    }
    return jsonify({'success': True, 'commands': commands})
```

### API Versioning
```python
# Version prefix for API routes
API_PREFIX = '/api/v1'

@app.route(f'{API_PREFIX}/configurations')
def get_configurations_v1():
    # Version 1 implementation
    pass

# Future version
@app.route('/api/v2/configurations')
def get_configurations_v2():
    # Version 2 with new features
    pass
```

## 🔒 Security Considerations

### Input Validation
```python
from marshmallow import Schema, fields, ValidationError

class ConfigurationSchema(Schema):
    device_name = fields.Str(required=True, validate=lambda x: len(x) <= 50)
    object_name = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    pin = fields.Int(required=True, validate=lambda x: 1 <= x <= 8)
    description = fields.Str(validate=lambda x: len(x) <= 200)

@app.route('/api/configurations', methods=['POST'])
def create_configuration():
    schema = ConfigurationSchema()
    try:
        data = schema.load(request.get_json())
        # Process validated data
        return jsonify({'success': True})
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400
```

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

@app.route('/api/voice/start')
@limiter.limit("10 per minute")
def start_voice_control():
    # Rate limited endpoint
    pass
```

## 📊 Monitoring & Logging

### Structured Logging
```python
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage
logger.info("Voice command processed", command="nyalakan lampu", action="on", user_id="user123")
```

### Metrics & Monitoring
```python
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
VOICE_COMMANDS_TOTAL = Counter('voice_commands_total', 'Total voice commands processed', ['action', 'status'])
COMMAND_PROCESSING_TIME = Histogram('command_processing_seconds', 'Time spent processing commands')

@app.route('/metrics')
def metrics():
    return generate_latest()

def process_voice_command(command):
    with COMMAND_PROCESSING_TIME.time():
        # Process command
        result = process_command_logic(command)

        # Record metrics
        VOICE_COMMANDS_TOTAL.labels(
            action=result.get('action'),
            status='success' if result.get('success') else 'failure'
        ).inc()

        return result
```

## 🚀 Deployment & CI/CD

### GitHub Actions CI
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Lint with flake8
      run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

    - name: Test with pytest
      run: pytest --cov=app --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

### Docker Development
```dockerfile
# Dockerfile.dev
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

# Copy source code
COPY . .

# Run development server
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000", "--debug"]
```

### Local Development with Docker
```bash
# Build development image
docker build -f Dockerfile.dev -t voice-control-dev .

# Run with volume mounting
docker run -p 8000:8000 -v $(pwd):/app voice-control-dev

# Run tests in container
docker run --rm voice-control-dev pytest
```

## 🤝 Contributing Guidelines

### Code Review Process
1. **Automated Checks**: CI must pass all tests and linting
2. **Manual Review**: At least one maintainer review required
3. **Testing**: New features must include comprehensive tests
4. **Documentation**: Update docs for API changes

### Commit Message Convention
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

Examples:
```
feat(voice): add support for custom wake words
fix(api): resolve race condition in device discovery
docs(api): update endpoint documentation
test(voice): add integration tests for speech recognition
```

### Branch Naming
- `feature/description`: New features
- `bugfix/issue-number-description`: Bug fixes
- `hotfix/critical-issue`: Critical fixes
- `docs/update-readme`: Documentation updates

## 📚 Additional Resources

### Learning Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SpeechRecognition Library](https://github.com/Uberi/speech_recognition)
- [Paho MQTT Client](https://www.eclipse.org/paho/)
- [Tailwind CSS](https://tailwindcss.com/)

### Development Tools
- [VSCode Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Postman](https://www.postman.com/) - API testing
- [MQTT Explorer](https://mqtt-explorer.com/) - MQTT debugging
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Community
- [GitHub Issues](https://github.com/your-repo/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/your-repo/discussions) - General discussions
- [Stack Overflow](https://stackoverflow.com/questions/tagged/flask) - Technical questions

---

**Happy coding! 🎉** Remember to write tests, follow conventions, and keep the codebase clean and maintainable.
