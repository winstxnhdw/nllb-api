use gxhash::HashMap;
use lingua::LanguageDetector;
use lingua::LanguageDetectorBuilder;
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

fn python_error<E: std::fmt::Display>(error: E) -> PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(error.to_string())
}

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
    language: &'static str,
}

#[pyclass(name = "LanguageDetector", frozen, immutable_type)]
struct Detector {
    lingua_languages: [&'static str; 74],
    fasttext_map: HashMap<&'static str, &'static str>,
    fasttext_model_call: Py<PyAny>,
    lingua_model: LanguageDetector,
    fasttext_k: u8,
}

#[pymethods]
impl Detector {
    #[new]
    fn new(py: Python, fasttext_model: Py<PyAny>) -> PyResult<Self> {
        let fasttext_map = HashMap::from_iter([
            ("__label__ace_Arab", "ace_Arab"),
            ("__label__ace_Latn", "ace_Latn"),
            ("__label__acm_Arab", "acm_Arab"),
            ("__label__acq_Arab", "acq_Arab"),
            ("__label__aeb_Arab", "aeb_Arab"),
            ("__label__afr_Latn", "afr_Latn"),
            ("__label__ajp_Arab", "ajp_Arab"),
            ("__label__aka_Latn", "aka_Latn"),
            ("__label__amh_Ethi", "amh_Ethi"),
            ("__label__apc_Arab", "apc_Arab"),
            ("__label__arb_Arab", "arb_Arab"),
            ("__label__arb_Latn", "arb_Latn"),
            ("__label__ars_Arab", "ars_Arab"),
            ("__label__ary_Arab", "ary_Arab"),
            ("__label__arz_Arab", "arz_Arab"),
            ("__label__asm_Beng", "asm_Beng"),
            ("__label__ast_Latn", "ast_Latn"),
            ("__label__awa_Deva", "awa_Deva"),
            ("__label__ayr_Latn", "ayr_Latn"),
            ("__label__azb_Arab", "azb_Arab"),
            ("__label__azj_Latn", "azj_Latn"),
            ("__label__bak_Cyrl", "bak_Cyrl"),
            ("__label__bam_Latn", "bam_Latn"),
            ("__label__ban_Latn", "ban_Latn"),
            ("__label__bel_Cyrl", "bel_Cyrl"),
            ("__label__bem_Latn", "bem_Latn"),
            ("__label__ben_Beng", "ben_Beng"),
            ("__label__bho_Deva", "bho_Deva"),
            ("__label__bjn_Arab", "bjn_Arab"),
            ("__label__bjn_Latn", "bjn_Latn"),
            ("__label__bod_Tibt", "bod_Tibt"),
            ("__label__bos_Latn", "bos_Latn"),
            ("__label__bug_Latn", "bug_Latn"),
            ("__label__bul_Cyrl", "bul_Cyrl"),
            ("__label__cat_Latn", "cat_Latn"),
            ("__label__ceb_Latn", "ceb_Latn"),
            ("__label__ces_Latn", "ces_Latn"),
            ("__label__cjk_Latn", "cjk_Latn"),
            ("__label__ckb_Arab", "ckb_Arab"),
            ("__label__crh_Latn", "crh_Latn"),
            ("__label__cym_Latn", "cym_Latn"),
            ("__label__dan_Latn", "dan_Latn"),
            ("__label__deu_Latn", "deu_Latn"),
            ("__label__dik_Latn", "dik_Latn"),
            ("__label__dyu_Latn", "dyu_Latn"),
            ("__label__dzo_Tibt", "dzo_Tibt"),
            ("__label__ell_Grek", "ell_Grek"),
            ("__label__eng_Latn", "eng_Latn"),
            ("__label__epo_Latn", "epo_Latn"),
            ("__label__est_Latn", "est_Latn"),
            ("__label__eus_Latn", "eus_Latn"),
            ("__label__ewe_Latn", "ewe_Latn"),
            ("__label__fao_Latn", "fao_Latn"),
            ("__label__fij_Latn", "fij_Latn"),
            ("__label__fin_Latn", "fin_Latn"),
            ("__label__fon_Latn", "fon_Latn"),
            ("__label__fra_Latn", "fra_Latn"),
            ("__label__fur_Latn", "fur_Latn"),
            ("__label__fuv_Latn", "fuv_Latn"),
            ("__label__gla_Latn", "gla_Latn"),
            ("__label__gle_Latn", "gle_Latn"),
            ("__label__glg_Latn", "glg_Latn"),
            ("__label__grn_Latn", "grn_Latn"),
            ("__label__guj_Gujr", "guj_Gujr"),
            ("__label__hat_Latn", "hat_Latn"),
            ("__label__hau_Latn", "hau_Latn"),
            ("__label__heb_Hebr", "heb_Hebr"),
            ("__label__hin_Deva", "hin_Deva"),
            ("__label__hne_Deva", "hne_Deva"),
            ("__label__hrv_Latn", "hrv_Latn"),
            ("__label__hun_Latn", "hun_Latn"),
            ("__label__hye_Armn", "hye_Armn"),
            ("__label__ibo_Latn", "ibo_Latn"),
            ("__label__ilo_Latn", "ilo_Latn"),
            ("__label__ind_Latn", "ind_Latn"),
            ("__label__isl_Latn", "isl_Latn"),
            ("__label__ita_Latn", "ita_Latn"),
            ("__label__jav_Latn", "jav_Latn"),
            ("__label__jpn_Jpan", "jpn_Jpan"),
            ("__label__kab_Latn", "kab_Latn"),
            ("__label__kac_Latn", "kac_Latn"),
            ("__label__kam_Latn", "kam_Latn"),
            ("__label__kan_Knda", "kan_Knda"),
            ("__label__kas_Arab", "kas_Arab"),
            ("__label__kas_Deva", "kas_Deva"),
            ("__label__kat_Geor", "kat_Geor"),
            ("__label__knc_Arab", "knc_Arab"),
            ("__label__knc_Latn", "knc_Latn"),
            ("__label__kaz_Cyrl", "kaz_Cyrl"),
            ("__label__kbp_Latn", "kbp_Latn"),
            ("__label__kea_Latn", "kea_Latn"),
            ("__label__khm_Khmr", "khm_Khmr"),
            ("__label__kik_Latn", "kik_Latn"),
            ("__label__kin_Latn", "kin_Latn"),
            ("__label__kir_Cyrl", "kir_Cyrl"),
            ("__label__kmb_Latn", "kmb_Latn"),
            ("__label__kmr_Latn", "kmr_Latn"),
            ("__label__kon_Latn", "kon_Latn"),
            ("__label__kor_Hang", "kor_Hang"),
            ("__label__lao_Laoo", "lao_Laoo"),
            ("__label__lij_Latn", "lij_Latn"),
            ("__label__lim_Latn", "lim_Latn"),
            ("__label__lin_Latn", "lin_Latn"),
            ("__label__lit_Latn", "lit_Latn"),
            ("__label__lmo_Latn", "lmo_Latn"),
            ("__label__ltg_Latn", "ltg_Latn"),
            ("__label__ltz_Latn", "ltz_Latn"),
            ("__label__lua_Latn", "lua_Latn"),
            ("__label__lug_Latn", "lug_Latn"),
            ("__label__luo_Latn", "luo_Latn"),
            ("__label__lus_Latn", "lus_Latn"),
            ("__label__lvs_Latn", "lvs_Latn"),
            ("__label__mag_Deva", "mag_Deva"),
            ("__label__mai_Deva", "mai_Deva"),
            ("__label__mal_Mlym", "mal_Mlym"),
            ("__label__mar_Deva", "mar_Deva"),
            ("__label__min_Arab", "min_Arab"),
            ("__label__min_Latn", "min_Latn"),
            ("__label__mkd_Cyrl", "mkd_Cyrl"),
            ("__label__plt_Latn", "plt_Latn"),
            ("__label__mlt_Latn", "mlt_Latn"),
            ("__label__mni_Beng", "mni_Beng"),
            ("__label__khk_Cyrl", "khk_Cyrl"),
            ("__label__mos_Latn", "mos_Latn"),
            ("__label__mri_Latn", "mri_Latn"),
            ("__label__mya_Mymr", "mya_Mymr"),
            ("__label__nld_Latn", "nld_Latn"),
            ("__label__nno_Latn", "nno_Latn"),
            ("__label__nob_Latn", "nob_Latn"),
            ("__label__npi_Deva", "npi_Deva"),
            ("__label__nso_Latn", "nso_Latn"),
            ("__label__nus_Latn", "nus_Latn"),
            ("__label__nya_Latn", "nya_Latn"),
            ("__label__oci_Latn", "oci_Latn"),
            ("__label__gaz_Latn", "gaz_Latn"),
            ("__label__ory_Orya", "ory_Orya"),
            ("__label__pag_Latn", "pag_Latn"),
            ("__label__pan_Guru", "pan_Guru"),
            ("__label__pap_Latn", "pap_Latn"),
            ("__label__pes_Arab", "pes_Arab"),
            ("__label__pol_Latn", "pol_Latn"),
            ("__label__por_Latn", "por_Latn"),
            ("__label__prs_Arab", "prs_Arab"),
            ("__label__pbt_Arab", "pbt_Arab"),
            ("__label__quy_Latn", "quy_Latn"),
            ("__label__ron_Latn", "ron_Latn"),
            ("__label__run_Latn", "run_Latn"),
            ("__label__rus_Cyrl", "rus_Cyrl"),
            ("__label__sag_Latn", "sag_Latn"),
            ("__label__san_Deva", "san_Deva"),
            ("__label__sat_Olck", "sat_Olck"),
            ("__label__scn_Latn", "scn_Latn"),
            ("__label__shn_Mymr", "shn_Mymr"),
            ("__label__sin_Sinh", "sin_Sinh"),
            ("__label__slk_Latn", "slk_Latn"),
            ("__label__slv_Latn", "slv_Latn"),
            ("__label__smo_Latn", "smo_Latn"),
            ("__label__sna_Latn", "sna_Latn"),
            ("__label__snd_Arab", "snd_Arab"),
            ("__label__som_Latn", "som_Latn"),
            ("__label__sot_Latn", "sot_Latn"),
            ("__label__spa_Latn", "spa_Latn"),
            ("__label__als_Latn", "als_Latn"),
            ("__label__srd_Latn", "srd_Latn"),
            ("__label__srp_Cyrl", "srp_Cyrl"),
            ("__label__ssw_Latn", "ssw_Latn"),
            ("__label__sun_Latn", "sun_Latn"),
            ("__label__swe_Latn", "swe_Latn"),
            ("__label__swh_Latn", "swh_Latn"),
            ("__label__szl_Latn", "szl_Latn"),
            ("__label__tam_Taml", "tam_Taml"),
            ("__label__tat_Cyrl", "tat_Cyrl"),
            ("__label__tel_Telu", "tel_Telu"),
            ("__label__tgk_Cyrl", "tgk_Cyrl"),
            ("__label__tgl_Latn", "tgl_Latn"),
            ("__label__tha_Thai", "tha_Thai"),
            ("__label__tir_Ethi", "tir_Ethi"),
            ("__label__taq_Latn", "taq_Latn"),
            ("__label__taq_Tfng", "taq_Tfng"),
            ("__label__tpi_Latn", "tpi_Latn"),
            ("__label__tsn_Latn", "tsn_Latn"),
            ("__label__tso_Latn", "tso_Latn"),
            ("__label__tuk_Latn", "tuk_Latn"),
            ("__label__tum_Latn", "tum_Latn"),
            ("__label__tur_Latn", "tur_Latn"),
            ("__label__twi_Latn", "twi_Latn"),
            ("__label__tzm_Tfng", "tzm_Tfng"),
            ("__label__uig_Arab", "uig_Arab"),
            ("__label__ukr_Cyrl", "ukr_Cyrl"),
            ("__label__umb_Latn", "umb_Latn"),
            ("__label__urd_Arab", "urd_Arab"),
            ("__label__uzn_Latn", "uzn_Latn"),
            ("__label__vec_Latn", "vec_Latn"),
            ("__label__vie_Latn", "vie_Latn"),
            ("__label__war_Latn", "war_Latn"),
            ("__label__wol_Latn", "wol_Latn"),
            ("__label__xho_Latn", "xho_Latn"),
            ("__label__ydd_Hebr", "ydd_Hebr"),
            ("__label__yor_Latn", "yor_Latn"),
            ("__label__yue_Hant", "yue_Hant"),
            ("__label__zho_Hans", "zho_Hans"),
            ("__label__zho_Hant", "zho_Hant"),
            ("__label__zsm_Latn", "zsm_Latn"),
            ("__label__zul_Latn", "zul_Latn"),
        ]);

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
            fasttext_map,
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
            .downcast_bound::<pyo3::types::PyList>(py)?
            .iter()
            .filter_map(|item| item.extract::<(f64, Bound<'_, PyString>)>().ok())
            .find(|(_, label)| !is_redundant_label(label))
            .ok_or_else(|| python_error("No prediction found!"))?;

        let fasttext_language = self
            .fasttext_map
            .get(fasttext_label.to_str()?)
            .ok_or_else(|| python_error("Unknown language label!"))?;

        let fasttext_prediction = Prediction {
            confidence: fasttext_confidence,
            language: fasttext_language,
        };

        if fasttext_confidence >= fasttext_confidence_threshold {
            return Ok(fasttext_prediction);
        }

        let &(lingua_language, lingua_confidence) = self
            .lingua_model
            .compute_language_confidence_values(text)
            .first()
            .ok_or_else(|| python_error("Failed to compute language confidence values!"))?;

        if lingua_confidence <= lingua_confidence_threshold {
            return Ok(fasttext_prediction);
        }

        let lingua_prediction = Prediction {
            confidence: lingua_confidence,
            language: self.lingua_languages[lingua_language as usize],
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
