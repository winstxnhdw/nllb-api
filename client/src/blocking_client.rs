use crate::structs::LanguageQuery;
use crate::structs::LanguageResponse;
use crate::structs::LoadQuery;
use crate::structs::TokenQuery;
use crate::structs::TokenResponse;
use crate::structs::TranslateQuery;
use crate::structs::TranslateResponse;
use crate::structs::UnloadQuery;

use reqwest::Error;
use reqwest::Proxy;
use reqwest::blocking::Client;
use reqwest::header;
use std::env;

pub struct TranslatorBlockingClient {
    client: Client,
    base_url: String,
}

impl TranslatorBlockingClient {
    pub fn new(
        base_url: &str,
        auth_token: Option<&str>,
        http_proxy: Option<&str>,
        https_proxy: Option<&str>,
        no_proxy: Option<&str>,
    ) -> Result<Self, Error> {
        let mut headers = header::HeaderMap::new();

        let auth_token_header = auth_token.and_then(|token| {
            let mut header = header::HeaderValue::try_from(token).ok()?;
            header.set_sensitive(true);
            Some(header)
        });

        if let Some(header) = auth_token_header {
            headers.insert(header::AUTHORIZATION, header);
        }

        let mut client_builder = Client::builder().default_headers(headers).http2_adaptive_window(true);

        let no_proxy_maybe = no_proxy
            .or(env::var("NO_PROXY").ok().as_deref())
            .or(env::var("no_proxy").ok().as_deref())
            .and_then(reqwest::NoProxy::from_string);

        let http_proxy_maybe = http_proxy
            .or(env::var("HTTP_PROXY").ok().as_deref())
            .or(env::var("http_proxy").ok().as_deref())
            .and_then(|proxy| Proxy::http(proxy).ok());

        let https_proxy_maybe = https_proxy
            .or(env::var("HTTPS_PROXY").ok().as_deref())
            .or(env::var("https_proxy").ok().as_deref())
            .and_then(|proxy| Proxy::http(proxy).ok());

        if let Some(proxy) = http_proxy_maybe {
            client_builder = client_builder.proxy(proxy.no_proxy(no_proxy_maybe.clone()));
        }

        if let Some(proxy) = https_proxy_maybe {
            client_builder = client_builder.proxy(proxy.no_proxy(no_proxy_maybe));
        }

        let client = client_builder.build()?;
        let translator_client = Self {
            client,
            base_url: base_url.to_string(),
        };

        Ok(translator_client)
    }

    pub fn load_model(&self, keep_cache: bool) -> Result<bool, Error> {
        let success = self
            .client
            .put(format!("{}/v4/translator", self.base_url))
            .query(&LoadQuery { keep_cache })
            .send()?
            .status()
            .is_success();

        Ok(success)
    }

    pub fn unload_model(&self, to_cpu: bool) -> Result<bool, Error> {
        let success = self
            .client
            .delete(format!("{}/v4/translator", self.base_url))
            .query(&UnloadQuery { to_cpu })
            .send()?
            .status()
            .is_success();

        Ok(success)
    }

    pub fn detect_language(
        &self,
        text: &str,
        fast_model_confidence_threshold: Option<f32>,
        accurate_model_confidence_threshold: Option<f32>,
    ) -> Result<LanguageResponse, Error> {
        let query = LanguageQuery {
            text,
            fast_model_confidence_threshold,
            accurate_model_confidence_threshold,
        };

        self.client
            .get(format!("{}/v4/language", self.base_url))
            .query(&query)
            .send()?
            .json::<LanguageResponse>()
    }

    pub fn translate(&self, text: &str, source: &str, target: &str) -> Result<String, Error> {
        let translation = self
            .client
            .get(format!("{}/v4/translator", self.base_url))
            .query(&TranslateQuery { text, source, target })
            .send()?
            .json::<TranslateResponse>()?
            .result;

        Ok(translation)
    }

    pub fn count_tokens(&self, text: &str) -> Result<u32, Error> {
        let tokens = self
            .client
            .get(format!("{}/v4/translator/tokens", self.base_url))
            .query(&TokenQuery { text })
            .send()?
            .json::<TokenResponse>()?
            .length;

        Ok(tokens)
    }
}
