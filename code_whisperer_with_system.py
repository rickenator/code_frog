"""
Filename: code_whisperer_with_system.py

Intent:
--------
The purpose of this script is to enhance the capabilities of an AI model (GPT-4) to handle 
complex software development conversations by dynamically managing and updating the context 
provided to the model. This includes identifying relevant categories from user inputs, 
retrieving key points, and ensuring the combined context stays within the model's token limit.

This is an extension of the original code_whisperer.py script, with additional functionality
to enable a system prompt that provides context and guidelines for the AI model to generate.
This may cost more tokens, but it ensures the AI model is well-informed about its role and may
be worth the investment for more accurate and relevant responses.


Description of the Strategy:
----------------------------
1. **Define Initial Categories and Keywords**: Start with a predefined set of categories 
   and associated keywords that cover various aspects of software development.
   
2. **Query Analysis using NLP and NER**: Use natural language processing (NLP) and named 
   entity recognition (NER) techniques to dynamically identify relevant terms and categories 
   from user inputs. 

3. **Dynamic Category Update**: If new relevant terms are identified that do not match existing 
   categories, dynamically add these terms to new categories, ensuring the system can adapt 
   to new topics.

4. **Context Retrieval and Combination**: Retrieve key points from all identified relevant 
   categories and combine them with recent interactions to form the context for the AI model. 
   Ensure the total token count for the combined context and user input stays within the model's limit.

5. **Generate AI Response**: Use the combined context to generate a relevant and accurate response 
   from the AI model. Store the interaction for future reference and context building.

Code Overview:
--------------
1. **Imports and Setup**: Import necessary libraries, set up NLP tools, and define the initial 
   set of categories and keywords.
   
2. **Function Definitions**:
    - `generate_response(prompt, max_tokens)`: Generate a response from the AI model based on the provided prompt.
    - `get_continuous_chunks(text)`: Extract continuous named entities from text using NER.
    - `determine_relevant_categories(query)`: Identify and return relevant categories from the user query.
    - `retrieve_context(session_id, limit)`: Retrieve recent interactions from the database.
    - `store_interaction(session_id, user_input, model_response)`: Store the user interaction in the database.
    - `store_key_points(session_id, category, summary)`: Store key points categorized by topic.
    - `get_key_points(session_id, category)`: Retrieve stored key points for a given category.
    - `update_key_points(session_id, category, new_points)`: Update the key points summary for a given category.
    - `extract_key_points_by_category(interactions)`: Extract and categorize key points from recent interactions.

3. **Example Workflow**:
    - Initialize the session and user input.
    - Retrieve and update context and key points.
    - Identify relevant categories based on the user input.
    - Combine key points with recent interactions to form the prompt.
    - Ensure the combined context and user input are within the token limit.
    - Generate and print the AI response.
    - Store the interaction in the database.

By following this strategy, the script ensures a robust and adaptive interaction with the AI model, 
capable of handling complex and evolving topics in software development.
"""



import openai
import sqlite3
import uuid
import nltk
from collections import Counter
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

openai.api_key = 'your-api-key'

# Define initial categories and keywords
category_keywords = {
    'requirements': ['requirements', 'specifications', 'needs', 'criteria', 'goals', 'objectives', 'user story'],
    'architecture and design': ['architecture', 'design', 'structure', 'blueprint', 'framework', 'model', 'diagram', 'pattern'],
    'implementation': ['implementation', 'coding', 'development', 'function', 'method', 'procedure', 'class', 'module', 'algorithm'],
    'testing': ['testing', 'tests', 'validation', 'verification', 'unit test', 'integration test', 'test case', 'test plan', 'QA'],
    'external APIs': ['API', 'external service', 'integration', 'third-party service', 'REST', 'SOAP', 'webhook', 'endpoint', 'API key'],
    'deployment': ['deployment', 'release', 'environment', 'production', 'staging', 'CI/CD', 'pipeline', 'rollout', 'rollback'],
    'documentation': ['documentation', 'doc', 'README', 'guide', 'manual', 'comments', 'annotations', 'spec'],
    'project management': ['project management', 'timeline', 'milestones', 'tasks', 'issues', 'tickets', 'backlog', 'sprint', 'agile', 'kanban', 'scrum']
}

