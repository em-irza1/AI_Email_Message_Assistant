import os
from groq import Groq
from groq import APIConnectionError, APIStatusError, RateLimitError


class GroqConfigurationError(Exception):
    """Raised when the Groq API is not configured."""


class GroqServiceError(Exception):
    """Raised when the Groq service cannot complete a request."""


def generate_with_groq(prompt):
    """Send a prompt to Groq and return the generated text."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key.strip() in {"", "your_actual_api_key_here", "replace_with_your_key"}:
        raise GroqConfigurationError()

    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    client = Groq(api_key=api_key, timeout=45.0, max_retries=1)

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful writing assistant. Improve the user's text "
                        "without inventing facts. Follow the requested format exactly."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            max_completion_tokens=1200,
        )
        return (completion.choices[0].message.content or "").strip()
    except RateLimitError:
        raise GroqServiceError("The AI service is busy or its usage limit was reached. Please wait a moment and try again.")
    except APIConnectionError:
        raise GroqServiceError("Unable to connect to the AI service. Check your internet connection and try again.")
    except APIStatusError as exc:
        # Do not expose provider response bodies, headers, or credentials.
        if exc.status_code in (401, 403):
            raise GroqServiceError("The API key was rejected. Check that your Groq API key is correct.")
        if exc.status_code == 404:
            raise GroqServiceError("The selected AI model is unavailable. Check GROQ_MODEL in your .env file.")
        raise GroqServiceError("The AI service could not process the request. Please try again.")
    except Exception:
        raise GroqServiceError("Something went wrong while contacting the AI service. Please try again.")
