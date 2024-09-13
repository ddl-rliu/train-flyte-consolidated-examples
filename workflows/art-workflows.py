"""
Author: ddl-ebrown

The workflow returns many artifacts outputs and regular outputs.
"""

# example code from https://github.com/ddl-jwu/domino-flows-playground

from flytekitplugins.domino.helpers import DominoJobTask, DominoJobConfig, Input, Output
from flytekit import workflow, dynamic
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, Optional, List, Dict, Annotated, Tuple, NamedTuple
from flytekit import Artifact as art

# Ideally we need to track 3 key pieces of data
# specific file name
# group name (artifact belongs to)
# type (type - data, model or report)

# TODO: how can callers be allowed to override the name property on each artifact?
# TODO: is there a way to set a default value for type? (to just plain "report")
Artifact = art(name="default", partition_keys=["file", "type", "group"])


# old code
# DominoData = Artifact(name="dominoData", type="data")
# PrepData = Artifact(name="prepData", partition_keys=["report_name"])
# TrainingData = Artifact(name="trainingData", partition_keys=["report_name"])

# TODO: users can still put there single artifact file into multiple types?
MultiPart = art(name="multipartition", partition_keys=["partition1", "partition2"])

# TODO: create a new workflow that uses NamedTuple instead to see how the json gets spit out
@workflow
def wf() -> Tuple[
    # Error - Binding a partition partition1's value dynamically is not allowed for workflows
    # Annotated[FlyteFile, Artifact(name="generic", partition_keys=["partition1", "partition2"])],
    Annotated[FlyteFile, art(name="generic")],
    # Error - Partition key name not found in ['partition1', 'partition2']
    # really the error is that name can't be specified again
    # Annotated[FlyteFile, MultiPart(name="generic", partition1="foo", partition2="bar")],
    Annotated[FlyteFile, MultiPart(partition1="foo", partition2="bar")],
    Annotated[FlyteFile, MultiPart(partition1="bar", partition2="foo")],

    # files that are annotated with the name "default" -- not ideal, but works
    Annotated[FlyteFile, Artifact(file="foo.pdf", type="report", group="report_foo")], 
    Annotated[FlyteFile, Artifact(file="bar.pdf", type="report", group="report_bar")],
    # normal workflow output with no annotations
    FlyteFile
    ]: 
    """
    pyflyte run --remote workflows.py training_workflow --data_path /mnt/data.csv
    """

    data_prep_results = DominoJobTask(    
        name="Prepare data",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        # TODO: NOTE: interestingly, type= doesn't need to be specified here??
        outputs={
            # this output is consumed by a subsequent task but also marked as an artifact
            "processed_data_out": Annotated[FlyteFile, Artifact(file="processed.sas7bdat", group="task_output")],
            # no downstream consumers -- simply an artifact output from an intermediate node in the graph
            "processed_data_out2": Annotated[FlyteFile, Artifact(file="processed2.sas7bdat", group="task_output2")],
        },
        use_latest=True,
    )(data_path="/mnt/train-flyte-consolidated-examples/data/data.csv")

    training_results = DominoJobTask(
        name="Train model",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            # NOTE: Marking the input with the Annotation doesn't seem to do anything different
            # "processed_data_in", Annotated[FlyteFile, PrepData(report_name="task_input")],
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "model": FlyteFile,
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data_out,epochs=10,batch_size=32)

    # TODO: test dynamic partition creation
    # return TrainingData.create_from()

    # return the result from 2nd node to the workflow annotated in different ways
    model = training_results['model']
    return model, model, model, model, model, model
