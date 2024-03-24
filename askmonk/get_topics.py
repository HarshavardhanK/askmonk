from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def gen_prompt(user_query, topics, from_graph):
    prompt = f"""
        You are a knowledge bot that provides topics related to the given prompt. Your task is to assess the user prompt and reply with a list of topics
        that is required to perform the task {"from the given list of topics" if from_graph else ""}. Prompt {"and comma seprated topic list" if from_graph else ""} is provided after <<<>>> .
        
        You will only respond with the list separated by comma, starting narrow, then going broad upto 5 topics. Do not include the word "Response". Do not provide explanations or notes. 
        {"Make sure pick only from the given list of topics, do not include new topics" if from_graph else ""}
        ####
        Here are some examples:
        
        Prompt: How do I write a function for calculating maximum flow in a flow network graph?
        {"Topics: Chaos Theory,Game Theory,Combinatorics,Stochastic Processes,Ford-Fulkerson method,Topology,Non-Euclidean Geometry,Number Theory,Breadth-First Search,Fractals,Directed Graphs,Graph Theory,Calculus of Variations" if from_graph else ""}
        Response: Ford-Fulkerson method,Breadth-First Search,Directed Graphs,Graph Theory
        Prompt: How to write fast fourier transform?
        {"Topics: Linear Algebra,Chaos Theory,Complex Numbers,Game Theory,Combinatorics,Cooley-Tukey Algorithm,Stochastic Processes,Ford-Fulkerson method,Topology,Non-Euclidean Geometry,Number Theory,Signal Processing,Breadth-First Search,Fractals,Directed Graphs,Graph Theory,Calculus" if from_graph else ""}
        Response: Cooley-Tukey Algorithm,Complex Numbers,Signal Processing,Linear Algebra,Calculus
        ###
    
        <<<
        Prompt: {user_query}
        {f"Topics:{topics}" if from_graph else ""}
        >>>
        """
    return prompt


def get_topics(user_query, api_key, model="mistral-large"):
    client = MistralClient(api_key=api_key)
    prompt = gen_prompt(user_query, topics=None, from_graph=False)
    # print(prompt)
    messages = [ChatMessage(role="user", content=prompt)]
    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content.split(",")
