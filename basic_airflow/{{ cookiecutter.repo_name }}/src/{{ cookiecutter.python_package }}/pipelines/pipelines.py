"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import node, pipeline

#############################################################################
from ..nodes.data_engineer import split_data

def create_de_pipeline(**kwargs):
    return pipeline(
        [
            node(
                split_data,
                ["example_iris_data", "params:example_test_data_ratio"],
                dict(
                    train_x="example_train_x",
                    train_y="example_train_y",
                    test_x="example_test_x",
                    test_y="example_test_y",
                ),
                name="split",
            )
        ]
    )

#############################################################################

from ..nodes.data_science import predict, report_accuracy, train_model

def create_ds_pipeline(**kwargs):
    return pipeline(
        [
            node(
                train_model,
                ["example_train_x", "example_train_y", "parameters"],
                "example_model",
                name="train",
            ),
            node(
                predict,
                dict(model="example_model", test_x="example_test_x"),
                "example_predictions",
                name="predict",
            ),
            node(
                report_accuracy,
                ["example_predictions", "example_test_y"],
                None,
                name="report",
            ),
        ]
    )

######################################################################
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    #pipelines = find_pipelines()
    #pipelines["__default__"] = sum(pipelines.values())
    #return pipelines

    data_processing_pipeline = create_de_pipeline()
    data_science_pipeline = create_ds_pipeline()

    return {
        "__default__": data_processing_pipeline + data_science_pipeline,
        "data_processing": data_processing_pipeline,
        "data_science": data_science_pipeline
    }