# LA VARIABILE 2.0

Sito statico gratuito su GitHub Pages, con raccolta RSS automatizzata da GitHub Actions.

## Pubblicazione

1. Carica nella radice del repository tutti i file e le cartelle di questo pacchetto (mantieni `.github/workflows/daily.yml`).
2. Apri `Settings > Pages > Build and deployment`, scegli `Deploy from a branch`, quindi `main` e `/(root)`, e salva.
3. Il sito previsto è https://luckino1986-hash.github.io/la-variabile2/ . Verifica l'effettiva attivazione.
4. Vai in `Actions > LA VARIABILE - edizione quotidiana > Run workflow` per una prima esecuzione.
5. Se il commit automatico fallisce per permessi, in `Settings > Actions > General > Workflow permissions` scegli `Read and write permissions` (se disponibile).

## Orario

Il workflow è pianificato per 05:45 e 06:45 UTC, così da intercettare rispettivamente le 07:45 italiane d'estate e d'inverno. In ogni caso viene generata al massimo una edizione al giorno; può esserci un secondo avvio privo di modifiche. GitHub Actions può avviarsi in ritardo.

## Qualità e limiti

È una **versione gratuita di base**: presenta i titoli e gli estratti forniti dai feed RSS, con i collegamenti alle fonti. Non crea riassunti redazionali autonomi di 60–100 parole, non legge/verifica integralmente le pagine degli articoli, e non può garantire 10–12 notizie ogni giorno. In assenza di almeno 10 elementi idonei, conserva l'ultima edizione. Alcuni indirizzi dei feed potrebbero non funzionare: il workflow registra quelli falliti. Le sezioni speciali restano vuote fino all'aggiunta di una fase editoriale affidabile.

GitHub Pages e GitHub Actions sono soggetti alle condizioni e ai limiti dei rispettivi piani gratuiti.
