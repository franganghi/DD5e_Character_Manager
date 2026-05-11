# File JSON di Dati

Tutti i file si trovano in `/jsons/`. Sono dati **di sola lettura** caricati a runtime dall'app.  
Fonte originale: D&D 5e SRD (System Reference Document) API-compatibile.

### Campi Localizzati (`_XX`)

Alcuni file JSON sono stati estesi con campi tradotti nella forma `{campo}_{lang}` (es. `name_it`, `desc_it`).  
La funzione `lf(item, field)` li legge automaticamente in base a `currentLang`.  
Campi `_XX` presenti per ora:

| File | Campi tradotti | Copertura |
|---|---|---|
| `spells.json` | `name_it`, `desc_it` | 319/319 incantesimi |
| `equipment.json` | `name_it`, `weight_it` | 237/237 item |
| `equipment-categories.json` | `name_it` | 39/39 categorie |
| altri file | — | nessun campo `_XX` ancora |

---

## File Principali (usati direttamente dall'app)

| File | Usato da | Descrizione |
|---|---|---|
| `races.json` | `loadRaceFeatureDB()`, wizard creazione | Razze giocabili (Elf, Dwarf, Human, ...) con bonus caratteristiche, tratti, linguaggi, subraces |
| `classes.json` | `loadClassFeatureDB()`, wizard creazione | Classi (Wizard, Fighter, Rogue, ...) con prerequisiti, proficienze, multiclassing |
| `features.json` | `loadClassFeatureDB()` | Feature di classe per livello (filtrate per classe selezionata) |
| `traits.json` | `loadRaceFeatureDB()` + `loadFeatsDB()` | Tratti razziali; riusato anche come database imprese (featsDatabase) |
| `languages.json` | `loadLanguagesDB()` | Lingue D&D 5e (Standard, Exotic) con parlanti |
| `spells.json` | `loadAbracadabraDB()` | Database completo incantesimi (livello, scuola, componenti, durata, danno, ...) |
| `equipment-categories.json` | `loadMyStuffDB()` | 39 categorie, 822 item referenziati; punta a `equipment.json` e `magic-items.json` come `target_file` |
| `equipment.json` | `loadMyStuffDB()` (via `target_file`) | 237 item: armor, weapon, adventuring-gear, tools, mounts-and-vehicles |
| `magic-items.json` | `loadMyStuffDB()` (via `target_file`) | 239 item: potion, ring, rod, scroll, staff, wand, wondrous-items e altro |
| `equipment.json` | `loadMyStuffDB()` (target) | Equipaggiamento generico (strumenti, kit, veicoli, ...) |
| `weapons.json` | `loadMyStuffDB()` (target) | Armi (semplici e marziali, mischia e a distanza) con danno, proprietà |
| `armors.json` | `loadMyStuffDB()` (target) | Armature con CA, requisito FOR, stealth disadvantage |
| `magic-items.json` | `loadMyStuffDB()` (target) | Oggetti magici con rarità e descrizione |
| `skills.json` | `renderBaseStats()` / `panel-skills` | Lista abilità con caratteristica associata |
| `subraces.json` | consulenza razza | Sottorrazze con bonus aggiuntivi |
| `subclasses.json` | consulenza classe | Sottoclassi con feature specifiche |

---

## File di Riferimento (non caricati direttamente nell'app)

Questi file sono dataset alternativi o specializzati. Alcuni sono sottoinsieme di `equipment.json` o `magic-items.json`; altri coprono aree non ancora implementate nell'app.

| File | Descrizione | Note |
|---|---|---|
| `weapons.json` | Armi con danno e proprietà | Incluso in `equipment.json` |
| `armors.json` | Armature con CA e requisiti | Incluso in `equipment.json` |
| `feats.json` | Imprese/Doti ufficiali | `loadFeatsDB()` usa `traits.json` al suo posto |
| `class_levels.json` | Progressione slot/cantrip per livello | Funzioni `getSlotsForClassLevel()` esistono ma non lo caricano |
| `skills.json` | Lista abilità con caratteristica associata | La lista in `panel-skills` è probabilmente hardcoded |
| `subclasses.json` | Sottoclassi con feature specifiche | Non usato |
| `subraces.json` | Sottorrazze con bonus aggiuntivi | Non usato |
| `ability-scores.json` | 6 caratteristiche con descrizione e skill associate | Non usato |
| `alignments.json` | Allineamenti (Lawful Good, Chaotic Evil, ...) | Non usato |
| `backgrounds.json` | Background con proficienze ed equipment | Non usato |
| `conditions.json` | Condizioni (Blinded, Charmed, ...) con effetti | Non usato |
| `damage-types.json` | Tipi di danno (Acid, Bludgeoning, ...) | Non usato |
| `magic-schools.json` | Scuole di magia (Abjuration, ...) | Non usato |
| `monsters.json` | Database mostri | Non usato |
| `names.json` | Nomi per razza/genere | Non usato |
| `proficiencies.json` | Proficienze in armi, armature, strumenti | Non usato |
| `rule-sections.json` | Sezioni delle regole D&D 5e | Non usato |
| `rules.json` | Regole di gioco con descrizioni | Non usato |
| `collections.json` | Collezioni di riferimenti incrociati | Non usato |
| `tables.json` | Tabelle di gioco (Exhaustion, Madness, ...) | Non usato |
| `weapon-properties.json` | Proprietà armi (Finesse, Heavy, Light, ...) | Non usato |

---

## Struttura equipment-categories.json

Questo file è il pivot del pannello `panel-mystuff`:

```json
[
  {
    "index": "light-armor",
    "label": "Light Armor",
    "equipment": [
      {
        "id": "padded-armor",
        "url": { "target_file": "equipment.json" }
      },
      {
        "id": "leather-armor",
        "url": { "target_file": "equipment.json" }
      }
    ]
  },
  {
    "index": "simple-melee-weapons",
    "label": "Simple Melee Weapons",
    "equipment": [
      {
        "id": "club",
        "url": { "target_file": "weapons.json" }
      }
    ]
  }
]
```

`loadMyStuffDB()` risolve ogni `target_file` per recuperare i dettagli completi di ogni item.

---

## Struttura races.json (estratto)

```json
{
  "index": "elf",
  "name": "Elf",
  "size": "Medium",
  "speed": 30,
  "ability_bonuses": [{ "ability_score": { "name": "DEX" }, "bonus": 2 }],
  "traits": [{ "index": "darkvision", "name": "Darkvision" }],
  "subraces": [{ "index": "high-elf", "name": "High Elf" }],
  "languages": [{ "name": "Common" }, { "name": "Elvish" }]
}
```

---

## Struttura spells.json (estratto)

```json
{
  "index": "fireball",
  "name": "Fireball",
  "level": 3,
  "school": { "name": "Evocation" },
  "casting_time": "1 action",
  "range": "150 feet",
  "components": ["V", "S", "M"],
  "duration": "Instantaneous",
  "desc": ["A bright streak..."],
  "damage": {
    "damage_type": { "name": "Fire" },
    "damage_at_slot_level": { "3": "8d6", "4": "9d6" }
  }
}
```

---

## Note sull'Encoding

I campi `desc` nei JSON possono essere:
- Una stringa semplice: `"desc": "Testo..."`
- Un array di stringhe: `"desc": ["Paragrafo 1", "Paragrafo 2"]`
- Un oggetto strutturato

Le funzioni `normalizeDesc()`, `normalizeProperties()`, `normalizeRange()`, `normalizeDamage()` gestiscono tutte queste varianti prima di presentare i dati all'utente.
