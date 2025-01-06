"""
Script for converting the PCDM ontology from RDF to LinkML YAML
"""
from schema_automator.importers.rdfs_import_engine import RdfsImportEngine
from linkml_runtime.dumpers import YAMLDumper
from pathlib import Path

def main():
    models_dir = Path().resolve() / "models"
    models_dir.mkdir(exist_ok=True)

    for model in ["models.rdf", "pcdm-ext/file-format-types.rdf", "pcdm-ext/rights.rdf", "pcdm-ext/use.rdf", "pcdm-ext/works.rdf"]:
        output_path = models_dir / f"{model.replace('.rdf', '.yaml')}"
        output_path.parent.mkdir(exist_ok=True)
        # model_url = f"https://raw.githubusercontent.com/duraspace/pcdm/refs/heads/main/{model}"
        model_url = f"https://raw.githubusercontent.com/multimeric/pcdm/refs/heads/fix-80/{model}"
        schema = RdfsImportEngine().convert(model_url, format="xml")
        YAMLDumper().dump(schema, str(output_path))

if __name__ == "__main__":
    main()
