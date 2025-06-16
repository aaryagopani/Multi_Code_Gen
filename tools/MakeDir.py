import os
import json

def create_structure(base_path, structure):
    for name, content in structure.items():
        current_path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(current_path, exist_ok=True)
            create_structure(current_path, content)
        else:
            os.makedirs(base_path, exist_ok=True)  # Ensures parent path exists
            with open(current_path, 'w') as f:
                f.write(f"// {content}\n")

def generate_project(json_data: dict, user_id: str):
    project_name = json_data['projectName']
    # Construct path: projects/user_id/temp/projectName
    base_path = os.path.join("projects", user_id, "temp", project_name)

    os.makedirs(base_path, exist_ok=True)  # Recursive dir creation
    print(f"📁 Creating project at: {base_path}")

    root_structure = json_data['directory']['root']
    create_structure(base_path, root_structure)

    print(f"✅ Project successfully generated at: {base_path}")