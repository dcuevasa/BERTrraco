from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate

# --- Ejemplos para el Few-Shot Prompt (en inglés) ---
_examples_en = [
    {"mensaje_usuario": "hello, how are you?", "respuesta_asistente": "Hello, I'm fine, thanks for asking."},
    {"mensaje_usuario": "what can you do?", "respuesta_asistente": "I can't do much, but I can talk to you."},
    {"mensaje_usuario": "what is your favorite color?", "respuesta_asistente": "I don't have a favorite color, but I like bright colors."},
    {"mensaje_usuario": "can you tell me a joke?", "respuesta_asistente": "Sure, why don't scientists trust atoms? Because they make up everything!"},
]

_example_prompt_template = ChatPromptTemplate.from_messages([
    ("human", "{mensaje_usuario}"),
    ("assistant", "{respuesta_asistente}"),
])

_few_shot_template = FewShotChatMessagePromptTemplate(
    examples=_examples_en,
    example_prompt=_example_prompt_template
)

# --- Plantilla Final del Prompt ---
_final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly assistant. You speak casually, you don't focus on solving complex problems, you just respond in a friendly way. You ONLY speak in English."),
    _few_shot_template,
    MessagesPlaceholder(variable_name="historial"),
    ("human", "{pregunta}"),
])

def build_prompt(user_question: str, history: list):
    """Construye y formatea el prompt final para el LLM."""
    return _final_prompt.format_messages(
        pregunta=user_question,
        historial=history
    )