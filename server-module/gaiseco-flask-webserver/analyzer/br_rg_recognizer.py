from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class BrRgRecognizer(PatternRecognizer):
    """
    Recognize RG number using regex and checksum.

    For more information about RG: https://en.wikipedia.org/wiki/CPF

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "RG", r"\d{2}\.\d{3}\.\d{3}-\d{1}",
            0.4,
        ),
        Pattern(
            "RG (weak)", r"\d{9}",
            0.05,
        ),
    ]

    CONTEXT = [
        "RG",
        "Registro Geral",
        "Documento de Identificação"  
        ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "pt",
        supported_entity: str = "BR_RG",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

    # def validate_result(self, pattern_text: str) -> bool:
    #     pattern_text_clean = ''.join(filter(str.isdigit, pattern_text))
    #     digits = [int(digit) for digit in pattern_text_clean]
    #     weights_1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    #     weights_2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

    #     checksum_1 = sum(digit * weight for digit, weight in zip(digits[:9], weights_1))
    #     checksum_1 %= 11

    #     if checksum_1 < 2:
    #         checksum_1 = 0
    #     else:
    #         checksum_1 = 11 - checksum_1

    #     checksum_2 = sum(digit * weight for digit, weight in zip(digits[:10], weights_2))
    #     checksum_2 %= 11

    #     if checksum_2 < 2:
    #         checksum_2 = 0
    #     else:
    #         checksum_2 = 11 - checksum_2

    #     return checksum_1 == digits[9] and checksum_2 == digits[10]