# Modular Modelling

## Introduction

The idea behind this small repository is to provide a low-tech YAML-based orchestration framework for Python.

One advantage of this framework is that it allows for the integration and swapping of different modules
(provided they have the correct I/O),
making the approach fairly "modular".

The originally intended use case is the subsequent execution of steps in a modelling pipeline, hence the name **Modular Modelling**.

Intended audiences for this repository include:
- Developers who are not intimately familiar with the use of config files to separate run settings from source code
- Project teams that benefit from a clear distinction between "modeller" and "developer" roles
- Developers who are aiming to build a pipeline out of various modules and need a sensible starting place
- Sets of project teams that work on similar problems and can benefit from sharing pipeline components

## Repo structure

```shell
├── cfg                                 #-Contains all configs (except the main one)
│    ├── modules                          #-Contains all step configs
│    │    ├── step1                         # Contains all step1 configs
│    │    │    └── step1_example.yml          # Specifies a step1 execution (dummy)
│    │    └── step2                         # Contains all step2 configs
│    │         ├── step2_example.yml          # Specifies a step2 execution (dummy)
│    │         └── step2_example_2.yml        # Specifies a step2 execution (dummy)
│    └── run                              #-Contains all run configs
│         ├── run_example_1.yml             # Specifies step configs for a run
│         └── run_example_2.yml             # Specifies step configs for a run
├── src                                 #-Contains all source code (except the main)
│    ├── modules                          #-Contains all available modules
│    │    ├── step1                         # Contains step1 code
│    │    │    └── main.py                    # Executes step1 (dummy)
│    │    └── step2                         # Contains step2 code
│    │         └── main.py                    # Executes step2 (dummy)
│    └── run                              #-Contains the run module
│         └── main.py                       #-Dynamically calls steps on step configs
├── config.yml                          # Specifies the runs to execute
├── main.py                             #-Calls the run module
└── requirements.txt                    # Contains required packages
```

Files and folder names commented with `#-` are designed not to be modified by the user.

## How it works

The architecture of the repository is fairly simple.
The module `main.py` in the project root is the entry point to the pipeline.
It reads the `config.yml` which specifies the runs that need to be executed (in order).
The runs are specified via the file names of run configs stored in `cfg/run` (without the suffix `.yml`):
```YAML
runs:
  - run_example_1
  - run_example_2
```
Then, each of the run configs are read and passed to the function `src.run.main.main`.
The run configs contain a list of steps with step config names in the order in which they need to be run:
```YAML
steps:
  - step: step1
    config: step1_example
  - step: step2
    config: step2_example
```
The function `src.run.main.main` goes through each step specified in the run config and dynamically imports the `main` functions from `src.modules.<step>.main`.
It then reads and passes each config dictionary from `cfg/modules/<step>/<config>.yml` as input to the imported functions.
```python
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
```

## Adding modules

To add a new module, simply create a folder inside `src/modules`, e.g., `step3` containing the module code with a `main.py` file.
This `main.py`file needs to contain a function called `main` taking a dictionary as input which can be constructed from reading a `.yml` file.

Additionally create a folder inside `src/cfg/modules` of the same name (`step3`) in order to store `.yml` configuration files for the module.

Now, any config file for the module can be referenced by a run config, which can in turn be selected for execution in the `config.yml`.
