from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.memory.open_ai import OpenAIMemory
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from lyzr_automata import Logger
from lyzr_automata.tools.prebuilt_tools import send_email_by_smtp_tool
from dotenv import load_dotenv
import os

load_dotenv()

# LOAD OUR API KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PASSWORD = os.getenv("PASSWORD")
EMAIL = os.getenv("EMAIL")

def send_cold_email(email_list, contact_info):
    # GPT 4 Text Model
    open_ai_model_text = OpenAIModel(
        api_key= OPENAI_API_KEY,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.3,
            "max_tokens": 1500,
        },
    )

    # Load memory from instructions file
    email_writer_memory = OpenAIMemory(
        file_path='data/instructions.txt'
    )

    # Create Agent with Memory
    email_writer_agent = Agent(
        prompt_persona="You are an intelligent email writer agent and assume the persona of a job seeker reaching out to potential employers or recruiters. The email should be professional, concise, and persuasive, highlighting the candidate's skills, experience, and why they are a good fit for the job description.",
        role="Cold Email writer",
        memory=email_writer_memory
    )

    # Create email writer Task
    email_writer_task = Task(
        name="Cold Email Creator",
        agent=email_writer_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Use the resume information and job description to write a cold email of 250 words to be sent to the recruiter. [IMPORTANT!] send the response in html use bullets for points and beautify it professionally. Return only the email. Don't leave any field empty. My personal details are : " + contact_info,
        log_output=True,
        enhance_prompt=False,
    )

    # Initialize email sender Tool
    email_sender_tool = send_email_by_smtp_tool(
        username=EMAIL,
        password=PASSWORD,
        host="smtp.gmail.com",
        port=587,
        sender_email=EMAIL
    )

    # Create email sender Task
    send_email_task = Task(
        name = "Send Email Task",
        tool = email_sender_tool,
        instructions="Send Email",
        model=open_ai_model_text,
        input_tasks = [email_writer_task],
        default_input = email_list
    )

    # Run Tasks using a pipeline
    logger = Logger()
    LinearSyncPipeline(
        logger=logger,
        name="Cold Emailer",
        completion_message="Email Sent!",
        tasks=[
            email_writer_task,
            send_email_task
        ],
    ).run()