"""Exact reviewed v2 baselines; no range inference or deployed Git attestation."""
from dataclasses import dataclass
from types import MappingProxyType

from .planning import INCOMPATIBLE, require

DEFAULT_RUNTIME = '0.10.0'


@dataclass(frozen=True)
class Baseline:
    runtime: str
    schema: str
    commit: str

    @property
    def public_schema(self):
        return 'spine-readback-' + self.runtime + '.schema.json'

    @property
    def receipt_readback(self):
        return 'captured_responses_only_spine_' + self.runtime


BASELINES = MappingProxyType({
    '0.10.0': Baseline('0.10.0', '19', '8f3c50b6fd1b4aa534e50925b7417a7a80d19122'),
    '0.12.0': Baseline('0.12.0', '20', '3e65ef0de9e73b62047a0f6328731db08ca91023'),
})


def runtime_baseline(runtime, *, category=INCOMPATIBLE):
    require(isinstance(runtime, str) and runtime in BASELINES,
            'unsupported_successor_runtime', category)
    return BASELINES[runtime]


def manifest_baseline(manifest, *, category=INCOMPATIBLE):
    versions = manifest['compatibility']['spine_runtime_versions']
    require(isinstance(versions, list) and len(versions) == 1,
            'successor_requires_exact_runtime', category)
    return runtime_baseline(versions[0], category=category)


def bind_transport(transport, runtime):
    """Bind concrete public adapters; test read sources may lack this hook.

    The observer independently validates every response under the selected
    baseline even for a supplied test source. No global validator is switched.
    """
    selected = runtime_baseline(runtime)
    select = getattr(transport, 'select_runtime', None)
    if select is not None:
        select(selected.runtime)
    return selected
