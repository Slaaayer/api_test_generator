# API Test Generator

## Overview

API Test Generator is a Python tool that automatically generates test methods and steps for API endpoints based on Swagger/OpenAPI specifications. This project simplifies the process of creating comprehensive API tests by parsing Swagger JSON files and generating Python test classes and methods.

## Features

- Automatically parse Swagger/OpenAPI JSON specifications
- Generate API method classes for different endpoint sections
- Create test steps for each API endpoint
- Support for various parameter types (query, body, header, formData)
- Code formatting with Ruff

## Prerequisites

- Python 3.10+
- Poetry for dependency management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Slaaayer/api_test_generator.git
cd api_test_generator
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Usage

### Basic Example

```python
from test_generator.src.generate_methods import generate_class_files
from test_generator.src.swagger_parsing import parse_swagger

# Parse Swagger specification
parsed_data = parse_swagger("https://petstore.swagger.io/v2/swagger.json")

# Generate test files
generate_class_files(
    parsed_data, 
    output_dir='output/pet_store_tests', 
    method_template_path='templates/methods_template.jinja',
    steps_template_path='templates/steps_template.jinja',
    api_instance_path='templates/api_instance_template.jinja',
    apikey="your_api_key", 
    bearer="your_bearer_token"
)
```

### Supported Swagger Parsing Options

- URL-based parsing: Provide a URL to a Swagger JSON specification
- File-based parsing: Load Swagger specification from a local JSON file

## Project Structure

- `src/swagger_parsing.py`: Swagger specification parser
- `src/generate_methods.py`: Test method and step generation
- `templates/`: Jinja2 templates for code generation
- `test/pet_store.py`: Example usage script

## Dependencies

- requests: HTTP requests
- jsonschema: JSON validation
- jinja2: Template rendering
- r2c: Additional utilities
- ruff: Code formatting and linting

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Contact

Ayoub BOUNAGA - ayoubebounaga@gmail.com

Project Link: [https://github.com/Slaaayer/api_test_generator](https://github.com/Slaaayer/api_test_generator)