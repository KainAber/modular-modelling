import importlib
from pathlib import Path

import yaml


def main(cfg: dict) -> None:
    # Iterate through steps
    for step_dict in cfg:
        # Extract step name
        step_name = next(iter(step_dict))

        # Extract step cfg
        step_cfg_name = step_dict[step_name]

        # Create project root path
        project_root_folder_path = Path(__file__).resolve().parents[2]

        # Construct step config path
        step_cfg_path = (
            project_root_folder_path
            / "cfg"
            / "modules"
            / step_name
            / f"{step_cfg_name}.yml"
        )

        # Read step config
        with open(step_cfg_path, "r") as file:
            step_cfg = yaml.safe_load(file)

        # Construct step main module path
        step_main_module_path = f"src.modules.{step_name}.main"

        # Import main step module
        step_main_module = importlib.import_module(step_main_module_path)

        # Get step main function
        step_main_func = getattr(step_main_module, "main")

        # Execute main on config
        step_main_func(step_cfg)
