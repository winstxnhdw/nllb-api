from typing import Protocol, Self
from unittest.mock import create_autospec

from fasttext_pybind import fasttext
from lingua import Language as LinguaLanguage
from lingua import LanguageDetector as LinguaLanguageDetector
from lingua import LanguageDetectorBuilder

from server.typedefs import Confidence, Language
from server.utils import huggingface_file_download


class FastTextProtocol(Protocol):
    def loadModel(self, model_path: str) -> None: ...  # noqa: N802
    def predict(
        self,
        text: str,
        k: int,
        threshold: float,
        on_unicode_error: str,
    ) -> list[tuple[float, str]]: ...


class LanguageDetector:
    """
    Summary
    -------
    a static class for the Language Detector

    Methods
    -------
    detect(
        text: str,
        fast_model_confidence_threshold: float,
        accurate_model_confidence_threshold: float
    ) -> tuple[Language, Confidence]
        detect the language of the input text
    """

    __slots__ = ('fast_extra_labels', 'fast_k', 'fast_model', 'lingua_languages', 'lingua_model')

    def __init__(
        self,
        fast_model: FastTextProtocol,
        lingua_model: LinguaLanguageDetector,
    ) -> None:
        self.fast_model = fast_model
        self.lingua_model = lingua_model
        self.lingua_languages = [
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

        self.fast_extra_labels = {
            '__label__ton_Latn',
            '__label__oss_Cyrl',
            '__label__che_Cyrl',
            '__label__ady_Cyrl',
            '__label__tah_Latn',
            '__label__diq_Latn',
            '__label__nia_Latn',
            '__label__nav_Latn',
            '__label__abk_Cyrl',
            '__label__bxr_Cyrl',
            '__label__wes_Latn',
            '__label__gom_Deva',
            '__label__udm_Cyrl',
            '__label__roh_Latn',
            '__label__alt_Cyrl',
            '__label__arn_Latn',
            '__label__ewo_Latn',
            '__label__xmf_Geor',
            '__label__pcm_Latn',
            '__label__bis_Latn',
            '__label__krc_Cyrl',
            '__label__chv_Cyrl',
            '__label__kal_Latn',
        }
        self.fast_k = len(self.fast_extra_labels) + 1

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        self.lingua_model.unload_language_models()
        del self.fast_model
        del self.lingua_model

    def detect(
        self,
        text: str,
        *,
        fast_model_confidence_threshold: float,
        accurate_model_confidence_threshold: float,
    ) -> tuple[Language, Confidence]:
        """
        Summary
        -------
        detect the language of the input text

        Parameters
        ----------
        text (str)
            the input to detect the language of

        fast_model_confidence_threshold (float)
            minimum acceptable confidence before using the accurate model results

        accurate_model_confidence_threshold (float)
            minimum acceptable confidence before falling back to the faster model results

        Returns
        -------
        language (Language)
            the detected language

        confidence (Confidence)
            the confidence score of the detected language
        """
        fast_confidence, label = next(
            (confidence, label)
            for confidence, label in self.fast_model.predict(text, self.fast_k, 0.0, 'strict')
            if label not in self.fast_extra_labels
        )

        fast_label: Language = label[9:]  # pyright: ignore [reportAssignmentType]

        if fast_confidence >= fast_model_confidence_threshold:
            return fast_label, fast_confidence

        confidence_value = self.lingua_model.compute_language_confidence_values(text)[0]

        if (confidence := confidence_value.value) <= accurate_model_confidence_threshold:
            return fast_label, fast_confidence

        return (
            self.lingua_languages[int(confidence_value.language)],  # pyright: ignore [reportReturnType, reportArgumentType]
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

    fast_model = fasttext()
    fast_model.loadModel(huggingface_file_download(repository, 'model.bin'))
    lingua_model = (
        LanguageDetectorBuilder.from_all_languages_without(LinguaLanguage.LATIN)
        .with_preloaded_language_models()
        .build()
    )

    return LanguageDetector(fast_model, lingua_model)
