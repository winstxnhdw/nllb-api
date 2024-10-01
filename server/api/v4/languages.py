from litestar import Litestar, get
from litestar.params import Parameter
from litestar.openapi.spec.example import Example
from typing import Annotated, List, Optional, Dict, Union
import pycountry
import langcodes
from server.types import Languages
from server.types import Standardization

# List of FLORES-200 codes
flores_codes: List[Languages] = [
    'ace_Arab',
    'ace_Latn',
    'acm_Arab',
    'acq_Arab',
    'aeb_Arab',
    'afr_Latn',
    'ajp_Arab',
    'aka_Latn',
    'amh_Ethi',
    'apc_Arab',
    'arb_Arab',
    'arb_Latn',
    'ars_Arab',
    'ary_Arab',
    'arz_Arab',
    'asm_Beng',
    'ast_Latn',
    'awa_Deva',
    'ayr_Latn',
    'azb_Arab',
    'azj_Latn',
    'bak_Cyrl',
    'bam_Latn',
    'ban_Latn',
    'bel_Cyrl',
    'bem_Latn',
    'ben_Beng',
    'bho_Deva',
    'bjn_Arab',
    'bjn_Latn',
    'bod_Tibt',
    'bos_Latn',
    'bug_Latn',
    'bul_Cyrl',
    'cat_Latn',
    'ceb_Latn',
    'ces_Latn',
    'cjk_Latn',
    'ckb_Arab',
    'crh_Latn',
    'cym_Latn',
    'dan_Latn',
    'deu_Latn',
    'dik_Latn',
    'dyu_Latn',
    'dzo_Tibt',
    'ell_Grek',
    'eng_Latn',
    'epo_Latn',
    'est_Latn',
    'eus_Latn',
    'ewe_Latn',
    'fao_Latn',
    'fij_Latn',
    'fin_Latn',
    'fon_Latn',
    'fra_Latn',
    'fur_Latn',
    'fuv_Latn',
    'gla_Latn',
    'gle_Latn',
    'glg_Latn',
    'grn_Latn',
    'guj_Gujr',
    'hat_Latn',
    'hau_Latn',
    'heb_Hebr',
    'hin_Deva',
    'hne_Deva',
    'hrv_Latn',
    'hun_Latn',
    'hye_Armn',
    'ibo_Latn',
    'ilo_Latn',
    'ind_Latn',
    'isl_Latn',
    'ita_Latn',
    'jav_Latn',
    'jpn_Jpan',
    'kab_Latn',
    'kac_Latn',
    'kam_Latn',
    'kan_Knda',
    'kas_Arab',
    'kas_Deva',
    'kat_Geor',
    'knc_Arab',
    'knc_Latn',
    'kaz_Cyrl',
    'kbp_Latn',
    'kea_Latn',
    'khm_Khmr',
    'kik_Latn',
    'kin_Latn',
    'kir_Cyrl',
    'kmb_Latn',
    'kmr_Latn',
    'kon_Latn',
    'kor_Hang',
    'lao_Laoo',
    'lij_Latn',
    'lim_Latn',
    'lin_Latn',
    'lit_Latn',
    'lmo_Latn',
    'ltg_Latn',
    'ltz_Latn',
    'lua_Latn',
    'lug_Latn',
    'luo_Latn',
    'lus_Latn',
    'lvs_Latn',
    'mag_Deva',
    'mai_Deva',
    'mal_Mlym',
    'mar_Deva',
    'min_Arab',
    'min_Latn',
    'mkd_Cyrl',
    'plt_Latn',
    'mlt_Latn',
    'mni_Beng',
    'khk_Cyrl',
    'mos_Latn',
    'mri_Latn',
    'mya_Mymr',
    'nld_Latn',
    'nno_Latn',
    'nob_Latn',
    'npi_Deva',
    'nso_Latn',
    'nus_Latn',
    'nya_Latn',
    'oci_Latn',
    'gaz_Latn',
    'ory_Orya',
    'pag_Latn',
    'pan_Guru',
    'pap_Latn',
    'pes_Arab',
    'pol_Latn',
    'por_Latn',
    'prs_Arab',
    'pbt_Arab',
    'quy_Latn',
    'ron_Latn',
    'run_Latn',
    'rus_Cyrl',
    'sag_Latn',
    'san_Deva',
    'sat_Olck',
    'scn_Latn',
    'shn_Mymr',
    'sin_Sinh',
    'slk_Latn',
    'slv_Latn',
    'smo_Latn',
    'sna_Latn',
    'snd_Arab',
    'som_Latn',
    'sot_Latn',
    'spa_Latn',
    'als_Latn',
    'srd_Latn',
    'srp_Cyrl',
    'ssw_Latn',
    'sun_Latn',
    'swe_Latn',
    'swh_Latn',
    'szl_Latn',
    'tam_Taml',
    'tat_Cyrl',
    'tel_Telu',
    'tgk_Cyrl',
    'tgl_Latn',
    'tha_Thai',
    'tir_Ethi',
    'taq_Latn',
    'taq_Tfng',
    'tpi_Latn',
    'tsn_Latn',
    'tso_Latn',
    'tuk_Latn',
    'tum_Latn',
    'tur_Latn',
    'twi_Latn',
    'tzm_Tfng',
    'uig_Arab',
    'ukr_Cyrl',
    'umb_Latn',
    'urd_Arab',
    'uzn_Latn',
    'vec_Latn',
    'vie_Latn',
    'war_Latn',
    'wol_Latn',
    'xho_Latn',
    'ydd_Hebr',
    'yor_Latn',
    'yue_Hant',
    'zho_Hans',
    'zho_Hant',
    'zsm_Latn',
    'zul_Latn',
]

