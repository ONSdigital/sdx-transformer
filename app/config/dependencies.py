from collections.abc import Callable

from app.config.specs import _build_spec_mapping, _prepop_spec_mapping, _spp_spec_mapping
from app.config.functions import _function_lookup
from app.definitions.input import SurveyMetadata
from app.definitions.executor import ExecutorBase
from app.definitions.mapper import BuildSpecMappingBase, PrepopMappingBase
from app.definitions.repository import BuildSpecRepositoryBase
from app.services.mappers.formatter_mappings import FormatterMapping
from app.services.mappers.spec_mappings import BuildSpecMapping, PrepopSpecMapping
from app.repositories.file_repository import BuildSpecFileRepository
from app.services.transform.execute import Executor
from app.transformers.submission import SubmissionSpecTransformer
from app.transformers.prepop import PrepopTransformer


def get_formatter_mapping() -> FormatterMapping:
    return FormatterMapping()


def get_spec_repository() -> BuildSpecRepositoryBase:
    return BuildSpecFileRepository()


def get_build_spec_mapping(repository: BuildSpecRepositoryBase) -> BuildSpecMappingBase:
    return BuildSpecMapping(_build_spec_mapping, repository)


def get_spp_spec_mapping(repository: BuildSpecRepositoryBase) -> BuildSpecMappingBase:
    return BuildSpecMapping(_spp_spec_mapping, repository)


def get_prepop_spec_mapping(repository: BuildSpecRepositoryBase) -> PrepopMappingBase:
    return PrepopSpecMapping(_prepop_spec_mapping, repository)


def get_func_lookup() -> dict[str, Callable]:
    return _function_lookup


def get_executor(func_lookup: dict[str, Callable]) -> ExecutorBase:
    return Executor(func_lookup)


def get_submission_transformer(
    survey_metadata: SurveyMetadata,
    spec_mapping: BuildSpecMappingBase,
    executor: ExecutorBase,
    formatter_mapping: FormatterMapping
) -> SubmissionSpecTransformer:

    return SubmissionSpecTransformer(
        survey_metadata,
        spec_mapping,
        executor,
        formatter_mapping)


def get_prepop_transformer(
    survey_id: str,
    spec_mapping: PrepopMappingBase,
    executor: ExecutorBase,
    formatter_mapping: FormatterMapping
) -> PrepopTransformer:
    return PrepopTransformer(
        survey_id,
        spec_mapping,
        executor,
        formatter_mapping)
