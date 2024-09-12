import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

# Set up the Streamlit app
st.set_page_config(page_title="Aira - Math & Code Assistant", page_icon="🧮")
st.title("Aira - The Math Problem Solver and Code Generator")

# Hardcoded Groq API key (replace with your actual API key)
groq_api_key = "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"

# Initialize the LLM (Groq model)
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Tool 1: Wikipedia for information retrieval
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find various information on the topics mentioned"
)

# Tool 2: Math solver tool (LLMMathChain)
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math-related questions. Only input mathematical expressions are needed."
)

# Tool 3: Code generation prompt template
code_prompt = """
You are an expert code generator. Given the task below, generate optimized and efficient code with clear comments. 
Task: {task}
Generated Code:
"""

code_prompt_template = PromptTemplate(
    input_variables=["task"],
    template=code_prompt
)

code_chain = LLMChain(llm=llm, prompt=code_prompt_template)
code_generator = Tool(
    name="Code Generator",
    func=code_chain.run,
    description="A tool for generating code based on user requirements."
)

# Tool 4: Math reasoning prompt template
math_reasoning_prompt = """
You are a math assistant tasked with solving users' mathematical questions. Logically arrive at the solution and provide a detailed explanation point-wise for the question below.
Question: {question}
Answer:
"""

math_reasoning_prompt_template = PromptTemplate(
    input_variables=["question"],
    template=math_reasoning_prompt
)

math_reasoning_chain = LLMChain(llm=llm, prompt=math_reasoning_prompt_template)
reasoning_tool = Tool(
    name="Math Reasoning",
    func=math_reasoning_chain.run,
    description="A tool for answering complex math problems with logical reasoning."
)

# Initialize the agent with both code generation and math-solving tools
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool, code_generator],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I am Aira, your assistant. I can help you solve math problems or generate code. How can I assist you today?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

# Input field for user's query
query = st.text_area("Enter your math problem or code generation task:", "I need to write a Python function to calculate factorial of a number.")

if st.button("Get Answer"):
    if query:
        with st.spinner("Processing your request..."):
            # Detect if it's a math or code task
            if "code" in query.lower() or "function" in query.lower() or "script" in query.lower():
                st.session_state.messages.append({"role": "user", "content": query})
                st.chat_message("user").write(query)

                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                response = assistant_agent.run(f"Generate code for the following task: {query}", callbacks=[st_cb])
            else:
                st.session_state.messages.append({"role": "user", "content": query})
                st.chat_message("user").write(query)

                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                response = assistant_agent.run(f"Solve this math problem: {query}", callbacks=[st_cb])

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write('### Response:')
            st.success(response)
    else:
        st.warning("Please enter a valid query")
