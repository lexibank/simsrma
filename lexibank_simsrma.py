import attr
from pathlib import Path

from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import progressbar, FormSpec, Cognate

from clldutils.misc import slug


@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)
    Variants = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    Family = attr.ib(default="Sino-Tibetan")
    SubGroup = attr.ib(default=None)


@attr.s
class CustomCognate(Cognate):
    STEDT = attr.ib(default=False)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "simsrma"
    concept_class = CustomConcept
    language_class = CustomLanguage
    cognate_class = CustomCognate
    
    form_spec = FormSpec(
            first_form_only=True,
            missing_data=['NA'],
            separators = '~',
            replacements=[(" - ", "-"), (" -", "-"), (" ", "_")]
            )

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("data.tsv", delimiter="\t", dicts=True)
        args.writer.add_sources()
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = '{0}_{1}'.format(concept.number, slug(concept.english))
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Number=concept.english,
                Variants=concept.attributes["lexibank_gloss"],
            )
            for variant in concept.attributes["lexibank_gloss"]:
                concepts[variant] = idx
            concepts[concept.english] = idx
        
        languages = args.writer.add_languages(lookup_factory="Name")
        # Only instance where the variant is switched, so we fix that manually.
        concepts["duck²⁹"] = "51_duck"

        for i, row in progressbar(enumerate(data)):
            for language in self.languages:
                if language != "Tangut":
                    entry = row.get(language["Name"])
                    if not entry:
                        entry = row.get(language["Name"] + "_form")
                    concept = concepts.get(row.get(language["Name"] + "_gloss"))
                    if entry and concept and entry not in ["NA"] and concept not in ["NA"]:
                        cogset = args.writer.add_forms_from_value(
                            Language_ID=language["Name"],
                            Parameter_ID=concept,
                            Value=entry,
                            Source="Sims2020",
                        )[0]
                        args.writer.add_cognate(
                            cogset,
                            Cognateset_ID=row["Set #1"],
                            STEDT=str(row["STEDT # "] if "STEDT # " in row else ""),
                            Source="Sims2020",
                        )
