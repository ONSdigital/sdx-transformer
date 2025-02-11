import json
from os.path import exists
import yaml
from sdx_gcp.app import get_logger
from app.definitions import BuildSpec


logger = get_logger()


def read_build_spec(spec_name: str, subdir: str = "pck") -> BuildSpec:
    """
    Looks up the relevant build spec for the submission provided.
    """
    filepath = f"build_specs/{subdir}/{spec_name}.yaml"
    if exists(filepath):
        logger.info(f"Getting build spec from {filepath}")
        with open(filepath) as y:
            build_spec: BuildSpec = yaml.safe_load(y.read())

    else:
        filepath = f"build_specs/{subdir}/{spec_name}.json"
        logger.info(f"Getting build spec from {filepath}")
        with open(filepath) as j:
            build_spec: BuildSpec = json.load(j)

    return build_spec
