import importlib
from pathlib import Path

import yaml


def main(cfg_path: Path) -> None:
    # Read config
    with cfg_path.open("r") as file:
        cfg_dict = yaml.safe_load(file)

    # Retrieve steps
    steps = cfg_dict["steps"]

    # Iterate through steps
    for step_dict in steps:
        # Extract module name
        step_module_name = step_dict["module"]

        # Extract step cfg
        step_cfg_name = step_dict["config"]

        # Create project root path
        project_root_folder_path = Path(__file__).parents[2]

        # Construct step config path
        step_cfg_path = (
            project_root_folder_path
            / "cfg"
            / "modules"
            / step_module_name
            / f"{step_cfg_name}.yml"
        )

        # Construct step main module path
        step_main_module_path = f"src.modules.{step_module_name}.main"

        # Import main step module
        step_main_module = importlib.import_module(step_main_module_path)

        # Get step main function
        step_main_func = getattr(step_main_module, "main")

        # Execute main on config path
        step_main_func(step_cfg_path)
