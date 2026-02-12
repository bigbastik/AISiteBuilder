## 🧠 AISiteBuilder
AISiteBuilder è una suite desktop per Windows che genera siti web professionali partendo da una semplice descrizione testuale. 
Scrivi cosa vuoi realizzare, premi Genera, e l’app costruisce automaticamente un sito pronto all’uso: 
HTML, CSS e asset vengono generati da una struttura dati solida e sempre rigenerabile.

# ✨ Funzionalità principali
Generazione automatica tramite AI (ollama, OpenAI, HuggingFace e altri provider configurabili) dal Configurator.
Copywriting realistico in italiano, coerente con il brand richiesto
Siti multipagina professionali, solo le pagine richieste nel prompt
Temi e layout preset, applicabili in qualsiasi momento
Editor visuale di pagine e sezioni
Rigenerazione HTML/CSS non distruttiva
Output ordinato (HTML / CSS / assets)
Configuratore AI incluso per impostare provider, modello, API key ed endpoint
Caricamento e sincronizzazione siti tramite FTP/SFTP
Possibilità di esportare il sito in formato ZIP pronto all’uso
Anteprima live del sito nel browser
Creazione, modifica, eliminazione di sezioni e inserimento immagini direttamente dall’editor

# 🪄 Come funziona
Inserisci una descrizione del sito (es. “Palestra moderna specializzata in fitness funzionale”)
Premi Genera sito
AISiteBuilder analizza la richiesta, pianifica pagine e sezioni, genera struttura, testi e stile coerente con il brand
Il sito viene creato nella cartella /project
Il file project.json è la fonte di verità: HTML e CSS vengono sempre rigenerati da lì, senza modifiche manuali
Puoi caricare direttamente il sito su server FTP/SFTP selezionando cartella remota e monitorando il progresso
Puoi esportare l’intero progetto in un archivio ZIP pronto per distribuzione
Puoi aprire il sito generato nel browser per anteprima live
L’editor consente di creare, modificare, eliminare sezioni e aggiungere immagini

# 🖼 Interfaccia
Campo di testo per il prompt
Log di avanzamento in tempo reale
Generazione asincrona (l’app non si blocca)
Editor per pagine e sezioni
Gestione Layout & Temi tramite preset
Configuratore AI per scegliere provider, modello, API key ed endpoint
Pulsanti per upload FTP/SFTP, esportazione ZIP e anteprima browser

# 🧩 Architettura
core/ → parsing AI, logica, generazione contenuti e sito
gui/ → interfaccia desktop (PySide6)
project/ → progetti generati (project.json, HTML, CSS)
library/ → layout e temi preset
ask-ai → Default Provider: mlvoca Model: tinyllama
La GUI non contiene logica di business: è solo un’interfaccia sopra il core.

# 🧩 Ragionamento all'avvio
AiSiteBuilder all'avvio cerca .json valido in /configurator, in assenza di .json valido utilizza Ollama (installato in locale), in assenza di entrambi, lavora offline.

⚙️ Requisiti
Windows 10 / 11
Versione portable (nessuna installazione necessaria)
Configuratore AI opzionale per collegare diversi provider e modelli

## 📌 Stato del progetto
✅ Core stabile
✅ GUI funzionante
✅ Layout e temi applicabili
✅ Rigenerazione affidabile
✅ Brand coerente su tutte le pagine e sezioni
✅ Filtraggio pagine non richieste dal prompt
✅ Upload FTP/SFTP funzionante
✅ Esportazione ZIP funzionante
✅ Anteprima browser disponibile
✅ Gestione completa di sezioni e immagini nell’editor

# 🔧 In continua evoluzione

# 📄 MIT License
