\# System Architecture



\## Version 1 — LLM-controlled gameplay



```mermaid

flowchart TD

&#x20;   Player\[Player] --> UI\[Streamlit interface]

&#x20;   UI --> History\[Session conversation history]

&#x20;   History --> Gemini\[Gemini Game Master]

&#x20;   Rules\[System prompt: room rules and solutions] --> Gemini

&#x20;   Gemini --> JSON\[Validate response JSON structure]

&#x20;   JSON --> Message\[Display game message]

&#x20;   JSON --> Victory\[Use model-provided escaped flag]

&#x20;   Message --> UI

&#x20;   Victory --> UI

```



\### How it works



1\. The player enters a natural-language action.

2\. Python sends the conversation and game instructions to Gemini.

3\. Gemini returns a message and an escaped flag.

4\. Python checks the response format and updates the interface.



\### Limitation



Checking JSON structure does not prove that an action is valid.

The model may invent inventory or accept false progress claims.

Version 1 testing demonstrated both problems.



\## Version 2 — Python-controlled gameplay



```mermaid

flowchart TD

&#x20;   Player\[Player] --> UI\[Streamlit interface]

&#x20;   UI --> Handler\[Python action handler]

&#x20;   Handler --> Engine\[Python game rules]

&#x20;   Engine <--> State\[Structured session state]

&#x20;   Engine --> Outcome\[Validated outcome]

&#x20;   Outcome --> Options\[Approved narration choices]

&#x20;   Options --> Gemini\[Gemini selects an option index]

&#x20;   Gemini --> Check\[Validate index type and range]

&#x20;   Check -->|Valid| Text\[Select approved text]

&#x20;   Check -->|Invalid| Fallback\[Use original outcome]

&#x20;   Gemini -->|API failure| Fallback

&#x20;   Text --> UI

&#x20;   Fallback --> UI

&#x20;   State --> Status\[Inventory and escape-status display]

&#x20;   Status --> UI

```



\### How it works



1\. The action handler recognizes a supported player command.

2\. Python checks inventory, codes, and puzzle prerequisites.

3\. Only the game rules can update the structured state.

4\. The validated outcome is used to construct narration choices.

5\. Gemini selects an option; Python validates the selection.

6\. If narration fails, the original outcome is displayed.

7\. The escape banner depends on Python state, not model output.



\### State tracked



\- Available objects

\- Examined objects

\- Inventory

\- Solved puzzles

\- Drawer status

\- Painting status

\- Escape status



\### Trust boundary



The narrator receives approved outcome descriptions.

It receives no state-changing tools, raw player commands, or full

collection of hidden puzzle solutions.



The model cannot add inventory, complete puzzles, or declare victory.

Arbitrary model text is not displayed.



\### Tradeoffs



\- Supported English commands are limited by the action handler.

\- Approved narration offers less variety than unrestricted generation.

\- State is session-based and is not saved to a database.

\- Local fallback preserves gameplay during API failures.



\## Credentials



Both versions load the Gemini API key from the private `.env` file.

The `.env.example` file contains only a placeholder.

The real `.env` file is excluded from Git.

