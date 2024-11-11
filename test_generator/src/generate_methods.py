from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os


def generate_class_files(
        parsed_data, 
        output_dir, 
        method_template_path, 
        steps_template_path, 
        api_instance_path, 
        apikey, 
        bearer
    ):
    """
    Generates a Python class file for each section in the Swagger spec.

    Parameters:
    - parsed_data (dict): Parsed Swagger data grouped by section.
    - output_dir (str): Directory to save the generated files.
    - method_template_path (str): Path to the Jinja Mehtod template file.
    - apikey (str): API key for the requests.
    - bearer (str): Bearer token for the requests.
    """

    Path(f"{output_dir}/methods").mkdir(parents=True, exist_ok=True)
    Path(f"{output_dir}/steps").mkdir(parents=True, exist_ok=True)
    Path(f"{output_dir}/scenarii").mkdir(parents=True, exist_ok=True)
    
    api_instance_env = Environment(loader=FileSystemLoader(os.path.dirname(api_instance_path)), trim_blocks=True, lstrip_blocks=True)
    api_instance_template = api_instance_env.get_template(os.path.basename(api_instance_path))
    
    api_instance_code = api_instance_template.render()

    output_file_path = os.path.join(output_dir, "methods", "api_instance.py")
    with open(output_file_path, "w") as file:
        file.write(api_instance_code)
    
    methods_env = Environment(loader=FileSystemLoader(os.path.dirname(method_template_path)), trim_blocks=True, lstrip_blocks=True)
    methods_template = methods_env.get_template(os.path.basename(method_template_path))

    steps_env = Environment(loader=FileSystemLoader(os.path.dirname(steps_template_path)), trim_blocks=True, lstrip_blocks=True)
    steps_template = steps_env.get_template(os.path.basename(steps_template_path))

    for section, methods in parsed_data.items():
        class_name = section.capitalize() + 'API'  # Class name for each section

        # Render the class file for each section
        rendered_code = methods_template.render(
            class_name=class_name,
            apikey=apikey,
            bearer=bearer,
            methods=methods
        )

        methods_file_name = f"{section}_api.py"
        # Write to a separate file for each section
        output_file_path = os.path.join(output_dir, "methods", methods_file_name)
        with open(output_file_path, "w") as file:
            file.write(rendered_code)
        
        print(f"Generated file for section '{section}': {output_file_path}")
        
        os.system(f"poetry run ruff check --fix --unsafe-fixes {output_file_path}")

        # Render the class file for each section
        rendered_code = steps_template.render(
            class_name=class_name,
            file_name=methods_file_name,
            methods=methods
        )

        # Write to a separate file for each section
        output_file_path = os.path.join(output_dir, "steps", f"{section}_steps_api.py")
        with open(output_file_path, "w") as file:
            file.write(rendered_code)
        
        os.system(f"poetry run ruff check --fix {output_file_path}")
        
        print(f"Generated file for section '{section}': {output_file_path}")
