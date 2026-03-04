import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
os.environ.setdefault("USER_AGENT", "ColdEmailGenerator/1.0")
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobright.ai/jobs/info/69a44345b600907a962a389b?utm_source=1121&imp_id=3667457648293191244__instant_push__1772374220962_9917&utm_medium=email")
    hiring_manager_linkedin = st.text_input("Hiring Manager LinkedIn URL (optional):", value="")
    col1, col2 = st.columns(2)
    with col1:
        generate_email = st.button("Generate Email")
    with col2:
        generate_linkedin_post = st.button("Generate LinkedIn Post")

    if generate_email or generate_linkedin_post:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                if generate_email:
                    content = llm.write_mail(job, links, hiring_manager_linkedin)
                else:
                    content = llm.write_linkedin_post(job, links, hiring_manager_linkedin)
                st.code(content, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)