# Dettaglio Pannelli UI

## Comportamento Comune

Tutti i pannelli condividono:
- **Drag handle** (`≡`) per il riposizionamento drag-and-drop (solo Edit Mode)
- **Pulsante 👁️** per nascondere il pannello (aggiunto alla lista "Pannelli nascosti")
- **Collasso** con chevron, stato persistito nel JSON di salvataggio
- **Edit / Read Mode**: i controlli con classe `.edit-only` scompaiono in Read Mode

---

## panel-header

**Titolo:** Character | Personaggio  
**Span:** 2 colonne  

| Campo | ID | Tipo | Note |
|---|---|---|---|
| Nome | `charName` | text input | aggiorna `headerCharNameDisplay` |
| Razza | `charRace` | text input | **locked** dopo creazione |
| Classe Principale | `charClassPrimary` | text input | **locked** dopo creazione |
| Livello Classe | `charLevel` | number | 1-20; trigger `updateSheet()` |
| Altezza | `charHeight` | text | |
| Peso | `charWeight` | text | |
| Livello Totale | `totalLevelDisplay` | span (calcolato) | somma tutti i livelli classe |
| Bonus Competenza | `profBonus` | span (calcolato) | formula standard D&D 5e |
| Peso Trasportato | `totalWeightDisplay` | span (calcolato) | somma myStuff[].weight |
| Peso Massimo | `maxWeight` | number | default 150 kg |

---

## panel-stats

**Titolo:** Ability Scores | Caratteristiche  
**Span:** 1 colonna  
**Renderizzato da:** `renderBaseStats()`

| Colonna | Descrizione |
|---|---|
| Base | Valore caratteristica (3-20) |
| TS | Checkbox tiro salvezza; modificatore calcolato |
| Bonus | Somma di tutti i bonus provenienti dagli altri pannelli |

Le 6 caratteristiche: STR / DEX / CON / INT / WIS / CHA (tradotte per lingua).  
`panel-saves` è stato **eliminato** nella v1.43 e integrato qui come colonna TS.

---

## panel-skills

**Titolo:** Skills | Abilità  
**Span:** 1 colonna  
**Dati da:** `jsons/skills.json`  
**Renderizzato in:** `#skillsContainer`

Lista statica di abilità D&D 5e con modificatore calcolato sulla base della caratteristica associata + proficiency bonus se proficcient.

---

## panel-combat

**Titolo:** Combat & AC | Combattimento  
**Span:** 1 colonna  

| Elemento | ID | Descrizione |
|---|---|---|
| PF Residui | `hpResidualDisplay` | = Max HP - Correnti (può essere negativo) |
| Iniziativa | `initiativeModifier` | = modificatore DEX |
| Percezione Passiva | `passivePerception` | = 10 + Percezione |
| Velocità | `charSpeed` | testo libero, default "30ft" |
| CA Totale | `totalAC` | calcolata da base + DEX + armature in myStuff |
| HP Massimi | `hpMax` | input numerico |
| HP Correnti | `hpCurrentCounter` | contatore con pulsanti +/-/R (mai sotto 0) |
| Dado Vita | `hitDice` | testo, es. "1d8" |
| Base AC | `baseACInput` | default 10 |
| Aggiungi DEX | `addDexToAC` | checkbox |

---

## panel-features

**Titolo:** Race & Class Features | Tratti  
**Span:** 2 colonne  

**Sezioni:**
1. **Feature Bonuses** (`#featuresSummary`) — tabella riepilogativa bonus STR/DEX/CON/INT/WIS/CHA/ATK/DMG per razza e classe
2. **Racial Traits** — ricerca da `traits.json` filtrata per razza; form con nome, descrizione, modificatore, caratteristica target
3. **Class Features** — ricerca da `features.json` filtrata per classe; form analogo

**Import automatico:** al completamento della wizard di creazione, `autoFillMainCareerFeatures()` importa i tratti compatibili.

---

## panel-multiclass

**Titolo:** Multiclass  
**Span:** 2 colonne  

Feature aggiuntive per personaggi multiclasse. Struttura analoga a `panel-features` ma per classi secondarie.

