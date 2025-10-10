# nllb-api

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![python](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13%20|%203.14-blue)](https://www.python.org/)

[![API](https://img.shields.io/endpoint?url=https%3A%2F%2Fwinstxnhdw-nllb-api.hf.space%2Fapi%2Fhealth&logo=huggingface&labelColor=%230B0F19&color=brightgreen)](https://huggingface.co/spaces/winstxnhdw/nllb-api)
[![main.yml](https://github.com/winstxnhdw/nllb-api/actions/workflows/main.yml/badge.svg)](https://github.com/winstxnhdw/nllb-api/actions/workflows/main.yml)
[![cuda.yml](https://github.com/winstxnhdw/nllb-api/actions/workflows/cuda.yml/badge.svg)](https://github.com/winstxnhdw/nllb-api/actions/workflows/cuda.yml)
[![clippy.yml](https://github.com/winstxnhdw/nllb-api/actions/workflows/clippy.yml/badge.svg)](https://github.com/winstxnhdw/nllb-api/actions/workflows/clippy.yml)
[![client.yml](https://github.com/winstxnhdw/nllb-api/actions/workflows/client.yml/badge.svg)](https://github.com/winstxnhdw/nllb-api/actions/workflows/client.yml)
[![formatter.yml](https://github.com/winstxnhdw/nllb-api/actions/workflows/formatter.yml/badge.svg)](https://github.com/winstxnhdw/nllb-api/actions/workflows/formatter.yml)

A fast CPU-based API for Meta's [No Language Left Behind](https://huggingface.co/docs/transformers/model_doc/nllb) distilled 1.3B 8-bit quantised variant, hosted on Hugging Face Spaces. To achieve faster executions, we are using [CTranslate2](https://github.com/OpenNMT/CTranslate2) as our inference engine.

> [!IMPORTANT]\
> NLLB was trained with input lengths not exceeding 512 tokens. Translating longer sequences might result in quality degradation. Consider splitting your input into smaller chunks if you begin observing artefacts.

## Usage

Simply cURL the endpoint like in the following. The `source` and `target` languages must be specified using FLORES-200 codes.

<details>

<summary> List of FLORES-200 Codes </summary>

<br>

Language                           | FLORES-200 Code
-----------------------------------|----------------
Acehnese (Arabic script)           | ace_Arab
Acehnese (Latin script)            | ace_Latn
Mesopotamian Arabic                | acm_Arab
Ta’izzi-Adeni Arabic               | acq_Arab
Tunisian Arabic                    | aeb_Arab
Afrikaans                          | afr_Latn
South Levantine Arabic             | ajp_Arab
Akan                               | aka_Latn
Amharic                            | amh_Ethi
North Levantine Arabic             | apc_Arab
Modern Standard Arabic             | arb_Arab
Modern Standard Arabic (Romanized) | arb_Latn
Najdi Arabic                       | ars_Arab
Moroccan Arabic                    | ary_Arab
Egyptian Arabic                    | arz_Arab
Assamese                           | asm_Beng
Asturian                           | ast_Latn
Awadhi                             | awa_Deva
Central Aymara                     | ayr_Latn
South Azerbaijani                  | azb_Arab
North Azerbaijani                  | azj_Latn
Bashkir                            | bak_Cyrl
Bambara                            | bam_Latn
Balinese                           | ban_Latn
Belarusian                         | bel_Cyrl
Bemba                              | bem_Latn
Bengali                            | ben_Beng
Bhojpuri                           | bho_Deva
Banjar (Arabic script)             | bjn_Arab
Banjar (Latin script)              | bjn_Latn
Standard Tibetan                   | bod_Tibt
Bosnian                            | bos_Latn
Buginese                           | bug_Latn
Bulgarian                          | bul_Cyrl
Catalan                            | cat_Latn
Cebuano                            | ceb_Latn
Czech                              | ces_Latn
Chokwe                             | cjk_Latn
Central Kurdish                    | ckb_Arab
Crimean Tatar                      | crh_Latn
Welsh                              | cym_Latn
Danish                             | dan_Latn
German                             | deu_Latn
Southwestern Dinka                 | dik_Latn
Dyula                              | dyu_Latn
Dzongkha                           | dzo_Tibt
Greek                              | ell_Grek
English                            | eng_Latn
Esperanto                          | epo_Latn
Estonian                           | est_Latn
Basque                             | eus_Latn
Ewe                                | ewe_Latn
Faroese                            | fao_Latn
Fijian                             | fij_Latn
Finnish                            | fin_Latn
Fon                                | fon_Latn
French                             | fra_Latn
Friulian                           | fur_Latn
Nigerian Fulfulde                  | fuv_Latn
Scottish Gaelic                    | gla_Latn
Irish                              | gle_Latn
Galician                           | glg_Latn
Guarani                            | grn_Latn
Gujarati                           | guj_Gujr
Haitian Creole                     | hat_Latn
Hausa                              | hau_Latn
Hebrew                             | heb_Hebr
Hindi                              | hin_Deva
Chhattisgarhi                      | hne_Deva
Croatian                           | hrv_Latn
Hungarian                          | hun_Latn
Armenian                           | hye_Armn
Igbo                               | ibo_Latn
Ilocano                            | ilo_Latn
Indonesian                         | ind_Latn
Icelandic                          | isl_Latn
Italian                            | ita_Latn
Javanese                           | jav_Latn
Japanese                           | jpn_Jpan
Kabyle                             | kab_Latn
Jingpho                            | kac_Latn
Kamba                              | kam_Latn
Kannada                            | kan_Knda
Kashmiri (Arabic script)           | kas_Arab
Kashmiri (Devanagari script)       | kas_Deva
Georgian                           | kat_Geor
Central Kanuri (Arabic script)     | knc_Arab
Central Kanuri (Latin script)      | knc_Latn
Kazakh                             | kaz_Cyrl
Kabiyè                             | kbp_Latn
Kabuverdianu                       | kea_Latn
Khmer                              | khm_Khmr
Kikuyu                             | kik_Latn
Kinyarwanda                        | kin_Latn
Kyrgyz                             | kir_Cyrl
Kimbundu                           | kmb_Latn
Northern Kurdish                   | kmr_Latn
Kikongo                            | kon_Latn
Korean                             | kor_Hang
Lao                                | lao_Laoo
Ligurian                           | lij_Latn
Limburgish                         | lim_Latn
Lingala                            | lin_Latn
Lithuanian                         | lit_Latn
Lombard                            | lmo_Latn
Latgalian                          | ltg_Latn
Luxembourgish                      | ltz_Latn
Luba-Kasai                         | lua_Latn
Ganda                              | lug_Latn
Luo                                | luo_Latn
Mizo                               | lus_Latn
Standard Latvian                   | lvs_Latn
Magahi                             | mag_Deva
Maithili                           | mai_Deva
Malayalam                          | mal_Mlym
Marathi                            | mar_Deva
Minangkabau (Arabic script)        | min_Arab
Minangkabau (Latin script)         | min_Latn
Macedonian                         | mkd_Cyrl
Plateau Malagasy                   | plt_Latn
Maltese                            | mlt_Latn
Meitei (Bengali script)            | mni_Beng
Halh Mongolian                     | khk_Cyrl
Mossi                              | mos_Latn
Maori                              | mri_Latn
Burmese                            | mya_Mymr
Dutch                              | nld_Latn
Norwegian Nynorsk                  | nno_Latn
Norwegian Bokmål                   | nob_Latn
Nepali                             | npi_Deva
Northern Sotho                     | nso_Latn
Nuer                               | nus_Latn
Nyanja                             | nya_Latn
Occitan                            | oci_Latn
West Central Oromo                 | gaz_Latn
Odia                               | ory_Orya
Pangasinan                         | pag_Latn
Eastern Panjabi                    | pan_Guru
Papiamento                         | pap_Latn
Western Persian                    | pes_Arab
Polish                             | pol_Latn
Portuguese                         | por_Latn
Dari                               | prs_Arab
Southern Pashto                    | pbt_Arab
Ayacucho Quechua                   | quy_Latn
Romanian                           | ron_Latn
Rundi                              | run_Latn
Russian                            | rus_Cyrl
Sango                              | sag_Latn
Sanskrit                           | san_Deva
Santali                            | sat_Olck
Sicilian                           | scn_Latn
Shan                               | shn_Mymr
Sinhala                            | sin_Sinh
Slovak                             | slk_Latn
Slovenian                          | slv_Latn
Samoan                             | smo_Latn
Shona                              | sna_Latn
Sindhi                             | snd_Arab
Somali                             | som_Latn
Southern Sotho                     | sot_Latn
Spanish                            | spa_Latn
Tosk Albanian                      | als_Latn
Sardinian                          | srd_Latn
Serbian                            | srp_Cyrl
Swati                              | ssw_Latn
Sundanese                          | sun_Latn
Swedish                            | swe_Latn
Swahili                            | swh_Latn
Silesian                           | szl_Latn
Tamil                              | tam_Taml
Tatar                              | tat_Cyrl
Telugu                             | tel_Telu
Tajik                              | tgk_Cyrl
Tagalog                            | tgl_Latn
Thai                               | tha_Thai
Tigrinya                           | tir_Ethi
Tamasheq (Latin script)            | taq_Latn
Tamasheq (Tifinagh script)         | taq_Tfng
Tok Pisin                          | tpi_Latn
Tswana                             | tsn_Latn
Tsonga                             | tso_Latn
Turkmen                            | tuk_Latn
Tumbuka                            | tum_Latn
Turkish                            | tur_Latn
Twi                                | twi_Latn
Central Atlas Tamazight            | tzm_Tfng
Uyghur                             | uig_Arab
Ukrainian                          | ukr_Cyrl
Umbundu                            | umb_Latn
Urdu                               | urd_Arab
Northern Uzbek                     | uzn_Latn
Venetian                           | vec_Latn
Vietnamese                         | vie_Latn
Waray                              | war_Latn
Wolof                              | wol_Latn
Xhosa                              | xho_Latn
Eastern Yiddish                    | ydd_Hebr
Yoruba                             | yor_Latn
Yue Chinese                        | yue_Hant
Chinese (Simplified)               | zho_Hans
Chinese (Traditional)              | zho_Hant
Standard Malay                     | zsm_Latn
Zulu                               | zul_Latn

</details>

### cURL

```bash
curl 'https://winstxnhdw-nllb-api.hf.space/api/v4/translator?text=Hello&source=eng_Latn&target=spa_Latn'
```

To stream translations as Server-Sent Events, you may query the `/translator/stream` endpoint instead.

```bash
curl -N 'https://winstxnhdw-nllb-api.hf.space/api/v4/translator/stream?text=Hello&source=eng_Latn&target=spa_Latn'
```

You can also determine the source language by querying the following API.

```bash
curl 'https://winstxnhdw-nllb-api.hf.space/api/v4/language?text=Hello'
```

### Python

Install the `nllb` Rust client library.

```bash
pip install "nllb @ git+https://git@github.com/winstxnhdw/nllb-api.git#subdirectory=client"
```

Then, you can use the `AsyncTranslatorClient` to interact with the API.

```python
from nllb import AsyncTranslatorClient

async def main():
    text = "Hello, world!"
    client = AsyncTranslatorClient("http://localhost:7860")
    language_prediction = await client.detect_language(text)
    response = await client.translate(text, source=language_prediction.language, target="spa_Latn")

asyncio.run(main())
```

## Self-Hosting

You can self-host the API and access the Swagger UI at [localhost:7860/api/schema/swagger](http://localhost:7860/api/schema/swagger) with the following minimal configuration

```bash
docker run --rm \
  -e SERVER_PORT=7860 \
  -p 7860:7860 \
  ghcr.io/winstxnhdw/nllb-api:main
```

### Cross-Origin Resource Sharing

You can configure CORS by passing the following environment variables.

```bash
docker run --rm \
  -e SERVER_PORT=7860 \
  -e ACCESS_CONTROL_ALLOW_ORIGIN=localhost,example.com \
  -e ACCESS_CONTROL_ALLOW_CREDENTIALS=true \
  -e ACCESS_CONTROL_ALLOW_HEADERS=X-Custom-Header,Upgrade-Insecure-Requests \
  -e ACCESS_CONTROL_EXPOSE_HEADERS=Content-Encoding,Kuma-Revision \
  -e ACCESS_CONTROL_MAX_AGE=3600 \
  -e ACCESS_CONTROL_ALLOW_METHOD_GET=true \
  -e ACCESS_CONTROL_ALLOW_METHOD_POST=true \
  -e ACCESS_CONTROL_ALLOW_METHOD_OPTIONS=true \
  -e ACCESS_CONTROL_ALLOW_METHOD_PUT=true \
  -e ACCESS_CONTROL_ALLOW_METHOD_DELETE=true \
  -e ACCESS_CONTROL_ALLOW_METHOD_PATCH=true \
  -e ACCESS_CONTROL_ALLOW_METHOD_HEAD=true \
  -e ACCESS_CONTROL_ALLOW_METHOD_TRACE=true \
  -p 7860:7860 \
  ghcr.io/winstxnhdw/nllb-api:main
```

### Optimisation

You can pass the following environment variables to optimise the API for your own uses. The value of `OMP_NUM_THREADS` increases the number of threads used to translate a given batch of inputs, while `TRANSLATOR_THREADS` increases the number of threads used to handle translate requests in parallel. It is recommended to not modify `WORKER_COUNT` as spawning multiple workers can lead to increased memory usage and poorer performance.

> [!IMPORTANT]\
> `OMP_NUM_THREADS` $\times$ `TRANSLATOR_THREADS` should not exceed the physical number of cores on your machine.

```bash
docker run --rm \
  -e SERVER_PORT=7860 \
  -e OMP_NUM_THREADS=6 \
  -e TRANSLATOR_THREADS=2 \
  -e WORKER_COUNT=1 \
  -p 7860:7860 \
  ghcr.io/winstxnhdw/nllb-api:main
```

### CUDA Support

You can accelerate your inference with CUDA by building with the `USE_CUDA` build argument.

```bash
docker build --build-arg USE_CUDA=1 -f Dockerfile.build -t nllb-api .
```

After building the image, you can run the image with the following.

> [!NOTE]\
> `OMP_NUM_THREADS` has no effect when CUDA is enabled.

```bash
docker run --rm --gpus all \
  -e SERVER_PORT=7860 \
  -e WORKER_COUNT=1 \
  -p 7860:7860 \
  nllb-api
```

### Telemetry

You can enable OpenTelemetry support by passing the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable. This enables exporting of traces, metrics and logs to the specified OTLP endpoint.

```bash
docker run --rm \
  -e SERVER_PORT=7860 \
  -e OTEL_RESOURCE_ATTRIBUTES=service.namespace=huggingface,deployment.environment=production \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp-gateway-prod-ap-southeast-1.grafana.net/otlp \
  -e OTEL_EXPORTER_OTLP_HEADERS="Authorization: Basic $OTEL_AUTH_TOKEN" \
  -e OTEL_METRIC_EXPORT_INTERVAL=10000 \
  -p 7860:7860 \
  ghcr.io/winstxnhdw/nllb-api:main
```

## Development

First, install the required dependencies for your editor with the following.

```bash
uv sync
```

Now, you can access the Swagger UI at [localhost:7860/api/schema/swagger](http://localhost:7860/api/schema/swagger) after spinning the server up locally with the following.

```bash
uv run docker-cpu
```
