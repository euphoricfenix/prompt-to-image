
## Overview
This is a Streamlit-based interactive chatbot application inspired by the character Rancho from the movie *3 Idiots*. The chatbot combines the power of **LangChain (Ollama)** for natural language processing and **Stability AI** for generating images. Users can chat with Rancho and even request visuals based on the conversation context.

## Features
- **Interactive Chat Interface**: Engage in natural conversations with Rancho, who embodies a cheerful and innovative engineering student persona.
- **Visual Context Generation**: Automatically generate relevant images using Stability AI when prompted by specific triggers.
- **Character Consistency**: Rancho's responses and generated images remain consistent with his predefined personality and surroundings.
- **Session Memory**: Chat history and image generation contexts are stored using Streamlit’s session state, ensuring continuity during interactions.

## Technology Stack
- **Streamlit**: For creating the web-based chat interface.
- **LangChain (Ollama)**: For language model-based chatbot responses.
- **Stability AI SDK**: For generating high-quality images based on user prompts.
- **Python**: Programming language used for building the app.

## Getting Started

### Prerequisites
1. **Python 3.8 or above**
2. **Stability AI API Key**
   - Sign up for Stability AI and obtain an API key.
   - Set the key as an environment variable: `STABILITY_KEY`.
3. Install the required Python libraries.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/euphoricfenix/prompt-to-image.git
   cd prompt-to-image
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

### Environment Variables
Ensure the following environment variable is set:
- `STABILITY_KEY`: Your Stability AI API key.

### Usage
- Type your message in the chat input field to interact with Rancho.
- Use prompts like "Can I see your college?" or "What do you look like?" to trigger image generation.

## File Structure
```
.
├── app.py                  # Main application file
├── requirements.txt        # Dependencies
├── generated_images/       # Folder to store generated images
└── README.md               # Documentation
```

## Key Functions

### Chatbot Interaction
- **`handle_chat_response()`**: Processes user input, generates responses using LangChain, and triggers image generation if necessary.

### Image Generation
- **`should_generate_image()`**: Determines if an image is needed based on the user's input.
- **`get_image_context()`**: Retrieves or merges image contexts for consistency.
- **`build_consistent_prompt()`**: Constructs a detailed prompt for Stability AI.
- **`generate_image()`**: Calls Stability AI API to generate and save an image.

### Session State Management
- **`initialize_session_state()`**: Initializes session variables for chat history and image memory.

## Customization
- **Modify Rancho’s Personality**:
  Edit the `SYSTEM_PROMPT` constant to redefine Rancho’s traits, appearance, and environment.
- **Add Visual Triggers**:
  Update the `VISUAL_TRIGGERS` list to detect additional keywords for image generation.

## Known Issues
- If the Stability AI API key is missing or incorrect, image generation will fail with a message in the console.
- Generated images are stored locally in the `generated_images` folder, which may grow in size over time.

## Future Enhancements
- **Cloud Storage**: Store generated images on a cloud service like AWS S3.
- **Asynchronous API Calls**: Improve performance by implementing async image generation.
- **Multi-Language Support**: Enable conversations in languages other than English.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request.

## Acknowledgments
- **LangChain** for the chatbot logic.
- **Stability AI** for image generation.
- The creators of *3 Idiots* for inspiring Rancho’s personality.