---

## panel-mystuff

**Titolo:** My Stuff / Il mio Equipaggiamento  
**Span:** 2 colonne  
**Sostituisce:** panel-weapons, panel-equipment, panel-protections (eliminati in v1.43)

**Flusso ricerca:**
1. Digita in `#myStuffSearchInput` → `filterItems('mystuff')` → ricerca su `myStuffDatabase`
2. Risultati in `#mystuffSearchResults` (popup dropdown) nel formato `[Categoria] - [Nome]`
3. Selezione con click o frecce ↑↓ + Enter; chiusura con ESC o click esterno
4. `populateMyStuffForm(item)` compila i campi del form

**Campi form (universali):**

| Campo | Descrizione |
|---|---|
| Nome | Nome oggetto |
| Categoria | Categoria equipment-categories.json |
| Descrizione | Testo descrittivo |
| Danno | Es. "1d6 slashing" |
| Raggio / Throw | Range getto (es. "20/60") |
| Danno Two-Handed | Danno a due mani |
| AC | Bonus classe armatura |
| Peso | In kg |
| Costo | Es. "15 gp" |
| Proprietà | Es. "Finesse, Light" |
| Modificatore Valore | Valore numerico bonus |
| Caratteristica Target | Es. "STR", "DEX" |

**Stati item:**
- **In Uso** (`inUse: true`) — contribuisce ai calcoli di CA, ATK, DMG, bonus caratteristiche
- **Trasportato** (`inUse: false`) — pesa ma non contribuisce ai calcoli

**Pulsanti per ogni item:** `[U]` Toggle uso | `[E]` Edit | `[X]` Elimina

**Rendering:** item raggruppati per categoria, ordinati per `myStuffCategoryOrder`

**Riepilogo (`updateMyStuffSummary`):** tabella dinamica con conteggi In Uso / Trasportato

---

## panel-wealth

**Titolo:** Wealth  
**Span:** 2 colonne  

Log transazioni di ricchezza con totali per tipo di moneta (CP, SP, EP, GP, PP).

---

## panel-feats

**Titolo:** Feats | Imprese  
**Span:** 2 colonne  
**Dati da:** `jsons/feats.json`

Ogni feat ha: nome, descrizione, razze compatibili, modificatore numerico, caratteristica target.

---

## panel-languages

**Titolo:** Languages | Lingue  
**Span:** 2 colonne  
**Dati da:** `jsons/languages.json`

Ogni lingua ha: nome, descrizione, tipo (es. "Standard"), parlanti.

---

## panel-wizard

**Titolo:** Wizard Info  
**Span:** 2 colonne  

Informazioni incantatore: livello incantatore, caratteristica di lancio, CD tiro salvezza, bonus attacco incantesimo.

---

## panel-spell-slots

**Titolo:** Spell Slots  
**Span:** 2 colonne  

**Colonne:** Classe/Livello | 0 (cantrip) | 1-9 (livelli slot) | Known (incantesimi conosciuti)

`getSlotsForClassLevel(className, level)` calcola gli slot dalla tabella in `jsons/class_levels.json`.  
`slotProgressions` in charLists persiste le progressioni aggiunte.

---

## panel-abracadabra

**Titolo:** Spells | Incantesimi  
**Span:** 2 colonne  
**Dati da:** `jsons/spells.json`

**Funzionalità:**
- Ricerca e selezione incantesimi dal database
- Raggruppamento per livello (0=cantrip)
- Contatori `U` (Usati) e `S` (Studiati) per incantesimo
- Riepilogo tabellare: righe Utilizzati/Studiati × colonne livelli + totale
- Reset separati per Usati e Studiati

---

## panel-notes

**Titolo:** Notes | Note  
**Span:** 2 colonne  

Area testo libero per appunti del giocatore.

---

## Pannelli Eliminati (legacy, pre-v1.43)

| Pannello rimosso | Sostituito da |
|---|---|
| `panel-weapons` | `panel-mystuff` |
| `panel-equipment` | `panel-mystuff` |
| `panel-protections` | `panel-mystuff` |
| `panel-saves` | Colonna TS in `panel-stats` |
