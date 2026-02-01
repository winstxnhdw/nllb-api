use lingua::LanguageDetector;
use lingua::LanguageDetectorBuilder;
use pyo3::IntoPyObject;
use pyo3::PyErr;
use pyo3::prelude::Bound;
use pyo3::prelude::Py;
use pyo3::prelude::PyAny;
use pyo3::prelude::PyResult;
use pyo3::prelude::Python;
use pyo3::prelude::pyclass;
use pyo3::prelude::pymethods;
use pyo3::types::PyAnyMethods;
use pyo3::types::PyListMethods;
use pyo3::types::PyString;
use pyo3::types::PyStringMethods;

const LINGUAGES: [&str; 74] = [
    "afr_Latn", "als_Latn", "arb_Latn", "hye_Armn", "azj_Latn", "eus_Latn", "bel_Cyrl", "ben_Beng",
    "nob_Latn", "bos_Latn", "bul_Cyrl", "cat_Latn", "zho_Hans", "hrv_Latn", "ces_Latn", "dan_Latn",
    "nld_Latn", "eng_Latn", "epo_Latn", "est_Latn", "fin_Latn", "fra_Latn", "lug_Latn", "kat_Geor",
    "deu_Latn", "ell_Grek", "guj_Gujr", "heb_Hebr", "hin_Deva", "hun_Latn", "isl_Latn", "ind_Latn",
    "gle_Latn", "ita_Latn", "jpn_Jpan", "kaz_Cyrl", "kor_Hang", "lvs_Latn", "lit_Latn", "mkd_Cyrl",
    "msa_Latn", "mri_Latn", "mar_Deva", "mon_Cyrl", "nno_Latn", "pes_Arab", "pol_Latn", "por_Latn",
    "pan_Guru", "ron_Latn", "rus_Cyrl", "srp_Cyrl", "sna_Latn", "slk_Latn", "slv_Latn", "som_Latn",
    "sot_Latn", "spa_Latn", "swh_Latn", "swe_Latn", "tgl_Latn", "tam_Taml", "tel_Telu", "tha_Thai",
    "tso_Latn", "tsn_Latn", "tur_Latn", "ukr_Cyrl", "urd_Arab", "vie_Latn", "cym_Latn", "xho_Latn",
    "yor_Latn", "zul_Latn",
];

const REDUNDANT_LABELS: [&str; 23] = [
    "__label__ton_Latn",
    "__label__oss_Cyrl",
    "__label__che_Cyrl",
    "__label__ady_Cyrl",
    "__label__tah_Latn",
    "__label__diq_Latn",
    "__label__nia_Latn",
    "__label__nav_Latn",
    "__label__abk_Cyrl",
    "__label__bxr_Cyrl",
    "__label__wes_Latn",
    "__label__gom_Deva",
    "__label__udm_Cyrl",
    "__label__roh_Latn",
    "__label__alt_Cyrl",
    "__label__arn_Latn",
    "__label__ewo_Latn",
    "__label__xmf_Geor",
    "__label__pcm_Latn",
    "__label__bis_Latn",
    "__label__krc_Cyrl",
    "__label__chv_Cyrl",
    "__label__kal_Latn",
];

#[cold]
#[inline(never)]
fn unlikely_python_error<E: std::fmt::Display>(error: E) -> PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(error.to_string())
}

#[inline(always)]
fn is_redundant_label(label: &Bound<'_, PyString>) -> bool {
    label
        .to_str()
        .is_ok_and(|label| REDUNDANT_LABELS.contains(&label))
}

#[pyclass(frozen, get_all, immutable_type)]
struct Prediction {
    confidence: f64,
    language: Py<PyString>,
}

#[pyclass(name = "LanguageDetector", frozen, immutable_type)]
struct Detector {
    fasttext_model_call: Py<PyAny>,
    lingua_model: LanguageDetector,
}

#[pymethods]
impl Detector {
    #[new]
    fn new(py: Python, fasttext_model: Py<PyAny>) -> PyResult<Self> {
        let detector = Self {
            lingua_model: LanguageDetectorBuilder::from_all_languages().build(),
            fasttext_model_call: fasttext_model.getattr(py, "predict")?,
        };

        Ok(detector)
    }

    fn detect(
        &self,
        py: Python,
        text: &str,
        fasttext_confidence_threshold: f64,
        lingua_confidence_threshold: f64,
    ) -> PyResult<Prediction> {
        let fasttext_arguments = (text, 24, 0.0, pyo3::intern!(py, "strict"));
        let (fasttext_confidence, fasttext_label) = self
            .fasttext_model_call
            .call1(py, fasttext_arguments)?
            .cast_bound::<pyo3::types::PyList>(py)?
            .iter()
            .filter_map(|item| item.extract::<(f64, Bound<'_, PyString>)>().ok())
            .find(|(_, label)| !is_redundant_label(label))
            .ok_or_else(|| unlikely_python_error("No prediction found!"))?;

        let fasttext_language = fasttext_label
            .to_str()?
            .strip_prefix("__label__")
            .ok_or_else(|| unlikely_python_error("Unknown language label!"))?;

        let fasttext_prediction = Prediction {
            confidence: fasttext_confidence,
            language: fasttext_language.into_pyobject(py)?.into(),
        };

        if fasttext_confidence >= fasttext_confidence_threshold {
            return Ok(fasttext_prediction);
        }

        let &(lingua_language, lingua_confidence) = self
            .lingua_model
            .compute_language_confidence_values(text)
            .first()
            .ok_or_else(|| unlikely_python_error("Failed to predict a language!"))?;

        if lingua_confidence <= lingua_confidence_threshold {
            return Ok(fasttext_prediction);
        }

        let language = LINGUAGES[lingua_language as usize]
            .into_pyobject(py)?
            .unbind();

        let lingua_prediction = Prediction {
            confidence: lingua_confidence,
            language,
        };

        Ok(lingua_prediction)
    }
}

#[pyo3::prelude::pymodule(gil_used = false)]
mod language {
    #[pymodule_export]
    use super::Detector;
    #[pymodule_export]
    use super::Prediction;
}
