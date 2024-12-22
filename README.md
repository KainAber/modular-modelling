# Modular Modelling

## Introduction

The idea behind this small repository is to provide a low-tech YAML-based orchestration framework for Python.

One advantage of this framework is that it allows for the seamless integration and swapping of different modules without the use of wrapper classes, making the approach fairly "modular"

The originally intended use case is the subsequent execution of steps in a modelling pipeline, hence the name **Modular Modelling**.

Intended audiences for this repository include:
- Developers who are not intimately familiar with the use of config files to separate run settings from source code
- Project teams that benefit from a clear distinction between "modeller" and "developer" roles
- Developers who are aiming to build a pipeline out of various modules and need a sensible starting place

## How it works

The architecture of the repository is fairly simple.
The module `main.py` in the project root is the entry point to the pipeline.
It reads the `config.yml` which specifies the runs that need to be executed (in order).
The runs are specified via the file names of run configs stored in `cfg/run` (without the suffix `.yml`):
```YAML
run:
  - run_example_1
  - run_example_2
```
The run configs contain a list of steps in the order in which they need to be run:
```YAML
- step1: step1_example
- step2: step2_example
```
Then, each of the run configs are read and passed to the function `src.run.main.main`.
This function dynamically imports the `main` functions from `src.modules.<STEP>.main` for each step specified in the run config
and passes the config dictionaries read from `cfg/modules/<STEP>` as inputs.
```python
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

To add a new module, simply create a folder inside `src/modules` containing the module code with a `main.py` file which contains a function called `main`. This function needs to take a dictionary as input which can be constructed from reading a `.yml` file.

Additionally create a folder inside `src/cfg/modules` of the same name in order to store `.yml` configuration files for the module.

Afterwards, any config file for the module can be referenced by a run config, which can in turn be selected for execution in the `config.yml`.