system_prompt = """
You are an advanced AI assistant specialized in software development. Your role is to assist users with various aspects of software engineering, including but not limited to:
- Requirements gathering and analysis
- Software architecture and design
- Implementation and coding in multiple programming languages
- Testing and quality assurance
- Integration with external APIs and services
- Deployment and CI/CD practices
- Documentation and technical writing
- Project management and agile methodologies

When providing responses, ensure they are detailed, technically accurate, and relevant to the user's query. Use appropriate software development terminology and examples where necessary. Stay focused on the context of software engineering and aim to provide practical and actionable advice.

If the user introduces new topics or specific technologies, incorporate those into the conversation and adapt your responses accordingly. Your goal is to be a comprehensive and knowledgeable resource for software development-related queries.
"""

def generate_response(prompt, max_tokens=150):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    current_chunk = []
    continuous_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    return continuous_chunk

def determine_relevant_categories(query):
    tokens = nltk.word_tokenize(query.lower())
    token_counts = Counter(tokens)
    relevant_categories = set()
    
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword.lower() in token_counts:
                relevant_categories.add(category)
    
    # Identify entities and map them to categories
    entities = get_continuous_chunks(query)
    for entity in entities:
        found_category = False
        for category, keywords in category_keywords.items():
            if any(keyword.lower() in entity.lower() for keyword in keywords):
                relevant_categories.add(category)
                found_category = True
                break
        if not found_category:
            # If no category matches, add to a new category
            category_keywords.setdefault('dynamic', []).append(entity)
            relevant_categories.add('dynamic')
    
    return relevant_categories

def retrieve_context(session_id, limit=5):
    c.execute('''
    SELECT user_input, model_response FROM interactions
    WHERE session_id = ?
    ORDER BY timestamp DESC
    LIMIT ?
    ''', (session_id, limit))
    return c.fetchall()

def store_interaction(session_id, user_input, model_response):
    c.execute('''
    INSERT INTO interactions (session_id, user_input, model_response)
    VALUES (?, ?, ?)
    ''', (session_id, user_input, model_response))
    conn.commit()

def store_key_points(session_id, category, summary):
    c.execute('''
    INSERT INTO key_points (session_id, category, summary)
    VALUES (?, ?, ?)
    ON CONFLICT(session_id, category) DO UPDATE SET summary=excluded.summary
    ''', (session_id, category, summary))
    conn.commit()

def get_key_points(session_id, category):
    c.execute('''
    SELECT summary FROM key_points WHERE session_id = ? AND category = ?
    ''', (session_id, category))
    result = c.fetchone()
    return result[0] if result else ""

def update_key_points(session_id, category, new_points):
    current_summary = get_key_points(session_id, category)
    updated_summary = current_summary + "\n" + new_points if current_summary else new_points
    store_key_points(session_id, category, updated_summary)

def extract_key_points_by_category(interactions):
    context_text = "\n".join([f"User: {ui}\nBot: {mr}" for ui, mr in interactions])
    prompt = f"Extract key points from the following conversation and categorize them into requirements, architecture and design, implementation, testing, external APIs, deployment, documentation, and project management:\n\n{context_text}"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=300,
        temperature=0.5,
        n=1,
        stop=None
    )
    categories = {category: '' for category in category_keywords.keys()}
    response_text = response.choices[0].text.strip()
    
    for line in response_text.split('\n'):
        for category in categories:
            if line.startswith(category + ':'):
                categories[category] += line[len(category + ':'):].strip() + "\n"
    
    return categories

# Example workflow
conn = sqlite3.connect('context.db')
c = conn.cursor()

session_id = str(uuid.uuid4())
user_input = "How does the overall architecture of the project integrate with external APIs and how should we manage Vulkan image buffers?"

context = retrieve_context(session_id)
new_interactions = retrieve_context(session_id)
new_key_points = extract_key_points_by_category(new_interactions)

for category, points in new_key_points.items():
    update_key_points(session_id, category, points)

relevant_categories = determine_relevant_categories(user_input)
if not relevant_categories:
    relevant_categories = category_keywords.keys()

key_points = "\n".join([get_key_points(session_id, category) for category in relevant_categories if get_key_points(session_id, category)])

combined_context = system_prompt + "\n\n" + key_points + "\n\n" + "\n".join([f"User: {ui}\nBot: {mr}" for ui, mr in context])
prompt = f"{combined_context}\nUser: {user_input}\nBot:"

# Ensure the combined context stays within the token limit
if len(combined_context.split()) + len(user_input.split()) <= 8192:
    response = generate_response(prompt)
    print(response)
    store_interaction(session_id, user_input, response)
else:
    print("Context size exceeds the token limit.")
