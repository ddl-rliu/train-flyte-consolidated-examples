"""
Author: ddl-galias

Workflow which calls nested workflows.
"""

from flytekitplugins.domino.helpers import run_domino_job_task
from flytekit import workflow


# pyflyte run --remote nested_workflow.py echo_nested_one
@workflow
def echo_nested_one():
    run_domino_job_task(
        "Echo Nested 1-1", 
        "echo nested1-1",
        use_project_defaults_for_omitted=True
    )
    run_domino_job_task(
        "Echo Nested 1-2", 
        "echo nested1-2",
        use_project_defaults_for_omitted=True
    )


# pyflyte run --remote nested_workflow.py echo_nested_one
@workflow
def echo_nested_one_dupe():
    run_domino_job_task(
        "Echo Nested Dupe1-1", 
        "echo nestedDupe1-1",
        use_project_defaults_for_omitted=True
    )
    run_domino_job_task(
        "Echo Nested Dupe1-2", 
        "echo nestedDupe1-2",
        use_project_defaults_for_omitted=True
    )


# pyflyte run --remote nested_workflow.py echo_nested_two
@workflow
def echo_nested_two():
    run_domino_job_task(
        "Echo Nested 2-1", 
        "echo nested2-1",
        use_project_defaults_for_omitted=True
    )
    echo_nested_one()
    echo_nested_one_dupe()


# pyflyte run --remote nested_workflow.py nest_user
@workflow
def wf():
    run_domino_job_task(
        "Echo Nested 3-1", 
        "echo nested3-1",
        use_project_defaults_for_omitted=True
    )
    echo_nested_two()
    return run_domino_job_task(
        "Echo Nested 3-2", 
        "echo nested3-2",
        use_project_defaults_for_omitted=True
    )
