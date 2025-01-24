import mkdocs_gen_files
from pathlib import Path

models = Path(__file__).parent / "models"

with mkdocs_gen_files.open("models.md", "w") as f:
    f.write("# Models\n")

    for subdir_name, vocab_name in [
        ("dc", "Dublin Core (DC)"),
        ("skos", "Simple Knowledge Organization System (SKOS)"),
        ("pcdm", "Portland Common Data Model (PCDM)"), 
        ("prof", "The Profiles Vocabulary (PROF)"),
        ("sdo", "Schema.org"),
        ("bioschemas", "Bioschemas"),
    ]:
        f.write(f"## {vocab_name}\n")
        subdir = models / subdir_name
        for file in sorted(subdir.iterdir()):
            f.write(f"- [{file.stem}]({file.relative_to(models)})\n")
