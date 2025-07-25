from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class BrCnjRecognizer(PatternRecognizer):
    """
    Recognize CNJ number using regex and checksum.

    For more information about CNJ: https://en.wikipedia.org/wiki/CNPJ

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Processo", r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}",
            0.4,
        ),
        Pattern(
            "Processo (weak)", r"\d{14}",
            0.05,
        ),
    ]

    CONTEXT = [
        "Processo",
        "Número do Processo",
        "Nº do Processo",
        "CNJ"    
        ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "pt",
        supported_entity: str = "BR_CNJ",
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

        NNNNNNN = int( pattern_text_clean[:7] )
        AAAA = int( pattern_text_clean[9:13] )
        JTR = int( pattern_text_clean[13:16] )
        OOOO = int( pattern_text_clean[16:20] )

        n1 = NNNNNNN % 97
        n2 = (n1 + AAAA + JTR) % 97
        n3 = 98 - (((n2 + OOOO) * 100) % 97)

        checksum_1 = n3 // 10
        checksum_2 = n3 % 10

        return checksum_1 == int(pattern_text_clean[7]) and checksum_2 == int(pattern_text_clean[8])
    