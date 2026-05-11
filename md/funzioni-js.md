# Catalogo Funzioni JavaScript

Tutte le funzioni sono definite inline in `index.html` all'interno di un unico `<script>` tag.

---

## Internazionalizzazione (i18n)

| Funzione | Riga | Descrizione |
|---|---|---|
| `setLanguage(lang)` | ~819 | Imposta la lingua (EN/IT/FR/DE/ES); aggiorna attributi `data-i18n` |
| `syncStartupLanguageButtons()` | ~811 | Aggiorna visivamente i pulsanti lingua nella startup overlay |
| `getStatLabel(stat)` | ~865 | Restituisce etichetta tradotta per una caratteristica (STR→FOR in IT, ecc.) |
| `lf(item, field)` | ~827 | **Helper localizzazione database.** Restituisce `item[field + '_' + currentLang]` se presente e non vuoto, altrimenti `item[field]`. Gestisce array (join `'\n'`). Usato in tutte le funzioni `populate*Form`, `filterItems`, `renderCustomList` e import automatici. |

---

## Startup e Creazione Personaggio

| Funzione | Riga | Descrizione |
|---|---|---|
| `openCreateWizard()` | ~1159 | Mostra il form creazione (wizard); popola select razza e classe da JSON |
| `cancelCreateWizard()` | ~1174 | Torna alla schermata LOAD/CREATE |
| `completeCharacterCreate()` | ~1188 | Valida i campi obbligatori e inizializza il personaggio |
| `applyDefaultCreatePanelSetup()` | ~1236 | Imposta ordine e visibilità default dei pannelli per un nuovo personaggio |
| `finishStartupFlow()` | ~1179 | Chiude la startup overlay e mostra il mainContainer |
| `triggerStartupLoad()` | ~1231 | Attiva il file picker per caricare un JSON esistente |
| `setCharIdentityLock(lock)` | ~1022 | Blocca/sblocca i campi Razza e Classe Principale |

---

## Caricamento Database JSON

| Funzione | Riga | Sorgente |
|---|---|---|
| `loadRaceFeatureDB()` | ~974 | `races.json`, `traits.json` |
| `loadClassFeatureDB()` | ~994 | `classes.json`, `features.json` |
| `loadFeatsDB()` | ~1304 | `traits.json` (nota: il nome della funzione è fuorviante, vedi TODO in memoria) |
| `loadLanguagesDB()` | ~1321 | `languages.json` |
| `loadAbracadabraDB()` | ~1385 | `spells.json` |
| `loadMyStuffDB()` | ~1503 | `equipment-categories.json` + tutti i target file referenziati |

`loadMyStuffDB()` è la più complessa: legge `equipment-categories.json`, poi carica dinamicamente ogni `target_file` referenziato (`equipment.json`, `magic-items.json`). Oltre a costruire `myStuffDatabase`, popola:
- `myStuffCategoryOrder` — ordine delle categorie
- `myStuffCategoryOrderMap` — map nome inglese → posizione per l'ordinamento
- `myStuffCategoryData` — map nome inglese → oggetto categoria completo (include `name_it` per localizzazione header)
- `myStuffNameMap` — map nome inglese item → oggetto DB item (per localizzare item già in charLists)

`parseAbracadabraEntry` e `parseMyStuffEntry` preservano tutti i campi `_XX` (es. `name_it`, `desc_it`) dal JSON grezzo, copiandoli nell'oggetto parsato.

---

## Normalizzazione Dati

| Funzione | Riga | Descrizione |
|---|---|---|
| `normalizeDesc(v)` | ~1421 | Normalizza descrizioni (array → stringa, oggetti → testo leggibile) |
| `normalizeProperties(v)` | ~1428 | Normalizza proprietà (array di oggetti → stringa "Finesse, Light") |
| `normalizeRange(v)` | ~1439 | Normalizza range (oggetto → "20/60" o "5 ft") |
| `normalizeDamage(v)` | ~1448 | Normalizza danno (oggetto → "1d8 slashing") |
| `normalizeSpellField(v)` | ~1336 | Normalizza campo generico incantesimo |
| `boolFromSpellValue(v)` | ~1343 | Converte valori booleani negli spell |
| `formatSpellDamageBlock(spell)` | ~1347 | Formatta il blocco danno di un incantesimo |
| `parseAbracadabraEntry(spell)` | ~1356 | Parsing completo di uno spell da spells.json → oggetto charLists |
| `parseMyStuffEntry(raw, cat, catIdx, tgt)` | ~1459 | Parsing completo di un item da JSON → oggetto myStuff |

---

## Sistema di Ricerca

