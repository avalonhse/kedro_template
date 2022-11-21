from pathlib import Path
from pipelinex import __version__

from pipelinex.flex_kedro.configure import configure_source
from pipelinex.flex_kedro.context.flexible_context import FlexibleContext

from kedro.framework.startup import bootstrap_project
from kedro.framework.hooks import _create_hook_manager

from kedro.config import ConfigLoader

#from kedro.framework.session import KedroSession
#from kedro.framework.context import KedroContext

if __name__ == "__main__":
   print("pipelinex version: ", __version__)

   project_path = Path(__file__).resolve().parent
   print("project path: ", project_path)

   source_path = configure_source(project_path)
   print("source path: ", source_path)

   conf_path = str(project_path / "conf")
   config_loader = ConfigLoader(conf_source=conf_path)
    
   context = FlexibleContext( 
       package_name="pipeline_pytorch",
       project_path=Path.cwd(),
       config_loader=config_loader,
       hook_manager=_create_hook_manager(),
   )
   context.run()

   #print(context.params)
   #print(dir(config_loader))

   metadata = bootstrap_project(Path.cwd())
   print("metadata: ", metadata)

   #with KedroSession.create(metadata.package_name) as session:
   #    session.run()
