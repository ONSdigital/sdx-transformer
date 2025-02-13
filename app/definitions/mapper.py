from app.definitions.spec_repo import BuildSpecRepository
from app.definitions.spec import BuildSpec


class Selector[T, U]:

    def choose(self, discriminator: T) -> U:
        pass


class Mapper[T, U]:

    def __init__(self, mappings: dict[str, Selector[T, U]]):
        self._mappings = mappings

    def get(self, key: str, discriminator: T) -> U:
        pass


class SpecMapping[T](Mapper[T, str]):

    def __init__(self, mappings: dict[str, Selector[T, str]], repository: BuildSpecRepository):
        super().__init__(mappings)
        self._repository = repository

    def get_build_spec(self, survey_id: str, discriminator: T) -> BuildSpec:
        pass
