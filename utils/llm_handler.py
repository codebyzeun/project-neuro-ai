import os
from ctransformers import AutoModelForCausalLM
import logging
from .persona import PERSONA_PROMPT
from config import AI_CONFIG, CHAT_CONFIG

logger = logging.getLogger('llm_handler')


class LlamaModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LlamaModel, cls).__new__(cls)
            cls._instance.model = None
        return cls._instance

    def __init__(self):
        if self.model is None:
            self._load_model()

    def _load_model(self):
        """Load the TinyLlama model using ctransformers"""
        model_path = os.getenv('MODEL_PATH')
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at {model_path}")
            raise FileNotFoundError(f"Model file not found at {model_path}")

        try:
            logger.info(f"Loading model from {model_path}...")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                model_type="llama",
                context_length=AI_CONFIG['context_window'],
                gpu_layers=0
            )
            logger.info(f"Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def generate_response(self, user_message, history=None):
        """Generate a response from the model with the sassy persona"""
        if history is None:
            history = []

        context = self._format_prompt(user_message, history)

        try:
            generated_text = self.model(
                context,
                max_new_tokens=AI_CONFIG['max_new_tokens'],
                temperature=AI_CONFIG['temperature'],
                top_p=AI_CONFIG['top_p'],
                repetition_penalty=AI_CONFIG['repeat_penalty'],
                stop=["User:", "Assistant:", "\n\n"]
            )

            return generated_text.strip()

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Ugh, I'm having a brain freeze right now. Try again later or whatever."

    def _format_prompt(self, user_message, history):
        """Format the prompt with history and the sassy persona"""
        prompt = PERSONA_PROMPT + "\n\n"

        for h_user, h_bot in history[-CHAT_CONFIG['history_limit']:]:
            prompt += f"User: {h_user}\nAssistant: {h_bot}\n\n"

        prompt += f"User: {user_message}\nAssistant:"

        return prompt