import os
import logging
import typer
from openai import OpenAI
from abc import ABC, abstractmethod
from consts import GPT_MODEL
from typing import Optional


def setup_logging():
    """
    Sets up the logging configuration for the application.
    """
    logging.basicConfig(
        level=logging.WARN,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


logger = logging.getLogger(__name__)
setup_logging()


def getOpenAiApiKey() -> Optional[str]:
    """
    Retrieves the OpenAI API key from environment variables.

    Returns:
        The OpenAI API key if found, otherwise None.
    """
    openAiApiKey = os.getenv("OPENAI_API_KEY")
    if not openAiApiKey:
        logger.error("OPENAI_API_KEY is not set. Please set the environment variable.")
    return openAiApiKey


class TextAnalyser(ABC):
    @abstractmethod
    def generate_text_report(self, text: str) -> Optional[str]:
        """
        Abstract method to generate a text report based on the input text.

        Args:
            text (str): The input text to analyze.

        Returns:
            Optional[str]: The generated report or None if the analysis failed.
        """
        pass


class TextAnalyserOpenAI(TextAnalyser):
    def __init__(self, model: str = GPT_MODEL) -> None:
        """
        Initializes the TextAnalyserOpenAI with a specified GPT model.

        Args:
            model (str): The model name to use for text analysis.
        """
        self.model = model
        self.client = OpenAI(api_key=getOpenAiApiKey())

    def _make_request(
        self, text: str, prompt_template: str, max_tokens: int = 100
    ) -> Optional[str]:
        """
        Makes a request to the OpenAI API to generate a report based on the input text and prompt template.

        Args:
            text (str): The input text to analyze.
            prompt_template (str): The prompt template to use for generating the report.
            max_tokens (int): The maximum number of tokens to generate.

        Returns:
            Optional[str]: The generated report or None if the request failed.
        """
        try:
            response = self.client.completions.create(
                model=self.model,
                prompt=prompt_template.format(text=text),
                max_tokens=max_tokens,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            logger.exception("Failed to make request.")
            return None

    def generate_text_report(self, text: str) -> Optional[str]:
        """
        Generates a text report for the given input text using a predefined prompt template.

        Args:
            text (str): The input text to analyze.

        Returns:
            Optional[str]: The generated text report or None if the analysis failed.
        """
        report_prompt = (
            "Generate a concise report that highlights key insights and patterns from the following data:\n\n{text}\n\n"
            "Report should have 4 sections: introduction, key insights, "
            "text analysis findings (sentiment analysis, topic modeling, entity recognition, "
            "readability level, textual heatmap with most popular tokens) and summary."
        )
        return self._make_request(text, report_prompt, 500)


def main(text: str):
    """
    The main function that runs the text analysis and prints the report.

    Args:
        text (str): The input text to analyze.
    """
    logger.info("Starting text analysis.")
    text_analyzer = TextAnalyserOpenAI()
    report = text_analyzer.generate_text_report(text)
    if report:
        print(report)
    else:
        logger.error("No report generated.")


if __name__ == "__main__":
    typer.run(main)
