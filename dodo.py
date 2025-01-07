from functools import partial
from pathlib import Path
from schema_automator.importers.rdfs_import_engine import RdfsImportEngine
from linkml_runtime.dumpers import YAMLDumper
from urllib.parse import urlparse, urljoin

models_root = Path(__file__).parent.resolve() / "models"

def rdf_to_linkml(rdf_urls: list[str], subdir: str, format: str) -> None:
    models_dir = models_root / subdir
    models_dir.mkdir(exist_ok=True)

    for model_url in rdf_urls:
        parsed = urlparse(model_url)
        rdf_path = Path(parsed.path)
        rdf_name = rdf_path.with_suffix(".yaml").name

        output_path = models_dir / rdf_name
        schema = RdfsImportEngine().convert(model_url, format=format)
        YAMLDumper().dump(schema, str(output_path))


def task_prof():
    """
    Converts prof ontology from RDF to LinkML YAML
    """
    return {
        "actions": [
            partial(
                rdf_to_linkml,
                ["https://www.w3.org/TR/dx-prof/rdf/prof.ttl"],
                subdir="prof",
                format="ttl",
            )
        ],
        "targets": ["models/prof/prof.yaml"],
    }


def task_skos():
    """
    Converts SKOS Simple Knowledge Organization System from RDF to LinkML YAML
    """
    return {
        "actions": [
            partial(
                rdf_to_linkml,
                ["https://www.w3.org/2004/02/skos/core.rdf"],
                subdir="skos",
                format="xml",
            )
        ],
        "targets": ["models/skos/core.yaml"],
    }


def task_dc():
    """
    Converts Dublin Core from RDF to LinkML YAML
    """
    return {
        "actions": [
            partial(
                rdf_to_linkml,
                [
                    "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_terms.ttl"
                ],
                subdir="dc",
                format="ttl",
            )
        ],
        "targets": ["models/dc/core.yaml"],
    }


def task_sdo():
    """
    Converts Schema.org from RDF to LinkML YAML
    """
    return {
        "actions": [
            partial(
                rdf_to_linkml,
                ["https://schema.org/version/latest/schemaorg-current-https.ttl"],
                subdir="sdo",
                format="ttl",
            )
        ],
        "targets": ["models/sdo/schemaorg-current-https.yaml"],
    }

def task_pcdm():
    """
    Converts PCDM from RDF to LinkML YAML
    """
    # Using my fork of the PCDM ontology due to https://github.com/duraspace/pcdm/issues/80
    base_url = "https://raw.githubusercontent.com/multimeric/pcdm/refs/heads/fix-80/"
    urls = ["models.rdf", "pcdm-ext/file-format-types.rdf", "pcdm-ext/rights.rdf", "pcdm-ext/use.rdf", "pcdm-ext/works.rdf"]
    return {
        "actions": [
            partial(
                rdf_to_linkml,
                [urljoin(base_url, x) for x in urls],
                subdir="pcdm",
                format="xml"
            )
        ],
        "targets": [str(models_root / path) for path in urls],
    }
