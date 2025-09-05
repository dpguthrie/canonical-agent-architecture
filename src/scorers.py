# Custom scorer to check if the right tools were used
def tool_usage_scorer(output=None, expected=None, metadata=None):
    print("metadata is:")
    print(metadata)
    if not expected or "tools_used" not in expected:
        return {"name": "tool_usage", "score": 1}

    # Extract tool calls from trace
    used_tools = metadata.get("tools_used", []) if metadata else []
    expected_tools = expected["tools_used"]

    correct_tools_used = all(tool in used_tools for tool in expected_tools)

    return {
        "name": "tool_usage",
        "score": 1 if correct_tools_used else 0,
        "metadata": {
            "expected_tools": expected_tools,
            "used_tools": used_tools,
            "correct": correct_tools_used,
        },
    }


# Custom scorer to check if required content appears in the response
def content_accuracy_scorer(output=None, expected=None):
    if not expected or "required_phrases" not in expected:
        return {"name": "content_accuracy", "score": 1}

    phrases = expected["required_phrases"]
    lower_output = (output or "").lower()

    found_phrases = [phrase for phrase in phrases if phrase.lower() in lower_output]

    score = len(found_phrases) / len(phrases) if phrases else 1

    return {
        "name": "content_accuracy",
        "score": score,
        "metadata": {
            "required_phrases": phrases,
            "found_phrases": found_phrases,
            "missing_phrases": [p for p in phrases if p not in found_phrases],
        },
    }
