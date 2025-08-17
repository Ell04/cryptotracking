"""

Runs semantic analysis using GDELT articles and anomaly dates of cryptocurrencies.

"""


from google.generativeai import GenerativeModel, configure
from utils import get_key

configure(api_key=get_key("gemini"))
class GeminiModel(GenerativeModel):
    def __init__(self, role:str, examples: str, instruction: str, model_name: str = "gemini-2.5-flash"):
        super().__init__(model_name=model_name)
        self.model_name = model_name
        self.role = role
        self.examples = examples
        self.instruction = instruction

    def build_prompt(self, articles: str) -> str:
        """
        Build the prompt for the LLM using the anomaly dates and articles.

        Take articles as input as is more dynamic than roles, examples, and instructions.

        Args:
            articles (str): The articles to include in the prompt.

        """
        return PromptBuild(articles, self.role, self.examples, self.instruction).build_prompt()

    def run_semantics(self, prompt: str, max_tokens: int = 1024) -> str:
        """
        
        Content generation (semantics) using the LLM based off input data (dates and articles).

        Parameters:
            prompt (str): The prompt to send to the LLM.
            max_tokens (int): The maximum number of tokens to generate.

        Returns:
            str: The generated content from the LLM.
        """
        response = self.generate(prompt=prompt, max_tokens=max_tokens)
        return response
    

class PromptBuild:
    @staticmethod
    def build_prompt(articles, role, example, instruction):
        prompt = f"""
        {role}

        {example}

        {instruction}

        {articles}
        """
        return prompt