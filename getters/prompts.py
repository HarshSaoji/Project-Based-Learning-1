from groq import Groq  # Importing the Groq library for interacting with the LLM API.

# Defining a template prompt for generating paragraph responses based on a given topic and word count.
prompt = """
Provide a paragraph answer for {} in {} words for the
identified cancer type."""

# Defining a template for Q&A format, where a context is provided along with a question.
qna = """
<context>
{}
</context>
Question: {}
"""

model_name = ""  # Placeholder for the model name to be used for LLM requests.

# Function to get drug-related information for a specific cancer type.
def get_drug(context, cancer):
    drug = llm.chat.completions.create(  # Making an API call to generate a response.
        messages=[            
            {
                'role': 'system',  # Setting the role as 'system' to provide instructions to the LLM.
                'content': prompt.format("Drug Use Advisory", "50")  # Formatting the prompt for a 50-word response.
            }
        ],
        model=model_name,  # Using the specified model.
    )
    return drug  # Returning the generated response.

# Function to get diagnosis-related information for a specific cancer type.
def get_diagnosis(context, cancer):
    diagnosis = llm.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': prompt.format("Diagnosis", "100")  # Formatting the prompt for a 100-word response.
            }
        ],
        model=model_name,
    )
    return diagnosis  # Returning the generated response.

# Function to handle general Q&A interactions based on a given context and user query.
def q_n_a(context, query):
    answer = llm.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': qna.format(context, query)  # Formatting the question with the given context.
            }
        ],
        model=model_name,
    )
    return answer  # Returning the generated response.
