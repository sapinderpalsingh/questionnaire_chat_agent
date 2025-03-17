import asyncio
import uuid
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents.azure_ai import AzureAIAgent, AzureAIAgentSettings
from azure.ai.projects.models import  FunctionTool, ToolSet
from models.user_state import UserState
from models.questionnaire import Questionnaire
from plugins.questionnaire_plugin import QuestionnairePlugin



async def main() -> None:
        # Read the JSON file
    file_path = 'questions\\questions_1.json'
    with open(file_path, 'r') as file:
        json_data = file.read()

    # Create a Questionnaire instance from the JSON data
    questionnaire = Questionnaire.from_json(json_data)
    print("Questionnaire loaded successfully!")

    user_id = str(uuid.uuid4())
    user_state = UserState(user_id=user_id, questions=questionnaire.questions)

    
    ai_agent_settings = AzureAIAgentSettings.create()

    async with (
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(credential=creds) as client,
    ):
        # 1. Create an agent on the Azure AI agent service
        agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
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
            """        
        )

        # 2. Create a Semantic Kernel agent for the Azure AI agent
        agent = AzureAIAgent(
            client=client,
            definition=agent_definition,
            # Optionally configure polling options
            # polling_options=RunPollingOptions(run_polling_interval=timedelta(seconds=1)),
        )
        agent.kernel.add_plugin(
            QuestionnairePlugin(user_state=user_state),
            plugin_name ="QuestionnairePlugin",
        )
        # 3. Create a new thread on the Azure AI agent service
        thread = await client.agents.create_thread()

        try:
            # Start the conversation
            while not user_state.is_completed:
                response = await agent.get_response(thread_id=thread.id)
                print(f"# {response.name}: {response.content}")
                await agent.add_chat_message(thread_id=thread.id, message=response.content)
            
                if user_state.is_completed:
                    await agent.add_chat_message(thread_id=thread.id, message="Thank you! All questions have been answered.")
                    user_state.save_state()
                else:        
                    user_response = input("Your answer: ")
                    await agent.add_chat_message(thread_id=thread.id, message=user_response)
  
        finally:
            # 6. Cleanup: Delete the thread and agent
            await client.agents.delete_thread(thread.id)
            await client.agents.delete_agent(agent.id)


if __name__ == "__main__":
    asyncio.run(main())