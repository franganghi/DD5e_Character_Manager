# DD5e Character Manager

Applicazione web **single-page** per la gestione della scheda personaggio di **Dungeons & Dragons 5e**, eseguibile localmente nel browser senza installazione.

**Versione corrente: v2.00**

TESTA l'applicazione: https://franganghi.github.io/DD5e_Character_Manager/

---

## Caratteristiche principali

- **14 pannelli** riorganizzabili via drag-and-drop: caratteristiche, abilità, combattimento, tratti, multiclasse, inventario, ricchezza, talenti, lingue, preparazione incantesimi, slot incantesimo, grimorio, note
- **Wizard di creazione** con selezione lingua, razza e classe; blocco post-creazione dei campi identità
- **5 lingue** selezionabili: EN, IT, FR, DE, ES — localizzazione estesa ai database JSON (`name_it`, `desc_it`, ecc.)
- **Ricerca full-text** con navigazione da tastiera (↑↓ Enter ESC) in tutti i pannelli collegati a database JSON
- **panel-mystuff**: inventario unificato con stati In Uso / Trasportato, calcolo CA e peso, raggruppamento per categoria
- **panel-abracadabra**: grimorio con raggruppamento per livello, contatori Usati/Studiati, reset separati
- **panel-stats**: tabella bonus sorgenti (Race Traits, Class Features, Multiclass, Feats, Abracadabra, My Stuff × 8 caratteristiche)
- **panel-combat**: layout a box riordinabili via drag-and-drop, con box TPC e DMG calcolati automaticamente
- **Salvataggio/Caricamento** JSON locale; retrocompatibilità con formati precedenti
- **Stampa** riepilogativa HTML dinamica
- Supporto **Edit / Read mode**, collasso e nascondi/ripristina pannelli

---

## Come avviare

Clona il repository e serve i file con un server HTTP locale (necessario per il fetch dei JSON):

```bash
git clone https://github.com/franganghi/DD5e_Character_Manager.git
cd DD5e_Character_Manager
python3 -m http.server 8000
```

Apri il browser su `http://localhost:8000`.

Non è necessario alcun build step, framework o dipendenza npm.

---

## Struttura file

```
DD5e_Character_Manager/
├── index.html              ← applicazione completa (HTML + JS inline)
├── styles.css              ← foglio di stile (dark mode, CSS variables, glass-morphism)
├── changelog               ← registro modifiche per versione
├── release_notes           ← note di rilascio storiche (v1.13 → v2.00)
├── json_translate.py       ← script per tradurre automaticamente i JSON via deep-translator
├── jsons/                  ← dataset D&D 5e SRD (sola lettura a runtime)
│   ├── equipment-categories.json   ← pivot per panel-mystuff
│   ├── equipment.json / magic-items.json  ← item equipaggiamento e oggetti magici
│   ├── spells.json                 ← grimorio (con campi _it tradotti)
│   ├── classes.json / races.json   ← usati nel wizard di creazione
│   ├── features.json / traits.json ← usati in panel-features
│   ├── languages.json              ← usato in panel-languages
│   ├── oldSpells/                  ← file spell per lingua (fonte traduzioni)
│   └── unused/                     ← file SRD non ancora integrati nell'app
├── md/                     ← documentazione tecnica del progetto
│   ├── INDICE.md
│   ├── struttura-progetto.md
│   ├── pannelli.md
│   ├── modello-dati.md
│   ├── funzioni-js.md
│   ├── dati-json.md
│   └── storia-sviluppo.md
└── CLAUDE.md               ← istruzioni per Claude Code (AI assistant)
```

---

## Traduzione database JSON

Lo script `json_translate.py` traduce automaticamente i campi dei file JSON usando [deep-translator](https://github.com/nidhaloff/deep-translator).

```bash
# Setup (una tantum)
python3 -m venv venv
source venv/bin/activate
pip install -U deep-translator requests

# Esecuzione
python3 json_translate.py <lingua>   # es: python3 json_translate.py it
```

Crediti lista incantesimi JSON: [dmcb su GitHub Gist](https://gist.github.com/dmcb/4b67869f962e3adaa3d0f7e5ca8f4912)

---

## Dati di gioco

I file JSON nella cartella `jsons/` provengono dal **D&D 5e SRD** (System Reference Document) in formato API-compatibile.  
Sono dati di **sola lettura** a runtime: l'applicazione li carica ma non li modifica.

---

## Licenza

Vedi file [LICENSE](LICENSE).
