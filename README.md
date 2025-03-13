# Semantic Kernel Chat Agent with Templated Questionnaire

## Overview

This sample demonstrates how to create a semantic kernel chat agent that interacts with users to complete a questionnaire. The agent fetches questions from the `UserState` and updates answers based on user input until all questions are answered.

## Key Components

### Models

- **Question**: Represents a question with its options and answer.
- **Option**: Represents an option for a question, including the label and the ID of the next question.
- **UserState**: Manages the state of the questionnaire for a user, including the list of questions, the current question, and whether the questionnaire is completed.
- **Questionnaire**: Loads questions from a JSON file and provides methods to convert the questionnaire to and from JSON.

### Plugins

- **QuestionnairePlugin**: Interacts with the `UserState` to fetch the next question and update answers based on user input. It uses semantic kernel functions to integrate with the chat agent.

### Main Script

- **sk_agent.py**: The main script that sets up the semantic kernel chat agent, reads the questionnaire from a JSON file, initializes the `UserState`, and starts the conversation with the user. The agent continues to ask questions and update answers until all questions are answered.

## How It Works

1. **Loading the Questionnaire**:
   - The JSON file containing the questions is read and parsed to create a `Questionnaire` instance.
   - The `Questionnaire` instance is used to initialize the `UserState` with a unique user ID and the list of questions.

2. **Setting Up the Semantic Kernel**:
   - An instance of the `Kernel` is created to register the `QuestionnairePlugin` and the chat completion service.
   - The function choice behavior is configured to automatically invoke kernel functions.

3. **Creating the Chat Agent**:
   - A `ChatCompletionAgent` is created with the kernel, a name, and detailed instructions on how to handle the questionnaire.
   - The agent is configured to use the `QuestionnairePlugin` to fetch questions and update answers.

4. **Starting the Conversation**:
   - A `ChatHistory` instance is created to hold the conversation.
   - The agent starts the conversation by fetching the first question from the `UserState` and presenting it to the user.
   - The user provides answers, which are updated in the `UserState` using the `QuestionnairePlugin`.
   - The agent continues to fetch and present questions until all questions are answered.

5. **Completing the Questionnaire**:
   - Once all questions are answered, the agent informs the user that the questionnaire is completed and saves the `UserState` to a JSON file.

## Instructions for Use

1. **Prepare the JSON File**:
   - Ensure that the JSON file containing the questions is available in the specified path and format.

2. **Run the Script**:

   1. Clone the repo
   1. Create virtual env and install dependencies

   ```
   uv venv --python=3.12
   source .venv/bin/activate
   uv sync
   uv run sk_agent.py
   ```
   - Execute the sk_agent.py script to start the semantic kernel chat agent.

3. **Interact with the Agent**:
   - Follow the prompts from the agent to answer the questions.
   - The agent will guide you through the questionnaire until all questions are answered.

4. **Completion**:
   - Once the questionnaire is completed, the agent will inform you and save the responses to a JSON file.

## Conclusion

This sample demonstrates how to create an interactive chat agent using semantic kernel functions to manage a questionnaire. The agent fetches questions, updates answers, and ensures a smooth conversation flow until the questionnaire is completed.

Samples questions json file has few questions with options and each option can decide what could be the next question, LLM drives pulling the next question and saving the response against that question. Use response could be the option number or exact option text or a free text sentence where LLM will try to map it to one of the options, if it fails to map then user will be asked to provide option again.