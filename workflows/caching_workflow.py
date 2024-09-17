"""
Author: ddl-galias

Workflow with caching enabled and many very complex inputs.
"""

import numpy as np
import pandas as pd
from utils.flyte import DominoTask, Input, Output
from flytekit import kwtypes, workflow
from flytekit.types.file import  FlyteFile
from flytekit.types.schema import FlyteSchema
from datetime import datetime, timedelta
from google.protobuf import duration_pb2
from typing import Union, Dict, List, IO, TypeVar, Annotated
import json
from enum import Enum
from flytekit.types.structured.structured_dataset import CSV
from flytekit.types.structured import register_csv_handlers

from flytekit.types.structured.structured_dataset import (
    StructuredDataset,
    StructuredDatasetDecoder,
    StructuredDatasetEncoder,
    StructuredDatasetTransformerEngine,
)

register_csv_handlers()

all_cols = kwtypes(Name=str, Age=int, Height=int)
df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [36, 22], "Height": [160, 178]})

sd = StructuredDataset(dataframe=df)

class Color(Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"

# union_value: Union[Union[str,int],str,int,bool,datetime,timedelta,FlyteFile,float,dict])
@workflow
def wf() -> None:
    """
    pyflyte run --remote inputs_complex_workflow.py wf
    """

    td = timedelta(days=3, minutes=10)

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
        ],
        cache=True,
        cache_version="v0",
    )

    data_prep_results_2 = DominoTask(
        name="Prepare data 2",
        command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        environment="Domino Standard Environment Py3.10 R4.4",
        hardware_tier="Small",
        inputs=[
            Input(name="data_path", type=str, value="/mnt/train-flyte-consolidated-examples/data/data.csv")
        ],
        outputs=[
            Output(name="processed_data", type=FlyteFile[TypeVar("csv")])
        ],
        cache=True,
        cache_version="v0",
    )

    data_prep_results_3 = DominoTask(
        name="Prepare data 3",
        command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        environment="Domino Standard Environment Py3.10 R4.4",
        hardware_tier="Small",
        inputs=[
            Input(name="data_path", type=str, value="/mnt/train-flyte-consolidated-examples/data/data.csv")
        ],
        outputs=[
            Output(name="processed_data", type=FlyteFile[TypeVar("txt")])
        ],
        cache=True,
        cache_version="v0",
    )

    DominoTask(
        name="Inputs workflow 2",
        command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        environment="Domino Standard Environment Py3.10 R4.4",
        hardware_tier="Small",
        inputs=[
            Input(
                name="map_input_base", 
                type=Dict[str, Union[str, float,FlyteFile[TypeVar("csv")],Dict[str, Union[str, FlyteFile[TypeVar("csv")]]]]], 
                value={
                    "value1": 11.1,
                    "value2": data_prep_results_2['processed_data'],
                    "value4": { "value4.1": 'hola', "value4.2": data_prep_results['processed_data'] },
                }
            ),
            Input(
                name="map_input_int", 
                type=Dict[int, str], 
                value={
                    1: '11.1',
                    3: '1',
                    3: '2',
                }
            ),
            Input(name="file_input", type=FlyteFile[TypeVar('csv')], value=data_prep_results_2['processed_data']),
            # Input(name="union_input", type=Union[Union[dict,float],str,int,bool,datetime,timedelta,FlyteFile], value=union_value),
            Input(name="datetime_input", type=datetime, value=datetime(2024, 5, 10)),
            Input(name="duration_input", type=timedelta, value=td),
            Input(
                name="struct_none", 
                type=dict, 
                value={}
            ),
            Input(
                name="struct_json", 
                type=dict, 
                value={
                    "values1": [1, 2, 3, 4, 5],
                    "values2": {
                        "number_value": 3,
                        "number_value": 3,
                        "number_value": 4
                    },
                    "values3": "1",
                    "values4": False,
                    "values5": 1,
                    "values5": None
                }
            ),
            Input(
                name="struct_list", 
                type=dict, 
                value={
                    "values": {
                        "number_value": 6
                    },
                }
            ),
            Input(
                name="collection_input", 
                type=List[Union[dict,float,FlyteFile[TypeVar("csv")],List[Union[str, FlyteFile[TypeVar("csv")]]]]], 
                value=[
                    11.1,
                    data_prep_results_2['processed_data'],
                    { "value": 11 },
                    ['hola', data_prep_results['processed_data']]
                ]
            ),
            Input(
                name="collection_file_only_one_level_input", 
                type=List[FlyteFile[TypeVar("csv")]], 
                value=[
                    data_prep_results['processed_data'],
                    data_prep_results_2['processed_data']
                ]
            ),
            Input(
                name="collection_boolean_only_one_level_input", 
                type=List[bool], 
                value=[
                    False,
                    True
                ]
            ),
            Input(
                name="collection_datetime_only_one_level_input", 
                type=List[datetime], 
                value=[
                    datetime(2024, 5, 10),
                    datetime(2023, 5, 10),
                    datetime(2022, 5, 10)
                ]
            ),
            Input(
                name="collection_duration_only_one_level_input", 
                type=List[timedelta], 
                value=[
                    td
                ]
            ),
            Input(
                name="collection_enum_only_one_level_input", 
                type=List[Color], 
                value=[
                    Color.BLUE,
                    Color.GREEN
                ]
            ),
            Input(
                name="collection_float_only_one_level_input", 
                type=List[float], 
                value=[
                    12.2,
                    12.0
                ]
            ),
            Input(
                name="collection_integer_only_one_level_input", 
                type=List[int], 
                value=[
                    11,
                    12,
                    0
                ]
            ),
            Input(
                name="collection_schema_only_one_level_input", 
                type=List[FlyteSchema], 
                value=[
                    df
                ]
            ),
            Input(
                name="collection_string_only_one_level_input", 
                type=List[str], 
                value=[
                    'hello!'
                ]
            ),
            Input(
                name="collection_struct_only_one_level_input", 
                type=List[dict], 
                value=[
                    {},
                ]
            ),
            Input(
                name="collection_stds_only_one_level_input", 
                type=List[Annotated[StructuredDataset, CSV]], 
                value=[
                    sd,
                ]
            ),
            Input(
                name="map_input", 
                type=Dict[str,Union[dict,float,FlyteFile[TypeVar("csv")],List[Union[str, FlyteFile[TypeVar("csv")]]]]], 
                value={
                    "v1": 11.1,
                    "v2": data_prep_results_2['processed_data'],
                    "v3": { "value": 11 },
                    "v4": ['hola', data_prep_results['processed_data']]
                }
            ),
            Input(
                name="map_file_only_one_level_input", 
                type=Dict[str, FlyteFile[TypeVar("csv")]], 
                value={
                    "v1": data_prep_results['processed_data'],
                    "v2": data_prep_results_2['processed_data']
                }
            ),
            Input(
                name="map_boolean_only_one_level_input", 
                type=Dict[str, bool], 
                value={
                    "v1": False,
                    "v2": True
                }
            ),
            Input(
                name="map_datetime_only_one_level_input", 
                type=Dict[str, datetime], 
                value={
                    "v1": datetime(2024, 5, 10),
                    "v2": datetime(2023, 5, 10),
                    "v3": datetime(2022, 5, 10)
                }
            ),
            Input(
                name="map_duration_only_one_level_input", 
                type=Dict[str, timedelta], 
                value={
                    "v1": td
                }
            ),
            Input(
                name="map_enum_only_one_level_input", 
                type=Dict[str, Color], 
                value={
                    "v1": Color.BLUE,
                    "v2": Color.GREEN
                }
            ),
            Input(
                name="map_float_only_one_level_input", 
                type=Dict[str, float], 
                value={
                    "v1": 12.2,
                    "v2": 12.0
                }
            ),
            Input(
                name="map_integer_only_one_level_input", 
                type=Dict[str, int], 
                value={
                    "v1": 11,
                    "v2": 12,
                    "v3": 0
                }
            ),
            Input(
                name="map_schema_only_one_level_input", 
                type=Dict[str, FlyteSchema], 
                value={
                    "v1": df
                }
            ),
            Input(
                name="map_string_only_one_level_input", 
                type=Dict[str, str], 
                value={
                    "v1": 'hello!'
                }
            ),
            Input(
                name="map_struct_only_one_level_input", 
                type=Dict[str, dict], 
                value={
                    "v1": {},
                }
            ),
            Input(
                name="map_stds_only_one_level_input", 
                type=Dict[str, Annotated[StructuredDataset, CSV]], 
                value={
                    "v1": sd,
                }
            ),
            Input(
                name="collection_file_only_multi_level_input", 
                type=List[List[FlyteFile[TypeVar("csv")]]], 
                value=[
                    [data_prep_results['processed_data'], data_prep_results['processed_data']],
                    [data_prep_results_2['processed_data']]
                ]
            ),
            Input(
                name="collection_file_only_three_level_input", 
                type=List[List[List[FlyteFile[TypeVar("txt")]]]], 
                value=[
                    [[data_prep_results_3['processed_data'], data_prep_results_3['processed_data']]],
                    [[data_prep_results_3['processed_data']]]
                ]
            ),
            Input(
                name="map_file_only_one_level_input", 
                type=Dict[str, FlyteFile[TypeVar("csv")]], 
                value={
                    "value2": data_prep_results_2['processed_data'],
                }
            ),
            Input(
                name="map_file_only_multi_level_input", 
                type=Dict[str, Dict[str,FlyteFile[TypeVar("csv")]]], 
                value={
                    "value2": {
                        "value2.1": data_prep_results['processed_data'],
                        "value2.2": data_prep_results_2['processed_data']
                    }
                }
            ),
            Input(
                name="map_file_only_three_level_input", 
                type=Dict[str, Dict[str,Dict[str,FlyteFile[TypeVar("csv")]]]], 
                value={
                    "value2": {
                        "value2.1": {
                            "value2.1.1": data_prep_results['processed_data'],
                        },
                        "value2.2": {
                            "value2.2.1": data_prep_results_2['processed_data']
                        }
                    }
                }
            ),
            Input(
                name="map_plus_list_file_only_three_level_input", 
                type=Dict[str, Dict[str,Dict[str,List[FlyteFile[TypeVar("csv")]]]]], 
                value={
                    "value2": {
                        "value2.1": {
                            "value2.1.1": [data_prep_results['processed_data']],
                        },
                        "value2.2": {
                            "value2.2.1": [data_prep_results['processed_data'], data_prep_results['processed_data']]
                        }
                    }
                }
            ),
            Input(
                name="collection_plus_map_file_only_three_level_input", 
                type=List[List[List[Dict[str,FlyteFile[TypeVar("txt")]]]]], 
                value=[
                    [[
                        {
                            "value1": data_prep_results_3['processed_data'],
                            "value2": data_prep_results_3['processed_data']
                        },
                        {
                            "valuealgo": data_prep_results_3['processed_data'],
                        }
                    ]],
                    [[
                        { "totallylost": data_prep_results_3['processed_data']
                        }]]
                ]
            ),
        ],
        outputs=[],
        cache=True,
        cache_version="v0",
    )
