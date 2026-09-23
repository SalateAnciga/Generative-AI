#!/usr/bin/env python
# coding: utf-8

# In[1]:


from google import genai
#This connects our python prg to the gemini model 
client = genai.Client(api_key="AQ.Ab8RN6IykaWMLFSfvmsatKAVh76d4D1GG7AkFeuTYtm9-0GVjQ")


# In[2]:


import os
import sys
sys.path.append('../..')
from ml_info import ML_INFORMATION_PROMPT
import panel as pn  # GUI
pn.extension()


# ## ML INFOMATION 

# In[3]:


ML_INFORMATION_PROMPT


# ## Create A ML Assistance

# In[4]:


system_prompt = f"""
You are a Machine Learning Assistant.

Answer the user's questions using the following information:

{ML_INFORMATION_PROMPT}

Rules:
- Answer clearly and simply.
- Give examples when useful.
- If the information is not available, say that you don't know.
- Do not make up information.
"""


# ## Rule Based Moderation

# In[5]:


def moderate_question(user_question):
    
    blocked_words = [
        "violence",
        "illegal",
        "hack",
        "kill",
        "pump",
        "password",
        "forwarding"
    ]

    for word in blocked_words:
        if word.lower() in user_question.lower():
            return False

    return True


# In[6]:


user_question = input("Ask a question: ")

if moderate_question(user_question):
    print("Question is allowed.")
else:
    print("Sorry, I cannot process this question.")


# ## Topic Moderation

# In[11]:


system_prompt =f"""
You are a topic moderator for a Machine Learning Assistant chatbot.

Your task is to check whether the user's question is related to:
- Machine Learning
- Deep Learning
- Artificial Intelligence
- Natural Language Processing (NLP)
- Python for Machine Learning
- Data Science
- Machine Learning algorithms
- Model training and evaluation

{ML_INFORMATION_PROMPT}
"""


# ## Generate Answer

# In[12]:


from google import genai
from google.genai import types

user_question = input("Ask a question: ")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=user_question,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt
    )
)

answer = response.text

print("ML Assistant:")
print(answer)


# In[13]:


evaluation_prompt =f"""
You are an evaluator for a Machine Learning Assistant chatbot.

Evaluate the assistant's answer based on the provided Machine Learning information.

Check the following:

1. Relevance - Does the answer directly address the user's question?
2. Correctness - Is the information technically correct?
3. Completeness - Does the answer provide enough information?
4. Clarity - Is the answer simple and easy to understand?
5. Topic relevance - Is the answer related to Machine Learning?

Give a score from 1 to 5 for each criterion.

At the end, give a short overall evaluation.

Use this format:

Relevance: X/5
Correctness: X/5
Completeness: X/5
Clarity: X/5
Topic Relevance: X/5

Overall Evaluation:
[short explanation]

Machine Learning Information:
{ML_INFORMATION_PROMPT}

User Question:
{user_question}

Assistant Answer:
{answer}
"""


# In[17]:


def evaluate_answer(user_question,answer):

    prompt = f"""
{evaluation_prompt}

User Question:
{user_question}

Chatbot Answer:
{answer}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
                max_output_tokens=500
        )
    )

    return response.text


# In[18]:


evaluation = evaluate_answer(
    user_question,
    answer
)
print("Evaluation:")
print(evaluation)


# In[ ]:




