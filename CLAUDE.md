# DD5e Character Manager

Applicazione web **single-page** per la gestione della scheda personaggio di Dungeons & Dragons 5e.

- **Versione:** v1.43
- **Stack:** HTML5 + CSS3 + JavaScript vanilla (no framework, no build step)
- **Entry point:** `index.html` (~3400 righe — HTML + JS inline)
- **Stile:** `styles.css` (dark mode, CSS variables, glass-morphism)
- **Dati:** 31 file JSON in `/jsons/` — sola lettura a runtime, fonte D&D 5e SRD

---

## Struttura File

```
DD5e_Character_Manager/
├── index.html              ← applicazione completa
├── styles.css              ← foglio di stile
├── changelog               ← registro modifiche per versione
├── jsons/                  ← dataset D&D 5e (sola lettura)
│   ├── equipment-categories.json   ← pivot per panel-mystuff
│   ├── classes.json / races.json   ← usati nel wizard di creazione
│   ├── features.json / traits.json ← usati in panel-features
│   ├── spells.json                 ← usato in panel-abracadabra
│   ├── languages.json              ← usato in panel-languages (feats.json NON usato: al suo posto traits.json)
│   ├── equipment.json / magic-items.json  ← unici target_file di equipment-categories.json (237+239 item)
│   └── ... (altri 17 file di riferimento)
└── md/                     ← documentazione del progetto
    ├── INDICE.md
    ├── struttura-progetto.md
    ├── pannelli.md
    ├── modello-dati.md
    ├── funzioni-js.md
    ├── dati-json.md
    └── storia-sviluppo.md
```

---

## Pannelli UI (14 pannelli)

| ID | Titolo | Span | Descrizione |
|---|---|---|---|
| `panel-header` | Character | 2 | Nome, razza, classe, livello, altezza, peso, peso trasportato, bonus competenza |
| `panel-stats` | Ability Scores | 1 | 6 caratteristiche: colonne base / TS / bonus aggregati; checkbox tiro salvezza |
| `panel-skills` | Skills | 1 | Lista abilità D&D 5e con modificatori calcolati |
| `panel-combat` | Combat & AC | 1 | HP (max/current/residui), iniziativa, CA totale, velocità, dado vita |
| `panel-features` | Race & Class Features | 2 | Tratti razziali + feature classe; tabella bonus; import automatico da JSON |
| `panel-multiclass` | Multiclass | 2 | Feature da classi secondarie |
| `panel-mystuff` | My Stuff | 2 | Inventario unificato; ricerca fulltext; stati In Uso / Trasportato; raggruppamento per categoria |
| `panel-wealth` | Wealth | 2 | Log transazioni moneta (CP/SP/EP/GP/PP) con totali |
| `panel-feats` | Feats | 2 | Imprese/Doti con modificatori e caratteristica target |
| `panel-languages` | Languages | 2 | Lingue conosciute |
| `panel-wizard` | Wizard Info | 2 | Info incantatore (livello, caratteristica, CD, bonus attacco) |
| `panel-spell-slots` | Spell Slots | 2 | Tabella slot per livello (0=cantrip) + colonna Known |
| `panel-abracadabra` | Spells | 2 | Grimorio con contatori Usati/Studiati e reset per livello |
| `panel-notes` | Notes | 2 | Note libere |

Tutti i pannelli supportano: **drag-and-drop**, **collasso**, **nascondi/ripristina** (👁️), **Edit/Read mode**.

---

## Stato dei Dati — `charLists`

```javascript
const charLists = {
    feats: [],              // Imprese/Doti
    wealthLog: [],          // Log transazioni ricchezza
    raceTraits: [],         // Tratti razziali
    classFeatures: [],      // Feature di classe
    multiClassFeatures: [], // Feature multiclasse
    languages: [],          // Lingue conosciute
    myStuff: [],            // Inventario unificato (armi, armature, oggetti)
    abracadabra: [],        // Incantesimi nel grimorio
    slotProgressions: [],   // Progressioni slot per livello/classe
    hiddenPanels: [],       // Pannelli nascosti dall'utente
    collapsedPanels: []     // Pannelli collassati
};
```

`charLists` è l'unico oggetto serializzato nel JSON di salvataggio.

### Flag `inUse` — presente su TUTTI gli array di charLists

Ogni item in ogni lista ha `inUse: true/false`. Quando `false`, l'item è visualizzato a opacità ridotta e i suoi `modVal`/`modTarget` non vengono sommati in `updateSheet()`. Il peso (myStuff) viene sempre conteggiato.

Il pulsante `[U]` in ogni pannello chiama `toggleItemUse(listName, index)`. Per myStuff il toggle passa tra "In Uso" e "Trasportato"; per gli altri tra "In Uso" e "Non in uso".

### Schema myStuff[] (il più complesso)

```javascript
{
    name, category, categoryIndex, desc,
    damage, twoHandedDamage, throwRange,
    ac, weight, cost, properties,
    modVal, modTarget,
    inUse: true   // true = In Uso (contribuisce a CA/ATK/DMG/bonus), false = Trasportato (solo peso)
}
```

### Campi modVal/modTarget

Presenti su: `myStuff`, `feats`, `raceTraits`, `classFeatures`, `multiClassFeatures`, `languages`, `abracadabra`.  
`updateSheet()` somma i bonus solo dagli item con `inUse !== false`.  
Liste incluse nel calcolo: raceTraits, classFeatures, multiClassFeatures, feats, languages, abracadabra, myStuff.

---

## Funzionalità Principali

| Feature | Dettaglio |
|---|---|
| **i18n** | 5 lingue: EN, IT, FR, DE, ES — selezionabile alla startup; `lf(item, field)` legge `item[field+'_'+currentLang]` dai database JSON |
| **Startup Wizard** | Overlay LOAD/CREATE; creazione richiede nome + razza + classe (locked post-creazione) |
| **Ricerca fulltext** | Sistema comune a tutti i pannelli JSON; navigazione con frecce ↑↓ + Enter + ESC |
| **Calcoli automatici** | CA totale, peso trasportato, bonus caratteristiche, proficiency bonus, tiri salvezza |
| **Salvataggio** | JSON scaricato via browser (`salvaJSON`) |
| **Caricamento** | File picker JSON (`caricaJSON`); migrazione automatica da vecchi formati |
| **Stampa** | Riepilogo HTML dinamico (`stampaScheda`); item "In Uso" in testa |

---

## Architettura JavaScript

Tutto il JS è inline in `index.html`. Pattern comune per ogni pannello con ricerca:

```
filterItems(type) → showItemResults(type) → selectItem(type, idx) → populate*Form(item)
                                                                           ↓
                                                                      add*Item()
                                                                           ↓
                                                               renderCustomList(listName)
                                                                           ↓
                                                                     updateSheet()
```

Funzioni chiave: `updateSheet()`, `renderCustomList()`, `salvaJSON()`, `caricaJSON()`, `stampaScheda()`, `loadMyStuffDB()`, `lf(item, field)`.

### Localizzazione Database (`lf`)

`lf(item, field)` è l'helper centrale per leggere campi tradotti dai database JSON:
- Restituisce `item[field + '_' + currentLang]` se presente e non vuoto
- Altrimenti ritorna `item[field]` (fallback inglese)
- Gestisce array (join `'\n'`)

**Regola Option A**: il valore tradotto viene scritto direttamente in charLists al momento dell'aggiunta (non al salvataggio). I vecchi item nei JSON di salvataggio mantengono il valore originale, ma `renderCustomList('myStuff')` li localizza via `myStuffNameMap` al momento del render.

Variabili di supporto (populate in `loadMyStuffDB`):
- `myStuffCategoryData` — map nome inglese → oggetto categoria (con `name_it`)
- `myStuffNameMap` — map nome inglese item → oggetto DB item (con `name_it`)

---

## Regole di Sviluppo

- **Non toccare pannelli esistenti** quando il task riguarda un nuovo pannello — isolare sempre le modifiche.
- I pannelli `panel-weapons`, `panel-equipment`, `panel-protections` sono stati **eliminati** nella v1.43 (confluiti in `panel-mystuff`). Non reintrodurli.
- `panel-saves` è stato **eliminato** nella v1.43 e integrato come colonna TS in `panel-stats`.
- La retrocompatibilità per i vecchi salvataggi è gestita in `caricaJSON()` — non rimuoverla.
- Tutta la documentazione si trova in `md/` — aggiornarla quando si fanno modifiche significative.

---

## Aree Future (pianificate, non ancora implementate)

- Visualizzazione incrociata degli item `myStuff` in altri pannelli (es. riepilogo armi equipaggiate)
- Specchietto dedicato attacco/difesa/vantaggio/svantaggio derivato da `myStuff`