# Helper function to get codes using pycountry and langcodes
def get_language_codes(flores_code: str) -> Dict[str, str]:
    codes = {}
    try:
        # Parse the FLORES-200 code
        iso6393_code, iso15924_code = flores_code.split('_')
        codes['FLORES-200'] = flores_code
        codes['ISO-639-3'] = iso6393_code
        codes['ISO-15924'] = iso15924_code

        # Get the language name from ISO-639-3 code
        lang = pycountry.languages.get(alpha_3=iso6393_code)
        if lang is None:
            # Try to lookup using other methods
            lang = pycountry.languages.lookup(iso6393_code)
        if lang:
            codes['name'] = lang.name
            # ISO-639-1
            codes['ISO-639-1'] = getattr(lang, 'alpha_2', '')
            # ISO 639-2
            codes['ISO-639-2/B'] = getattr(lang, 'bibliographic', '')
            # IETF-BCP-47
            codes['IETF-BCP-47'] = langcodes.standardize_tag(codes['ISO-639-1'] or iso6393_code)
            # RFC-5646 (Same as IETF BCP 47)
            codes['RFC-5646'] = codes['IETF-BCP-47']
            # CLDR (Common Locale Data Repository)
            codes['CLDR'] = codes['IETF-BCP-47']
            # Ethnologue, SIL, LC codes
            codes['Ethnologue'] = iso6393_code
            codes['SIL'] = iso6393_code.upper()
            codes['LC'] = codes['ISO-639-2/B'] or codes['ISO-639-3']

        else:
            # If language not found
            codes['name'] = 'Unknown'
    except Exception as e:
        # Handle parsing errors
        codes['name'] = 'Unknown'
        print(f"Error processing code {flores_code}: {e}")
    return codes

# Build the languages data structure
languages_list = []
for flores_code in flores_codes:
    codes = get_language_codes(flores_code)
    languages_list.append(codes)

@get("/languages")
def languages(
    standardization: Annotated[
        Optional[Standardization],
        Parameter(
            description="Standardization code to sort the languages by.",
            examples=[
                Example(
                    summary="Sort by name",
                    description="Sorting by name is the default.",
                    value="",
                ),
                Example(
                    summary="Sort by IETF codes",
                    description="Use IETF-BCP-47 standardization for sorting.",
                    value="IETF-BCP-47",
                ),
                Example(
                    summary="Sort by ISO-639-1 codes",
                    description="Use ISO-639-1 standardization for sorting.",
                    value="ISO-639-1",
                ),
                Example(
                    summary="Sort by RFC-5646 codes",
                    description="Use RFC-5646 standardization for sorting.",
                    value="RFC-5646",
                ),
                Example(
                    summary="Sort by ISO-15924 script codes",
                    description="Use ISO-15924 script standardization for sorting by script code.",
                    value="ISO-15924",
                ),
                Example(
                    summary="Sort by ISO-639-3 codes",
                    description="Use ISO-639-3 standardization for sorting by language codes.",
                    value="ISO-639-3",
                ),
                Example(
                    summary="Sort by Ethnologue codes",
                    description="Use Ethnologue standardization for sorting by Ethnologue language codes.",
                    value="Ethnologue",
                ),
                Example(
                    summary="Sort by SIL codes",
                    description="Use SIL standardization for sorting by SIL language codes.",
                    value="SIL",
                ),
            ],
        ),
    ] = None,
) -> Dict[Union[Languages, Standardization], Dict[Standardization, str]]:
    if standardization and standardization in languages_list[0]:
        # Sort by the specified standardization code
        result = {
            lang[standardization]: {key: value for key, value in lang.items() if key != standardization}
            for lang in languages_list
            if lang.get(standardization)
        }
    else:
        # Default sorting by language name
        result = {
            lang["name"]: {key: value for key, value in lang.items() if key != "name"}
            for lang in languages_list
        }
    return result

app = Litestar(route_handlers=[languages])

