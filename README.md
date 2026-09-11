# Singapore Travel Assistant

An AI-powered Singapore Travel Assistant that combines **Retrieval-Augmented Generation (RAG)** with **Model Context Protocol (MCP)** tools.

The application can answer Singapore travel questions using a curated knowledge base and can also retrieve **real-time information** such as Singapore weather and currency conversion.

---

## Features

- Singapore travel information using RAG
- ChromaDB vector database for semantic search
- Knowledge base built from trusted Singapore travel sources
- MCP-based external tools
- Current Singapore weather information
- Currency conversion
- FastAPI backend
- Simple HTML/CSS/JavaScript frontend
- LLM-based response generation
- RAG + MCP combined responses

---

# Architecture

```text
                    ┌─────────────────────┐
                    │     Web Frontend    │
                    │   HTML / CSS / JS   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Router / Agent    │
                    │                     │
                    │  Decide RAG or MCP │
                    └───────┬───────┬─────┘
                            │       │
                ┌───────────┘       └────────────┐
                ▼                                ▼
       ┌─────────────────┐              ┌─────────────────┐
       │      RAG        │              │       MCP       │
       │                 │              │                 │
       │ ChromaDB        │              │ Weather Tool    │
       │ Embeddings      │              │ Currency Tool   │
       │ Retriever       │              │                 │
       └────────┬────────┘              └────────┬────────┘
                │                                │
                └──────────────┬─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │        LLM          │
                    │ Generate Response   │
                    └─────────────────────┘
```

---

# Knowledge Base

The RAG knowledge base contains Singapore travel information from the following sources.

### 1. Wikivoyage Singapore Travel Guide

Provides information about:

- Singapore districts
- Attractions
- Transportation
- Food
- Accommodation
- Practical travel guidance
- General travel information

Source:

https://en.wikivoyage.org/wiki/Singapore

### 2. Visit Singapore — Essential Travel Information

Provides practical information such as:

- Travel requirements
- Getting around Singapore
- General travel tips
- Useful information for visitors

Source:

https://www.visitsingapore.com/travel-tips/essential-travel-information/

### 3. Visit Singapore — Enjoy Singapore in 7 Days

Provides a sample seven-day Singapore itinerary.

Source:

https://www.visitsingapore.com/content/visitsingapore/en/travel-tips/travelling-to-singapore/itineraries/7-days-in-singapore

### 4. Visit Singapore — Singapore Itineraries

Provides Singapore itinerary and attraction planning information.

Source:

https://www.visitsingapore.com/singapore-itineraries/1-day-guide-to-jewel-changi/

---

# Knowledge Base Directory

The downloaded and processed Markdown documents are stored in:

```text
data/singapore/
```

The directory contains files such as:

```text
data/
└── singapore/
    ├── wikivoyage_singapore.md
    ├── visit_singapore_essential.md
    ├── visit_singapore_7_days.md
    └── visit_singapore_itineraries.md
```

---

# Creating the Knowledge Base

The project includes a script that downloads the configured source documents and creates the Markdown knowledge-base files.

Run:

```bash
python scripts/download_sources.py
```

The script:

1. Reads the configured source URLs.
2. Downloads the source content.
3. Processes the HTML content.
4. Extracts the relevant text.
5. Converts the content into Markdown.
6. Adds source information/front matter.
7. Saves the resulting files under:

```text
data/singapore/
```

After downloading the documents, create/update the ChromaDB vector store using:

```bash
python -m app.rag.ingest
```

---

# RAG Workflow

The RAG pipeline follows these steps:

```text
Knowledge Base Documents
        │
        ▼
Document Loading
        │
        ▼
Text Splitting / Chunking
        │
        ▼
Embeddings
        │
        ▼
ChromaDB
        │
        ▼
Semantic Search
        │
        ▼
Relevant Documents
        │
        ▼
Prompt + Context
        │
        ▼
LLM
        │
        ▼
Final Answer
```

When a user asks a question about Singapore travel information, the application retrieves relevant information from the ChromaDB knowledge base and provides that information as context to the LLM.

---

