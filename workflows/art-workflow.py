"""
Author: ddl-ebrown
"""

from flytekitplugins.domino.helpers import (
    run_domino_job_task,
)
from flytekit import workflow, Artifact

DominoArtifact = Artifact(partition_keys=["type"])

# ReportArtifact = Artifact(partition_keys=[])
# Pricing = Artifact(name="pricing", partition_keys=["region"]) 
# @task def t1() -> Annotated[pd.DataFrame, Pricing], Annotated[float, EstError]:

# df = get_pricing_results()
# dt = get_time() 
# return Pricing.create_from(df, region=”dubai”), 
#     EstError.create_from(msq_error, dataset=”train”, time_partition=dt)
# @task def my_task() -> Annotated[pd.DataFrame, RideCountData(region=Inputs.region)]:

# … return RideCountData.create_from(df, time_partition=datetime.datetime.now())

@workflow
def workflow() -> None:
    """
    pyflyte run --remote workflow.py workflow
    """

    return run_domino_job_task(
        flyte_task_name="SleepTest",
        command="cp model.py /workflow/output/",
        output_specs=[
            
        ],
        # example passing environment and hardware tier name. uses project defaults for everything else that has a default
        use_project_defaults_for_omitted=True,
        hardware_tier_name="Small",
    )