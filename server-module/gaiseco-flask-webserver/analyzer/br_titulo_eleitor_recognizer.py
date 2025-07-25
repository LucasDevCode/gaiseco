from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class BrTERecognizer(PatternRecognizer):
    """
    Recognize Titulo de Eleitor number using regex and checksum.

    For more information about Titulo de Eleitor: https://en.wikipedia.org/wiki/CNPJ
                                                  https://www.cadcobol.com.br/cobol_dv_calcula_titulo_eleitor.htm

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        # Pattern(
        #     "Titulo de Eleitor", r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}",
        #     0.4,
        # ),
        Pattern(
            "Titulo de Eleitor (weak)", r"\d{12}",
            0.1,
        ),
    ]

    CONTEXT = [
        "Titulo de Eleitor",
        "e-Titulo"      
        ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "pt",
        supported_entity: str = "BR_TITULO_ELEITOR",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

    def validate_result(self, pattern_text: str) -> bool:
        pattern_text_clean = ''.join(filter(str.isdigit, pattern_text))
        digits = [int(digit) for digit in pattern_text_clean]
        weights_1 = [2,3,4,5,6,7,8,9]
        weights_2 = [7,8,9]

        checksum_1 = sum(digit * weight for digit, weight in zip(digits[:8], weights_1))
        checksum_1 %= 11

        if checksum_1 == 10:
            checksum_1 = 0

        checksum_2 = sum(digit * weight for digit, weight in zip(digits[8:11], weights_2))
        checksum_2 %= 11

        if checksum_2 == 10:
            checksum_2 = 0

        return checksum_1 == digits[10] and checksum_2 == digits[11]