# AI Email & Message Assistant

A full-stack Generative AI mini project for Bano Qabil (BQ-024). It turns rough text into clearer messages using Flask, JavaScript Fetch API, and the Groq API.

## Features

- Four message categories: Professional Email, Student Message, Leave Application, and Formal Request.
- Three writing tones: Professional, Polite, and Friendly.
- Real Groq API generation (not hardcoded sample output).
- Frontend and backend validation.
- Loading state, friendly errors, and fresh AI generation on Regenerate.
- Copy, download as `.txt`, and clear controls.
- Responsive interface for desktop and mobile.
- API key stays on the server in `.env`.

## Project structure

```text
AI_Email_Message_Assistant/
├── app.py
├── groq_service.py
├── prompts.py
├── requirements.txt
├── .env                 # create this yourself; never upload it
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Windows setup

1. Install Python 3.10 or newer.
2. Extract the ZIP and open the `AI_Email_Message_Assistant` folder in VS Code.
3. Open the VS Code terminal in that folder.
4. Create a virtual environment:

   ```powershell
   py -m venv venv
   ```

5. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run:

   ```bat
   venv\Scripts\activate.bat
   ```

6. Install packages:

   ```powershell
   py -m pip install -r requirements.txt
   ```

7. Copy `.env.example` and name the copy `.env`. In PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

8. Open `.env` and replace `replace_with_your_key` with your own Groq API key:

   ```env
   GROQ_API_KEY=your_actual_key_here
   GROQ_MODEL=openai/gpt-oss-20b
   ```

   Create/manage your key in the official Groq console: https://console.groq.com/keys

9. Run the app:

   ```powershell
   py app.py
   ```

10. Open http://127.0.0.1:5000 in your browser.

Keep the terminal window running while using the website. You do not need to type messages or view generated results in the terminal.

## Model configuration

The default model is `openai/gpt-oss-20b`, listed in Groq's current production model documentation when this project was prepared. If it is not available to your account in the future, change `GROQ_MODEL` in `.env` to another active chat model listed at https://console.groq.com/docs/models.

## GitHub safety

- Do **not** upload `.env`.
- Do upload `.env.example`, source files, `requirements.txt`, and this README.
- Before committing, check that `.env` is ignored:

  ```powershell
  git status --ignored
  ```

## How the application works

1. The browser collects the message, category, and tone.
2. JavaScript sends JSON to `POST /generate` using Fetch API.
3. Flask validates the values and calls `build_prompt()` in `prompts.py`.
4. `groq_service.py` sends the prompt to Groq using the private key loaded from `.env`.
5. Flask returns JSON containing `success` and `generated_message`.
6. JavaScript updates the output card without reloading the page.

## Python concepts demonstrated

- **Variables and data types:** request data, strings, lists, and dictionaries.
- **Input/output:** JSON received from the browser and JSON returned to it.
- **Conditionals:** input checks and error handling.
- **Lists:** supported message categories and tones.
- **Dictionaries:** category-specific prompt instructions.
- **Functions:** `build_prompt()` and `generate_with_groq()`.
- **Modules:** Flask routes, prompt logic, and API service are separated into files.
- **String operations:** trimming, checking, and formatting text.
- **API integration:** Groq chat completion request.

A `while` loop is not necessary for this event-driven web application; adding an artificial menu loop would not improve the design. The browser handles repeated user actions, and Regenerate makes a new backend/API request.

## Troubleshooting

- **API key is missing:** confirm the file is named exactly `.env` (not `.env.txt`) and contains `GROQ_API_KEY=...`. Restart `py app.py` after changing it.
- **API key rejected:** verify the key in your Groq console; never paste it into chat or GitHub.
- **Unable to connect:** check your internet connection.
- **Model unavailable:** set `GROQ_MODEL` to an active model from Groq's model list.
- **Module not found:** activate `venv` and run `py -m pip install -r requirements.txt` again.

## Important

This project sends the text you submit to Groq to generate the response. Do not submit passwords, private account information, or other sensitive information.
