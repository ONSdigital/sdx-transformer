import json
from os.path import exists
import yaml
from sdx_gcp.app import get_logger
from app.definitions.spec import BuildSpec
from app.definitions.repository import BuildSpecRepository

logger = get_logger()


class BuildSpecFileRepository(BuildSpecRepository):
    dir: str = "build_specs"

    def get_build_spec(self, spec_name: str) -> BuildSpec:
        """
        Looks up the relevant build spec for the submission provided.
        """
        filepath = f"{self.dir}/{spec_name}.yaml"
        if exists(filepath):
            logger.info(f"Getting build spec from {filepath}")
            with open(filepath) as y:
                build_spec: BuildSpec = yaml.safe_load(y.read())

        else:
            filepath = f"{self.dir}/{spec_name}.json"
            logger.info(f"Getting build spec from {filepath}")
            with open(filepath) as j:
                build_spec: BuildSpec = json.load(j)

        return build_spec
