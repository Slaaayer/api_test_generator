from test_generator.src.generate_methods import generate_class_files
from test_generator.src.swagger_parsing import parse_swagger


if __name__ == "__main__":
    parsed_data = parse_swagger("https://petstore.swagger.io/v2/swagger.json")
    generate_class_files(parsed_data, 
                        output_dir='output/pet_store_tests', 
                        method_template_path='templates/methods_template.jinja',
                        steps_template_path='templates/steps_template.jinja',
                        api_instance_path='templates/api_instance_template.jinja',
                        apikey="your_api_key", 
                        bearer="your_bearer_token")