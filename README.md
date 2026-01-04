# Kabarak University Virtual Assistant

A Rasa-based conversational AI chatbot designed to handle common university inquiries and provide
24/7 automated support for students, staff, and prospective applicants.

## Project Overview

This project addresses the challenges universities face in providing timely and accurate information
through traditional methods like notice boards, static web pages, and human assistants. The virtual
assistant leverages Natural Language Processing (NLP) and machine learning to understand user
queries and provide instant, consistent responses.

## Features

- **24/7 Availability**: Provides round-the-clock support without human intervention
- **Natural Language Understanding**: Processes user queries in natural English
- **Intent Recognition**: Identifies user intentions from text input
- **Conversational Flow**: Maintains context through multi-turn conversations
- **Web-based Interface**: Clean, responsive chat interface built with React.js

## Technology Stack

- **Backend Framework**: Rasa 3.6.21
- **Frontend**: React.ts
- **Programming Language**: Python 3.10.18
- **Database**: PostgreSQL
- **Deployment**: Localhost

## System Requirements

- Python 3.10
- Node.js and npm
- Postgres database
- Docker
- Minimum of 2GB RAM
- Minimum if 10 GB Storage

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jim-03/kabu-assist.git
   cd kabu-assist
   ```
2. **Run the setup scripts**

   **Linux:**
    ```shell
   ./setup.sh # .\setup.ps1
    ```

3. **Create a `.env` file containing the following:

```dotenv
export DB_HOST=localhost# db host
export DB_PORT=5432# port number
export DB_NAME=chats# the name of the database to store chats
export DB_USER=username# Your db username
export DB_PASS=password#The password to your database
export GEMINI_API_KEY=api_key#API key from https://aistudio.google.com
```
4. **Export the environment variables**
    ```shell
    source .env
    ```
   
5. **Activate the virtual environment(if not activated)**
    ```shell
   cd chatbot-core
    source .venv/bin/activate  # source .venv\Scripts\Activate.ps1
    ```

6. **Start the server**
    ```shell
    rasa run --enable-api --cors "*"
    ```

7. **Start the actions server in a separate (activated) terminal**
   ```shell
    rasa run actions
    ```
   
8. **Start the frontend**
    ```shell
    npm run dev
    ```
   
9. **In your browser, visit https://localhost:3000**

## Sample Interactions

The chatbot can handle various types of university inquiries:

- **Admissions**: "What are the admission requirements?", "Is there an application fee and how much
  is it?"
- **Services**: "Do you accept cash payments?", "What are the library hours?"
- **Contact Information**: "What's the university's phone number?"
- **General**: Greetings, farewells, and help requests

## System Architecture

The system consists of five main modules:

1. **Intent Classification Module**: Determines user intentions using NLU
2. **Entity Recognition Module**: Identifies specific entities in queries
3. **Training Data Module**: Stores and manages training data
4. **Dialog Management Module**: Controls conversation flow using predefined stories
5. **Interface Module**: Web-based UI for user interaction

## Benefits

- **Automated Support**: Reduces workload on administrative staff
- **Consistency**: Provides uniform responses to similar queries
- **Scalability**: Can handle multiple users simultaneously
- **Cost-effective**: Eliminates need for additional human resources
- **Learning Capability**: Can be retrained with new data as needed

## Limitations

- Limited to English language only
- Relies on pre-trained responses for accuracy
- May struggle with highly complex or unexpected queries
- Requires periodic retraining for new information

## License

This project is developed as part of a Bachelor of Science in Computer Science degree requirement at
Kabarak University.

The project contains a copy of the University's website and shouldn't be deployed to the public to
avoid copyright violation

## Contributing

This is an academic project, but suggestions and improvements are welcome. Please feel free to
submit issues or pull requests.

## Support

For questions or support regarding this project, please contact the Department of Computer Science
at Kabarak University.