# MCP Tools

The application also uses MCP tools for information that should come from external/current sources rather than the static knowledge base.

The current MCP tools are:

| MCP Tool | Purpose |
|---|---|
| `get_singapore_weather` | Get current Singapore weather information |
| `convert_currency` | Convert one currency into another |

---

## 1. `get_singapore_weather`

The `get_singapore_weather` MCP tool provides current weather information for Singapore.

It should be used for questions where the user needs **current weather information**.

### Example questions

```text
What is the current weather in Singapore?
```

```text
What is the weather in Singapore right now?
```

```text
Is it raining in Singapore currently?
```

```text
What is the current temperature in Singapore?
```

The tool is preferred instead of the RAG knowledge base because weather information changes frequently and should not be answered from static documents.

---

## 2. `convert_currency`

The `convert_currency` MCP tool is used for currency conversion.

It can be used when the user wants to convert an amount from one currency to another.

### Example questions

```text
Convert 50,000 INR to SGD.
```

```text
How much is 1,000 USD in SGD?
```

```text
Convert 500 SGD to INR.
```

```text
How much Singapore dollars will I get for 20,000 INR?
```

This information should be obtained through the MCP tool rather than the static RAG knowledge base because exchange rates change over time.

---

# RAG vs MCP

The application decides whether the user's question should be answered using the knowledge base or an MCP tool.

| User Question | Approach |
|---|---|
| What are the main attractions in Singapore? | RAG |
| What are the best districts to visit? | RAG |
| Give me a 7-day Singapore itinerary. | RAG |
| What are the essential travel tips for Singapore? | RAG |
| Tell me about Jewel Changi Airport. | RAG |
| What is the current weather in Singapore? | MCP |
| Is it raining in Singapore right now? | MCP |
| Convert INR 50,000 to SGD. | MCP |
| How much is USD 1,000 in SGD? | MCP |

### Simple rule

```text
Static / documented Singapore information
                ↓
               RAG

Current / dynamic information
                ↓
               MCP
```

---

# Combining RAG and MCP

The application can also use both RAG and MCP tools for the same question.

For example:

```text
What should I do in Singapore today and what is the current weather?
```

The application can:

```text
User Question
      │
      ├──────────────► RAG
      │                │
      │                └── Singapore attractions
      │
      └──────────────► MCP
                       │
                       └── get_singapore_weather
                                │
                                ▼
                         Current weather
                                │
                                ▼
                       Combined LLM Response
```

Another example:

```text
Suggest a 7-day Singapore trip and tell me how much INR 50,000
is worth in SGD.
```

The application can:

```text
                    User Question
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
             RAG                    MCP
              │                     │
              ▼                     ▼
      7-day itinerary       convert_currency
              │                     │
              └──────────┬──────────┘
                         ▼
                         LLM
                         │
                         ▼
                  Final Response
```

This demonstrates how the application combines **knowledge-based retrieval** with **real-time tools**.

---

# MCP Tool Summary

| Tool | Type | Used For | Example |
|---|---|---|---|
| `get_singapore_weather` | MCP | Current weather | "What is the weather in Singapore now?" |
| `convert_currency` | MCP | Currency conversion | "Convert INR 50,000 to SGD." |

---

# RAG + MCP Decision Strategy

The application follows this general strategy:

```text
                     User Question
                           │
                           ▼
                    Query Analysis/Query Router
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       Static Knowledge             Current Data
             │                           │
             ▼                           ▼
            RAG                          MCP
             │                           │
             │                 ┌─────────┴─────────┐
             │                 │                   │
             │                 ▼                   ▼
             │       get_singapore_weather   convert_currency
             │
             └──────────────┬────────────────────┘
                            ▼
                           LLM
                            │
                            ▼
                     Final Response
```

---

# Updating the Knowledge Base

If the source information changes, run:

```bash
python scripts/download_sources.py
```

Then rebuild/update the vector database:

```bash
python -m app.rag.ingest
```

The workflow is:

