use lingua::LanguageDetector;
use lingua::LanguageDetectorBuilder;
use pyo3::intern;
use pyo3::prelude::pyclass;
use pyo3::prelude::pymethods;
use pyo3::prelude::Bound;
use pyo3::prelude::Py;
use pyo3::prelude::PyAny;
use pyo3::prelude::PyResult;
use pyo3::prelude::Python;
use pyo3::types::PyAnyMethods;
use pyo3::types::PyList;
use pyo3::types::PyListMethods;
use pyo3::types::PyModuleMethods;
use pyo3::types::PyString;
use pyo3::types::PyStringMethods;
use pyo3::PyErr;

fn python_error<E: std::fmt::Display>(error: E) -> PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(error.to_string())
}

fn map_language(language: &str) -> PyResult<&'static str> {
    match language {
        "__label__ace_Arab" => Ok("ace_Arab"),
        "__label__ace_Latn" => Ok("ace_Latn"),
        "__label__acm_Arab" => Ok("acm_Arab"),
        "__label__acq_Arab" => Ok("acq_Arab"),
        "__label__aeb_Arab" => Ok("aeb_Arab"),
        "__label__afr_Latn" => Ok("afr_Latn"),
        "__label__ajp_Arab" => Ok("ajp_Arab"),
        "__label__aka_Latn" => Ok("aka_Latn"),
        "__label__amh_Ethi" => Ok("amh_Ethi"),
        "__label__apc_Arab" => Ok("apc_Arab"),
        "__label__arb_Arab" => Ok("arb_Arab"),
        "__label__arb_Latn" => Ok("arb_Latn"),
        "__label__ars_Arab" => Ok("ars_Arab"),
        "__label__ary_Arab" => Ok("ary_Arab"),
        "__label__arz_Arab" => Ok("arz_Arab"),
        "__label__asm_Beng" => Ok("asm_Beng"),
        "__label__ast_Latn" => Ok("ast_Latn"),
        "__label__awa_Deva" => Ok("awa_Deva"),
        "__label__ayr_Latn" => Ok("ayr_Latn"),
        "__label__azb_Arab" => Ok("azb_Arab"),
        "__label__azj_Latn" => Ok("azj_Latn"),
        "__label__bak_Cyrl" => Ok("bak_Cyrl"),
        "__label__bam_Latn" => Ok("bam_Latn"),
        "__label__ban_Latn" => Ok("ban_Latn"),
        "__label__bel_Cyrl" => Ok("bel_Cyrl"),
        "__label__bem_Latn" => Ok("bem_Latn"),
        "__label__ben_Beng" => Ok("ben_Beng"),
        "__label__bho_Deva" => Ok("bho_Deva"),
        "__label__bjn_Arab" => Ok("bjn_Arab"),
        "__label__bjn_Latn" => Ok("bjn_Latn"),
        "__label__bod_Tibt" => Ok("bod_Tibt"),
        "__label__bos_Latn" => Ok("bos_Latn"),
        "__label__bug_Latn" => Ok("bug_Latn"),
        "__label__bul_Cyrl" => Ok("bul_Cyrl"),
        "__label__cat_Latn" => Ok("cat_Latn"),
        "__label__ceb_Latn" => Ok("ceb_Latn"),
        "__label__ces_Latn" => Ok("ces_Latn"),
        "__label__cjk_Latn" => Ok("cjk_Latn"),
        "__label__ckb_Arab" => Ok("ckb_Arab"),
        "__label__crh_Latn" => Ok("crh_Latn"),
        "__label__cym_Latn" => Ok("cym_Latn"),
        "__label__dan_Latn" => Ok("dan_Latn"),
        "__label__deu_Latn" => Ok("deu_Latn"),
        "__label__dik_Latn" => Ok("dik_Latn"),
        "__label__dyu_Latn" => Ok("dyu_Latn"),
        "__label__dzo_Tibt" => Ok("dzo_Tibt"),
        "__label__ell_Grek" => Ok("ell_Grek"),
        "__label__eng_Latn" => Ok("eng_Latn"),
        "__label__epo_Latn" => Ok("epo_Latn"),
        "__label__est_Latn" => Ok("est_Latn"),
        "__label__eus_Latn" => Ok("eus_Latn"),
        "__label__ewe_Latn" => Ok("ewe_Latn"),
        "__label__fao_Latn" => Ok("fao_Latn"),
        "__label__fij_Latn" => Ok("fij_Latn"),
        "__label__fin_Latn" => Ok("fin_Latn"),
        "__label__fon_Latn" => Ok("fon_Latn"),
        "__label__fra_Latn" => Ok("fra_Latn"),
        "__label__fur_Latn" => Ok("fur_Latn"),
        "__label__fuv_Latn" => Ok("fuv_Latn"),
        "__label__gla_Latn" => Ok("gla_Latn"),
        "__label__gle_Latn" => Ok("gle_Latn"),
        "__label__glg_Latn" => Ok("glg_Latn"),
        "__label__grn_Latn" => Ok("grn_Latn"),
        "__label__guj_Gujr" => Ok("guj_Gujr"),
        "__label__hat_Latn" => Ok("hat_Latn"),
        "__label__hau_Latn" => Ok("hau_Latn"),
        "__label__heb_Hebr" => Ok("heb_Hebr"),
        "__label__hin_Deva" => Ok("hin_Deva"),
        "__label__hne_Deva" => Ok("hne_Deva"),
        "__label__hrv_Latn" => Ok("hrv_Latn"),
        "__label__hun_Latn" => Ok("hun_Latn"),
        "__label__hye_Armn" => Ok("hye_Armn"),
        "__label__ibo_Latn" => Ok("ibo_Latn"),
        "__label__ilo_Latn" => Ok("ilo_Latn"),
        "__label__ind_Latn" => Ok("ind_Latn"),
        "__label__isl_Latn" => Ok("isl_Latn"),
        "__label__ita_Latn" => Ok("ita_Latn"),
        "__label__jav_Latn" => Ok("jav_Latn"),
        "__label__jpn_Jpan" => Ok("jpn_Jpan"),
        "__label__kab_Latn" => Ok("kab_Latn"),
        "__label__kac_Latn" => Ok("kac_Latn"),
        "__label__kam_Latn" => Ok("kam_Latn"),
        "__label__kan_Knda" => Ok("kan_Knda"),
        "__label__kas_Arab" => Ok("kas_Arab"),
        "__label__kas_Deva" => Ok("kas_Deva"),
        "__label__kat_Geor" => Ok("kat_Geor"),
        "__label__knc_Arab" => Ok("knc_Arab"),
        "__label__knc_Latn" => Ok("knc_Latn"),
        "__label__kaz_Cyrl" => Ok("kaz_Cyrl"),
        "__label__kbp_Latn" => Ok("kbp_Latn"),
        "__label__kea_Latn" => Ok("kea_Latn"),
        "__label__khm_Khmr" => Ok("khm_Khmr"),
        "__label__kik_Latn" => Ok("kik_Latn"),
        "__label__kin_Latn" => Ok("kin_Latn"),
        "__label__kir_Cyrl" => Ok("kir_Cyrl"),
        "__label__kmb_Latn" => Ok("kmb_Latn"),
        "__label__kmr_Latn" => Ok("kmr_Latn"),
        "__label__kon_Latn" => Ok("kon_Latn"),
        "__label__kor_Hang" => Ok("kor_Hang"),
        "__label__lao_Laoo" => Ok("lao_Laoo"),
        "__label__lij_Latn" => Ok("lij_Latn"),
        "__label__lim_Latn" => Ok("lim_Latn"),
        "__label__lin_Latn" => Ok("lin_Latn"),
        "__label__lit_Latn" => Ok("lit_Latn"),
        "__label__lmo_Latn" => Ok("lmo_Latn"),
        "__label__ltg_Latn" => Ok("ltg_Latn"),
        "__label__ltz_Latn" => Ok("ltz_Latn"),
        "__label__lua_Latn" => Ok("lua_Latn"),
        "__label__lug_Latn" => Ok("lug_Latn"),
        "__label__luo_Latn" => Ok("luo_Latn"),
        "__label__lus_Latn" => Ok("lus_Latn"),
        "__label__lvs_Latn" => Ok("lvs_Latn"),
        "__label__mag_Deva" => Ok("mag_Deva"),
        "__label__mai_Deva" => Ok("mai_Deva"),
        "__label__mal_Mlym" => Ok("mal_Mlym"),
        "__label__mar_Deva" => Ok("mar_Deva"),
        "__label__min_Arab" => Ok("min_Arab"),
        "__label__min_Latn" => Ok("min_Latn"),
        "__label__mkd_Cyrl" => Ok("mkd_Cyrl"),
        "__label__plt_Latn" => Ok("plt_Latn"),
        "__label__mlt_Latn" => Ok("mlt_Latn"),
        "__label__mni_Beng" => Ok("mni_Beng"),
        "__label__khk_Cyrl" => Ok("khk_Cyrl"),
        "__label__mos_Latn" => Ok("mos_Latn"),
        "__label__mri_Latn" => Ok("mri_Latn"),
        "__label__mya_Mymr" => Ok("mya_Mymr"),
        "__label__nld_Latn" => Ok("nld_Latn"),
        "__label__nno_Latn" => Ok("nno_Latn"),
        "__label__nob_Latn" => Ok("nob_Latn"),
        "__label__npi_Deva" => Ok("npi_Deva"),
        "__label__nso_Latn" => Ok("nso_Latn"),
        "__label__nus_Latn" => Ok("nus_Latn"),
        "__label__nya_Latn" => Ok("nya_Latn"),
        "__label__oci_Latn" => Ok("oci_Latn"),
        "__label__gaz_Latn" => Ok("gaz_Latn"),
        "__label__ory_Orya" => Ok("ory_Orya"),
        "__label__pag_Latn" => Ok("pag_Latn"),
        "__label__pan_Guru" => Ok("pan_Guru"),
        "__label__pap_Latn" => Ok("pap_Latn"),
        "__label__pes_Arab" => Ok("pes_Arab"),
        "__label__pol_Latn" => Ok("pol_Latn"),
        "__label__por_Latn" => Ok("por_Latn"),
        "__label__prs_Arab" => Ok("prs_Arab"),
        "__label__pbt_Arab" => Ok("pbt_Arab"),
        "__label__quy_Latn" => Ok("quy_Latn"),
        "__label__ron_Latn" => Ok("ron_Latn"),
        "__label__run_Latn" => Ok("run_Latn"),
        "__label__rus_Cyrl" => Ok("rus_Cyrl"),
        "__label__sag_Latn" => Ok("sag_Latn"),
        "__label__san_Deva" => Ok("san_Deva"),
        "__label__sat_Olck" => Ok("sat_Olck"),
        "__label__scn_Latn" => Ok("scn_Latn"),
        "__label__shn_Mymr" => Ok("shn_Mymr"),
        "__label__sin_Sinh" => Ok("sin_Sinh"),
        "__label__slk_Latn" => Ok("slk_Latn"),
        "__label__slv_Latn" => Ok("slv_Latn"),
        "__label__smo_Latn" => Ok("smo_Latn"),
        "__label__sna_Latn" => Ok("sna_Latn"),
        "__label__snd_Arab" => Ok("snd_Arab"),
        "__label__som_Latn" => Ok("som_Latn"),
        "__label__sot_Latn" => Ok("sot_Latn"),
        "__label__spa_Latn" => Ok("spa_Latn"),
        "__label__als_Latn" => Ok("als_Latn"),
        "__label__srd_Latn" => Ok("srd_Latn"),
        "__label__srp_Cyrl" => Ok("srp_Cyrl"),
        "__label__ssw_Latn" => Ok("ssw_Latn"),
        "__label__sun_Latn" => Ok("sun_Latn"),
        "__label__swe_Latn" => Ok("swe_Latn"),
        "__label__swh_Latn" => Ok("swh_Latn"),
        "__label__szl_Latn" => Ok("szl_Latn"),
        "__label__tam_Taml" => Ok("tam_Taml"),
        "__label__tat_Cyrl" => Ok("tat_Cyrl"),
        "__label__tel_Telu" => Ok("tel_Telu"),
        "__label__tgk_Cyrl" => Ok("tgk_Cyrl"),
        "__label__tgl_Latn" => Ok("tgl_Latn"),
        "__label__tha_Thai" => Ok("tha_Thai"),
        "__label__tir_Ethi" => Ok("tir_Ethi"),
        "__label__taq_Latn" => Ok("taq_Latn"),
        "__label__taq_Tfng" => Ok("taq_Tfng"),
        "__label__tpi_Latn" => Ok("tpi_Latn"),
        "__label__tsn_Latn" => Ok("tsn_Latn"),
        "__label__tso_Latn" => Ok("tso_Latn"),
        "__label__tuk_Latn" => Ok("tuk_Latn"),
        "__label__tum_Latn" => Ok("tum_Latn"),
        "__label__tur_Latn" => Ok("tur_Latn"),
        "__label__twi_Latn" => Ok("twi_Latn"),
        "__label__tzm_Tfng" => Ok("tzm_Tfng"),
        "__label__uig_Arab" => Ok("uig_Arab"),
        "__label__ukr_Cyrl" => Ok("ukr_Cyrl"),
        "__label__umb_Latn" => Ok("umb_Latn"),
        "__label__urd_Arab" => Ok("urd_Arab"),
        "__label__uzn_Latn" => Ok("uzn_Latn"),
        "__label__vec_Latn" => Ok("vec_Latn"),
        "__label__vie_Latn" => Ok("vie_Latn"),
        "__label__war_Latn" => Ok("war_Latn"),
        "__label__wol_Latn" => Ok("wol_Latn"),
        "__label__xho_Latn" => Ok("xho_Latn"),
        "__label__ydd_Hebr" => Ok("ydd_Hebr"),
        "__label__yor_Latn" => Ok("yor_Latn"),
        "__label__yue_Hant" => Ok("yue_Hant"),
        "__label__zho_Hans" => Ok("zho_Hans"),
        "__label__zho_Hant" => Ok("zho_Hant"),
        "__label__zsm_Latn" => Ok("zsm_Latn"),
        "__label__zul_Latn" => Ok("zul_Latn"),
        _ => Err(python_error(format!("Unknown language code: {}", language))),
    }
}

fn is_redundant_label(label: &str) -> bool {
    matches!(
        label,
        "__label__ton_Latn"
            | "__label__oss_Cyrl"
            | "__label__che_Cyrl"
            | "__label__ady_Cyrl"
            | "__label__tah_Latn"
            | "__label__diq_Latn"
            | "__label__nia_Latn"
            | "__label__nav_Latn"
            | "__label__abk_Cyrl"
            | "__label__bxr_Cyrl"
            | "__label__wes_Latn"
            | "__label__gom_Deva"
            | "__label__udm_Cyrl"
            | "__label__roh_Latn"
            | "__label__alt_Cyrl"
            | "__label__arn_Latn"
            | "__label__ewo_Latn"
            | "__label__xmf_Geor"
            | "__label__pcm_Latn"
            | "__label__bis_Latn"
            | "__label__krc_Cyrl"
            | "__label__chv_Cyrl"
            | "__label__kal_Latn"
    )
}

#[allow(dead_code)]
#[cfg_attr(not(any(Py_3_8, Py_3_9)), pyclass(frozen, get_all, immutable_type))]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass(frozen, get_all))]
struct Prediction {
    confidence: f64,
    language: &'static str,
}

#[cfg_attr(
    not(any(Py_3_8, Py_3_9)),
    pyclass(name = "LanguageDetector", frozen, immutable_type)
)]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass(name = "LanguageDetector", frozen))]
struct Detector {
    lingua_languages: [&'static str; 74],
    fasttext_model: Py<PyAny>,
    lingua_model: LanguageDetector,
    fasttext_k: u8,
}

#[pymethods]
impl Detector {
    #[new]
    fn new(fasttext_model: Py<PyAny>) -> PyResult<Self> {
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
            fasttext_model,
            lingua_model: LanguageDetectorBuilder::from_all_languages().build(),
            fasttext_k: 24,
            lingua_languages,
        };

