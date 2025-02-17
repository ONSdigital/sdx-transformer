from collections.abc import Callable

from app.config.formatters import _formatter_mapping
from app.config.specs import _build_spec_mapping, _prepop_spec_mapping
from app.config.functions import _function_lookup
from app.definitions.data import SurveyMetadata
from app.definitions.executor import ExecutorBase
from app.definitions.mapper import BuildSpecMappingBase, PrepopMappingBase, FormatterMappingBase
from app.definitions.repository import BuildSpecRepositoryBase
from app.mappers.formatter_mappings import FormatterMapping
from app.mappers.spec_mappings import BuildSpecMapping, PrepopSpecMapping
from app.repositories.file_repository import BuildSpecFileRepository
from app.transform.execute import Executor
from app.transformers.flat import FlatSpecTransformer
from app.transformers.looped import LoopedSpecTransformer
from app.transformers.prepop import PrepopTransformer


def get_spec_repository() -> BuildSpecRepositoryBase:
    return BuildSpecFileRepository()


def get_build_spec_mapping(repository: BuildSpecRepositoryBase) -> BuildSpecMappingBase:
    return BuildSpecMapping(_build_spec_mapping, repository)


def get_prepop_spec_mapping(repository: BuildSpecRepositoryBase) -> PrepopMappingBase:
    return PrepopSpecMapping(_prepop_spec_mapping, repository)


def get_formatter_mapping() -> FormatterMappingBase:
    return FormatterMapping(_formatter_mapping)


def get_func_lookup() -> dict[str, Callable]:
    return _function_lookup


def get_executor(func_lookup: dict[str, Callable]) -> ExecutorBase:
    return Executor(func_lookup)


def get_flat_transformer(
    survey_metadata: SurveyMetadata,
    spec_mapping: BuildSpecMappingBase,
    executor: ExecutorBase,
    formatter_mapping: FormatterMappingBase
) -> FlatSpecTransformer:

    return FlatSpecTransformer(
        survey_metadata,
        spec_mapping,
        executor,
        formatter_mapping)


def get_looped_transformer(
    survey_metadata: SurveyMetadata,
    spec_mapping: BuildSpecMappingBase,
    executor: ExecutorBase,
    formatter_mapping: FormatterMappingBase
) -> LoopedSpecTransformer:

    return LoopedSpecTransformer(
        survey_metadata,
        spec_mapping,
        executor,
        formatter_mapping)


def get_prepop_transformer(
    survey_id: str,
    spec_mapping: PrepopMappingBase,
    executor: ExecutorBase,
    formatter_mapping: FormatterMappingBase
) -> PrepopTransformer:
    return PrepopTransformer(
        survey_id,
        spec_mapping,
        executor,
        formatter_mapping)
