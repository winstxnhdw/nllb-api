from unittest.mock import create_autospec

from fasttext import load_model
from fasttext.FastText import _FastText as FastText
from lingua import Language as LinguaLanguage
from lingua import LanguageDetector as LinguaLanguageDetector
from lingua import LanguageDetectorBuilder

from server.typedefs import Confidence, Language
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

    __slots__ = ('fast_model', 'fast_threshold', 'lingua_languages', 'lingua_model', 'lingua_threshold')

    def __init__(
        self,
        fast_model: FastText,
        lingua_model: LinguaLanguageDetector,
        *,
        fast_threshold: float,
        lingua_threshold: float,
    ) -> None:
        self.fast_threshold = fast_threshold
        self.lingua_threshold = lingua_threshold
        self.fast_model = fast_model
        self.lingua_model = lingua_model
        self.lingua_languages = [
            None,  # Padding
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
            None,  # Latin is not supported by NLLB
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

    def detect(self, text: str) -> tuple[Language, Confidence]:
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

        confidence (Confidence)
            the confidence score of the detected language
        """
        labels, scores = next(zip(*self.fast_model.predict([text]), strict=True))
        fast_label: Language = labels[0][9:]  # pyright: ignore [reportAssignmentType]
        fast_confidence = float(scores[0])

        if fast_confidence >= self.fast_threshold:
            return fast_label, fast_confidence

        confidence_value = self.lingua_model.compute_language_confidence_values(text)[0]

        if (confidence := confidence_value.value) <= self.lingua_threshold:
            return fast_label, fast_confidence

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

    lingua_model = (
        LanguageDetectorBuilder.from_all_languages_without(LinguaLanguage.LATIN)
        .with_preloaded_language_models()
        .build()
    )

    return LanguageDetector(
        load_model(huggingface_file_download(repository, 'model.bin')),
        lingua_model,
        fast_threshold=0.85,
        lingua_threshold=0.85,
    )
