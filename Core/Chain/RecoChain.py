from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable
from langchain_community.chat_models import ChatOllama
import requests
import json

def runRecommendationEngineInChainMode():
    # Get current weather
    weather_info = get_weather_data("11691")
    itemization_info = get_itemization_data("2025-05-01", "2025-07-01")

    """
    When building a prompt, keep all the static text that is going to be repeatedly
    used in the beginning of the prompt, and include the dynamic content such as
    weather_info and itemization_info in our example at the end.
    This is useful for prompt caching. Prompt caching is used on OpenAI new models (not sure about other LLMs)
    Currently getting json parser error with llama if variables are included at end
    """
    # Prompt
    prompt = ChatPromptTemplate.from_template("""
    You are a smart energy assistant.
    Here is the hourly weather data of previous bill cycle and current bill cycle: {weather_info}
    Here is the monthly itemization data of previous bill cycle and current bill cycle: {itemization_info}
    Analyse weather data and itemization data, based on this, give recommendation to the user about what can be done to reduce consumption.
    Anything to check for in the appliances?
    Your response must be a JSON object with the following fields:
    - "title": a short title for the recommendation
    - "image_description": a short description of the image that can be used for the recommendation
    - "body": 1-2 line summary
    - "description": detailed explanation (max 200 words)
    Do not return anything except the JSON. Do not include phrases like "Based on the provided data" etc
    """)
    # Parser
    parser = JsonOutputParser()
    # Chain
    chain: Runnable = prompt | llm | parser

    print("\n🚀 Generating Response from LLM ..\n")

    # Run
    response = chain.invoke({
        "weather_info": weather_info,
        "itemization_info": itemization_info
    })

    #print(response)

    if response:
        print("💡 Sucessfully Fetched Recommendation\n")
    else:
        print("⚠️ Failed To Fetch Recommendation\n")

    return json.dumps(response, indent=2)