| Funzione | Riga | Descrizione |
|---|---|---|
| `getSearchElements(type)` | ~1404 | Restituisce {input, resultsEl, database} per il tipo dato |
| `filterItems(type)` | ~1559 | Filtra il database per query usando `lf` su tutti i campi testuali; mostra risultati con nomi localizzati |
| `showItemResults(type)` | ~1631 | Popola il dropdown con tutti gli item; usa `lf(item, 'name')` per il display |
| `selectItem(type, index)` | ~1661 | Seleziona un item dal dropdown; chiama la funzione `populate*` appropriata |

**Tipi supportati:** `'feat'` | `'language'` | `'mystuff'` | `'abracadabra'` | `'racetrait'` | `'classfeature'`

La ricerca avviene **sempre nella lingua corrente**: se `currentLang === 'it'`, `filterItems` usa `lf(item, 'desc')` che legge `item.desc_it` se presente.

Il keydown handler globale (dentro DOMContentLoaded) gestisce la navigazione frecce ↑↓ + Enter + ESC per tutti i dropdown.

---

## Popolamento Form

Tutte le funzioni `populate*Form` usano `lf(item, field)` per i campi testuali: il valore mostrato nel form è già nella lingua corrente. Quando l'utente clicca Add, il valore tradotto viene salvato direttamente in charLists (Option A).

| Funzione | Riga | Descrizione |
|---|---|---|
| `populateFeatForm(item)` | ~1693 | Compila il form feat; usa `lf` per `name`, `desc` |
| `populateLanguageForm(item)` | ~1717 | Compila il form lingua; usa `lf` per `name`, `desc` |
| `populateMyStuffForm(item)` | ~1818 | Compila il form omnibus di panel-mystuff; usa `lf` per `name`, `desc`, `properties` |
| `populateAbracadabraForm(item)` | ~1844 | Compila il form incantesimo; usa `lf` per `name`, `desc`, `range`, `castingTime`, `duration`, `material`, `higherLevel` |
| `populateRaceTraitForm(item)` | ~1135 | Compila il form tratto razziale; usa `lf` per `name`, `desc` |
| `populateClassFeatureForm(item)` | ~1147 | Compila il form feature classe; usa `lf` per `name`, `desc` |

---

## Import Automatico Feature

| Funzione | Riga | Descrizione |
|---|---|---|
| `autoFillMainCareerFeatures()` | ~1061 | Import automatico tratti razza e feature classe al completamento wizard; usa `lf` per nome e desc |
| `importRaceTraitsFromRace(race)` | ~1740 | Aggiunge tratti razziali compatibili in raceTraits; usa `lf` per nome e desc dei tratti |
| `importClassFeaturesFromClass(cls)` | ~1787 | Aggiunge feature classe in classFeatures; usa `lf` per nome e desc delle feature |
| `isFeatureRaceCompatible(feature, raceIndex)` | ~1104 | Verifica compatibilità feature con razza |
| `refreshFeatureSelectionLists()` | ~1116 | Aggiorna le liste di selezione feature dopo cambio razza/classe |
| `getRaceBySelection()` | ~1035 | Legge la razza selezionata dal database |
| `getClassBySelection()` | ~1048 | Legge la classe selezionata dal database |
| `statIndexToModTarget(statIndex)` | ~1735 | Converte indice caratteristica → stringa target ("STR", "DEX", ...) |

---

## Aggiunta Item

| Funzione | Riga | Descrizione |
|---|---|---|
| `addMyStuffItem()` | ~2675 | Aggiunge item all'inventario da form; chiama `renderCustomList` e `updateMyStuffSummary` |
| `addFeatItem()` | ~2724 | Aggiunge impresa |
| `addLanguageItem()` | ~2744 | Aggiunge lingua |
| `addAbracadabraItem()` | ~1863 | Aggiunge incantesimo al grimorio |
| `addCustomFeature(listName, ...)` | ~2624 | Aggiunge feature generica (raceTraits, classFeatures) |
| `addCustomItem(listName, ...)` | ~2654 | Aggiunge item generico (notes, ecc.) |
| `addWealth()` | ~3040 | Aggiunge transazione ricchezza |
| `addSlotProgression()` | ~2573 | Aggiunge progressione slot incantesimo |

---

## Gestione Item Esistenti

| Funzione | Riga | Descrizione |
|---|---|---|
| `toggleMyStuffUse(index)` | ~2762 | Alterna stato In Uso / Trasportato per un item myStuff |
| `editCustomItem(listName, index)` | ~2945 | Apre l'item in modifica nel form |
| `removeCustomItem(listName, index)` | ~3030 | Rimuove item dall'array e aggiorna rendering |
| `incrementAbracadabraUsed(index)` | ~1904 | +1 al contatore Usati di un incantesimo |
| `incrementAbracadabraStudied(index)` | ~1912 | +1 al contatore Studiati |
| `resetAbracadabraUsed()` | ~1920 | Azzera tutti i contatori Usati |
| `resetAbracadabraStudied()` | ~1928 | Azzera tutti i contatori Studiati |

