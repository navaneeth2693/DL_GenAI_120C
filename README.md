\# AI Escape Room — The Locked Library



A Python escape-room application built with Streamlit and Google Gemini.

Players investigate a library, discover clues, collect a key, and solve

puzzles to unlock the exit.



\## Technologies



\- Python 3.11

\- Streamlit

\- Google Gen AI Python SDK

\- python-dotenv

\- Git and GitHub



The application uses the `gemini-3.5-flash-lite` model.

API access depends on the model's availability and your project's quota.

Use a free-tier project with billing disabled for this assignment.



\## Game environment



The room contains five interactive objects:



\- Desk

\- Bookshelf

\- Locked drawer

\- Painting

\- Exit door



Players examine objects, interpret clues, open the drawer, collect a key,

unlock the painting, and solve the final exit challenge.



\## Version 1



Run `app\_v1.py`.



Gemini receives the room rules and conversation history. It determines

the outcome of player actions and returns an escape-completion flag.



Observed limitations:

\- It allowed a key to be used before collection.

\- It accepted a false claim that prerequisite puzzles were completed.



The Git tag `v1.0` preserves the original working baseline.

`app.py` also contains the Version 1 application.



\## Version 2



Run `app\_v2.py`.



Python maintains structured game state and validates actions.

Inventory, puzzle progress, and victory are controlled by Python.



Gemini selects from approved narration options containing the validated

outcome. Raw model text is not displayed. If the API fails or returns an

invalid selection, the application uses the original local response.



This improves consistency but limits narrative creativity.

The action handler supports a bounded set of English commands,

rather than unrestricted natural-language understanding.



\## Install and run — Windows PowerShell



Install Python 3.11 and Git, then clone this repository using its GitHub URL.

Open PowerShell in the downloaded project folder.



Create the environment and install dependencies:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



Create your private configuration file:



```powershell

Copy-Item .env.example .env

notepad .env

```



Replace the placeholder with your Gemini API key.

Get a key from https://aistudio.google.com/apikey.

Never commit or share your actual key.



Start Version 1:



```powershell

.\\.venv\\Scripts\\python.exe -m streamlit run app\_v1.py

```



Or start Version 2:



```powershell

.\\.venv\\Scripts\\python.exe -m streamlit run app\_v2.py

```



Open the local URL printed by Streamlit, normally http://localhost:8501.

Press Ctrl+C in PowerShell to stop the application.



\## How to play



Start with:



```text

examine the desk

inspect the bookshelf

```



Other supported Version 2 actions include:



```text

open the drawer with code 1234

collect the brass key

use the brass key on the painting

unlock the door with code 1234

check my inventory

```



1234 is an example, not a solution.

Enter one action at a time and use the clues to discover the real codes.

Click Restart game to clear the current session.



\## Run automated checks



```powershell

.\\.venv\\Scripts\\python.exe test\_game\_logic.py

.\\.venv\\Scripts\\python.exe test\_actions.py

.\\.venv\\Scripts\\python.exe test\_narrator.py

```



These checks run locally without making Gemini requests.

The narrator tests simulate provider failure and invalid model output.



\## Testing and evidence



See `TEST\_RESULTS.md` for:

\- Observed Version 1 live-model behavior

\- Version 2 rule-validation results

\- Simulated narrator failures

\- Walkthrough results and limitations of the evidence



Screenshots are stored in `screenshots/`.



\## Main files



| File | Purpose |

|---|---|

| app\_v1.py | Version 1 interface and LLM-controlled gameplay |

| app\_v2.py | Version 2 interface |

| game\_logic.py | Authoritative state and puzzle rules |

| action\_handler.py | Player-command recognition and routing |

| narrator.py | Constrained Gemini narration and fallback |

| TEST\_RESULTS.md | Test evidence and comparison |

| requirements.txt | Python dependencies |

| .env.example | Configuration template without credentials |



\## Limitations



\- Game progress is stored in the Streamlit session, not a database.

\- Version 2 recognizes only documented commands and supported synonyms.

\- Narration is constrained to approved alternatives.

\- API requests can fail or reach quota limits.

\- Puzzle solutions are visible in the source code.

\- Version 1's passing tests do not guarantee future model consistency.



\## AI assistance



This project was developed with assistance from an AI coding assistant.

The implementation was built and tested incrementally.

The submitted code, design decisions, and limitations should be understood

and explained by the student.



\## Architecture



See \[ARCHITECTURE.md](ARCHITECTURE.md) for diagrams and explanations

of both versions.

