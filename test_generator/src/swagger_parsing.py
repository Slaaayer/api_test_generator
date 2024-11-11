import requests
import json

def resolve_ref(ref, swagger_spec):
    """Recursively resolve a $ref in the Swagger spec."""
    keys = ref.lstrip("#/").split("/")
    ref_data = swagger_spec
    for key in keys:
        ref_data = ref_data.get(key)
        if ref_data is None:
            raise ValueError(f"Reference '{ref}' not found in Swagger spec.")
    return ref_data

def get_body_parameters(param_info, swagger_spec):
    """
    Extract parameters and their types from a Swagger schema, following references recursively.
    
    Args:
    - param_info: dict containing the body parameter schema (e.g., {"in": "body", "schema": {...}})
    - swagger_spec: dict containing the entire Swagger specification
    
    Returns:
    - dict: A dictionary where keys are parameter names and values are types
    """
    def extract_properties(schema):
        parameters = {}
        
        # Handle case where schema has a $ref directly
        if "$ref" in schema:
            schema = resolve_ref(schema["$ref"], swagger_spec)
        
        # If schema is an object, iterate over its properties
        if schema.get("type") == "object" and "properties" in schema:
            for prop, prop_info in schema["properties"].items():
                if "$ref" in prop_info:
                    # Recursively resolve referenced properties
                    resolved_schema = resolve_ref(prop_info["$ref"], swagger_spec)
                    parameters[prop] = extract_properties(resolved_schema)
                else:
                    # Direct property without further references
                    parameters[prop] = prop_info.get("type", "unknown")
        
        # Handle arrays, which may contain items with references
        elif schema.get("type") == "array" and "items" in schema:
            item_schema = schema["items"]
            if "$ref" in item_schema:
                # Resolve reference within array items
                resolved_schema = resolve_ref(item_schema["$ref"], swagger_spec)
                parameters["items"] = extract_properties(resolved_schema)
            else:
                # Direct type within array items
                parameters["items"] = item_schema.get("type", "unknown")
        
        return parameters
    
    # Start processing the provided parameter's schema
    body_params = extract_properties(param_info["schema"])
    return body_params

def parse_swagger(swagger, format="url"):
    """
    Parses a Swagger JSON specification and extracts API endpoint details,
    organized by sections (tags).
    
    Parameters:
    - swagger (str): URL of the Swagger JSON file.
    - format (str): Format of the Swagger, either URL or Json file 

    Returns:
    - Dictionary with tags as keys, and a list of endpoint details per tag.
    """
    if format == "url":
        swagger_spec = requests.get(swagger).json()
    elif format == "file":
        with open(swagger, 'r') as f:
            swagger_spec = json.load(f)
    api_sections = {}

    for path, methods in swagger_spec.get('paths', {}).items():
        for method, details in methods.items():
            tags = details.get('tags', ['default'])
            for tag in tags:
                if tag not in api_sections:
                    api_sections[tag] = []
                
                api_info = {
                    'endpoint': path,
                    'method': method.upper(),
                    'name': details.get('operationId', f"{method}_{path.replace('/', '_').strip('_')}"),
                    'description': details.get('summary', ''),
                    'params': [],
                    'query_params': {},
                    'body': {},
                    'formdata': {},
                    'header': {},
                }

                responses = details.get('responses', {})
                if '200' in responses and 'schema' in responses['200']:
                    api_info['schema'] = responses['200']['schema']

                # Extract parameters for the endpoint
                parameters = details.get('parameters', [])
                for param in parameters:
                    param_info = {
                        'name': param.get('name'),
                        'in': param.get('in'),  # Location of the parameter: query, path, body, etc.
                        'required': param.get('required', False),
                        'type': param.get('type', 'string'),
                        'schema': param.get('schema', None)
                    }
                    api_info['params'].append(param_info)

                    # Categorize query and body parameters
                    if param_info['in'] == 'query':
                        api_info['query_params'][param_info['name']] = param_info['type']
                    elif param_info['in'] == 'body':
                        try:
                            api_info['body'] = get_body_parameters(param_info, swagger_spec)
                        except Exception:
                            api_info['body'] = {'body': 'data'}
                    elif param_info['in'] == 'formData':
                        api_info['formdata'][param_info['name']] = param_info['type']
                    elif param_info['in'] == 'header':
                        api_info['header'][param_info['name']] = param_info['type']

                api_sections[tag].append(api_info)

    return api_sections
