import requests
import concurrent.futures
import time
from typing import List, Dict, Tuple

# List of complex sentences to translate
sentences: List[str] = [
    "The quick brown fox jumps over the lazy dog.",
    "In the midst of chaos, there is also opportunity.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "The only thing we have to fear is fear itself.",
    "I think, therefore I am.",
    "Life is what happens when you're busy making other plans.",
    "The journey of a thousand miles begins with a single step.",
    "It was the best of times, it was the worst of times.",
    "Ask not what your country can do for you; ask what you can do for your country."
]

# List of FLORES-200 target language codes (excluding 'eng_Latn' as it is the source language)
language_codes = [
    'ace_Arab', 'ace_Latn', 'acm_Arab', 'acq_Arab', 'aeb_Arab', 'afr_Latn', 'ajp_Arab', 'aka_Latn',
    'amh_Ethi', 'apc_Arab', 'arb_Arab', 'arb_Latn', 'ars_Arab', 'ary_Arab', 'arz_Arab', 'asm_Beng',
    'ast_Latn', 'awa_Deva', 'ayr_Latn', 'azb_Arab', 'azj_Latn', 'bak_Cyrl', 'bam_Latn', 'ban_Latn',
    'bel_Cyrl', 'bem_Latn', 'ben_Beng', 'bho_Deva', 'bjn_Arab', 'bjn_Latn', 'bod_Tibt', 'bos_Latn',
    'bug_Latn', 'bul_Cyrl', 'cat_Latn', 'ceb_Latn', 'ces_Latn', 'cjk_Latn', 'ckb_Arab', 'crh_Latn',
    'cym_Latn', 'dan_Latn', 'deu_Latn', 'dik_Latn', 'dyu_Latn', 'dzo_Tibt', 'ell_Grek', 'epo_Latn',
    'est_Latn', 'eus_Latn', 'ewe_Latn', 'fao_Latn', 'fij_Latn', 'fin_Latn', 'fon_Latn', 'fra_Latn',
    'fur_Latn', 'fuv_Latn', 'gla_Latn', 'gle_Latn', 'glg_Latn', 'grn_Latn', 'guj_Gujr', 'hat_Latn',
    'hau_Latn', 'heb_Hebr', 'hin_Deva', 'hne_Deva', 'hrv_Latn', 'hun_Latn', 'hye_Armn', 'ibo_Latn',
    'ilo_Latn', 'ind_Latn', 'isl_Latn', 'ita_Latn', 'jav_Latn', 'jpn_Jpan', 'kab_Latn', 'kac_Latn',
    'kam_Latn', 'kan_Knda', 'kas_Arab', 'kas_Deva', 'kat_Geor', 'knc_Arab', 'knc_Latn', 'kaz_Cyrl',
    'kbp_Latn', 'kea_Latn', 'khm_Khmr', 'kik_Latn', 'kin_Latn', 'kir_Cyrl', 'kmb_Latn', 'kmr_Latn',
    'kon_Latn', 'kor_Hang', 'lao_Laoo', 'lij_Latn', 'lim_Latn', 'lin_Latn', 'lit_Latn', 'lmo_Latn',
    'ltg_Latn', 'ltz_Latn', 'lua_Latn', 'lug_Latn', 'luo_Latn', 'lus_Latn', 'lvs_Latn', 'mag_Deva',
    'mai_Deva', 'mal_Mlym', 'mar_Deva', 'min_Arab', 'min_Latn', 'mkd_Cyrl', 'plt_Latn', 'mlt_Latn',
    'mni_Beng', 'khk_Cyrl', 'mos_Latn', 'mri_Latn', 'mya_Mymr', 'nld_Latn', 'nno_Latn', 'nob_Latn',
    'npi_Deva', 'nso_Latn', 'nus_Latn', 'nya_Latn', 'oci_Latn', 'gaz_Latn', 'ory_Orya', 'pag_Latn',
    'pan_Guru', 'pap_Latn', 'pes_Arab', 'pol_Latn', 'por_Latn', 'prs_Arab', 'pbt_Arab', 'quy_Latn',
    'ron_Latn', 'run_Latn', 'rus_Cyrl', 'sag_Latn', 'san_Deva', 'sat_Olck', 'scn_Latn', 'shn_Mymr',
    'sin_Sinh', 'slk_Latn', 'slv_Latn', 'smo_Latn', 'sna_Latn', 'snd_Arab', 'som_Latn', 'sot_Latn',
    'spa_Latn', 'als_Latn', 'srd_Latn', 'srp_Cyrl', 'ssw_Latn', 'sun_Latn', 'swe_Latn', 'swh_Latn',
    'szl_Latn', 'tam_Taml', 'tat_Cyrl', 'tel_Telu', 'tgk_Cyrl', 'tgl_Latn', 'tha_Thai', 'tir_Ethi',
    'taq_Latn', 'taq_Tfng', 'tpi_Latn', 'tsn_Latn', 'tso_Latn', 'tuk_Latn', 'tum_Latn', 'tur_Latn',
    'twi_Latn', 'tzm_Tfng', 'uig_Arab', 'ukr_Cyrl', 'umb_Latn', 'urd_Arab', 'uzn_Latn', 'vec_Latn',
    'vie_Latn', 'war_Latn', 'wol_Latn', 'xho_Latn', 'ydd_Hebr', 'yor_Latn', 'yue_Hant', 'zho_Hans',
    'zho_Hant', 'zsm_Latn', 'zul_Latn'
]

# Number of target languages to translate into
N: int = 5  # Ensure this matches the number of languages in language_codes

# Ensure that we have at least N languages in the list
if len(language_codes) < N:
    print(f"Error: Only {len(language_codes)} language codes provided, but N={N} requested.")
    exit(1)

# Function to make a translation request
def translate(text: str, target_lang: str) -> Dict:
    url: str = 'http://127.0.0.1:7860/api/v3/translate'
    params: Dict[str, str] = {
        'text': text,
        'source': 'eng_Latn',
        'target': target_lang
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
    return response.json()

# Select N target languages
targets: List[str] = language_codes[:N]

# List to store durations for each sentence
durations: List[float] = []

# Main loop to translate each sentence into N languages
for sentence in sentences:
    print(f"\nTranslating sentence: \"{sentence}\"")
    # Start timing
    start_time: float = time.time()

    # Use ThreadPoolExecutor to send requests in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=N) as executor:
        # Map the translate function to the target languages
        futures: Dict[concurrent.futures.Future, str] = {
            executor.submit(translate, sentence, lang): lang for lang in targets
        }
        # Collect results
        for future in concurrent.futures.as_completed(futures):
            lang: str = futures[future]
            try:
                result: Dict = future.result()
                # Optionally, process the result here
                # print(f"Translation to {lang}: {result}")
            except Exception as e:
                print(f'Error translating to {lang}: {e}')

    # End timing
    end_time: float = time.time()
    duration: float = end_time - start_time
    durations.append(duration)

    print(f'Translated into {N} languages in {duration:.2f} seconds')

# Calculate average duration
average_duration: float = sum(durations) / len(durations)
print(f"\nAverage time for translating each sentence into {N} languages: {average_duration:.2f} seconds")