```text
Source Websites
      │
      ▼
download_sources.py
      │
      ▼
data/singapore/*.md
      │
      ▼
app.rag.ingest
      │
      ▼
ChromaDB
      │
      ▼
RAG Retriever
```

---

# Project Structure

```text
project-root/
│
├── app/
│   ├── main.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── retriever.py
│   │   └── ...
│   │
│   ├── mcp/
│   │   └── ...
│   │
│   └── ...
│
├── data/
│   └── singapore/
│       ├── wikivoyage_singapore.md
│       ├── visit_singapore_essential.md
│       ├── visit_singapore_7_days.md
│       └── visit_singapore_itineraries.md
│
├── scripts/
│   └── download_sources.py
│
├── chroma_db/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── .env
└── README.md
```

---

# Setup

## 1. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure  variables

Create a config.py file and add the required API configuration.

Example:

```env
gemini_api_key=your_api_key
```

Use the variables required by the current application configuration.

---

# Build the Knowledge Base

Download the Singapore source documents:

```bash
python scripts/download_sources.py
```

Then create the ChromaDB index:

```bash
python -m app.rag.ingest
```

---

# Run the Backend

Start the FastAPI application using the project's configured startup command.

For example:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Run the Frontend

The frontend is a simple:

```text
HTML + CSS + JavaScript
```
```bash
go to : frontend folder, Then run below cmd.
python -m http.server 5500
```
application.

Open the frontend `index.html` in the browser or serve the frontend using a local HTTP server, depending on the project configuration.

The frontend sends user questions to the FastAPI backend and displays the generated response.

---

# Sample Questions

## RAG Questions

```text
What are the main attractions in Singapore?
Response: 
### Knowledge Base Facts

According to the **Singapore — Travel guide at Wikivoyage** (Source: [Wikivoyage](https://en.wikivoyage.org/wiki/Singapore)), notable attractions and highlights include:

* **Cultural & Religious Sites:**
  * **Sri Mariamman Temple:** A colourful Hindu temple located in Chinatown.
  * **Masjid Sultan:** A stately historic mosque located on Arab Street.
  * **Kong Meng San Phor Kark See Monastery:** A vast monastery complex near Ang Mo Kio/Bishan.
  * **Burmese Buddhist Temple:** Located in Balestier.
  * *(Note: Places of worship generally welcome non-followers outside of regular service times).*

* **Sightseeing, Arts & Entertainment:**
  * **Marina Bay & Singapore River:** A central area with clusters of skyscrapers, shopping, and waterfront scenery.
  * **Esplanade – Theatres on the Bay:** A world-class performing arts facility located in Marina Bay and the performance home for groups such as the Singapore Symphony Orchestra.

* **Shopping Districts:**
  * **Orchard Road** and **Bugis**.

* **Nature & Scenic Walks:**
  * **Southern Ridges Walk:** A 9 km trail through the hills and jungles of southern Singapore, featuring the 36-metre-high **Henderson Waves** pedestrian bridge with views overlooking the sea and jungle.

---

### Current Information (MCP)
* No MCP tools were used for this query.

---

### AI Recommendations
*(Please note: The following are suggestions and general travel recommendations, not verified facts from the knowledge base).*

* **Cultural Exploration:** Consider dedicating half a day to explore Chinatown (around Sri Mariamman Temple) and Arab Street (around Masjid Sultan) to experience Singapore's multicultural heritage and dining.
* **Outdoor Timing:** If you plan to walk the Southern Ridges or visit Henderson Waves, consider going in the morning or late afternoon when temperatures are generally milder.
Intent: RAG | MCP: None | Sources: Essential Singapore Travel Information, Singapore — Travel guide at Wikivoyage
```

