use pyo3::prelude::pyclass;
use pyo3::prelude::pymethods;
use pyo3::prelude::Bound;
use pyo3::prelude::Py;
use pyo3::prelude::PyAny;
use pyo3::prelude::PyResult;
use pyo3::prelude::Python;
use pyo3::types::PyModuleMethods;
use pyo3::types::PyString;
use pyo3_async_runtimes::tokio::future_into_py;
use reqwest::header;
use reqwest::Client;
use reqwest::Proxy;
use serde::Deserialize;
use serde::Serialize;
use std::env;
use std::sync::Arc;

#[cfg_attr(not(any(Py_3_8, Py_3_9)), pyclass(frozen, immutable_type))]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass(frozen))]
struct TranslatorClient {
    client: Arc<Client>,
    base_url: Arc<String>,
}

#[cfg_attr(not(any(Py_3_8, Py_3_9)), pyclass(frozen, get_all, immutable_type))]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass(frozen, get_all))]
#[allow(dead_code)]
#[derive(Deserialize)]
struct Language {
    language: String,
    confidence: f64,
}

#[derive(Serialize)]
struct LanguageQuery<'a> {
    text: &'a str,
}

#[derive(Deserialize)]
struct TranslateResponse {
    result: String,
}

#[derive(Serialize)]
struct TranslateQuery<'a> {
    text: &'a str,
    source: &'a str,
    target: &'a str,
}

#[derive(Deserialize)]
struct TokenResponse {
    length: u32,
}

#[derive(Serialize)]
struct TokenRequest<'a> {
    text: &'a str,
}

#[derive(Serialize)]
struct LoadQuery {
    keep_cache: bool,
}

#[derive(Serialize)]
struct UnloadQuery {
    to_cpu: bool,
}

fn python_error<E: std::fmt::Display>(error: E) -> pyo3::PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(error.to_string())
}

trait WithGIL: Sized {
    fn with_gil<F>(f: F) -> PyResult<Self>
    where
        F: for<'py> FnOnce(Python<'py>) -> PyResult<Self>;
}

impl<T> WithGIL for T {
    fn with_gil<F>(f: F) -> PyResult<Self>
    where
        F: for<'py> FnOnce(Python<'py>) -> PyResult<Self>,
    {
        Python::with_gil(f)
    }
}

#[pymethods]
impl TranslatorClient {
    #[new]
    #[pyo3(signature = (base_url = "https://winstxnhdw-nllb-api.hf.space", *, auth_token = None, http_proxy = None, https_proxy = None, no_proxy = None))]
    fn new(
        base_url: &str,
        auth_token: Option<&str>,
        http_proxy: Option<&str>,
        https_proxy: Option<&str>,
        no_proxy: Option<&str>,
    ) -> PyResult<Self> {
        let mut headers = header::HeaderMap::new();

        let auth_token_header = auth_token.and_then(|token| {
            let mut header = header::HeaderValue::try_from(token).ok()?;
            header.set_sensitive(true);
            Some(header)
        });

        if let Some(header) = auth_token_header {
            headers.insert(header::AUTHORIZATION, header);
        }

        let mut client_builder = Client::builder()
            .default_headers(headers)
            .http2_adaptive_window(true);

        let no_proxy_maybe = no_proxy
            .or(env::var("NO_PROXY").ok().as_deref())
            .and_then(reqwest::NoProxy::from_string);

        let http_proxy_maybe = http_proxy
            .or(env::var("HTTP_PROXY").ok().as_deref())
            .and_then(|proxy| Proxy::http(proxy).ok());

        let https_proxy_maybe = https_proxy
            .or(env::var("HTTPS_PROXY").ok().as_deref())
            .and_then(|proxy| Proxy::http(proxy).ok());

        if let Some(proxy) = http_proxy_maybe {
            client_builder = client_builder.proxy(proxy.no_proxy(no_proxy_maybe.clone()));
        }

        if let Some(proxy) = https_proxy_maybe {
            client_builder = client_builder.proxy(proxy.no_proxy(no_proxy_maybe));
        }

        let client = client_builder.build().map_err(python_error)?;
        let translator_client = Self {
            client: Arc::new(client),
            base_url: Arc::new(format!("{}/api", base_url)),
        };

        Ok(translator_client)
    }

