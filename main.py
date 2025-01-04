from pathlib import Path

import yaml

from src.run.main import main as run_main


def main(cfg_path: Path) -> None:
    # Read config dictionary
    with cfg_path.open("r") as file:
        cfg_dict = yaml.safe_load(file)

    # Extract all runs
    run_list = cfg_dict["runs"]

    # Iterate through runs
    for run_name in run_list:
        # Create project root path
        project_root_folder_path = Path(__file__).parent

        # Construct run config path
        run_cfg_path = project_root_folder_path / "cfg" / "run" / f"{run_name}.yml"

        # Ruh
        run_main(run_cfg_path)


if __name__ == "__main__":
    # Create project root path
    project_root_folder_path = Path(__file__).parent

    # Construct config path
    cfg_path = (project_root_folder_path / "config.yml").resolve()

    # Run main
    main(cfg_path)
