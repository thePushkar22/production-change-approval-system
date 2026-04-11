from fastapi import FastAPI

app = FastAPI(
    title="Production Change Approval System",
    description="A rule-based system to validate infrastructure changes before execution",
    version="1.0.0"
)


# --- Your logic functions ---

def generate_plan(data):
    plan = []
    plan.append(f"Action: {data.get('action')}")
    plan.append(f"Target: {data.get('resource')}/{data.get('name')}")
    plan.append(f"Environment: {data.get('environment')}")

    if data.get("action") == "scale":
        plan.append(f"Desired replicas: {data.get('replicas')}")

    return plan


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


# --- API Endpoint ---

from fastapi import Body

@app.post("/validate-change", summary="Validate infrastructure change")
def validate_change(
    data: dict = Body(
        example={
            "action": "scale",
            "resource": "deployment",
            "name": "payment-service",
            "replicas": 10,
            "environment": "production"
        }
    )
):
    plan = generate_plan(data)
    validations, result = validate_rules(data)

    return {
        "plan": plan,
        "validation": validations,
        "result": result
    }