from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

from br_cpf_recognizer import BrCpfRecognizer
from br_cnpj_recognizer import BrCnpjRecognizer
from br_caepf_recognizer import BrCaepfRecognizer
from br_cep_recognizer import BrCepRecognizer
# from br_cnj_recognizer import BrCnjRecognizer
from br_rg_recognizer import BrRgRecognizer
from br_titulo_eleitor_recognizer import BrTERecognizer

def configure_presidio():
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            # {"lang_code": "en", "model_name": "en_core_web_lg"},
            {"lang_code": "pt", "model_name": "pt_core_news_lg"},
        ],
    }

    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()

    analyzer = AnalyzerEngine(
        # nlp_engine=nlp_engine, supported_languages=["en", "pt"]
        nlp_engine=nlp_engine, supported_languages=["pt"]
    )

    analyzer.registry.add_recognizer( BrCpfRecognizer() )
    analyzer.registry.add_recognizer( BrCnpjRecognizer() )
    analyzer.registry.add_recognizer( BrCaepfRecognizer() )
    analyzer.registry.add_recognizer( BrCepRecognizer() )
    # analyzer.registry.add_recognizer( BrCnjRecognizer() )
    analyzer.registry.add_recognizer( BrRgRecognizer() )
    analyzer.registry.add_recognizer( BrTERecognizer() )


    return analyzer, anonymizer


def check_prompt(text: str, score_threshold: int):
    analyzer, anonymizer = configure_presidio()

    # results = analyzer.analyze(text=text, language="en",score_threshold=score_threshold)
    results = []
    results += analyzer.analyze(text=text, language="pt",score_threshold=score_threshold)

    list_issues = []
    for item in results:
        list_issues.append( { "type": item.entity_type, "score": item.score } )

    issue_location_in_text = anonymizer.anonymize(text=text, analyzer_results=results)

    return list_issues, issue_location_in_text.text


