"""Command line tools for manipulating a Kedro project.
Intended to be invoked via `kedro`."""

import click
import kedro
from kedro.framework.cli.project import (
    ASYNC_ARG_HELP,
    CONFIG_FILE_HELP,
    FROM_INPUTS_HELP,
    FROM_NODES_HELP,
    LOAD_VERSION_HELP,
    NODE_ARG_HELP,
    PARAMS_ARG_HELP,
    PIPELINE_ARG_HELP,
    RUNNER_ARG_HELP,
    TAG_ARG_HELP,
    TO_NODES_HELP,
    TO_OUTPUTS_HELP,
    project_group,
)
from kedro.framework.cli.utils import (
    CONTEXT_SETTINGS,
    _config_file_callback,
    _get_values_as_tuple,
    _reformat_load_versions,
    _split_params,
    env_option,
    split_string,
)

from kedro.framework.session import KedroSession
from kedro.utils import load_obj

def insert_params_template(element, params):
    #print("Params =", params,". Element =", element)
    if element in params:
        element = params[element]
        #print("checked = ", element)
    return element

def check_path(directory):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

def check_paths(dirs, common_path):
    for dir_name in dirs:
        check_path(common_path + dir_name)

def prepare_data_saving():
    import os
    parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace("\\","/")
    data_path = parent_path + "/data/" + os.path.basename(os.getcwd())

    data_dirs = ["/01_raw","/02_intermediate","/03_primary","/06_models","/logs"]
    check_paths(data_dirs, data_path)

@click.group(context_settings=CONTEXT_SETTINGS, name=__file__)
def cli():
    """Command line tools for manipulating a Kedro project."""

@project_group.command()
@click.option(
    "--from-inputs", type=str, default="", help=FROM_INPUTS_HELP, callback=split_string
)
@click.option(
    "--to-outputs", type=str, default="", help=TO_OUTPUTS_HELP, callback=split_string
)
@click.option(
    "--from-nodes", type=str, default="", help=FROM_NODES_HELP, callback=split_string
)
@click.option(
    "--to-nodes", type=str, default="", help=TO_NODES_HELP, callback=split_string
)
@click.option("--node", "-n", "node_names", type=str, multiple=True, help=NODE_ARG_HELP)
@click.option(
    "--runner", "-r", type=str, default=None, multiple=False, help=RUNNER_ARG_HELP
)
@click.option("--async", "is_async", is_flag=True, multiple=False, help=ASYNC_ARG_HELP)
@env_option
@click.option("--tag", "-t", type=str, multiple=True, help=TAG_ARG_HELP)
@click.option(
"--load-version",
"-lv",
type=str,
multiple=True,
help=LOAD_VERSION_HELP,
callback=_reformat_load_versions,
)
@click.option("--pipeline", "-p", type=str, default=None, help=PIPELINE_ARG_HELP)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help=CONFIG_FILE_HELP,
    callback=_config_file_callback,
)
@click.option(
    "--params",
    type=click.UNPROCESSED,
    default="",
    help=PARAMS_ARG_HELP,
    callback=_split_params,
)
# pylint: disable=too-many-arguments,unused-argument
def run(
    tag,
    env,
    runner,
    is_async,
    node_names,
    to_nodes,
    from_nodes,
    from_inputs,
    to_outputs,
    load_version,
    pipeline,
    config,
    params,
):
    prepare_data_saving()

    from pipelinex import __version__
    print("pipelinex version: ", __version__)

    from pathlib import Path
    project_path = Path(__file__).resolve().parent.parent.parent
    print("project path: ", project_path)
    package_name = Path(__file__).resolve().parent.name
    print("package_name: ", package_name)

    from pipelinex.flex_kedro.configure import configure_source
    source_path = configure_source(project_path)
    print("source path: ", source_path)

    from os.path import exists
    if exists("src/config/base/param_components.yml"):
        import yaml
        with open("src/config/base/param_components.yml", "r") as stream:
            try:
                content = yaml.safe_load(stream)

                if "templated_pipelines" in content:
                    for pipeline in content["templated_pipelines"]["instances"]:
                        # deep copy the 1st pipeline to new pipeline
                        import copy
                        new_pipeline = copy.deepcopy(content["templated_pipelines"]["pipelines"][pipeline["template"]])
                        for node in new_pipeline["nodes"]:
                            for element in node:
                                if isinstance(node[element],list):
                                    for index, sub_element in enumerate(node[element]):
                                        node[element][index] = sub_element.replace("namespace",pipeline["namespace"])
                                if isinstance(node[element],str):
                                    node[element] = node[element].replace("namespace",pipeline["namespace"])
                            node["name"]=pipeline["name"]+"_"+node["func"]
                            #print("Node =", node)
                        content["PIPELINES"][pipeline["name"]] = new_pipeline
                
                #### combined pipeline
                if "combined_pipelines" in content:
                    for pipeline_name in content["combined_pipelines"]:
                        # deep copy the 1st pipeline to new pipeline
                        content["PIPELINES"][pipeline_name] = content["PIPELINES"] [content["combined_pipelines"][pipeline_name][0]]

                        # copy NODE contents of the next 2nd pipelines to the content of the new pipeline
                        for pipeline in content["combined_pipelines"][pipeline_name][1:]:
                            content["PIPELINES"][pipeline_name]["nodes"].extend(content["PIPELINES"] [pipeline]["nodes"])

                import io
                with io.open("src/config/base/parameters.yml", 'w', encoding='utf8') as outfile:
                    yaml.dump(content, outfile, default_flow_style=False, allow_unicode=True)

            except yaml.YAMLError as exc:
                print(exc)

    from kedro.framework.project import settings
    conf_path = str(project_path / settings.CONF_SOURCE)
    if settings.CONFIG_LOADER_CLASS == kedro.config.TemplatedConfigLoader:
        config_loader = settings.CONFIG_LOADER_CLASS(
            conf_source=conf_path,
            globals_pattern = settings.CONFIG_LOADER_ARGS["globals_pattern"]
        )
    else:
        config_loader = settings.CONFIG_LOADER_CLASS(conf_source=conf_path)
    
    ############# FlexibleContext  ##########################
    from pipelinex.flex_kedro.context.flexible_context import FlexibleContext
    from kedro.framework.hooks import _create_hook_manager
    context = FlexibleContext( 
      package_name=package_name,
      project_path=Path.cwd(),
      config_loader=config_loader,
      hook_manager=_create_hook_manager(),
    )

    """Run the pipeline."""
    ##### ADD YOUR CUSTOM RUN COMMAND CODE HERE #####
    runner = load_obj(runner or "SequentialRunner", "kedro.runner")
    tag = _get_values_as_tuple(tag) if tag else tag
    node_names = _get_values_as_tuple(node_names) if node_names else node_names

    from .flexible_kedro import FlexibleKedroSession
    with FlexibleKedroSession.create(env=env, extra_params=params) as session:
        session.set_pipelines(context._kedro_pipelines)

        # session.run(
        #     tags=tag,
        #     runner=runner(is_async=is_async),
        #     node_names=node_names,
        #     from_nodes=from_nodes,
        #     to_nodes=to_nodes,
        #     from_inputs=from_inputs,
        #     to_outputs=to_outputs,
        #     load_versions=load_version,
        #     pipeline_name=pipeline,
        # )

        context.run()
