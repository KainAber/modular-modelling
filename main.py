from pathlib import Path

import yaml

from src.run import main as run_main


def main(cfg: dict) -> None:
    # Extract all runs
    run_list = cfg["run"]

    # Iterate through runs
    for run_name in run_list:
        # Create project root path
        project_root_folder_path = Path(__file__).resolve().parents[0]

        # Construct run config path
        run_cfg_path = project_root_folder_path / "cfg" / "run" / f"{run_name}.yml"

        # Read run config
        with open(run_cfg_path, "r") as file:
            run_cfg = yaml.safe_load(file)

        # Ruh
        run_main.main(run_cfg)


if __name__ == "__main__":
    # Create project root path
    project_root_folder_path = Path(__file__).resolve().parents[0]

    # Construct config path
    cfg_path = project_root_folder_path / "config.yml"

    # Read config dictionary
    with open(cfg_path, "r") as file:
        cfg = yaml.safe_load(file)

    # Run main
    main(cfg)