        Ok(detector)
    }

    #[pyo3(signature = (text, *, fasttext_confidence_threshold, lingua_confidence_threshold))]
    fn detect<'a>(
        &self,
        py: Python<'a>,
        text: &str,
        fasttext_confidence_threshold: f64,
        lingua_confidence_threshold: f64,
    ) -> PyResult<Prediction> {
        let fasttext_arguments = (text, self.fasttext_k, 0.0, intern!(py, "strict"));
        let mut predictions = self
            .fasttext_model
            .call_method1(py, intern!(py, "predict"), fasttext_arguments)?
            .downcast_bound::<PyList>(py)?
            .iter();

        let prediction =
            predictions.find(|item| match item.extract::<(f64, Bound<'a, PyString>)>() {
                Ok((_, label)) => !is_redundant_label(label.to_str().unwrap_or("")),
                _ => true,
            });

        let (fasttext_confidence, fasttext_language) = prediction
            .ok_or_else(|| python_error("No prediction found!"))?
            .extract::<(f64, Bound<'a, PyString>)>()?;

        let fasttext_prediction = Prediction {
            confidence: fasttext_confidence,
            language: map_language(fasttext_language.to_str()?)?,
        };

        if fasttext_confidence >= fasttext_confidence_threshold {
            return Ok(fasttext_prediction);
        }

        let lingua_confidence_values = self.lingua_model.compute_language_confidence_values(text);
        let (lingua_language, lingua_confidence) = lingua_confidence_values
            .first()
            .ok_or_else(|| python_error("Failed to compute language confidence values!"))?;

        if *lingua_confidence <= lingua_confidence_threshold {
            return Ok(fasttext_prediction);
        }

        let lingua_prediction = Prediction {
            confidence: *lingua_confidence,
            language: self.lingua_languages[*lingua_language as usize],
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
