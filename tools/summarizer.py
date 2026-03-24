from langchain.tools import tool

# Text longer than this will be previewed and flagged for summarization
_LONG_TEXT_THRESHOLD = 1500
_PREVIEW_LENGTH = 500


@tool
def summarize_text(text: str) -> str:
    """
    Summarize or preview a long piece of text.
    Use this tool when you have a large block of text that needs to be condensed,
    or when you want to signal that a text is too long to process in full.
    Input should be the raw text you want to summarize.
    This tool returns a trimmed preview for very long texts and signals
    the agent to handle summarization in its reasoning step.
    """
    text = text.strip()

    if not text:
        return "Error: No text provided to summarize."

    word_count = len(text.split())
    char_count = len(text)

    if char_count <= _LONG_TEXT_THRESHOLD:
        # Short enough — return as-is with metadata
        return (
            f"[Text is short enough to process directly — {word_count} words, "
            f"{char_count} characters]\n\n{text}"
        )

    # Long text: return a preview and instruct the agent
    preview = text[:_PREVIEW_LENGTH].rsplit(" ", 1)[0]  # cut cleanly on word boundary
    remaining_words = len(text[_PREVIEW_LENGTH:].split())

    return (
        f"[LONG TEXT DETECTED: {word_count} words, {char_count} characters. "
        f"Showing first {_PREVIEW_LENGTH} characters as preview. "
        f"Approximately {remaining_words} more words follow. "
        f"You should summarize the key points from this text in your response.]\n\n"
        f"--- PREVIEW ---\n{preview}...\n--- END PREVIEW ---"
    )
