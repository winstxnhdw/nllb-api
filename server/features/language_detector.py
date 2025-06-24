from unittest.mock import create_autospec

from fasttext import load_model
from fasttext.FastText import _FastText as FastText
from lingua import Language as LinguaLanguage
from lingua import LanguageDetector as LinguaLanguageDetector
from lingua import LanguageDetectorBuilder

from server.typedefs import Language, Score
from server.utils import huggingface_file_download


class LanguageDetector:
    """
    Summary
    -------
    a static class for the Language Detector

    Methods
    -------
    detect(text: str) -> tuple[Language, Score]
        detect the language of the input text
    """

    __slots__ = ('fast_model', 'lingua_languages', 'lingua_model')

    def __init__(self, fast_model: FastText, lingua_model: LinguaLanguageDetector) -> None:
        self.fast_model = fast_model
        self.lingua_model = lingua_model
        self.lingua_languages = [
            None,
            'afr_Latn',
            'als_Latn',
            'arb_Latn',
            'hye_Armn',
            'azj_Latn',
            'eus_Latn',
            'bel_Cyrl',
            'ben_Beng',
            'nob_Latn',
            'bos_Latn',
            'bul_Cyrl',
            'cat_Latn',
            'zho_Hans',
            'hrv_Latn',
            'ces_Latn',
            'dan_Latn',
            'nld_Latn',
            'eng_Latn',
            'epo_Latn',
            'est_Latn',
            'fin_Latn',
            'fra_Latn',
            'lug_Latn',
            'kat_Geor',
            'deu_Latn',
            'ell_Grek',
            'guj_Gujr',
            'heb_Hebr',
            'hin_Deva',
            'hun_Latn',
            'isl_Latn',
            'ind_Latn',
            'gle_Latn',
            'ita_Latn',
            'jpn_Jpan',
            'kaz_Cyrl',
            'kor_Hang',
            None,
            'lvs_Latn',
            'lit_Latn',
            'mkd_Cyrl',
            'msa_Latn',
            'mri_Latn',
            'mar_Deva',
            'mon_Cyrl',
            'nno_Latn',
            'pes_Arab',
            'pol_Latn',
            'por_Latn',
            'pan_Guru',
            'ron_Latn',
            'rus_Cyrl',
            'srp_Cyrl',
            'sna_Latn',
            'slk_Latn',
            'slv_Latn',
            'som_Latn',
            'sot_Latn',
            'spa_Latn',
            'swh_Latn',
            'swe_Latn',
            'tgl_Latn',
            'tam_Taml',
            'tel_Telu',
            'tha_Thai',
            'tso_Latn',
            'tsn_Latn',
            'tur_Latn',
            'ukr_Cyrl',
            'urd_Arab',
            'vie_Latn',
            'cym_Latn',
            'xho_Latn',
            'yor_Latn',
            'zul_Latn',
        ]

    def detect(self, text: str) -> tuple[Language, Score]:
        """
        Summary
        -------
        detect the language of the input text

        Parameters
        ----------
        text (str)
            the input to detect the language of

        Returns
        -------
        language (Language)
            the detected language

        score (Score)
            the confidence score of the detected language
        """
        labels, scores = next(zip(*self.fast_model.predict([text]), strict=True))
        fast_label: Language = labels[0][9:]  # pyright: ignore [reportAssignmentType]
        fast_score = float(scores[0])

        if fast_score >= 0.85:  # noqa: PLR2004
            return fast_label, fast_score

        confidence_value = self.lingua_model.compute_language_confidence_values(text)[0]

        if (confidence := confidence_value.value) <= 0.1:  # noqa: PLR2004
            return fast_label, fast_score

        return (
            self.lingua_languages[confidence_value.language.value],  # pyright: ignore [reportReturnType]
            confidence,
        )


def get_language_detector(repository: str, *, stub: bool) -> LanguageDetector:
    """
    Summary
    -------
    get the language detector

    Parameters
    ----------
    repository (str)
        the repository to download the model from

    stub (bool)
        whether to return a stub object

    Returns
    -------
    language_detector (LanguageDetector)
        the language detector
    """
    if stub:
        return create_autospec(LanguageDetector)

    return LanguageDetector(
        load_model(huggingface_file_download(repository, 'model.bin')),
        LanguageDetectorBuilder.from_all_languages_without(LinguaLanguage.LATIN).build(),
    )