```text
How can a tourist travel around Singapore?
Response:
### Knowledge Base Facts

According to the **Singapore — Travel guide at Wikivoyage** (Source: [Wikivoyage](https://en.wikivoyage.org/wiki/Singapore)):

* **Modes of Transport Available:** Options for getting around Singapore include train, bus, boat, taxi, rideshare, car, bicycle, and on foot.
* **Walking (On Foot):**
  * Singapore is very pedestrian-friendly, with plentiful and well-maintained pavements and marked pedestrian crossings in the main business district and along major roads. Drivers are generally careful and give way at marked crossings.
  * Jaywalking is illegal and subject to fines of $25 and up to three months in jail (though rarely enforced).
  * Due to the tropical heat, humidity, and common afternoon thunderstorms during monsoon seasons, it is recommended to carry a water bottle, a small towel, and an umbrella. Walking early in the morning, ducking into air-conditioned shops/cafes/museums to cool off, or exploring after sundown are effective ways to manage the climate.

*(Note: The provided knowledge base does not contain detailed operational specifics or route maps for trains, buses, boats, or rideshares beyond listing them as transportation options).*

---

### Current Information (MCP)
* No MCP tools were used for this query.

---

### AI Recommendations
*(Please note: The following are general travel recommendations and suggestions, not verified facts from the knowledge base).*

* **Public Transit (MRT & Buses):** Singapore's Mass Rapid Transit (MRT) subway and public bus networks are typically the most efficient and cost-effective ways to travel across the island. You can generally use contactless credit/debit cards or mobile wallets directly at the gantries.
* **Taxis & Rideshares:** Booking via rideshare apps (such as Grab) or flagging local metered taxis is widely accessible when traveling in groups or late at night.
* **Transit Cards:** If you prefer a physical transit card, tourist passes or stored-value cards are commonly purchased at major MRT stations and convenience stores.
Intent: RAG | MCP: None | Sources: Singapore — Travel guide at Wikivoyage, Essential Singapore Travel Information
```
---

## MCP Questions

### Weather

```text
What is the current weather in Singapore?
Response:
### Knowledge Base Facts
* No knowledge-base context was retrieved for this query.

---

### Current Information (MCP)
* **Tool Used:** `WEATHER_MCP` (Provider: Open-Meteo)

* **Current Conditions (as of 20:00 local time):**
  * **Temperature:** 28.3°C
  * **Feels-like (Apparent) Temperature:** 33.7°C
  * **Relative Humidity:** 77%
  * **Current Precipitation:** 0.0 mm
  * **Wind Speed:** 4.4 km/h

* **Upcoming Daily Forecast:**
  * **9 September:** High 33.1°C / Low 25.7°C | 82% chance of rain (approx. 5.4 mm, rain showers).
  * **10 September:** High 31.2°C / Low 24.0°C | 91% chance of rain (approx. 4.9 mm, rain showers).
  * **11 September:** High 29.4°C / Low 23.6°C | 100% chance of rain (approx. 18.0 mm, thunderstorms).

---

### AI Recommendations
*(Please note: The following are general suggestions based on current conditions, not verified facts).*

* **Rain Preparedness:** With high rain probabilities (82%–100%) and potential thunderstorms in the forecast over the next few days, carry a compact umbrella or lightweight rain jacket when heading out.
* **Hydration & Comfort:** The humidity is high (feels-like temperature reaching ~34°C). Staying well-hydrated and wearing breathable clothing is advised.
* **Indoor Backup Plans:** For days with high precipitation or thunderstorm forecasts (especially September 11), consider planning visits to indoor attractions such as shopping centers along Orchard Road or indoor cultural venues like the Esplanade.
Intent: WEATHER_MCP | MCP: get_singapore_weather (success) | Sources: None
```

```text
Is it raining in Singapore right now?
Response:
### Knowledge Base Facts
* The knowledge base does not contain real-time weather information, and no knowledge-base context was retrieved for this query.

---

### Current Information (MCP)
* **Tool Used:** `WEATHER_MCP` (Provider: Open-Meteo)
* **Current Precipitation:** **0.0 mm** (as of 20:00 local time)
* **Current Status:** It is **not raining right now** in Singapore. 

*(Note: While it is currently dry, the daily forecast indicates an 82% probability of rain/showers for the day).*

---

### AI Recommendations
*(Please note: The following are general suggestions based on the forecast, not verified facts).*

* **Keep Rain Gear Handy:** Even though it is not raining at the moment, showers are frequent and the chance of precipitation remains high, so carrying an umbrella or rain cover when going out is recommended.
Intent: WEATHER_MCP | MCP: get_singapore_weather (success) | Sources: None
```

