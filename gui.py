import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Crew, Process
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from Agents import search_queries_recommendation_agent, search_engine_agent, scraping_agent, procurement_report_author_agent
from Tasks import search_queries_recommendation_task, search_engine_task, scraping_task, procurement_report_author_task
import agentops

# Load environment variables
load_dotenv()

# Streamlit UI
st.set_page_config(page_title="AI Procurement System", layout="wide")
st.title("🔍 AI Procurement System")

# User Inputs
company_name = st.text_input("🏢 Company Name")
about_company = st.text_area("📜 About Your Company")
product_name = st.text_input("🛍️ Product Name")
country_name = st.text_input("🌍 Country Name")
language = st.text_input("🗣️ Language")

# Ensure session state is initialized
if "user_data" not in st.session_state:
    st.session_state["user_data"] = {}

if "workflow_completed" not in st.session_state:
    st.session_state["workflow_completed"] = False

# Submit button logic
if st.button("🚀 Submit"):
    if company_name and product_name and country_name:
        with st.status("Running AI workflow... Please wait.", expanded=True) as status:
            st.session_state["user_data"] = {
                "company_name": company_name,
                "about_company": about_company,
                "product_name": product_name,
                "country_name": country_name,
                "language": language
            }

            # Initialize AgentOps safely
            agentops_api_key = os.getenv("AGENTOPS_API_KEY")
            if agentops_api_key:
                agentops.init(api_key=agentops_api_key, skip_auto_end_session=True)
            else:
                st.warning("⚠️ AGENTOPS_API_KEY not found! Proceeding without monitoring.")

            # Define company context
            company_context = StringKnowledgeSource(
                content=st.session_state["user_data"]["about_company"]
            )

            # Create CrewAI workflow
            crew = Crew(
                agents=[
                    search_queries_recommendation_agent,
                    search_engine_agent,
                    scraping_agent,
                    procurement_report_author_agent
                ],
                tasks=[
                    search_queries_recommendation_task,
                    search_engine_task,
                    scraping_task,
                    procurement_report_author_task
                ],
                process=Process.sequential,
                knowledge_sources=[company_context]
            )

            # Run CrewAI workflow
            results = crew.kickoff(inputs={
                "company_name": st.session_state["user_data"]["company_name"],
                "product_name": st.session_state["user_data"]["product_name"],
                "websites_list": ["www.amazon.eg", "www.jumia.com.eg", "www.noon.com/egypt-en"],
                "country_name": st.session_state["user_data"]["country_name"],
                "no_keywords": 10,
                "language": st.session_state["user_data"]["language"],
                "score_th": 0.10,
                "top_recommendations_no": 10
            })

            status.update(label="✅ Workflow completed!", state="complete", expanded=False)
            st.session_state["workflow_completed"] = True

# Display output files if workflow is completed
if st.session_state["workflow_completed"]:
    st.subheader("📂 Generated Reports:")

    output_dir = os.getenv('output_dir')
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

    files = [f for f in os.listdir(output_dir) if f.endswith((".txt", ".json", ".html"))]

    if files:
        for file in files:
            file_path = os.path.join(output_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            with st.expander(f"📄 {file}"):
                st.code(content, language="markdown")
    else:
        st.warning("⚠️ No output files found in the directory.")

# Restart button
if st.button("🔄 Restart Workflow"):
    st.session_state["workflow_completed"] = False
    st.rerun()
