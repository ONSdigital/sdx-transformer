from app.definitions.spec import BuildSpec
from app.transformers.spec import SpecTransformer


class PrepopTransformer(SpecTransformer[str]):

    def _load(self, s: str) -> BuildSpec:
        return self._spec_mapping.get_build_spec(s)