### Currency

```text
Convert INR 50,000 to SGD.
Response:
### Current Information (MCP)
*Tool used: CURRENCY_MCP (Frankfurter)*

* **Amount Converted:** 50,000 INR
* **Converted Amount:** 667.43 SGD
* **Exchange Rate:** ~0.01335 SGD per 1 INR (Date: 2026-09-08)
Intent: CURRENCY_MCP | MCP: convert_currency (success) | Sources: None
```

```text
Convert USD 1,000 to SGD.
Response:
### Current Information (MCP)
*Tool used: CURRENCY_MCP (Frankfurter)*

* **Amount Converted:** 1,000 USD
* **Converted Amount:** 1,264.09 SGD
* **Exchange Rate:** ~1.26409 SGD per 1 USD (Date: 2026-09-08)
Intent: CURRENCY_MCP | MCP: convert_currency (success) | Sources: None
```
---

## RAG + MCP Questions

```text
What are the best attractions to visit in Singapore today,
and what is the current weather?
```

```text
Create a 7-day Singapore itinerary and convert INR 50,000
to SGD.
Response:
### Current Information (MCP)

* **MCP Tool Used:** `CURRENCY_MCP` (Provider: Frankfurter, Date: 2026-09-10)
  * **Exchange Rate:** 1 INR = 0.01327 SGD
  * **Conversion:** 50,000 INR = **663.50 SGD**
* **Weather Information:** No weather tool results were provided, so current live weather conditions could not be retrieved.

---

### Knowledge Base Facts

* **Currency & Exchange:**
  * The Singapore currency is the Singapore dollar (S$ or SGD), which is divided into 100 cents. 
  * South Asian currencies, including the Indian rupee, can generally be exchanged at very good rates at Mustafa in Little India. Other fiercely competitive money changers are clustered at Change Alley (next to Raffles Place MRT). Major hotels and department stores offer comparatively poor exchange rates.
    * *Source:* Singapore — Travel guide at Wikivoyage  
    * *URL:* https://en.wikivoyage.org/wiki/Singapore
* **Indoor Winter Sports & Attractions:**
  * Singapore hosts a permanent indoor snow center called Snow City, where visitors can experience winter activities and ski/snowboard lessons. 
  * Kallang Ice World at Leisure Park Kallang offers ice skating.
    * *Source:* Singapore — Travel guide at Wikivoyage  
    * *URL:* https://en.wikivoyage.org/wiki/Singapore
* **Itineraries Context:**
  * *Note on Knowledge Base:* The provided knowledge base does not contain enough detailed information to build a complete 7-day sightseeing itinerary (it references a 1-day Jewel Changi guide and section outlines). Therefore, the day-by-day plan below is provided as **AI Recommendations**.
    * *Source:* singapore_itineraries  
    * *URL:* https://www.visitsingapore.com/singapore-itineraries/1-day-guide-to-jewel-changi/

---

### AI Recommendations: 7-Day Singapore Itinerary

*(Please note: The following schedule consists of suggested planning recommendations based on typical travel routes, not verified facts from the knowledge base.)*

#### **Day 1: Arrival & Marina Bay Area**
* **Morning / Afternoon:** Arrive at Changi Airport and explore the indoor attractions at Jewel Changi.
* **Evening:** Head to Marina Bay, stroll along the Marina Bay Sands boardwalk, and view the Spectra light and water show.

#### **Day 2: Heritage Hubs & Little India**
* **Morning:** Explore the vibrant streets of Little India. (You can also exchange money at Mustafa Centre if needed).
* **Afternoon:** Visit Kampong Gelam (Arab Street and Haji Lane) for boutique shopping, street art, and cafes.
* **Evening:** Explore the Bugis street markets and dinner at a nearby hawker center.

#### **Day 3: Culture & Chinatown**
* **Morning:** Visit Chinatown's heritage streets, Buddha Tooth Relic Temple, and Sri Mariamman Temple.
* **Afternoon:** Sample local street food at Maxwell Food Centre or Chinatown Complex.
* **Evening:** Walk along Clarke Quay and the Singapore River.

#### **Day 4: Gardens & Nature**
* **Morning:** Visit the Singapore Botanic Gardens (a UNESCO World Heritage site).
* **Afternoon:** Head over to Gardens by the Bay; visit the cooled conservatories (Flower Dome and Cloud Forest).
* **Evening:** Watch the Garden Rhapsody light show at the Supertree Grove.

#### **Day 5: Sentosa Island Fun**
* **Morning:** Take the cable car or monorail to Sentosa Island.
* **Afternoon:** Visit Universal Studios Singapore or relax along Siloso and Palawan beaches.
* **Evening:** Enjoy dinner by the waterfront at VivoCity.

#### **Day 6: Unique Indoor Escapes & Shopping**
* **Morning / Afternoon:** Beat the tropical heat with indoor activities such as Snow City in Jurong or ice skating at Kallang Ice World.
* **Evening:** Browse the retail malls and flagship stores along Orchard Road.

#### **Day 7: Civic District & Departure**
* **Morning:** Stroll through the Civic District (National Gallery Singapore, Merlion Park).
* **Afternoon:** Pick up souvenirs and head back to Changi Airport for your departure flight.
Intent: RAG + CURRENCY_MCP | MCP: convert_currency (success) | Sources: Essential Singapore Travel Information, Singapore — Travel guide at Wikivoyage, singapore_itineraries
```

