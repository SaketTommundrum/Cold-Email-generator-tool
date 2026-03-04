import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

class Chain:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=SecretStr(api_key) if api_key else None,
        )


    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION
            The scraped text is from the job posting page of a website
            Your job is to extract the job postings and return them in JSON format containing following keys: 'role', 'experience','skills' and 'description'.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE): 
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})

        try:
            json_parser = JsonOutputParser()
            content = res.content
            if not isinstance(content, str):
                content = "".join(
                    block if isinstance(block, str) else str(block.get("text", ""))
                    for block in content
                )
            json_res = json_parser.parse(content)
        except OutputParserException:
            raise OutputParserException('Context too big. Unable to parse jobs')
        return json_res if isinstance(json_res, list) else [json_res]

    def write_mail(self, job, links, hiring_manager_linkedin=""):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### HIRING MANAGER LINKEDIN (OPTIONAL):
            {hiring_manager_linkedin}

            ### INSTRUCTION:
            You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
            If the LinkedIn URL is provided, personalize the opening line using neutral professional language and reference the profile context without inventing unverified details.
            Remember you are Mohan, BDE at AtliQ. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        linkedin_value = hiring_manager_linkedin.strip() if isinstance(hiring_manager_linkedin, str) else ""
        res = chain_email.invoke({
            "job_description": str(job),
            "link_list": links,
            "hiring_manager_linkedin": linkedin_value if linkedin_value else "Not provided",
        })
        return res.content

    def write_linkedin_post(self, job, links, hiring_manager_linkedin=""):
        prompt_post = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### HIRING MANAGER LINKEDIN (OPTIONAL):
            {hiring_manager_linkedin}

            ### INSTRUCTION:
            You are Mohan, a business development executive at AtliQ.
            Write a short, professional LinkedIn outreach post/message tailored to this hiring need.
            Mention AtliQ's relevant capabilities and naturally include 1-2 of these portfolio links: {link_list}
            If the LinkedIn URL is provided, personalize the opening in neutral professional language without inventing unverified details.
            Keep it concise, scannable, and CTA-driven.
            Do not provide a preamble.

            ### LINKEDIN POST (NO PREAMBLE):
            """
        )
        chain_post = prompt_post | self.llm
        linkedin_value = hiring_manager_linkedin.strip() if isinstance(hiring_manager_linkedin, str) else ""
        res = chain_post.invoke({
            "job_description": str(job),
            "link_list": links,
            "hiring_manager_linkedin": linkedin_value if linkedin_value else "Not provided",
        })
        return res.content

if __name__=="__main__":
    print(os.getenv("GROQ_API_KEY"))
