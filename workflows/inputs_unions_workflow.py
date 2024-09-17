"""
Author: ddl-galias

Workflow with many complex union inputs.
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
    pyflyte run --remote inputs_unions_workflow.py wf
    """

    DominoTask(
        name="Rare inputs workflow 2",
        command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        environment="Domino Standard Environment Py3.10 R4.4",
        hardware_tier="Small",
        inputs=[
            Input(
                name="map_union_nested", 
                type=Dict[
                    str,
                    Union[
                        Dict[str,
                            Union[
                                Dict[
                                        str,
                                        Union[List[str], str
                                    ]
                                ],
                                List[
                                    Union[
                                        Dict[
                                            str,
                                            Union[List[str], str]
                                        ]
                                    ]
                                ]
                            ]
                        ],
                        List[
                            Union[
                                Dict[
                                        str,
                                        Union[List[str], str
                                    ]
                                ],
                                List[
                                    Union[
                                        Dict[
                                            str,
                                            Union[List[str], str]
                                        ]
                                    ]
                                ],
                                str
                            ]
                        ]
                    ]
                ], 
                value={
                    "v1": {
                        "v1.1": [{ "v1.1.1": ["1"] }],
                    },
                    "v2": [
                        { "v2.1": ["hi!"]}
                    ]
                }
            ),Input(
                name="map_list_nested", 
                type=List[
                    Union[
                        Dict[str,
                            Union[
                                Dict[
                                        str,
                                        Union[List[str], str
                                    ]
                                ],
                                List[
                                    Union[
                                        Dict[
                                            str,
                                            Union[List[str], str]
                                        ]
                                    ]
                                ]
                            ]
                        ],
                        List[
                            Union[
                                Dict[
                                        str,
                                        Union[List[str], str
                                    ]
                                ],
                                List[
                                    Union[
                                        Dict[
                                            str,
                                            Union[List[str], str]
                                        ]
                                    ]
                                ],
                                str
                            ]
                        ]
                    ]
                ], 
                value=[
                    {
                        "v1.1": [{ "v1.1.1": ["1"] }],
                    },
                    [
                        { "v2.1": ["hi!"]}
                    ]
                ]
            ),
            Input(
                name="union", 
                type=Union[
                        Dict[str,
                            Union[
                                Dict[
                                        str,
                                        Union[List[str], str
                                    ]
                                ],
                                List[
                                    Union[
                                        Dict[
                                            str,
                                            Union[List[str], str]
                                        ]
                                    ]
                                ]
                            ]
                        ],
                        List[
                            Union[
                                Dict[
                                        str,
                                        Union[List[str], str
                                    ]
                                ],
                                List[
                                    Union[
                                        Dict[
                                            str,
                                            Union[List[str], str]
                                        ]
                                    ]
                                ],
                                str
                            ]
                        ]
                    ],
                value=
                    {
                        "v1.1": [{ "v1.1.1": ["1"] }],
                    },
            ),
        ],
        outputs=[],
    )
