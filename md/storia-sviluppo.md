# Storia di Sviluppo

## Cross-Reference: Sessione Gemini → Stato Attuale

La sessione esportata da Gemini (`creazione gestione personaggio con gemini.md`) documenta la sessione di sviluppo del pannello `panel-mystuff`, che è l'evoluzione più significativa dell'applicazione.

---

## Cronologia Sviluppo (da git log + changelog)

### Commits Git

| Hash | Messaggio | Significato |
|---|---|---|
| `a697b5a` | Update index.html | Ultima modifica applicata (v1.43) |
| `d68f40d` | aggiunti item in dir jsons | Aggiunta file JSON nel dataset |
| `b4ecebc` | Add files via upload | Caricamento iniziale file |
| `07e167a` | Create README | Creazione README jsons |
| `b1baf65` | Delete jsons directory | Rimozione cartella jsons (poi ricreata) |

### Versione Corrente

**v1.43** — versione più recente, molto ricca di funzionalità (changelog completo in `/changelog`).

---

## Sessione Gemini: Sviluppo panel-mystuff

### Contesto di Partenza
L'app aveva già i pannelli:
- `panel-weapons` — armi
- `panel-equipment` — equipaggiamento generico
- `panel-protections` — armature e protezioni

La richiesta era di creare un pannello unificato `panel-mystuff` che gestisse tutto l'equipaggiamento in modo più avanzato.

### Prima Iterazione (fallita)

**Problema:** Gemini ha creato il pannello ma contestualmente ha tentato di fondere le funzionalità dei vecchi pannelli, rompendo `panel-stuff`, `panel-saves`, `panel-skills`.

**Decisione utente:** Ripristino del file originale e ripartenza.

**Lezione:** Isolare le modifiche a un solo nuovo pannello senza toccare i pannelli esistenti.

### Seconda Iterazione (riuscita, con istruzioni precise)

**Istruzione chiave dell'utente:**
> "non toccare alcun pannello precedente. concentrati a creare il nuovo panel-mystuff in modo che funzioni come ho descritto"

**Risultato:**
1. `loadMyStuffDB()` — carica da `equipment-categories.json` + target file
2. Form omnibus (campi per danno, CA, peso, costo, proprietà, modificatori)
3. Rendering raggruppato per categoria
4. Retrocompatibilità nel caricamento

### Fix Successivi (nella stessa sessione)

1. **Bug ESC/blur** — il dropdown di ricerca non si chiudeva con ESC o cambio focus → risolto con handler globale
2. **Navigazione frecce** — aggiunta navigazione ↑↓ + Enter nei dropdown (per tutti i pannelli)
3. **Formato display** — risultati ricerca in formato `[Categoria] - [Nome Item]`
4. **Stato In Uso / Trasportato** — pulsante `[U]` toggle; calcoli attivi solo per item "In Uso"

### Eliminazione Pannelli Legacy

Dopo la corretta implementazione di `panel-mystuff`, i vecchi pannelli sono stati eliminati:
- `panel-weapons` → rimosso
- `panel-equipment` → rimosso
- `panel-protections` → rimosso

La retrocompatibilità è garantita in `caricaJSON()`.

---

## Evoluzione Architetturale (da changelog v1.43)

### Nuove Funzionalità Principali

| Feature | Dettaglio |
|---|---|
| Startup Wizard | Overlay iniziale LOAD/CREATE con selezione lingua |
| Lock post-creazione | Razza e Classe Principale non modificabili dopo creazione |
| panel-mystuff | Inventario unificato con stati In Uso/Trasportato |
| panel-abracadabra | Grimorio con contatori Usati/Studiati e reset |
| panel-spell-slots | Colonna cantrip (livello 0) e colonna Known |
| Collasso pannelli | Stato persistito nel JSON |
| panel-stats ristrutturato | Colonne base/TS/bonus; integrazione panel-saves |
| Riepilogo features | Tabella bonus Razza/Classe × caratteristiche |
| HP counter | Pulsanti +/-/R; indicatore PF Residui |

### Pattern Ripetuto

L'architettura mostra un pattern chiaro per ogni pannello con ricerca:

```
[Input ricerca] → filterItems(type) → showItemResults(type)
     ↓
[Dropdown risultati] → selectItem(type, index) → populate*Form(item)
     ↓
[Form campi] → add*Item() → renderCustomList(listName)
     ↓
[Lista items] → [U] toggle | [E] edit | [X] remove
     ↓
updateSheet() → updateMyStuffSummary() / updateFeaturesSummary()
```

---

## Decisioni di Design Notevoli

### myStuff come unica fonte di verità

Tutto l'equipaggiamento confluisce in `charLists.myStuff`. I calcoli di CA, peso e modificatori caratteristiche leggono solo da qui. Non esiste più separazione tra armi/armature/oggetti nella struttura dati.

### inUse flag

Il flag `inUse` su ogni item di myStuff distingue:
- **In Uso** → contribuisce a CA, ATK, DMG, bonus caratteristiche
- **Trasportato** → solo peso nel totale trasportato

Questo permette di portare oggetti senza equipaggiarli effettivamente.

### panel-saves eliminato e integrato

Il salvataggio dei tiri salvezza è ora nella colonna TS di `panel-stats`, riducendo il numero di pannelli e concentrando le informazioni sulle caratteristiche in un unico punto.

### Startup Overlay con lock identità

La scelta di bloccare Razza e Classe Principale dopo la creazione è una scelta di design D&D-fedele: questi elementi definiscono il personaggio in modo permanente e cambiarli retroattivamente sarebbe anomalo rispetto al gioco da tavolo.

---

## Problemi Noti / Aree Future

Dedotto dal changelog e dalla sessione Gemini:

1. **Visualizzazione incrociata myStuff** — la sessione menziona che "successivamente faremo in modo che la sola visualizzazione di item di specifiche categorie sarà ANCHE mostrata altrove" → non ancora implementato
2. **Specchietto attacco/difesa** — menzione in sessione di "specchietto dedicato per raggruppare le informazioni di attacco, difesa, vantaggio/svantaggio" → non ancora implementato  
3. **Retrocompatibilità etichette legacy** — alcune chiavi legacy restano per non rompere salvataggi precedenti (nota nel changelog)
