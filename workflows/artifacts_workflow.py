"""
Author: ddl-ebrown

The workflow returns many artifacts outputs and regular outputs.
"""

from flytekitplugins.domino.helpers import DominoJobTask, DominoJobConfig, Input, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, Optional, List, Dict, Annotated, Tuple, NamedTuple
from flytekit import Artifact
import uuid

# key pieces of data to collect

# artifact groups are identified uniquely by uuid
# * key (uuid)
# * name
# * type

# artifact files within each group are identified uniquely by uuid
# * key (uuid)
# * filename
# * artifact group (foreign key)

# the problem is the way that Flyte stores metadata and how the existing development experience works
# it makes it cumbersome to place artifacts into specific groups b/c of how the Python types are defined

# we need to change the DX because:
# it's error prone
# requires specifying the group values as partitions again and again
# requires more code than should be necessary, including predefining Artifacts by name instead of inside the Annotation
# the name of the artifact should be able to automatically set the extension (used by frontend for file previews)

# also note its worth investigating behavior dynamic partitions - i.e. ReportArtifact.create_from()

# upstream code here shows some examples
# https://github.com/flyteorg/flytekit/blob/master/flytekit/core/artifact.py#L371
# https://github.com/flyteorg/flytekit/blob/master/tests/flytekit/unit/core/test_artifacts.py

# to use partition_keys (necessary for Domino), we have to define this type up front -- this entire definition should be eliminated
ReportArtifact = Artifact(name="report.pdf", partition_keys=["key", "type", "group"], version=str(uuid.uuid4()))
ReportArtifact2 = Artifact(name="report2.pdf", partition_keys=["key", "type", "group"], version=str(uuid.uuid4()))
ReportArtifact3 = Artifact(name="report3.pdf", partition_keys=["key", "type", "group"], version=str(uuid.uuid4()))
ReportArtifact4 = Artifact(name="report4.pdf", partition_keys=["key", "type", "group"], version=str(uuid.uuid4()))
ReportArtifact5 = Artifact(name="report5.pdf", partition_keys=["key", "type", "group"], version=str(uuid.uuid4()))
ReportArtifact6 = Artifact(name="report6.pdf", partition_keys=["key", "type", "group"], version=str(uuid.uuid4()))

# this part is especially awful and something our helpers should take care of
ReportGroupId1 = str(uuid.uuid4())
ReportGroupId2 = str(uuid.uuid4())

# ideally, a group is defined like this
# ReportGroup = Group(name="my custom report", type=Report)

@workflow
def wf() -> Tuple[
    Annotated[FlyteFile, ReportArtifact(key=ReportGroupId1, type="report", group="report_foo")], 
    Annotated[FlyteFile, ReportArtifact2(key=ReportGroupId1, type="report", group="report_foo")], 
    Annotated[FlyteFile, ReportArtifact3(key=ReportGroupId2, type="report", group="report_bar")], 
    Annotated[FlyteFile, ReportArtifact4(key=ReportGroupId2, type="report", group="report_bar")], 
    Annotated[FlyteFile, ReportArtifact5(key=ReportGroupId2, type="report", group="report_bar")], 
    Annotated[FlyteFile, ReportArtifact6(key=ReportGroupId2, type="report", group="report_bar")], 

    # ideally the definition looks more like this:
    # Annotated[FlyteFile, Artifact(name="report.pdf", Group=ReportGroup)], 
    # this could be further simplified in the programming model if we know that these artifacts are only a single file like
    # ArtifactFile(name="report.pdf", Group=ReportGroup)

    # normal workflow output with no annotations
    FlyteFile
    ]: 
    """py
    pyflyte run --remote artifacts_workflow.py wf
    """

    data_prep_results = DominoJobTask(    
        name="Prepare data",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            # NOTE: Flyte normally suppports this -- but notice there are no partitions, which make them useless to Domino
            # this output is consumed by a subsequent task but also marked as an artifact
            "processed_data": Annotated[FlyteFile, Artifact(name="processed.sas7bdat", version=str(uuid.uuid4()))],
            # no downstream consumers -- simply an artifact output from an intermediate node in the graph
            "processed_data2": Annotated[FlyteFile, Artifact(name="processed2.sas7bdat", version=str(uuid.uuid4()))],
        },
        use_latest=True,
    )(data_path="/mnt/train-flyte-consolidated-examples/data/data.csv")

    training_results = DominoJobTask(
        name="Train model",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "model": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    training_results2 = DominoJobTask(
        name="Train model",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "model": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    training_results3 = DominoJobTask(
        name="Train model",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "model": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    # return the result from 2nd node to the workflow annotated in different ways
    model = training_results['model']
    model2 = training_results2['model']
    model3 = training_results3['model']
    return model, model2, model, model, model2, model3, model
