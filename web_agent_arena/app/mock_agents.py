import random


def get_mock_response(task_type: str) -> str:
    """Mock function to simulate agent responses."""
    responses = {
        "wikipedia": [
            "https://en.wikipedia.org/wiki/Battle_of_Waterloo",
            "https://en.wikipedia.org/wiki/Ancient_Egyptian_architecture",
            "https://en.wikipedia.org/wiki/Theory_of_relativity",
            "https://en.wikipedia.org/wiki/Renaissance_art",
            "https://en.wikipedia.org/wiki/Quantum_mechanics",
        ],
        "search": [
            "I found the information about renewable energy trends in Europe.",
            "The latest statistics on global climate change can be found in the IPCC report.",
            "According to recent studies, electric vehicle adoption is increasing worldwide.",
            "The research paper discusses advances in artificial intelligence.",
            "The data shows significant progress in sustainable agriculture practices.",
        ],
        "qa": [
            "The capital of France is Paris.",
            "The speed of light is approximately 299,792 kilometers per second.",
            "Water freezes at 0 degrees Celsius at standard atmospheric pressure.",
            "The Earth's atmosphere is primarily composed of nitrogen and oxygen.",
            "The human body has 206 bones.",
        ],
    }

    task_responses = responses.get(task_type, responses["wikipedia"])
    return random.choice(task_responses)