```text
What should I do in Singapore today based on the attractions
in the knowledge base and the current weather?
Response:
### Knowledge Base Facts

According to the **Singapore — Travel guide at Wikivoyage** (Source: [Wikivoyage](https://en.wikivoyage.org/wiki/Singapore)):

* **Climate & Walking Advice:** Singapore is very pedestrian-friendly, but tropical heat and humidity can be exhausting, and afternoon thunderstorms are common. Visitors are advised to get an early start, carry an umbrella, water bottle, and small towel, and pop into air-conditioned shops, cafes, and museums or head to shopping malls/pools before noon. Evenings after sundown are comparatively cooler.
* **Available Attractions & Districts:**
  * **Cultural Highlights:** Sri Mariamman Temple (Chinatown), Masjid Sultan (Arab Street).
  * **Sightseeing & Arts:** Marina Bay waterfront, Singapore River, and the Esplanade – Theatres on the Bay.
  * **Shopping Areas:** Orchard Road and Bugis.
  * **Nature/Scenic Trails:** Southern Ridges Walk and Henderson Waves.

---

### Current Information (MCP)

* **Tool Used:** `WEATHER_MCP` (Provider: Open-Meteo)
* **Current Conditions:** 
  * **Temperature:** 28.3°C (Apparent "Feels-like" temperature: 33.7°C)
  * **Humidity:** 77%
  * **Current Precipitation:** 0.0 mm
  * **Daily Forecast:** High of 33.1°C with an **82% probability of rain/showers**.

---

### AI Recommendations (1-Day Itinerary)

*(Please note: The following itinerary is a suggested travel plan based on current weather conditions and knowledge-base attractions, not verified facts).*

Given the high humidity, high apparent temperature (~34°C), and an 82% chance of rain showers (especially in the afternoon), this single-day plan emphasizes outdoor cultural visits in the morning, air-conditioned indoor shelter during peak afternoon heat and rain risk, and evening sightseeing after dark.

---

#### **Day 1: Singapore Highlights & Weather-Adapted Plan**

* **Morning (08:30 – 11:30) | Outdoor Cultural Exploration**
  * **Chinatown & Arab Street:** Start early to take advantage of the cooler morning hours. Visit **Sri Mariamman Temple** in Chinatown and **Masjid Sultan** along Arab Street. 
  * *Tip:* Bring a water bottle and umbrella to stay protected from morning sunshine or sudden light showers.

* **Midday / Afternoon (11:30 – 16:30) | Air-Conditioned Indoor Retreat & Shopping**
  * **Orchard Road or Bugis:** Head indoors during the hottest part of the day and peak thunderstorm window. Explore the air-conditioned shopping centers, grab lunch at local indoor food halls, and stay sheltered from rain.
  * **Esplanade – Theatres on the Bay:** Alternatively, visit the Esplanade in Marina Bay to explore the indoor arts and performance spaces while staying out of the heat.

* **Evening (17:30 onwards) | Marina Bay & Singapore River Walk**
  * **Marina Bay & Singapore River:** As the sun sets and temperatures drop, walk along the Marina Bay waterfront and Singapore River promenade. The skyline and architecture provide great evening views in more comfortable temperatures.
Intent: RAG + WEATHER_MCP | MCP: get_singapore_weather (success) | Sources: Singapore — Travel guide at Wikivoyage, Essential Singapore Travel Information
```
---

