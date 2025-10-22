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
use pyo3::types::PyModuleMethods;
use pyo3::types::PyString;
use pyo3::types::PyStringMethods;

#[cold]
#[inline(never)]
fn unlikely_python_error<E: std::fmt::Display>(error: E) -> PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(error.to_string())
}

#[inline(always)]
fn is_redundant_label(label: &Bound<'_, PyString>) -> bool {
    label == "__label__ton_Latn"
        || label == "__label__oss_Cyrl"
        || label == "__label__che_Cyrl"
        || label == "__label__ady_Cyrl"
        || label == "__label__tah_Latn"
        || label == "__label__diq_Latn"
        || label == "__label__nia_Latn"
        || label == "__label__nav_Latn"
        || label == "__label__abk_Cyrl"
        || label == "__label__bxr_Cyrl"
        || label == "__label__wes_Latn"
        || label == "__label__gom_Deva"
        || label == "__label__udm_Cyrl"
        || label == "__label__roh_Latn"
        || label == "__label__alt_Cyrl"
        || label == "__label__arn_Latn"
        || label == "__label__ewo_Latn"
        || label == "__label__xmf_Geor"
        || label == "__label__pcm_Latn"
        || label == "__label__bis_Latn"
        || label == "__label__krc_Cyrl"
        || label == "__label__chv_Cyrl"
        || label == "__label__kal_Latn"
}

#[pyclass(frozen, get_all, immutable_type)]
struct Prediction {
    confidence: f64,
    language: Py<PyString>,
}

#[pyclass(name = "LanguageDetector", frozen, immutable_type)]
struct Detector {
    lingua_languages: [&'static str; 74],
    fasttext_model_call: Py<PyAny>,
    lingua_model: LanguageDetector,
    fasttext_k: u8,
}

#[pymethods]
impl Detector {
    #[new]
    fn new(py: Python, fasttext_model: Py<PyAny>) -> PyResult<Self> {
        let lingua_languages: [&'static str; 74] = [
            "afr_Latn", "als_Latn", "arb_Latn", "hye_Armn", "azj_Latn", "eus_Latn", "bel_Cyrl",
            "ben_Beng", "nob_Latn", "bos_Latn", "bul_Cyrl", "cat_Latn", "zho_Hans", "hrv_Latn",
            "ces_Latn", "dan_Latn", "nld_Latn", "eng_Latn", "epo_Latn", "est_Latn", "fin_Latn",
            "fra_Latn", "lug_Latn", "kat_Geor", "deu_Latn", "ell_Grek", "guj_Gujr", "heb_Hebr",
            "hin_Deva", "hun_Latn", "isl_Latn", "ind_Latn", "gle_Latn", "ita_Latn", "jpn_Jpan",
            "kaz_Cyrl", "kor_Hang", "lvs_Latn", "lit_Latn", "mkd_Cyrl", "msa_Latn", "mri_Latn",
            "mar_Deva", "mon_Cyrl", "nno_Latn", "pes_Arab", "pol_Latn", "por_Latn", "pan_Guru",
            "ron_Latn", "rus_Cyrl", "srp_Cyrl", "sna_Latn", "slk_Latn", "slv_Latn", "som_Latn",
            "sot_Latn", "spa_Latn", "swh_Latn", "swe_Latn", "tgl_Latn", "tam_Taml", "tel_Telu",
            "tha_Thai", "tso_Latn", "tsn_Latn", "tur_Latn", "ukr_Cyrl", "urd_Arab", "vie_Latn",
            "cym_Latn", "xho_Latn", "yor_Latn", "zul_Latn",
        ];

        let detector = Self {
            lingua_model: LanguageDetectorBuilder::from_all_languages().build(),
            fasttext_model_call: fasttext_model.getattr(py, "predict")?,
            fasttext_k: 24,
            lingua_languages,
        };

        Ok(detector)
    }

    #[pyo3(signature = (text, *, fasttext_confidence_threshold, lingua_confidence_threshold))]
    fn detect(
        &self,
        py: Python,
        text: &str,
        fasttext_confidence_threshold: f64,
        lingua_confidence_threshold: f64,
    ) -> PyResult<Prediction> {
        let fasttext_arguments = (text, self.fasttext_k, 0.0, pyo3::intern!(py, "strict"));
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

        let language = self.lingua_languages[lingua_language as usize].into_pyobject(py)?;
        let lingua_prediction = Prediction {
            confidence: lingua_confidence,
            language: language.into(),
        };

        Ok(lingua_prediction)
    }
}

#[pyo3::prelude::pymodule()]
fn language(m: &Bound<'_, pyo3::prelude::PyModule>) -> PyResult<()> {
    m.add_class::<Detector>()?;
    m.add_class::<Prediction>()?;
    Ok(())
}
