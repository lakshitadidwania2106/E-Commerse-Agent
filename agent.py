from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable


MAX_ITERATIONS = 10
MODEL = "qwen3:1.7b"

#--------TOOL---------

@tool
def get_product_price(product:str) -> float:
    """ Look up the price of a product in the catalogue."""
    print(f" >> Executing get_product_price:(product='{product}')")
    prices = { 'laptop' : 1000, 'mouse' : 20, 'keyboard' : 50 }
    return prices.get(product,0)

@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """ Apply a discount tier to a price and return final price
    discount tiers: gold, silver, bronze"""
    print(f" >> Executing apply_discount:(price='{price}', discount_tier='{discount_tier}')")
    discount_percentage = { 'gold' : 0.5, 'silver' : 0.2, 'bronze' : 0.1 }
    discount=discount_percentage.get(discount_tier,0)
    return price * (1 - discount)


#-----AGENT LOOP---- the thinking to action to observation loop

@traceable(name="Langchain Agent Loop")
def run_agent(question:str):
    tools = [get_product_price, apply_discount]
    total_dict= {t.name:t for t in tools}
    
    llm = init_chat_model(f"ollama:{MODEL}",temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    
    print(f"Question: {question}")
    print( "=" * 60)
    
    messages = [
        SystemMessage(
            content =(
                "yOUR ARE a helpful shopping assistance."
                "You can access to product catalogue tool"
                "and a discount tool.\n\n"
                "STRICT RULES: U MUST FOLLOW THIS EXACTLY:\n"
                "1. never guess or assume any product price"
                "you must call get_product_price tool first to get the price\n"
                "2. only call apply_discount AFTER getting the price\n"
                "3. ALWAYS use the exact tool names above\n"
            )
        ),
        HumanMessage(content=question),
        
    ]
    
    #THE AGENT LOOP
    for iteration in range(MAX_ITERATIONS+1): #send msg to lllm and then excute the tool for think
        print(f"\n ----  Iteration {iteration} ----")
        ai_message = llm_with_tools.invoke(messages) #call the tool with messages as input
        tool_calls = ai_message.tool_calls
        
        #if no tool call - means agent doesn't need to think tm - direct final answer
        
        if not tool_calls:
            print(f"FINAL ANSWER: {ai_message.content}")
            return ai_message.content
        
        #seeing one tool call working -
        tool_call = tool_calls[0] 
        tool_name = tool_call.get("name") # getting the name of the tool
        tool_input = tool_call.get("args") #getting args of the tool



if __name__=="__main__":
    print("Hello Langchain Agent (.bind_tools)!")
    print()
    result= run_agent("what is the price of laptop after applying a gold discount?")

