from orchestrator.workflow import run_workflow


if __name__ == "__main__":
    sample_task = "Create a Python function that validates email addresses with regex and unit tests."
    result = run_workflow(sample_task)
    print("Workflow finished:")
    print(result)
