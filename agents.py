from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv

load_dotenv()

#Chat Model
llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)

#1st agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
    )

#2nd agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )

#writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a expert research writer.  write clear, structured and insightful report."),
    ("human","""write a detailed research report based on the topic below.

Topic = {topic}"

Research gathered:
{research}

Structure the report as:
     - Introduction
     - Key findings (minimum 3 well explained points)
     - conclusion
     - Source (list all the URLs used for research)

Be detailed, factual and professional.""")

])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a sharpa and constructive research critic. Be honest and specific."),
    ("human","""Review the researc report below and eveluate it strictly.
     
Report:
{report}
     
Respond in this exact format:
     
Score: x/10
Strengths:
- ...
- ...
     
Areas of improvement:
- ...
- ...   

One live verdict:
""")
])

critic_chain = critic_prompt | llm | StrOutputParser()
     
