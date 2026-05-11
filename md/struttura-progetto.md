# Struttura Progetto: DD5e Character Manager

## Panoramica

Applicazione web **single-page** (SPA) per la gestione della scheda personaggio di **Dungeons & Dragons 5e**.  
Versione attuale: **v1.43**  
Stack tecnologico: HTML5 + CSS3 + JavaScript vanilla (no framework)  
File principale: `index.html` (unico file applicativo, ~3400+ righe)  
Foglio di stile: `styles.css`  
Dati: 31 file JSON in `/jsons/`

---

## Albero dei File

```
DD5e_Character_Manager/
├── index.html              ← applicazione completa (HTML + JS inline)
├── styles.css              ← stile (dark mode, glass-morphism, CSS variables)
├── changelog               ← registro modifiche per versione
├── .codex                  ← file vuoto (placeholder)
├── jsons/                  ← dataset D&D 5e (sola lettura a runtime)
│   ├── ability-scores.json
│   ├── alignments.json
│   ├── armors.json
│   ├── backgrounds.json
│   ├── classes.json
│   ├── class_levels.json
│   ├── collections.json
│   ├── conditions.json
│   ├── damage-types.json
│   ├── equipment-categories.json   ← catalogo categorie equipaggiamento
│   ├── equipment.json
│   ├── feats.json
│   ├── features.json
│   ├── languages.json
│   ├── magic-items.json
│   ├── magic-schools.json
│   ├── monsters.json
│   ├── names.json
│   ├── proficiencies.json
│   ├── races.json
│   ├── rule-sections.json
│   ├── rules.json
│   ├── skills.json
│   ├── spells.json
│   ├── subclasses.json
│   ├── subraces.json
│   ├── tables.json
│   ├── traits.json
│   ├── weapon-properties.json
│   ├── weapons.json
│   └── README
├── md/                     ← documentazione del progetto (questa cartella)
│   ├── struttura-progetto.md       ← questo file
│   ├── pannelli.md                 ← dettaglio pannelli UI
│   ├── modello-dati.md             ← struttura dati charLists e salvataggio JSON
│   ├── funzioni-js.md              ← catalogo funzioni JavaScript
│   ├── dati-json.md                ← descrizione dei file JSON di dati
│   └── storia-sviluppo.md          ← cronologia sviluppo con cross-ref sessione Gemini
├── jsonTranslate/           ← utility/script per traduzione JSON (non in tracking)
└── testfile.test            ← file di test (non in tracking)
```

---

## Pannelli UI (14 pannelli)

| ID Pannello | Titolo (EN) | Span | Contenuto principale |
|---|---|---|---|
| `panel-header` | Character | 2 | Nome, razza, classe, livello, altezza, peso, livello totale, bonus competenza, peso trasportato |
| `panel-stats` | Ability Scores | 1 | 6 caratteristiche con colonne base / TS / bonus; checkbox tiro salvezza |
| `panel-skills` | Skills | 1 | Lista abilità con modificatori calcolati |
| `panel-combat` | Combat & AC | 1 | HP (max/current/residui), iniziativa, percezione passiva, velocità, CA totale, dado vita |
| `panel-features` | Race & Class Features | 2 | Tratti razziali + feature di classe; tabella riepilogativa bonus; import auto da races.json/features.json |
| `panel-multiclass` | Multiclass | 2 | Feature da multiclasse |
| `panel-mystuff` | My Stuff / Il mio Equipaggiamento | 2 | Inventario unificato (armi, armature, oggetti magici, equipaggiamento); stati In Uso / Trasportato; ricerca fulltext; raggruppamento per categoria |
| `panel-wealth` | Wealth | 2 | Log transazioni moneta; totali per tipo |
| `panel-feats` | Feats | 2 | Imprese/doti con modificatori e caratteristica target |
| `panel-languages` | Languages | 2 | Lingue conosciute |
| `panel-wizard` | Wizard Info | 2 | Info incantatore (livello, caratteristica, CD, bonus attacco) |
| `panel-spell-slots` | Spell Slots | 2 | Tabella slot per livello (0=cantrip), colonna Known per classi specifiche |
| `panel-abracadabra` | Spells | 2 | Grimorio (da spells.json); contatori Usati/Studiati; riepilogo tabellare per livello |
| `panel-notes` | Notes | 2 | Note libere |

**Funzionalità comuni a tutti i pannelli:**
- Visibilità toggle (👁️) con lista pannelli nascosti restaurabile
- Drag-and-drop per riordinamento
- Collasso/espansione (con persistenza nel JSON di salvataggio)
- Modalità Lettura / Modifica (`toggleViewMode`)

---

## Funzionalità Globali

| Funzionalità | Dettaglio |
|---|---|
| **i18n** | 5 lingue: EN, IT, FR, DE, ES — selezionabile alla startup |
| **Startup Wizard** | Overlay iniziale con scelta LOAD / CREATE; CREATE richiede nome+razza+classe (locked dopo creazione) |
| **Salvataggio** | JSON scaricato via browser (`salvaJSON`) |
| **Caricamento** | File picker JSON (`caricaJSON`); migrazione automatica da vecchi formati |
| **Stampa** | Riepilogo HTML generato dinamicamente (`stampaScheda`); equipaggiamento "In Uso" in testa |
| **Ricerca** | Sistema fulltext per tutti i pannelli collegati a JSON; navigazione da tastiera (frecce + Enter + ESC) |
| **Calcoli** | AC totale, peso trasportato, modificatori caratteristiche, bonus competenza, tiri salvezza, skill check |

---

## Modalità Operative

```
Startup Overlay
  ├── LOAD → file picker JSON → caricaJSON() → finishStartupFlow()
  └── CREATE → openCreateWizard() → completeCharacterCreate() → applyDefaultCreatePanelSetup() → finishStartupFlow()

Runtime
  ├── Edit Mode  (default) → tutti i controlli visibili
  └── Read Mode            → nasconde drag-handle, pulsanti edit-only
```

---

## Persistenza Dati (JSON Salvataggio)

Il file JSON prodotto da `salvaJSON()` contiene:

```json
{
  "charName": "...",
  "charRace": "...",
  "charClassPrimary": "...",
  "charLevel": 1,
  "hpMax": 0, "hpCurrent": 0,
  "baseACInput": 10, "addDexToAC": true,
  "language": "it",
  "charLists": {
    "feats": [],
    "wealthLog": [],
    "raceTraits": [],
    "classFeatures": [],
    "multiClassFeatures": [],
    "languages": [],
    "myStuff": [],
    "abracadabra": [],
    "slotProgressions": [],
    "hiddenPanels": [],
    "collapsedPanels": []
  }
}
```

**Retrocompatibilità:** `caricaJSON` converte automaticamente i vecchi salvataggi con `weapons`, `equipment`, `protections` separati → formato unificato `myStuff`.
