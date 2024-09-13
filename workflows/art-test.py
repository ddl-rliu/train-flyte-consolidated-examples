"""
Author: ddl-ebrown

The workflow creates a single artifact.
"""

from flytekitplugins.domino.helpers import DominoJobTask, DominoJobConfig, Input, Output
from flytekit import workflow, dynamic
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, Optional, List, Dict, Annotated, Tuple, NamedTuple
from flytekit import Artifact as art
import uuid

Artifact = art(name="default", partition_keys=["file", "type", "group"], version=str(uuid.uuid4()))

@workflow
def wf() -> Annotated[FlyteFile, Artifact(file="processed.sas7bdat", type="data", group="task_output")]: 
    """
    pyflyte run --remote test.py training_workflow --data_path /mnt/data.csv
    """

    data_prep_results = DominoJobTask(    
        name="Prepare data",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/scripts/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            "processed_data": FlyteFile,
        },
        use_latest=True,
    )(data_path="/mnt/train-flyte-consolidated-examples/data/data.csv")

    return data_prep_results['processed_data_out']