    fn detect_language<'a>(
        &self,
        py: Python<'a>,
        text: Py<PyString>,
    ) -> PyResult<Bound<'a, PyAny>> {
        let client = self.client.clone();
        let base_url = self.base_url.clone();

        future_into_py(py, async move {
            let url = format!("{}/v4/language", base_url);
            let query = LanguageQuery::with_gil(|py| {
                let query = LanguageQuery {
                    text: text.to_str(py)?,
                };

                Ok(query)
            })?;

            let response = client
                .get(url)
                .query(&query)
                .send()
                .await
                .map_err(python_error)?
                .json::<Language>()
                .await
                .map_err(python_error)?;

            Ok(response)
        })
    }

    #[pyo3(signature = (*, keep_cache = false))]
    fn load_model<'a>(&self, py: Python<'a>, keep_cache: bool) -> PyResult<Bound<'a, PyAny>> {
        let client = self.client.clone();
        let base_url = self.base_url.clone();

        future_into_py(py, async move {
            let url = format!("{}/v4/translator", base_url);
            let request = LoadQuery { keep_cache };
            let success = client
                .put(url)
                .query(&request)
                .send()
                .await
                .map_err(python_error)?
                .status()
                .is_success();

            Ok(success)
        })
    }

    #[pyo3(signature = (*, to_cpu = false))]
    fn unload_model<'a>(&self, py: Python<'a>, to_cpu: bool) -> PyResult<Bound<'a, PyAny>> {
        let client = self.client.clone();
        let base_url = self.base_url.clone();

        future_into_py(py, async move {
            let url = format!("{}/v4/translator", base_url);
            let request = UnloadQuery { to_cpu };
            let success = client
                .delete(url)
                .query(&request)
                .send()
                .await
                .map_err(python_error)?
                .status()
                .is_success();

            Ok(success)
        })
    }

    #[pyo3(signature = (text, *, source, target))]
    fn translate<'a>(
        &self,
        py: Python<'a>,
        text: Py<PyString>,
        source: Py<PyString>,
        target: Py<PyString>,
    ) -> PyResult<Bound<'a, PyAny>> {
        let client = self.client.clone();
        let base_url = self.base_url.clone();

        future_into_py(py, async move {
            let url = format!("{}/v4/translator", base_url);
            let request = TranslateQuery::with_gil(|py| {
                let request = TranslateQuery {
                    text: text.to_str(py)?,
                    source: source.to_str(py)?,
                    target: target.to_str(py)?,
                };

                Ok(request)
            })?;

            let response = client
                .get(url)
                .query(&request)
                .send()
                .await
                .map_err(python_error)?
                .json::<TranslateResponse>()
                .await
                .map_err(python_error)?
                .result;

            Ok(response)
        })
    }

    fn count_tokens<'a>(&self, py: Python<'a>, text: Py<PyString>) -> PyResult<Bound<'a, PyAny>> {
        let client = self.client.clone();
        let base_url = self.base_url.clone();

        future_into_py(py, async move {
            let url = format!("{}/v4/translator/tokens", base_url);
            let request = TokenRequest::with_gil(|py| {
                let request = TokenRequest {
                    text: text.to_str(py)?,
                };

                Ok(request)
            })?;

            let response = client
                .post(url)
                .json(&request)
                .send()
                .await
                .map_err(python_error)?
                .json::<TokenResponse>()
                .await
                .map_err(python_error)?
                .length;

            Ok(response)
        })
    }
}

#[pyo3::prelude::pymodule(name = "nllb")]
fn nllb(m: &Bound<'_, pyo3::prelude::PyModule>) -> PyResult<()> {
    m.add_class::<TranslatorClient>()?;
    m.add_class::<Language>()?;
    Ok(())
}
