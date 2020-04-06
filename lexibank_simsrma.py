import attr
from pathlib import Path

from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import progressbar, FormSpec, Cognate

import lingpy
from clldutils.misc import slug


@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)
    Variants = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    Family = attr.ib(default="Sino-Tibetan")


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
            separators = '~'
            )

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv('data.tsv', delimiter='\t', dicts=True)
        args.writer.add_sources()
        # TODO: add concepts with `add_concepts`
        concepts = {}
        for concept in self.concepts:
            idx = '{0}_{1}'.format(concept['NUMBER'], slug(concept['ENGLISH']))
            args.writer.add_concept(
                ID=idx,
                Name=concept['ENGLISH'],
                Number=concept['NUMBER'],
                Variants=concept['VARIANTS'],
            )
            for variant in concept['VARIANTS'].split('//'):
                concepts[variant] = idx
            concepts[concept['ENGLISH']] = idx
        
        languages = args.writer.add_languages(lookup_factory="Name")
        for i, row in progressbar(enumerate(data)):
            for language in self.languages:
                if language != 'Tangut':
                    entry = row.get(language['Name'])
                    if not entry:
                        entry = row.get(language['Name']+'_form')
                    concept = concepts.get(row.get(language['Name']+'_gloss'))
                    if entry and concept and not entry in ['NA'] and not concept in ['NA']:
                        cogset = args.writer.add_forms_from_value(
                            Language_ID=language['Name'],
                            Parameter_ID=concept,
                            Value=entry,
                            Source="Sims2020",
                        )[0]
                        args.writer.add_cognate(
                                cogset,
                                Cognateset_ID=row['Set #1'],
                                STEDT=str(row['STEDT # '] if 'STEDT # ' in row else
                                    ''),
                                Source='Sims2020'
                                )


