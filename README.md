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
├── cfg                                 #-Contains configs for modules and runs
│    ├── modules                          #-Contains configs for modules
│    │    ├── mod1                          # Contains configs for module 'mod1'
│    │    │    └── mod1_example.yml           # Specifies a mod1 execution (dummy)
│    │    └── mod2                          # Contains configs for module 'mod2'
│    │         ├── mod2_example.yml           # Specifies a mod2 execution (dummy)
│    │         └── mod2_example_2.yml         # Specifies a mod2 execution (dummy)
│    └── run                              #-Contains configs for runs
│         ├── run_example_1.yml             # Specifies module configs for a run
│         └── run_example_2.yml             # Specifies module configs for a run
├── src                                 #-Contains source code for modules and runs
│    ├── modules                          #-Contains available modules
│    │    ├── mod1                          # Contains code for module 'mod1'
│    │    │    └── main.py                    # Executes module 'mod1' (dummy)
│    │    └── mod2                          # Contains code for module 'mod2'
│    │         └── main.py                    # Executes module 'mod2' (dummy)
│    └── run                              #-Contains code for runs
│         └── main.py                       #-Executes a run by dynamically calling modules
├── config.yml                          # Specifies the run executions
├── main.py                             #-Executes runs by calling the run module on each run
└── requirements.txt                    # Contains required packages
```

Files and folder names commented with `#-` are designed to not be modified by the user.

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
Then, each run config path is constructed and passed to the function `src.run.main.main`.
The run configs contain a list of steps with step config names in the order in which they need to be run:
```YAML
steps:
  - module: mod1
    config: mod1_example
  - module: mod2
    config: mod2_example
```
The function `src.run.main.main` goes through each step specified in the run config and dynamically imports the `main` functions from `src.modules.<module>.main`.
It then passes each step config path `cfg/modules/<module>/<config>.yml` as a `Path` object as input to the imported functions.
```python
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
```

## Adding modules

To add a new module, simply create a folder inside `src/modules`, e.g., `mod3` containing the module code with a `main.py` file.
This `main.py`file needs to contain a function called `main` taking a `Path` object as input pointing to a `.yml` file.

Additionally create a folder inside `src/cfg/modules` of the same name (`mod3`) in order to store `.yml` configuration files for the module.

Now, any config file for the module can be referenced by a run config, which can in turn be selected for execution in the `config.yml`.
