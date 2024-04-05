# Cold Email Generator

**Author** - Rasswanth S  
**Email** - rasswanth@lyzr.ai

A cold email generator using Lyzr-Automata. With the help of your resume and a job description, this app can send out personalised cold emails to the provided email IDs. 

## Flow Diagram
![Architecture Flow Diagram](<Cold Mailer.png>)

## Steps
1. Create a Text-to-Text Model (GPT-4) using OpenAIModel
2. Using OpenAIMemory, create a vector store memory for the agent that contains resume and job description information.
3. *email_writer_agent* - Create a Lyzr Agent for text email creation using the memory.
4. *email_writer_task* - Create Lyzr Task with instructions on writing the email using email_writer_agent agent.
5. *email_sender_tool* - Initialise the pre-built email sender tool
6. *send_email_task* - create another Lyzr Task that is going to send our email.
7. Run tasks in LinearSyncPipeline

## Links

**Medium** - https://medium.com/@rasswanthshankar/get-hired-faster-how-to-use-lyzr-automata-to-draft-personalized-cold-emails-38fc870ab2ca

**Video Walkthrough** - https://www.youtube.com/watch?v=hXLAN0qFP9g