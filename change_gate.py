import yaml
import sys


# Step 1: Parse YAML
def parse_input(file_path):
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print("Error: File not found")
        sys.exit(1)
    except Exception as e:
        print("Error reading YAML:", e)
        sys.exit(1)


# Step 2: Validate required fields
def validate_input(data):
    required_fields = ["action", "environment"]

    for field in required_fields:
        if field not in data:
            print(f"Error: Missing required field '{field}'")
            sys.exit(1)


# Step 3: Generate plan
def generate_plan(data):
    plan = []
    plan.append(f"Action: {data.get('action')}")
    plan.append(f"Target: {data.get('resource')}/{data.get('name')}")
    plan.append(f"Environment: {data.get('environment')}")

    if data.get("action") == "scale":
        plan.append(f"Desired replicas: {data.get('replicas')}")

    return plan


# Step 4: Validation rules
def validate_rules(data):
    validations = []
    result = "AUTO-APPROVED"

    action = data.get("action")
    env = data.get("environment")
    replicas = data.get("replicas", 0)

    if action == "delete" and env == "production":
        validations.append("Deletion in production is not allowed")
        result = "BLOCKED"

    elif action == "scale" and env == "production" and replicas > 5:
        validations.append("Production environment detected")
        validations.append("Scaling above threshold requires approval")
        result = "APPROVAL REQUIRED"

    elif action == "apply" and env == "staging":
        validations.append("Safe deployment in staging")
        result = "AUTO-APPROVED"

    else:
        validations.append("No risky conditions detected")
        result = "AUTO-APPROVED"

    return validations, result


# Main
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python change_gate.py <yaml_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    data = parse_input(file_path)
    validate_input(data)

    plan = generate_plan(data)
    validations, result = validate_rules(data)

    print("\nPLAN:")
    for item in plan:
        print("-", item)

    print("\nVALIDATION:")
    for v in validations:
        print("-", v)

    print("\nRESULT:")
    print(result)