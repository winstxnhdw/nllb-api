mod blocking_client;
mod client;
mod structs;

use pyo3::prelude::PyResult;
use pyo3::prelude::pyclass;
use pyo3::prelude::pymethods;

use crate::blocking_client::TranslatorBlockingClient;
use crate::client::TranslatorClient;
use crate::structs::LanguageResponse;

pyo3::create_exception!(nllb, ClientError, pyo3::exceptions::PyRuntimeError);
pyo3::create_exception!(nllb, ApiError, pyo3::exceptions::PyRuntimeError);

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
        let client =
            TranslatorBlockingClient::new(base_url, auth_token, http_proxy, https_proxy, no_proxy)
                .map_err(|e| ClientError::new_err(e.to_string()))?;

        Ok(Self { client })
    }

    #[pyo3(signature = (*, keep_cache = false))]
    fn load_model(&self, keep_cache: bool) -> PyResult<bool> {
        self.client
            .load_model(keep_cache)
            .map_err(|e| ApiError::new_err(e.to_string()))
    }

    #[pyo3(signature = (*, to_cpu = false))]
    fn unload_model(&self, to_cpu: bool) -> PyResult<bool> {
        self.client
            .unload_model(to_cpu)
            .map_err(|e| ApiError::new_err(e.to_string()))
    }

    fn detect_language(&self, text: &str) -> PyResult<LanguageResponse> {
        self.client
            .detect_language(text)
            .map_err(|e| ApiError::new_err(e.to_string()))
    }

    #[pyo3(signature = (text, *, source, target))]
    fn translate(&self, text: &str, source: &str, target: &str) -> PyResult<String> {
        self.client
            .translate(text, source, target)
            .map_err(|e| ApiError::new_err(e.to_string()))
    }

    fn count_tokens(&self, text: &str) -> PyResult<u32> {
        self.client
            .count_tokens(text)
            .map_err(|e| ApiError::new_err(e.to_string()))
    }
}

#[cfg_attr(
    not(any(Py_3_8, Py_3_9)),
    pyclass(name = "AsyncTranslatorClient", frozen, immutable_type)
)]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass(name = "AsyncTranslatorClient", frozen))]
struct AsyncPyTranslatorClient {
    client: TranslatorClient,
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
        let client = TranslatorClient::new(base_url, auth_token, http_proxy, https_proxy, no_proxy)
            .map_err(|e| ClientError::new_err(e.to_string()))?;

        Ok(Self { client })
    }

    #[pyo3(signature = (*, keep_cache = false))]
    async fn load_model(&self, keep_cache: bool) -> PyResult<bool> {
        self.client
            .load_model(keep_cache)
            .await
            .map_err(|e| ApiError::new_err(e.to_string()))
    }

    #[pyo3(signature = (*, to_cpu = false))]
    async fn unload_model(&self, to_cpu: bool) -> PyResult<bool> {
        self.client
            .unload_model(to_cpu)
            .await
            .map_err(|e| ApiError::new_err(e.to_string()))
    }

    async fn detect_language(&self, text: String) -> PyResult<LanguageResponse> {
        self.client
            .detect_language(&text)
            .await
            .map_err(|e| ApiError::new_err(e.to_string()))
    }

    #[pyo3(signature = (text, *, source, target))]
    async fn translate(&self, text: String, source: String, target: String) -> PyResult<String> {
        self.client
            .translate(&text, &source, &target)
            .await
            .map_err(|e| ApiError::new_err(e.to_string()))
    }

    async fn count_tokens(&self, text: String) -> PyResult<u32> {
        self.client
            .count_tokens(&text)
            .await
            .map_err(|e| ApiError::new_err(e.to_string()))
    }
}

#[pyo3::prelude::pymodule(gil_used = false)]
mod nllb {
    #[pymodule_export]
    use super::ApiError;
    #[pymodule_export]
    use super::AsyncPyTranslatorClient;
    #[pymodule_export]
    use super::ClientError;
    #[pymodule_export]
    use super::LanguageResponse;
    #[pymodule_export]
    use super::PyTranslatorClient;
}
