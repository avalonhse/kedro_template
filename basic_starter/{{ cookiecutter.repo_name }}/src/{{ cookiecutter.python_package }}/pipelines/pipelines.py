
from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

###################################################################

from ..nodes.data_engineer import create_model_input_table, preprocess_companies, preprocess_shuttles


def create_de_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_companies,
                inputs="companies",
                outputs="preprocessed_companies",
                name="preprocess_companies_node",
            ),
            node(
                func=preprocess_shuttles,
                inputs="shuttles",
                outputs="preprocessed_shuttles",
                name="preprocess_shuttles_node",
            ),
            node(
                func=create_model_input_table,
                inputs=["preprocessed_shuttles", "preprocessed_companies", "reviews"],
                outputs="model_input_table",
                name="create_model_input_table_node",
            ),
        ],
        namespace="data_processing",
        inputs=["companies", "shuttles", "reviews"],
        outputs="model_input_table",
    )

###################################################################

from ..nodes.data_science import evaluate_model, split_data, train_model

def create_ds_pipeline(**kwargs) -> Pipeline:
    pipeline_instance = pipeline(
        [
            node(
                func=split_data,
                inputs=["model_input_table", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="regressor",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["regressor", "X_test", "y_test"],
                outputs=None,
                name="evaluate_model_node",
            ),
        ]
    )
    ds_pipeline_1 = pipeline(
        pipe=pipeline_instance,
        inputs="model_input_table",
        namespace="active_modelling_pipeline",
    )
    ds_pipeline_2 = pipeline(
        pipe=pipeline_instance,
        inputs="model_input_table",
        namespace="candidate_modelling_pipeline",
    )
    return pipeline(
        pipe=ds_pipeline_1 + ds_pipeline_2,
        inputs="model_input_table",
        namespace="data_science",
    )

###################################################################
from typing import Dict

from kedro.framework.project import find_pipelines

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

    return {"__default__": data_processing_pipeline + data_science_pipeline }
