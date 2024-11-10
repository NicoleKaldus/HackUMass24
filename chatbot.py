from dotenv import load_dotenv
import os
import json
import get_by_keywords

load_dotenv()

# Load the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

# tools = []
MAX_FUNCTION_CALL_ATTEMPTS = 5


# with open("chatbot_tools.json") as f:
#     # t is a json containing an array of tools
#     # each tool is a json object with a function
#     t = json.load(f)
#     tools = t["tools"]1

# print(tools)

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )
#
# print(completion.choices[0].message)


def construct_message_object(role, content):
    """
    Construct a message object for the OpenAI API

    Args:
        role (str): The role of the message
        content (str): The content of the message

    Returns:
        A message object for the OpenAI API of the form {"role": role, "content": content}
    """
    if role not in ["system", "user", "assistant"]:
        raise ValueError("The role must be either 'system', 'user', or 'assistant'")
    if isinstance(content, str) is False:
        raise ValueError("The content must be a string")
    return {"role": role, "content": content}


def construct_chat_object(system_message, user_message, chat_history=None):
    """
    Construct a chat object for the OpenAI API

    Args:
        system_message (str): The system message. Required if chat_history is None, unused otherwise
        user_message (str): The user message
        chat_history (list): The chat history. Must be a list of message objects

    Returns:
        A chat object for the OpenAI API of the form [{"role": role, "content": content}, ...]
    """
    messages = []
    print("OAEFHAEIUFHOAEIUFheioaufh")
    print(system_message, user_message, chat_history, sep="\n")

    if isinstance(user_message, str) is False:
        raise ValueError("The user message must be a string")
    if chat_history is not None:  # we have a chat history
        for message in chat_history:
            if "role" not in message.keys() or "content" not in message.keys():
                raise ValueError(
                    "The message object must have a 'role' and 'content' key"
                )
            messages.append(message)
        messages.append(construct_message_object("user", user_message))
        return messages

    # We don't have a chat history
    if isinstance(system_message, str) is False:
        raise ValueError("The system message must be a string")

    messages.append(construct_message_object("system", system_message))
    messages.append(construct_message_object("user", user_message))
    return messages


def construct_tool_response_chat_object(tool_call_id, response, chat_history):
    """
    Construct a message object for the OpenAI API for a tool response

    Args:
        tool_call_id (str): The tool call ID
        response (object): The response to the tool call
            response is expected to be an object {"<response>": <response>, ...}
            ex. {location: "New York, NY", temperature: "72°F"}
        chat_history (list): The chat history. Must be a list of message objects

    Returns:
        A list of message objects for the OpenAI API of the form [{"role": role, "content": content}, ...]

    """
    print("\n\n\n\n", response, "\n\n\n")
    exit()
    tool_response_object = {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": json.dumps(response),
    }

    messages = chat_history
    messages.append(tool_response_object)

    return messages


def attempt_tool_calls(completion, max_attempts, chat_history):
    """
    Attempt to call a tool function in the chatbot

    Args:
        completion (object): The completion object from the OpenAI API
        max_attempts (int): The maximum number of function call attempts
        chat_history (list): The chat history. Must be a list of message objects

    Returns:
        completion (object): The new completion object from the OpenAI API
        chat_history (list): The updated chat history
    """

    attempts = 0
    # Chat asks for a function call
    while (
        completion.choices[0].finish_reason == "tool_calls"
        and attempts < max_attempts
        and completion.choices[0].message.tool_calls is not None
    ):
        # print("completion", completion.choices[0].message)
        tool_call = completion.choices[0].message.tool_calls[0]  # get the tool call
        function_name = tool_call.function.name  # get the name of the function to call
        parameters = (
            tool_call.function.arguments
        )  # get the parameters to pass to the function
        result = handle_function_calls(function_name, parameters)  # call the function
        chat_history.append(
            completion.choices[0].message
        )  # append the tool call to the chat history

        new_message_list = construct_tool_response_chat_object(
            tool_call.id, result, chat_history
        )  # construct the message object for the tool response
        # print("new_message_list", new_message_list)
        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=new_message_list
        )
        attempts += 1

    return completion, chat_history


def start_chat(system_message, user_message, tools=None):
    """
    Start a chat with the OpenAI API

    Args:
        system_message (str): The system message
        user_message (str): The user message

    Returns:
        A message object generated by the OpenAI API of the form {"role": role, "content": content}
        The chat history so far
        Both are stored in a tuple (message, chat_history)
    """
    toReturn = None
    chat_object = construct_chat_object(system_message, user_message)
    completion = None
    if tools is not None:
        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=chat_object, tools=tools
        )
    else:
        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=chat_object
        )
    # Check for tool calls
    completion, chat_history = attempt_tool_calls(
        completion, MAX_FUNCTION_CALL_ATTEMPTS, chat_object
    )
    chat_history.append(completion.choices[0].message)
    toReturn = (completion.choices[0].message, chat_history)

    return toReturn


def continue_chat(user_message, chat_history, tools=None, add_user_msg=True):
    """
    Continue a chat with the OpenAI API

    Args:
        user_message (str): The user message
        chat_history (list): The chat history. Must be a list of message objects

    Returns:
        A message object of the form {"role": role, "content": content}
        the chat history so far
        Both are stored in a tuple (message, chat_history)
    """
    toReturn = None
    chat_object = construct_chat_object(None, user_message, chat_history)
    completion = None
    if tools is not None:
        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=chat_object, tools=tools
        )
    else:
        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=chat_object
        )

    if add_user_msg:
        chat_history.append(construct_message_object("user", user_message))

    completion, chat_history = attempt_tool_calls(
        completion, MAX_FUNCTION_CALL_ATTEMPTS, chat_history
    )
    chat_history.append(completion.choices[0].message)
    toReturn = (completion.choices[0].message, chat_history)
    return toReturn


def handle_function_calls(function_name, parameters):
    """
    Handle function calls in the chatbot

    Args:
        function_name (str): The name of the function to call
        parameters (object): The parameters to pass to the function
            { "parameter_name": parameter_value, ... }

    Returns:
        An object containing the result of the function call. Try to make the response as readable as possible
        { "response": response, ... }
        Ex. { "location": "New York, NY", "temperature": "72°F" }
    """
    match function_name:
        case "example_function":
            return {"function_result": example_function()}
        # Add more cases here for other functions
        case "ask_goose_by_keywords":
            return get_by_keywords.ask_goose_by_keywords(parameters)
        case "ask_sam_by_keywords":
            return get_by_keywords.ask_sam_by_keywords(parameters)
        case _:
            raise ValueError(f"Function {function_name} not recognized")
    return None


def example_function():
    return "Hello, World!"
