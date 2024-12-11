# How the Web Application Works

## Overview
This document describes the working of the application, outlining its components, workflows, and processes. The application uses Flask as the backend framework and integrates custom Named Entity Recognition (NER), Roxie API, and Groq's LLM API for processing legal documents and user inputs.

## Application Workflow
The application consists of two main workflows:
1. **Entity Extraction and Case Statement Retrieval**
2. **User Prompt Submission with AI Response Generation**

## 1. Entity Extraction and Case Statement Retrieval
### Step 1: User Input (Frontend)
- The user provides a **sample case** in the input box on the frontend (left section of the page).
- On clicking the **"Extract"** button, the text is sent to the backend for processing via the `/extract` endpoint.

### Step 2: Named Entity Recognition (NER)
- The `/extract` endpoint triggers the NER process using `legal_ner_script.py`.
- **Process Details**:
   - The input text is processed using a custom NER model (`en_legal_ner_trf`), which identifies legal entities.
   - Entity types include:
      - `PROVISION`
      - `STATUTE`
      - `CASE_NAME`
      - `DATE`
   - Entities of type `PROVISION` and `STATUTE` are combined into a single label, `PROVISION_STATUTE`.
   - The extracted entities are returned as a string.

### Step 3: Query Roxie API
- The extracted entities are sent to the **HPCC Systems' Roxie API** using `send_to_roxie.py`.
- **Process Details**:
   - The API query is based on the NER-extracted entity information.
   - The Roxie API responds with relevant legal case statements, by doing efficient searching and ranking of the case statements from the data corpus. The **Searching** process is discussed in the **Searching Techinques used in HPCC** folder.
   - The statements are formatted and include line numbers for reference.

### Step 4: Frontend Update
- The server sends the extracted entities and the Roxie case statements back to the frontend.
- The frontend dynamically updates:
   - **Entity Tags**: Displayed as tags below the input box.
   - **Case Statements**: Displayed in a list with a "Show More" option for long statements.

## 2. User Prompt Submission with AI Response Generation
### Step 1: User Prompt (Frontend)
- The user enters a **prompt** (question or query) in the input box on the right section of the page.
- On clicking the **"Submit"** button, the prompt is sent to the backend via the `/submit` endpoint.

### Step 2: Retrieve Case Statements (Session)
- The `/submit` endpoint retrieves the previously extracted **case statements** from the session.

### Step 3: Query Groq's LLM API
- The extracted case statements and the user prompt are sent to **Groq's LLM API** using `send_to_groq.py`.
- **Process Details**:
   - The input includes both the **case statements** and the **user's prompt**.
   - Groq's API processes this input and generates a relevant response.
   - The response is returned to the backend.

### Step 4: Frontend Update
- The server sends the Groq API response back to the frontend.
- The frontend dynamically updates the response in a **textarea** on the right section of the page.

## **Key Components**
### **Backend**
1. **Flask Application** (`app.py`):
   - Handles the following endpoints:
      - `/` → Serves the frontend HTML page.
      - `/extract` → Processes entity extraction and queries Roxie API.
      - `/submit` → Sends the user prompt and case statements to Groq API.
   - Uses session to store case statements temporarily.
2. **NER Script** (`legal_ner_script.py`):
   - Performs named entity extraction using the `en_legal_ner_trf` spaCy model.
   - Combines and formats specific entity types.
3. **Roxie API Integration** (`send_to_roxie.py`):
   - Queries Roxie API to fetch related case statements.
4. **Groq LLM API Integration** (`send_to_groq.py`):
   - Sends user prompts and case statements to Groq's LLM API for response generation.

### **Frontend**
1. **HTML** (`index.html`):
   - Two sections for input and response:
      - Left → Sample case input and extracted entities.
      - Right → User prompt input and AI response display.
2. **CSS** (`style.css`):
   - Provides clean and responsive styling.
3. **JavaScript** (`script.js`):
   - Handles button clicks, AJAX requests to backend endpoints, and dynamic content updates.


## **Conclusion**
This application provides an interactive interface for extracting legal entities, retrieving related case statements, and generating responses using Groq's AI API. The modular design ensures easy maintenance and scalability for future enhancements.