---

## Rendering

| Funzione | Riga | Descrizione |
|---|---|---|
| `renderCustomList(listName)` | ~2769 | Renderizza la lista di un pannello (router centrale) |
| `renderBaseStats()` | ~2303 | Renderizza la griglia caratteristiche in panel-stats |
| `renderHiddenPanels()` | ~2367 | Aggiorna la lista di pannelli nascosti (barra di ripristino) |
| `renderSlotProgressions()` | ~2586 | Renderizza la tabella slot incantesimo |
| `renderWealthLog()` | ~3059 | Renderizza il log ricchezza |

`renderCustomList` gestisce: `feats`, `languages`, `myStuff` (con raggruppamento per categoria), `raceTraits`, `classFeatures`, `multiClassFeatures`, `abracadabra` (con raggruppamento per livello), `wealthLog`.

Il branch `myStuff` localizza al volo:
- **Header categoria**: `lf(myStuffCategoryData[cat], 'name')` — traduce "Adventuring Gear" → "Equipaggiamento da Avventura"
- **Nome item**: lookup in `myStuffNameMap[item.name]` + `lf` — traduce anche item già salvati in inglese nei JSON esistenti
- **Ordinamento**: usa i nomi localizzati per il `localeCompare`

---

## Calcoli e Aggiornamenti

| Funzione | Riga | Descrizione |
|---|---|---|
| `updateSheet()` | ~2414 | Ricalcola tutto: CA, peso, bonus, proficiency, tiri salvezza, skill |
| `updateHeaderName()` | ~2099 | Aggiorna il nome personaggio nella menu bar |
| `updateFileInfo()` | ~2108 | Aggiorna l'indicatore [Unsaved] / nome file |
| `updateTotalWeight()` | ~2528 | Ricalcola peso trasportato da myStuff[].weight |
| `updateFeaturesSummary()` | ~1988 | Aggiorna la tabella bonus in panel-features |
| `updateMyStuffSummary()` | ~2058 | Aggiorna il riepilogo In Uso / Trasportato in panel-mystuff |
| `updateAbracadabraSummary()` | ~1936 | Aggiorna la tabella riepilogativa incantesimi |
| `updateWealthTotals()` | ~3053 | Ricalcola i totali per tipo moneta |
| `adjustHpCounter(delta)` | ~2512 | +/-  HP Correnti (non scende sotto 0) |
| `resetHpCounter()` | ~2521 | Azzera HP Correnti |

---

## Calcoli Slot Incantesimo

| Funzione | Riga | Descrizione |
|---|---|---|
| `getSlotsForClassLevel(className, level)` | ~2543 | Restituisce array slot da class_levels.json |
| `getCantripsForClassLevel(className, level)` | ~2555 | Restituisce numero cantrip conosciuti |
| `getSpellsKnownForClassLevel(className, level)` | ~2564 | Restituisce incantesimi conosciuti |

---

## UI / Pannelli

| Funzione | Riga | Descrizione |
|---|---|---|
| `hidePanel(panelId, titleStrKey)` | ~2347 | Nasconde il pannello, aggiunge a hiddenPanels |
| `restorePanel(panelId)` | ~2355 | Ripristina il pannello nascosto |
| `toggleViewMode()` | ~2288 | Alterna Edit / Read Mode |
| `applyViewModeState(isViewMode)` | ~2261 | Applica lo stato modalità visiva |
| `initPanelCollapseControls()` | ~2122 | Inizializza i controlli di collasso per tutti i pannelli |
| `setPanelCollapsed(panelId, collapsed)` | ~2142 | Imposta lo stato collasso di un pannello |
| `togglePanelCollapse(panelId)` | ~2169 | Alterna collasso/espansione |
| `initDragAndDrop()` | ~2384 | Inizializza il drag-and-drop per il riordinamento pannelli |

---

## Salvataggio / Caricamento

| Funzione | Riga | Descrizione |
|---|---|---|
| `salvaJSON()` | ~3220 | Serializza lo stato in JSON e scarica il file |
| `caricaJSON(event)` | ~3287 | Legge un file JSON, migra dati legacy, ripristina lo stato |
| `stampaScheda()` | ~3078 | Genera e apre una finestra di stampa HTML con riepilogo |

---

## Helper / Utility

| Funzione | Riga | Descrizione |
|---|---|---|
| `listNames(arr)` | ~929 | Array → stringa nomi separati da virgola |
| `buildRaceSummary(race)` | ~933 | Costruisce testo descrittivo di una razza |
| `buildClassSummary(cls)` | ~954 | Costruisce testo descrittivo di una classe |
| `parseTagList(value)` | ~2048 | Parsing stringa tag separati da virgola |
| `getUseLabel(item)` | ~2053 | Restituisce etichetta "In Uso" / "Trasportato" tradotta |
