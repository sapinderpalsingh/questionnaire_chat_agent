import uuid
import asyncio
from models.questionnaire import Questionnaire
from models.question import Question
from models.user_state import UserState
from plugins.questionnaire_plugin import QuestionnairePlugin

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments

async def main():
    print("Hello from cba-questionnaire-agent!")

    # Read the JSON file
    file_path = 'questions\\questions_1.json'
    with open(file_path, 'r') as file:
        json_data = file.read()

    # Create a Questionnaire instance from the JSON data
    questionnaire = Questionnaire.from_json(json_data)
    print("Questionnaire loaded successfully!")

    user_id = str(uuid.uuid4())
    user_state = UserState(user_id=user_id, questions=questionnaire.questions)

    # Create the instance of the Kernel to register the plugin and service
    service_id = "service_id"
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion(service_id=service_id))

    # Configure the function choice behavior to auto invoke kernel functions
    settings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create the agent
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="questionnaire_agent",
        instructions=""""
        You are an expert questionnaire agent whose primary task is to ask users questions and record their responses accurately. You must follow these strict guidelines:
 
        Question Handling
        Retrieve Questions Only from the Plugin:
        
        You will strictly use the QuestionnairePlugin to fetch questions.
        You must not ask any questions that are not provided by the plugin.
        Presenting Questions and Options:
        
        You must ask each question along with its available options.
        The answer options must be presented in a numbered list format (1, 2, 3, 4).
        The user can select their answer by choosing either the option number or the exact option text.
        Intent Mapping & Answer Validation:
        
        If the user provides a free-text answer, you must map their intent to the closest available option.
        If their intent does not match any of the four options, politely ask them to choose from the given options to ensure accuracy.
        Conversation Flow:
        
        Always ask the full question with all available options.
        Continue asking questions until no further questions are available from the plugin.
        Once all questions are answered, confirm that responses have been recorded and terminate the conversation by informing the user that they will be contacted for further assistance.
        """,
        plugins=[QuestionnairePlugin(user_state)],
        arguments=KernelArguments(settings=settings),
    )

    # Create a chat history to hold the conversation
    chat_history = ChatHistory()
    
    # Start the conversation
    while not user_state.is_completed:
        response = await agent.get_response(chat_history)
        print(f"# {response.name}: {response.content}")
        chat_history.add_assistant_message(response.content)
       
        if user_state.is_completed:
            chat_history.add_assistant_message("Thank you! All questions have been answered.")
            user_state.save_state()
        else:        
            user_response = input("Your answer: ")
            chat_history.add_user_message(user_response)

if __name__ == "__main__":
    asyncio.run(main())