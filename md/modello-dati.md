# Modello Dati

## charLists — Oggetto Principale

`charLists` è l'unico oggetto di stato runtime che viene serializzato nel JSON di salvataggio.

```javascript
const charLists = {
    feats: [],             // Imprese/Doti
    wealthLog: [],         // Log transazioni ricchezza
    raceTraits: [],        // Tratti razziali (da traits.json o manuali)
    classFeatures: [],     // Feature di classe (da features.json o manuali)
    multiClassFeatures: [], // Feature multiclasse
    languages: [],         // Lingue conosciute
    myStuff: [],           // Inventario unificato (armi, armature, oggetti)
    abracadabra: [],       // Incantesimi nel grimorio
    slotProgressions: [],  // Progressioni slot per livello/classe
    hiddenPanels: [],      // Pannelli nascosti dall'utente
    collapsedPanels: []    // Pannelli collassati (non nascosti)
};
```

---

## Schema Elementi per Array

### feats[]
```javascript
{
    name: "Nome impresa",
    desc: "Descrizione",
    races: "Razze compatibili",
    modVal: 1,            // modificatore numerico (opzionale)
    modTarget: "STR",     // caratteristica target (opzionale)
    inUse: true,          // true = In Uso (bonus attivi), false = Non in uso
    timestamp: "10/05/2026, 12:00:00"
}
```

### wealthLog[]
```javascript
{
    type: "GP",           // CP | SP | EP | GP | PP
    amount: 50,
    desc: "Descrizione transazione",
    timestamp: "..."
}
```

### raceTraits[] / classFeatures[] / multiClassFeatures[]
```javascript
{
    name: "Nome tratto",
    desc: "Descrizione",
    modVal: 2,            // bonus numerico
    modTarget: "STR",     // caratteristica interessata (STR|DEX|CON|INT|WIS|CHA|ATK|DMG)
    inUse: true,          // true = In Uso (bonus attivi), false = Non in uso
    sourceTag: "race_elf", // tag sorgente per aggiornamenti
    timestamp: "..."
}
```

### languages[]
```javascript
{
    name: "Common",
    desc: "Descrizione",
    type: "Standard",     // tipo lingua (da languages.json)
    speakers: "Humans",
    inUse: true,          // true = In Uso, false = Non in uso
    timestamp: "..."
}
```

### myStuff[]
```javascript
{
    name: "Longsword",
    category: "Martial Melee Weapons",  // da equipment-categories.json label
    categoryIndex: "martial-melee-weapons",
    desc: "Descrizione",
    damage: "1d8 slashing",
    twoHandedDamage: "1d10 slashing",
    throwRange: "",       // es. "20/60"
    ac: 0,                // bonus CA (per armature)
    weight: 1.5,          // in kg
    cost: "15 gp",
    properties: "Versatile",
    modVal: 0,            // bonus a caratteristica
    modTarget: "",        // es. "STR"
    inUse: true,          // true = In Uso, false = Trasportato
    timestamp: "..."
}
```

### abracadabra[]
```javascript
{
    name: "Fireball",
    level: 3,             // 0 = cantrip
    school: "Evocation",
    castingTime: "1 action",
    range: "150 feet",
    components: "V, S, M",
    duration: "Instantaneous",
    desc: "...",
    damage: "8d6 fire",
    modVal: "",           // modificatore numerico (opzionale)
    modTarget: "",        // caratteristica target (opzionale)
    inUse: true,          // true = In Uso (bonus attivi), false = Non in uso
    usedCount: 0,         // contatore utilizzi (pulsante +U)
    studiedCount: 0,      // contatore studiati (pulsante +S)
    timestamp: "..."
}
```

### slotProgressions[]
```javascript
{
    className: "Wizard",
    classLevel: 5,
    slots: [0, 4, 3, 2, 1, 0, 0, 0, 0, 0],  // indice = livello slot (0=cantrip)
    known: 10,            // incantesimi conosciuti (opzionale)
    timestamp: "..."
}
```

### hiddenPanels[]
```javascript
{
    id: "panel-stats",
    titleKey: "Caratteristiche"
}
```

### collapsedPanels[]
```javascript
{
    id: "panel-notes"
}
```

---

## Database Runtime (non persistiti)

Questi array sono popolati al caricamento della pagina dai file JSON e NON vengono salvati nel JSON personaggio.

| Variabile | Sorgente | Uso |
|---|---|---|
| `featsDatabase` | `jsons/feats.json` | Ricerca imprese |
| `languagesDatabase` | `jsons/languages.json` | Ricerca lingue |
| `myStuffDatabase` | `jsons/equipment-categories.json` + target files | Catalogo equipaggiamento |
| `abracadabraDatabase` | `jsons/spells.json` | Catalogo incantesimi |
| `raceFeatureDatabase` | `jsons/races.json` | Info razze per wizard |
| `classFeatureDatabase` | `jsons/classes.json` | Info classi per wizard |
| `raceTraitSelectionDatabase` | `jsons/traits.json` | Selezione tratti razziali |
| `classFeatureSelectionDatabase` | `jsons/features.json` | Selezione feature classe |
| `myStuffCategoryOrder` | derivato da equipment-categories.json | Ordine categorie per rendering |
| `myStuffCategoryOrderMap` | derivato | Map index → position |

---

## Formato File JSON Salvataggio

Esempio struttura completa:

```json
{
    "charName": "Aldric Stormborn",
    "charRace": "Elf",
    "charClassPrimary": "Wizard",
    "charLevel": 5,
    "charHeight": "180cm",
    "charWeight": "70kg",
    "charSpeed": "30ft",
    "hpMax": 32,
    "hpCurrent": 25,
    "hitDice": "5d6",
    "baseACInput": 10,
    "addDexToAC": true,
    "maxWeight": 150,
    "language": "it",
    "str": 10, "dex": 16, "con": 14, "int": 18, "wis": 12, "cha": 8,
    "strTS": false, "dexTS": false, "conTS": false, "intTS": true, "wisTS": true, "chaTS": false,
    "charLists": { ... }
}
```

---

## Retrocompatibilità

`caricaJSON()` gestisce automaticamente i vecchi formati:

```javascript
// Migrazione da formato legacy (pre-v1.43)
if (data.weapons)     → converte in myStuff con category = "Weapons"
if (data.equipment)   → converte in myStuff con category = "Equipment"
if (data.protections) → converte in myStuff con category = "Armor"
```

La migrazione avviene prima di qualsiasi rendering, quindi è trasparente all'utente.
