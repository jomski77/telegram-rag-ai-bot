
## Telegram Monitoring and Real-Time Messaging Application  

This is a Flask-based web application designed to serve as a quick reference guide and messaging platform. The application integrates with Telegram using the python-telegram-bot library and provides real-time communication through Flask-SocketIO. It utilizes Retrieval-Augmented Generation (RAG) to enhance its querying and response capabilities, ensuring that users receive contextually relevant and accurate information derived from embedded documents and resources.
---

## Overview  
- Real-time tracking and logging of incoming Telegram messages.  
- Displaying message interactions on a web-based interface using WebSocket communication.  
- Managing embedded data storage for efficient query handling.  

---

## Prerequisites  

- **Python Version**: 3.10 (recommended)  
- **Telegram Bot Token**: Obtain this using [BotFather](https://t.me/botfather) on Telegram. (Included)  
- **Python Packages**: Listed under "Required Packages" below.  
- **Required Models:** Ensure the following models are installed in Ollama: (Change the used model in the '.env' file)
    - deepseek-r1:1.5b (or other models)
    - nomic-embed-text



## Installing Models in Ollama

After installing Ollama, download the required models using the following commands:
    ```sh
    ollama pull deepseek-r1:1.5b
    ollama pull nomic-embed-text
    ```
---


## Installation Instructions  

1. **Clone the Repository**:  
    ```sh
    git clone <repository-url>
    cd <repository-folder>
    ```

2. **Create and Activate a Virtual Environment**:  
    ```sh
    python -m venv venv
    source venv/bin/activate    # On Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies**:  
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**:  
    This application uses an `.env` file to store sensitive configuration data.  
    Create an `.env` file in the project root and add the following:  
    ```env
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
    LLM_MODEL=your_model_config_here
    ```

    - `TELEGRAM_BOT_TOKEN`: This is the unique token for your Telegram bot.  
    - `LLM_MODEL`: This configures the model to be used for processing queries.  

---

## Project Structure and Purpose  

- **app.py**:  
    The primary application file responsible for:  
      - Monitoring all incoming Telegram messages.  
      - Tracking outgoing responses.  
      - Displaying interactions on the web interface using Flask-SocketIO.  

- **populate_database.py**:  
    Facilitates the processing and embedding of PDF files located in the `data` folder into the Chroma vector storage.  
      - Utilizes the "nomic-embed-text" model for embedding.  
      - Accepts the optional `--reset` command to clear the database before reloading.  
      - Provides a comprehensive summary of the embedding process upon completion.  

- **query_data.py**:  
    Contains the template for query prompts and the core function that handles data querying.  

- **cli_query.py**:  
    Enables users to perform data queries directly from the command line interface.  

- **telegram_bot.py**:  
    Launches a Telegram bot to receive and respond to user inquiries, leveraging the application's data processing capabilities.  

- **test_rag.py**:  
    Includes basic tests to validate the application's understanding and processing of the embedded data.  

---

## Running the Application  

To start the main application:  
```sh
python app.py
```
This will launch the web interface, accessible at:  
```
http://localhost:5000
```

To process and embed PDF files into the Chroma vector storage:  
```sh
python populate_database.py --reset
```
This command will reset the existing database and initiate the embedding process. A detailed summary will be provided upon completion.  

To query the embedded data using the terminal:  
```sh
python cli_query.py
```

To initiate the Telegram bot for monitoring and responding to messages:  
```sh
python telegram_bot.py
```

---

## Troubleshooting Guide  
- **WebSocket Connection Issues**: Verify that `cors_allowed_origins="*"` is set within the SocketIO configuration.  
- **Telegram Bot Not Responding**: Double-check the `TELEGRAM_BOT_TOKEN` in the `.env` file to ensure accuracy.  
- **Database Issues**: If database inconsistencies are observed, run the `populate_database.py` script with the `--reset` option to clear and reload the data.  

