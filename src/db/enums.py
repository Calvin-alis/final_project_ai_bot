from enum import Enum # StrEnum

class SessionMode(str, Enum):
    GPT = 'gpt'
    TALK = 'talk'
    QUIZ = 'quiz'
    RANDOM = 'random'
    