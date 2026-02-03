from langchain.agents import initialize_agent, AgentType

def runRecommendationEngineInAgentMode():
    tools = [get_weather_data_tool, get_itemization_data_tool]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=2,
        agent_kwargs={
            "system_message": (
                "You are a smart energy assistant. "
                "You analyze weather data and itemized energy usage, "
                "and then provide recommendations to help reduce energy consumption. "
                "start : 2025-05-01 and end : 2025-07-01 for itemization, and user's zip code is 11691"
                "Use the tools to fetch data if needed."
                "Always respond ONLY in the following JSON format:\n\n"
                "{\n"
                '  "title": "short recommendation title",\n'
                '  "body": "1-2 line summary of the recommendation",\n'
                '  "image_description": "a short description of the image that can be used for the recommendation", \n'
                '  "description": "Detailed explanation (not more than 200 words)."\n'
                "}\n\n"
                "Here is an example:\n\n"
                "{\n"
                '  "title": "Use Ceiling Fans During Mild Weather",\n'
                '  "body": "Ceiling fans consume far less electricity than air conditioners.",\n'
                '  "image_description": "a short description of the image that can be used for the recommendation", \n'
                '  "description": "During moderate weather (around 22°C), ceiling fans can effectively circulate air and maintain comfort at a much lower energy cost than ACs. '
                'This helps reduce energy bills and environmental impact. ACs should be reserved for hotter conditions."'
                "\n}\n\n"
                "Do not include anything else — not even greetings or extra text — only output JSON."
            )
        }
    )

    response = agent.run(
        "User lives in ZIP code 11691. Itemization period is from 2025-05-01 to 2025-07-01. "
        "Recommend how to improve energy consumption efficiently using available tools."
        "Only return a JSON object. Do not explain or add any other text."
    )

    print(response)