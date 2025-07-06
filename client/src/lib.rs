mod blocking_client;
mod client;
mod structs;

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
use std::sync::Arc;

use crate::blocking_client::TranslatorBlockingClient;
use crate::client::TranslatorClient;
use crate::structs::LanguageResponse;

fn python_error<E: std::fmt::Display>(error: E) -> pyo3::PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(error.to_string())
}

#[cfg_attr(
    not(any(Py_3_8, Py_3_9)),
    pyclass(name = "TranslatorClient", frozen, immutable_type)
)]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass(name = "TranslatorClient", frozen))]
struct PyTranslatorClient {
    client: TranslatorBlockingClient,
}

#[pymethods]
impl PyTranslatorClient {
    #[new]
    #[pyo3(signature = (base_url = "https://winstxnhdw-nllb-api.hf.space", *, auth_token = None, http_proxy = None, https_proxy = None, no_proxy = None))]
    fn new(
        base_url: &str,
        auth_token: Option<&str>,
        http_proxy: Option<&str>,
        https_proxy: Option<&str>,
        no_proxy: Option<&str>,
    ) -> PyResult<Self> {
        let blocking_client =
            TranslatorBlockingClient::new(base_url, auth_token, http_proxy, https_proxy, no_proxy)
                .map_err(python_error)?;

        let client = Self {
            client: blocking_client,
        };

        Ok(client)
    }

    #[pyo3(signature = (*, keep_cache = false))]
    fn load_model(&self, keep_cache: bool) -> PyResult<bool> {
        let success = self.client.load_model(keep_cache).map_err(python_error)?;
        Ok(success)
    }

    #[pyo3(signature = (*, to_cpu = false))]
    fn unload_model(&self, to_cpu: bool) -> PyResult<bool> {
        let success = self.client.unload_model(to_cpu).map_err(python_error)?;
        Ok(success)
    }

    fn detect_language(&self, text: &str) -> PyResult<LanguageResponse> {
        let language = self.client.detect_language(text).map_err(python_error)?;
        Ok(language)
    }

    #[pyo3(signature = (text, *, source, target))]
    fn translate(&self, text: &str, source: &str, target: &str) -> PyResult<String> {
        let response = self
            .client
            .translate(text, source, target)
            .map_err(python_error)?;

        Ok(response)
    }

    fn count_tokens(&self, text: &str) -> PyResult<u32> {
        let tokens = self.client.count_tokens(text).map_err(python_error)?;
        Ok(tokens)
    }
}

#[cfg_attr(
    not(any(Py_3_8, Py_3_9)),
    pyclass(name = "AsyncTranslatorClient", frozen, immutable_type)
)]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass(name = "AsyncTranslatorClient", frozen))]
struct AsyncPyTranslatorClient {
    client: Arc<TranslatorClient>,
}

#[pymethods]
impl AsyncPyTranslatorClient {
    #[new]
    #[pyo3(signature = (base_url = "https://winstxnhdw-nllb-api.hf.space", *, auth_token = None, http_proxy = None, https_proxy = None, no_proxy = None))]
    fn new(
        base_url: &str,
        auth_token: Option<&str>,
        http_proxy: Option<&str>,
        https_proxy: Option<&str>,
        no_proxy: Option<&str>,
    ) -> PyResult<Self> {
        let translator_client =
            TranslatorClient::new(base_url, auth_token, http_proxy, https_proxy, no_proxy)
                .map_err(python_error)?;

        let client = Self {
            client: Arc::new(translator_client),
        };

        Ok(client)
    }

    #[pyo3(signature = (*, keep_cache = false))]
    fn load_model<'a>(&self, py: Python<'a>, keep_cache: bool) -> PyResult<Bound<'a, PyAny>> {
        let client = self.client.clone();

        future_into_py(py, async move {
            let success = client.load_model(keep_cache).await.map_err(python_error)?;
            Ok(success)
        })
    }

    #[pyo3(signature = (*, to_cpu = false))]
    fn unload_model<'a>(&self, py: Python<'a>, to_cpu: bool) -> PyResult<Bound<'a, PyAny>> {
        let client = self.client.clone();

        future_into_py(py, async move {
            let success = client.unload_model(to_cpu).await.map_err(python_error)?;
            Ok(success)
        })
    }

    fn detect_language<'a>(
        &self,
        py: Python<'a>,
        text: Py<PyString>,
    ) -> PyResult<Bound<'a, PyAny>> {
        let client = self.client.clone();

        future_into_py(py, async move {
            let text_str = Python::with_gil(|py| text.to_str(py))?;
            let language = client
                .detect_language(text_str)
                .await
                .map_err(python_error)?;

            Ok(language)
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

        future_into_py(py, async move {
            let (text_str, source_str, target_str) = Python::with_gil(|py| -> PyResult<_> {
                let text = text.to_str(py)?;
                let source = source.to_str(py)?;
                let target = target.to_str(py)?;

                Ok((text, source, target))
            })?;

            let response = client
                .translate(text_str, source_str, target_str)
                .await
                .map_err(python_error)?;

            Ok(response)
        })
    }

    fn count_tokens<'a>(&self, py: Python<'a>, text: Py<PyString>) -> PyResult<Bound<'a, PyAny>> {
        let client = self.client.clone();

        future_into_py(py, async move {
            let text_str = Python::with_gil(|py| text.to_str(py))?;
            let tokens = client.count_tokens(text_str).await.map_err(python_error)?;
            Ok(tokens)
        })
    }
}

#[pyo3::prelude::pymodule()]
fn nllb(m: &Bound<'_, pyo3::prelude::PyModule>) -> PyResult<()> {
    m.add_class::<AsyncPyTranslatorClient>()?;
    m.add_class::<PyTranslatorClient>()?;
    m.add_class::<LanguageResponse>()?;
    Ok(())
}
