           _    ___ ____ ___ _____ _____ ____  _   _ ___ _     ____  _____ ____  
          / \  |_ _/ ___|_ _|_   _| ____| __ )| | | |_ _| |   |  _ \| ____|  _ \ 
         / _ \  | |\___ \| |  | | |  _| |  _ \| | | || || |   | | | |  _| | |_) |
        / ___ \ | | ___) | |  | | | |___| |_) | |_| || || |___| |_| | |___|  _ < 
       /_/   \_\___|____/___| |_| |_____|____/ \___/|___|_____|____/|_____|_| \_\
   
                                                           
🧠 AISuiteBuilder

AISuiteBuilder è una suite desktop per Windows che genera siti web professionali completi partendo da una semplice descrizione testuale.
Scrivi cosa vuoi realizzare, premi Genera, e l’app costruisce automaticamente un sito pronto all’uso, senza scrivere una riga di codice.
Il sistema è progettato per produrre output reali e utilizzabili, non demo: HTML, CSS e asset vengono generati a partire da una struttura dati solida e sempre rigenerabile.

✨ Funzionalità principali

🖥 Applicazione desktop Windows (portable)
🤖 Generazione automatica tramite AI
🧱 Siti multipagina professionali
✍️ Copywriting realistico in italiano, diverso per ogni pagina
🎨 Temi e layout preset, applicabili in qualsiasi momento
🧩 Editor visuale di pagine e sezioni
🔁 Rigenerazione HTML/CSS non distruttiva
📁 Output ordinato (HTML / CSS / assets)
🚀 Nessuna configurazione richiesta all’utente

🪄 Come funziona

Inserisci una descrizione del sito
(es. “Studio legale moderno specializzato in diritto del lavoro”)

Premi Genera sito
AISuiteBuilder:
analizza la richiesta, pianifica pagine e sezioni, genera struttura, testi e stile
Il sito viene creato nella cartella /project
👉 Il file project.json è la fonte di verità:
HTML e CSS vengono sempre rigenerati da lì, mai modificati manualmente.

🖼 Interfaccia

Campo di testo per il prompt
Log di avanzamento in tempo reale
Generazione asincrona (l’app non si blocca)
Editor per pagine e sezioni
Gestione Layout & Temi tramite preset
Design scuro moderno e pulito

🧩 Architettura

Il progetto è strutturato in modo modulare ed estendibile:
core/ → parsing AI, logica, generazione contenuti e sito
gui/ → interfaccia desktop (PySide6)
project/ → progetti generati (project.json, HTML, CSS)
library/ → layout e temi preset
La GUI non contiene logica di business: è solo un’interfaccia sopra il core.

⚙️ Requisiti

Windows 10 / 11
Versione portable (nessuna installazione necessaria)
💡 In modalità sviluppo il core può essere collegato a modelli AI diversi (anche locali), ma l’utente finale non deve configurare nulla.

📌 Stato del progetto
✅ Core stabile
✅ GUI funzionante
✅ Layout e temi applicabili
✅ Rigenerazione affidabile

🔧 In continua evoluzione
📄 Licenza

MIT License

