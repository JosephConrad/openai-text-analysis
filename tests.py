import unittest
from unittest.mock import patch
from main import TextAnalyserOpenAI, getOpenAiApiKey


class TestGetOpenAiApiKey(unittest.TestCase):

    @patch("main.os.getenv")
    @patch("main.logger.error")
    def test_get_openai_api_key_exists(self, mock_logger_error, mock_getenv):
        """
        Test if OpenAI API key exists
        """
        mock_getenv.return_value = "test_api_key"
        result = getOpenAiApiKey()
        self.assertEqual(result, "test_api_key")
        mock_logger_error.assert_not_called()

    @patch("main.os.getenv")
    @patch("main.logger.error")
    def test_get_openai_api_key_not_exists(self, mock_logger_error, mock_getenv):
        """
        Test if OpenAI API key not exists
        """
        mock_getenv.return_value = None
        result = getOpenAiApiKey()
        self.assertIsNone(result)
        mock_logger_error.assert_called_once_with(
            "OPENAI_API_KEY is not set. Please set the environment variable."
        )


class TestTextAnalyserOpenAI(unittest.TestCase):

    @patch("main.getOpenAiApiKey", return_value="mock_api_key")
    @patch("main.OpenAI")
    def setUp(self, mock_openai, mock_getapikey):
        """
        Setup for tests with mocked OpenAI client and API key retrieval.
        """
        self.analyser = TextAnalyserOpenAI()

    @patch("main.TextAnalyserOpenAI._make_request")
    def test_generate_text_report_success(self, mock_make_request):
        """
        Test successful generation of text report.
        """
        mock_text = "Test text"
        mock_report = "Mocked report content"
        mock_make_request.return_value = mock_report

        report = self.analyser.generate_text_report(mock_text)

        self.assertEqual(report, mock_report)
        mock_make_request.assert_called_once()
        mock_make_request.assert_called_with(mock_text, unittest.mock.ANY, 500)

    @patch("main.TextAnalyserOpenAI._make_request")
    def test_make_request_called_with_correct_arguments(self, mock_make_request):
        """
        Test that _make_request is called with correct arguments.
        """
        mock_text = "Test text"
        self.analyser.generate_text_report(mock_text)

        prompt_template = (
            "Generate a concise report that highlights key insights and patterns from the following data:\n\n{text}\n\n"
            "Report should have 4 sections: introduction, key insights, "
            "text analysis findings (sentiment analysis, topic modeling, entity recognition, "
            "readability level, textual heatmap with most popular tokens) and summary."
        )

        mock_make_request.assert_called_once_with(mock_text, prompt_template, 500)


if __name__ == "__main__":
    unittest.main()
