

class Selector[T, U]:

    def choose(self, discriminator: T) -> U:
        pass


class Mapper[T, U]:

    def __init__(self, mappings: dict[str, Selector[T, U]]):
        self._mappings = mappings

    def get(self, key: str, discriminator: T) -> U:
        selector: Selector[T, U] = self._mappings.get(key)
        return selector.choose(discriminator)
