from functools import partial
from pathlib import Path
from typing import Any, Iterable
from schema_automator.importers.rdfs_import_engine import RdfsImportEngine
from linkml_runtime.dumpers import YAMLDumper
from urllib.parse import urlparse, urljoin
from linkml.linter.linter import Linter, RuleLevel

models_root = Path(__file__).parent.resolve() / "models"

def url_to_path(url: str, subdir: str, suffix: str = ".yml") -> Path:
    """
    Converts a URL to a local file path

    Params:
        url: URL of the remote file
        subdir: Subdirectory in which to save the file
        suffix: New file extension for the local file
    """
    models_dir = models_root / subdir
    models_dir.mkdir(parents=True, exist_ok=True)
    parsed = urlparse(url)
    rdf_path = Path(parsed.path).with_suffix(suffix)
    rdf_name = rdf_path.with_suffix(".yaml").name
    return models_dir / rdf_name

def rdf_to_linkml(rdf_url: str, subdir: str, format: str) -> None:
    """
    Converts a remote RDF file to LinkML YAML

    Params:
        rdf_url:  URL of the RDF file
        subdir: subdirectory to save the YAML file
        format: format of the RDF file (e.g. "xml", "ttl")
    """
    output_path = url_to_path(rdf_url, subdir)
    schema = RdfsImportEngine().convert(rdf_url, format=format)
    YAMLDumper().dump(schema, str(output_path))

def validate_linkml(model_path: Path) -> None:
    """
    Validates a LinkML YAML file and raises an error if any validation problems are found
    """
    for problem in Linter().validate_schema(model_path):
        if problem.level is RuleLevel.error:
            raise ValueError(problem.message)

def download_and_validate(rdf_url: str, subdir: str, format: str) -> Iterable[dict[str, Any]]:
    """
    Task generator that yields two tasks: one to convert an RDF file to LinkML YAML, and another to validate the YAML file
    """
    output_path = url_to_path(rdf_url, subdir)
    yield {
        "name": f"Convert {rdf_url}",
        "actions": [
            partial(
                rdf_to_linkml,
                rdf_url,
                subdir=subdir,
                format=format
            )
        ],
        "targets": [output_path],
    }
    yield {
        "name": f"Validate {rdf_url}",
        "file_dep": [output_path],
        "actions": [partial(validate_linkml, output_path)],
    }


def task_prof():
    """
    Converts prof ontology from RDF to LinkML YAML
    """
    yield from download_and_validate("https://www.w3.org/TR/dx-prof/rdf/prof.ttl", "prof", "ttl")

def task_skos():
    """
    Converts SKOS Simple Knowledge Organization System from RDF to LinkML YAML
    """
    yield from download_and_validate("https://www.w3.org/2004/02/skos/core.rdf", "skos", "xml")

def task_dc():
    """
    Converts Dublin Core from RDF to LinkML YAML
    """
    yield from download_and_validate("https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_terms.ttl", "dc", "ttl")

def task_sdo():
    """
    Converts Schema.org from RDF to LinkML YAML
    """
    yield from download_and_validate("https://schema.org/version/latest/schemaorg-current-https.ttl", "sdo", "ttl")

def task_pcdm():
    """
    Converts PCDM from RDF to LinkML YAML
    """
    # Using my fork of the PCDM ontology due to https://github.com/duraspace/pcdm/issues/80
    base_url = "https://raw.githubusercontent.com/multimeric/pcdm/refs/heads/fix-80/"
    for url in ["models.rdf", "pcdm-ext/file-format-types.rdf", "pcdm-ext/rights.rdf", "pcdm-ext/use.rdf", "pcdm-ext/works.rdf"]:
        full_url = urljoin(base_url, url)
        yield from download_and_validate(full_url, "pcdm", "xml")
