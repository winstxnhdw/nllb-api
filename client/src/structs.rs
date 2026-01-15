use pyo3::prelude::pyclass;
use serde::Deserialize;
use serde::Serialize;

#[cfg_attr(
    not(any(Py_3_8, Py_3_9)),
    pyclass(name = "LanguagePrediction", frozen, get_all, immutable_type)
)]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass(name = "LanguagePrediction", frozen, get_all))]
#[derive(Deserialize)]
pub struct LanguageResponse {
    language: String,
    confidence: f64,
}

#[derive(Serialize)]
pub struct LanguageQuery<'a> {
    pub text: &'a str,
    pub fast_model_confidence_threshold: Option<f32>,
    pub accurate_model_confidence_threshold: Option<f32>,
}

#[derive(Deserialize)]
pub struct TranslateResponse {
    pub result: String,
}

#[derive(Serialize)]
pub struct TranslateQuery<'a> {
    pub text: &'a str,
    pub source: &'a str,
    pub target: &'a str,
}

#[derive(Deserialize)]
pub struct TokenResponse {
    pub length: u32,
}

#[derive(Serialize)]
pub struct TokenQuery<'a> {
    pub text: &'a str,
}

#[derive(Serialize)]
pub struct LoadQuery {
    pub keep_cache: bool,
}

#[derive(Serialize)]
pub struct UnloadQuery {
    pub to_cpu: bool,
}
