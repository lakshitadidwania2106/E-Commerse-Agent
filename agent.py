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
    pass



if __name__=="__main__":
    print("Hello Langchain Agent (.bind_tools)!")
    print()
    result= run_agent("what is the price of laptop after applying a gold discount?")

