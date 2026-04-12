from pathlib import Path
import sys

import genanki
import yaml

if len(sys.argv) < 2:
    print("Usage: python build_anki_deck.py <output_file>")
    sys.exit(1)

LAPIS_TEMPLATE_ID = 1667218449922
LAPIS_DECK_ID = 1759068131726
BUILD_DIR = Path(__file__).resolve().parent
SRC_DIR = BUILD_DIR.parent / "src"

with open(SRC_DIR / "front.html", "r", encoding="utf-8") as front_file:
    front_content = front_file.read()

with open(SRC_DIR / "back.html", "r", encoding="utf-8") as back_file:
    back_content = back_file.read()

with open(SRC_DIR / "styling.css", "r", encoding="utf-8") as css_file:
    css_content = css_file.read()

with open(BUILD_DIR / "anki_fields.yaml", "r", encoding="utf-8") as fields_file:
    anki_fields = yaml.safe_load(fields_file)

lapis = genanki.Model(
    LAPIS_TEMPLATE_ID,
    "Lapis",
    fields=anki_fields,
    templates=[
        {
            "name": "Mining",
            "qfmt": front_content,
            "afmt": back_content,
        },
    ],
    css=css_content,
)

deck = genanki.Deck(LAPIS_DECK_ID, "Lapis")

expected_field_count = len(anki_fields)

with open(BUILD_DIR / "example_card.csv", "r", encoding="utf-8") as f:
    for line_number, line in enumerate(f, start=1):
        fields_content = line.rstrip("\r\n").split("\t")
        if len(fields_content) != expected_field_count:
            raise ValueError(
                f"example_card.csv line {line_number}: expected "
                f"{expected_field_count} fields, got {len(fields_content)}"
            )
        deck.add_note(
            genanki.Note(
                model=lapis, fields=fields_content, tags=["アニメ::小市民シリーズ"]
            )
        )

package = genanki.Package(deck)
package.media_files = [
    str(BUILD_DIR / "media_files" / "yomitan_audio_2024-07-20-15-08-08-382.ogg"),
    str(BUILD_DIR / "media_files" / "shoushiminseries04_08m44s853ms_08m47s653ms.ogg"),
    str(BUILD_DIR / "media_files" / "shoushiminseries04_08m46s485ms.webp"),
    str(BUILD_DIR / "media_files" / "yomitan_dictionary_media_1_2024-07-20-15-08-08-382.svg"),
]
package.write_to_file(sys.argv[1])
