"""
Author: ddl-galias

Workflow with many complex inputs.
"""

import numpy as np
import pandas as pd
import re
from utils.flyte import DominoTask, Input, Output
from flytekit import workflow, kwtypes, StructuredDatasetType, LiteralType, Literal
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema
from datetime import datetime, timedelta
from flytekit.models.types import SimpleType
from google.protobuf import duration_pb2
from typing import Union, Dict, List, IO, TypeVar, Annotated
from types import NoneType
from flyteidl.core import types_pb2 as _types_pb2
import json
from enum import Enum
from flytekit.types.structured import register_csv_handlers
from flytekit.types.structured.structured_dataset import CSV

register_csv_handlers()


from flytekit.types.structured.structured_dataset import (
    StructuredDataset,
    StructuredDatasetDecoder,
    StructuredDatasetEncoder,
    StructuredDatasetTransformerEngine,
)

all_cols = kwtypes(Name=str, Age=int, Height=int)
df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [36, 22], "Height": [160, 178]})

sd = StructuredDataset(dataframe=df)



class Color(Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"

matches = re.search(r'[0-9]+', "testme"); matches; type(matches)

@workflow
def wf() -> None:
    """
    pyflyte run --remote inputs_rare_workflow.py wf
    """

    data_prep_results = DominoTask(
        name="Prepare data",
        command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        environment="Domino Standard Environment Py3.10 R4.4",
        hardware_tier="Small",
        inputs=[
            Input(name="data_path", type=str, value="/mnt/train-flyte-consolidated-examples/data/data.csv")
        ],
        outputs=[
            Output(name="processed_data", type=FlyteFile[TypeVar("csv")])
        ]
    )

    # data_prep_nada = DominoTask(
    #     name="Prepare nada",
    #     command="touch /workflow/outputs/nada",
    #     environment="Domino Standard Environment Py3.10 R4.4",
    #     hardware_tier="Small",
    #     outputs=[
    #         Output(name="nada", type=NoneType)
    #     ]
    # )

    DominoTask(
        name="Rare inputs workflow 2",
        command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        environment="Domino Standard Environment Py3.10 R4.4",
        hardware_tier="Small",
        inputs=[
            Input(
                name="collection_input", 
                type=List[Union[dict,float,FlyteFile[TypeVar("csv")],List[Union[str, FlyteFile[TypeVar("csv")]]]]], 
                value=[
                    11.1,
                    data_prep_results['processed_data'],
                    { "value": 11 },
                    ['hola', data_prep_results['processed_data']]
                ]
            ),
            Input(
                name="structured_data_set_input", 
                type=Annotated[StructuredDataset, CSV], 
                value=sd
            ),
            Input(
                name="enum_input", 
                type=Color, 
                value=Color.BLUE
            ),
            # Input(
            #     name="none_input", 
            #     type=NoneType,
            #     value=data_prep_nada['nada']
            # ),
            Input(
                name="schema_input", 
                type=FlyteSchema,
                value=df
            ),
            Input(
                name="blob_input", 
                type=FlyteFile[TypeVar("csv")],
                value=data_prep_results['processed_data']
            ),
            Input(
                name="boolean_input", 
                type=bool,
                value=True
            ),
            Input(
                name="float_input", 
                type=float,
                value=14.4
            ),
            Input(
                name="integer_input", 
                type=int,
                value=14
            )
        ],
        outputs=[],
    )
