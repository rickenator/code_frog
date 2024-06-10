# Code Whisperer

Code Whisperer is an advanced AI assistant specialized in software development. This project aims to enhance the capabilities of an AI model (GPT-4) to handle complex software development conversations by dynamically managing and updating the context provided to the model.

This is a Work In Progress (WIP) and not a complete application of the framework which itself may be incomplete. 

It would also need a UI and some testing as to whether the system prompt is worth the investment.

If we roughly estimate the $ cost with the sample system prompt:

226 (System Prompt) + 250 (Key Points) + 250 (Recent Interactions) + 29 (User Input) = 755 tokens
Assume the cost is $0.03 / 1000 tokens = $0.02265 per message (example doesn't reflect actual prices, you'll have to check yourself.)



## Features

- **Requirements Gathering and Analysis**: Assist with collecting and analyzing software requirements.
- **Software Architecture and Design**: Provide guidance on software architecture and design patterns.
- **Implementation and Coding**: Help with coding in multiple programming languages.
- **Testing and Quality Assurance**: Offer strategies for testing and quality assurance.
- **Integration with External APIs**: Support for integrating with various external APIs and services.
- **Deployment and CI/CD**: Advise on deployment practices and continuous integration/continuous deployment (CI/CD).
- **Documentation and Technical Writing**: Assist with creating documentation and technical writing.
- **Project Management**: Provide tips and best practices for project management and agile methodologies.

## How It Works

### Local Storage for Enhanced Context

Code Whisperer uses local storage to manage and enhance context across interactions. By storing key points and interactions in a local SQLite database, the system can:

- **Persist Context Across Sessions**: Maintain a consistent context over multiple interactions and sessions, providing more coherent and relevant responses.
- **Retrieve Key Points**: Dynamically fetch and combine key points from various categories to ensure that the model has access to the most relevant information.
- **Update Context**: Continuously update the context based on new interactions and information, ensuring that the assistant's responses remain accurate and up-to-date.


### NLP for Categorical and Keyword Expansion

The project employs natural language processing (NLP) techniques to dynamically identify relevant categories and expand keywords:

- **Named Entity Recognition (NER)**: Extracts named entities from user input to identify specific terms and concepts.
- **Keyword Matching**: Matches user input against predefined keywords to categorize the query accurately.
- **Dynamic Category Update**: Adds new terms to categories if they are identified as relevant but not previously included, ensuring the system can adapt to new topics and terminologies.

## Files

- `code_whisperer.py`: The initial implementation of the AI assistant for software development.
- `code_whisperer_with_system.py`: Enhanced version with a system prompt to focus the model on software development.

## Getting Started

1. **Clone the Repository**:
   ```sh
   git clone git@github.com:yourusername/code_whisperer.git
   cd code_whisperer

2. **Set Up the Environment**:
   Make sure you have Python installed. Set up a virtual environment and install required packages.
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
3. **Add Your OpenAI API Key**:
   Make sure to set your OpenAI API key in your environment.
   ```sh
   export OPENAI_API_KEY='your-api-key'

4. **Running the Script**:
   ```sh
   python code_whisperer.py
   # or
   python code_whisperer_with_system.py


## Contributing
   Ideas for improvements and experiences are welcomed.

## License

Code Whisperer © 2024 by Rick Goldberg is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International

   


   
