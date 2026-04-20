from agents import build_search_agent, writer_chain, build_reader_agent, critic_chain
from tools import web_search, scrape_url
from langchain_core.messages import HumanMessage

def run_research_pipeline(topic: str) -> dict:

    state = {}

    #Search agent work
    print("\n" + "="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
    "messages": [HumanMessage(content=f"find recent, reliable detailed information about: {topic}.")]
    })
    state["search_results"] = search_result['messages'][-1].content

    print("\n search results", state['search_results'])

    #step 2 reader agent
    print("\n" + "="*50)
    print("step 2- reader agent is scraping top .")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
    "messages": [HumanMessage(
        content=f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
    )]
})

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n scraped content: \n", state['scraped_content'])

    #step 3 writer agent
    print("\n" + "="*50)
    print("step 3- writer agent is drafting the report.")
    print("="*50)

    research_combined = (
    f"SEARCH RESULTS : \n {state['search_results']} \n\n"
    f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
)

    state["report"] = writer_chain.invoke({
    "topic" : topic,
    "research" : research_combined
})

    print("\n Final Report\n", state['report'])

    #critic agent
    print("\n" + "="*50)
    print("step 4- critic agent is reviewing the report.")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state["report"]
    })

    print("\n critic report \n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    run_research_pipeline(topic)