# Making [JmdictFurigana](https://github.com/Doublevil/JmdictFurigana) compatible with [SudachiPy](https://pypi.org/project/SudachiPy/)

## Create transformed dictionary files

1. install [wanakana](https://pypi.org/project/wanakana/): `pip install wanakana`
2. run in terminal:

```
python main.py initial_directory transformed_directory
```

- initial_directory - directory with initial Jmdictfurigana json files
- transformed_directory - directory where json files with transformed dictionaries should be created

## Initial vs Transformed dictionary formats

For fast items accessing JmdictFurigana dictionaries should be transformed

from:

```
[
    {text: surface,
     reading: reading,
     furigana: [{ruby: part_surface, rt: part_reading}, ...]
     },
    ...
]
```

to:

```
{
    surface: {
              to_katakana(reading_1): 
                    [[surface_part_1, to_katakana(reading_1_part_1)], [surface_part_2, to_katakana(reading_1_part_2)], ...],
              to_katakana(reading_2): 
                    [[surface_part_1, to_katakana(reading_2_part_1)], [surface_part_2, to_katakana(reading_2_part_2)], ...],
              ...
              },
    ...
}
```

For items that have the same (surface, to_katakana(surface_reading)) furigana with the greatest number of parts (maximum
length) is chosen.

Readings are transformed to katakana for making them compatible with `sudachipy.Morpheme`
since `morpheme.reading_form()` is always written in katakana.

## Dictionaries usage

```
from json import load
from sudachipy import Dictionary

text = '可笑しい'
tokenizer = Dictionary().create()
morphemes = tokenizer.tokenize(text)
path = 'path/to/transformed/dictionary/file.json'

with open(path, encoding='utf-8-sig') as file:
    dictionary = load(file)
    for morpheme in morphemes:
        parts = dictionary[morpheme.surface()][morpheme.reading_form()]
        print(parts)
```

```
[['可', 'オ'], ['笑', 'カ'], ['しい', 'シイ']]
```
