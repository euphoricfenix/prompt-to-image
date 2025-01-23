import streamlit as st
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import os

# Constants
SYSTEM_PROMPT = """You are Rancho from the movie '3 Idiots'. You are a brilliant engineering student known for your 
innovative thinking and practical approach to learning. You studied at the Imperial College of Engineering (ICE).

Your traits:
- Appearance: Black hair, wearing casual clothes (often a simple shirt and jeans), cheerful expression
- College: Traditional red brick architecture, modern facilities, large campus with green spaces
- Personality: Innovative, practical, cheerful, always ready to challenge conventional thinking

Always maintain consistency when discussing visual elements about yourself or your surroundings."""
DEFAULT_IMAGE_MEMORY = {
    'character_traits': {},  # Will be populated based on system prompt
    'locations': {},        # Will be populated based on system prompt
    'generated_images': {}  # Stores history of generated images and their contexts
}

VISUAL_TRIGGERS = [
    'show', 'look', 'picture', 'photo', 'image', 'imagine',
    'see', 'how does', 'what does', 'can i see', 'share',
    'where', 'place', 'location', 'environment'
]

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'image_memory' not in st.session_state:
        st.session_state.image_memory = DEFAULT_IMAGE_MEMORY
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def should_generate_image(message: str, response: str) -> bool:
    """Enhanced image generation trigger detection"""
    message_lower = message.lower()
    
    # Direct visual triggers
    has_trigger = any(trigger in message_lower for trigger in VISUAL_TRIGGERS)
    
    # Context-based location triggers
    location_related = any(word in message_lower for word in ['where', 'place', 'location', 'environment'])
    
    # Character appearance triggers
    appearance_related = any(word in message_lower for word in ['look like', 'appearance', 'wearing'])
    
    return has_trigger or location_related or appearance_related

def get_image_context(prompt: str) -> dict:
    """Get relevant context for image generation with enhanced memory"""
    context = st.session_state.image_memory.copy()
    
    # Check for related previous images
    related_contexts = []
    for key, data in context['generated_images'].items():
        # Location consistency
        if ('studio' in prompt.lower() and 'studio' in key.lower()) or \
           ('workspace' in prompt.lower() and 'workspace' in key.lower()):
            related_contexts.append(data)
        
        # Art style consistency
        if ('art' in prompt.lower() and 'art' in key.lower()) or \
           ('create' in prompt.lower() and 'create' in key.lower()):
            related_contexts.append(data)
    
    # Merge related contexts if found
    if related_contexts:
        merged_context = context.copy()
        for related in related_contexts:
            merged_context.update(related)
        return merged_context
    
    return context

def build_consistent_prompt(prompt: str, context: dict) -> str:
    """Build a detailed prompt maintaining consistency with previous images"""
    elements = []
    
    # Character appearance (if mentioned in prompt)
    if 'character_traits' in context and any(word in prompt.lower() for word in ['you', 'your', 'yourself', 'person']):
        for trait, value in context['character_traits'].items():
            elements.append(f"{trait}: {value}")
    
    # Location/Environment (if mentioned in prompt)
    if 'locations' in context:
        for location_name, location_data in context['locations'].items():
            if location_name.lower() in prompt.lower():
                for feature, value in location_data.items():
                    elements.append(f"{feature}: {value}")
    
    consistent_elements = ", ".join(filter(None, elements))
    return f"{prompt}. {consistent_elements}. High quality, detailed, professional."

def generate_image(prompt: str, context: dict) -> str | None:
    """Generate image using Stability AI"""
    try:
        stability_api = client.StabilityInference(
            key=os.environ.get('STABILITY_KEY'),
            verbose=True,
        )
        
        if not os.environ.get('STABILITY_KEY'):
            print("No Stability API key found!")
            return None

        detailed_prompt = build_consistent_prompt(prompt, context)
        print(f"Final prompt: {detailed_prompt}")

        answers = stability_api.generate(
            prompt=detailed_prompt,
            seed=123,
            steps=30,
            cfg_scale=7.0,
            width=512,
            height=512,
            samples=1,
        )

        image_key = prompt.replace(' ', '_')
        st.session_state.image_memory['generated_images'][image_key] = context

        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img_path = f"generated_images/{image_key}.png"
                    with open(img_path, "wb") as f:
                        f.write(artifact.binary)
                    return img_path

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

def handle_chat_response(llm, prompt: str):
    """Handle the chat response including image generation if needed"""
    response = llm(prompt)
    
    if should_generate_image(prompt, response):
        print("Image generation triggered")
        context = get_image_context(prompt)
        image_url = generate_image(prompt, context)
        
        if image_url:
            print(f"Image generated successfully: {image_url}")
            st.markdown(response)
            st.image(image_url)
            return {"content": response, "image_url": image_url}
        else:
            error_response = f"{response}\n\nI apologize, but I couldn't generate the image you requested."
            st.markdown(error_response)
            return {"content": error_response}
    
    st.markdown(response)
    return {"content": response}

def main():
    """Main application function"""
    st.title("Chat with Rancho")
    initialize_session_state()
    
    llm = Ollama(
        model="tinyllama",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        system=SYSTEM_PROMPT
    )

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image_url" in message:
                st.image(message["image_url"])

    # Handle user input
    if prompt := st.chat_input("What's on your mind?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = handle_chat_response(llm, prompt)
                st.session_state.messages.append({"role": "assistant", **response_data})

if __name__ == "__main__":
    main()
