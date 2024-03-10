from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin, findDataFromJson

load_dotenv()
if __name__ == "__main__":
    print("Langchain Data Processing")
    linkedin_profile_url = linkedin_lookup_agent(name="input")
    print(linkedin_profile_url)
    template = """"
    given the {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    prompt_template = PromptTemplate(input_variables=["information"], template=template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=prompt_template)

    linkedin_data = scrape_linkedin(linkedin_profile_url=linkedin_profile_url)

    # linkedin_data = findDataFromJson()

    result = chain.run(information=linkedin_data)
    print(result)