# Key Concepts Demonstrated

This project demonstrates:

- Retrieval-Augmented Generation (RAG)
- Vector embeddings
- Semantic search
- ChromaDB
- Knowledge-base ingestion
- Prompt/context construction
- LLM-based question answering
- Model Context Protocol (MCP)
- MCP tool calling
- Tool-based routing
- Combining RAG and MCP
- FastAPI
- Frontend-to-backend integration

---

# End-to-End Flow

```text
                         User
                          │
                          ▼
                  HTML/CSS/JS Frontend
                          │
                          ▼
                     FastAPI API
                          │
                          ▼
                   Query Router
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
            RAG                       MCP
             │                         │
       ChromaDB                  ┌─────┴─────┐
       Retrieval                 │           │
             │                   ▼           ▼
             │          get_singapore_   convert_
             │             weather        currency
             │
             └────────────┬──────────────┘
                          ▼
                         LLM
                          │
                          ▼
                    Final Response
                          │
                          ▼
                      Frontend
```

---

# Important Commands

### Download/update knowledge-base documents

```bash
python scripts/download_sources.py
```

### Create/update ChromaDB

```bash
python -m app.rag.ingest
```

### Start FastAPI

```bash
uvicorn app.main:app --reload
```

### API documentation

```text
http://127.0.0.1:8000/docs
```

### Run Frontend

```bash
Go to: frontend folder, Then run below command
python -m http.server 5500
```

---

# Knowledge Source Configuration

The source configuration used by the download script is:

```python
SOURCES = [
    {
        "filename": "wikivoyage_singapore.md",
        "title": "Singapore — Travel guide at Wikivoyage",
        "source": "Wikivoyage",
        "url": "https://en.wikivoyage.org/wiki/Singapore",
    },
    {
        "filename": "visit_singapore_essential.md",
        "title": "Essential Singapore Travel Information",
        "source": "Visit Singapore",
        "url": "https://www.visitsingapore.com/travel-tips/essential-travel-information/",
    },
    {
        "filename": "visit_singapore_7_days.md",
        "title": "Enjoy Singapore in 7 Days",
        "source": "Visit Singapore",
        "url": "https://www.visitsingapore.com/content/visitsingapore/en/travel-tips/travelling-to-singapore/itineraries/7-days-in-singapore",
    },
    {
        "filename": "visit_singapore_itineraries.md",
        "title": "Singapore Itineraries",
        "source": "Visit Singapore",
        "url": "https://www.visitsingapore.com/singapore-itineraries/1-day-guide-to-jewel-changi/",
    },
]
```

The four configured sources are downloaded and stored as Markdown files under:

```text
data/singapore/
```

---

# Summary

This application combines two different types of AI capabilities:

### RAG

Used for **stable Singapore travel knowledge** stored in the project's knowledge base.

```text
Singapore Travel Documents
        ↓
     ChromaDB
        ↓
    Retriever
        ↓
Relevant Context
        ↓
       LLM
```

### MCP

Used for **dynamic external information**:

```text
Current Singapore Weather
        ↓
get_singapore_weather
```

and:

```text
Currency Conversion
        ↓
convert_currency
```

Together, RAG and MCP allow the Singapore Travel Assistant to provide both **grounded travel information** and **current real-time information**.