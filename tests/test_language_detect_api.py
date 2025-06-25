# ruff: noqa: S101


from httpx import Response
from litestar import Litestar
from litestar.status_codes import HTTP_400_BAD_REQUEST
from litestar.testing import AsyncTestClient
from pytest import mark

from server.typedefs import Language


def get_language(response: Response) -> str | None:
    return response.json().get('language')


def get_confidence(response: Response) -> float | None:
    return response.json().get('confidence')


async def detect_language(
    client: AsyncTestClient[Litestar],
    text: str,
    *,
    fast_model_confidence_threshold: float = 0.85,
    accurate_model_confidence_threshold: float = 0.35,
) -> Response:
    parameters = {
        'text': text,
        'fast-model-confidence-threshold': fast_model_confidence_threshold,
        'accurate-model-confidence-threshold': accurate_model_confidence_threshold,
    }

    return await client.get('/v4/language', params=parameters)


@mark.anyio
@mark.parametrize(
    ('text', 'language'),
    [('She sells seashells', 'eng_Latn'), ('El gato está sentado en la alfombra', 'spa_Latn')],
)
async def test_detect_language_api(session_client: AsyncTestClient[Litestar], text: str, language: str) -> None:
    response = await detect_language(session_client, text)

    assert get_language(response) == language
    assert isinstance(get_confidence(response), float)


@mark.anyio
async def test_detect_language_with_empty_text(session_client: AsyncTestClient[Litestar]) -> None:
    response = await detect_language(session_client, '')
    assert response.status_code == HTTP_400_BAD_REQUEST


@mark.anyio
async def test_detect_language_with_long_text(session_client: AsyncTestClient[Litestar]) -> None:
    text = (
        'She sells seashells by the seashore, '
        'The shells she sells are surely seashells. '
        'So if she sells shells on the seashore, '
        "I'm sure she sells seashore shells. "
    )

    response = await detect_language(session_client, text * 100)

    assert response.status_code == HTTP_400_BAD_REQUEST


@mark.anyio
@mark.parametrize(
    'text',
    [
        'She sells seashells\n',
        'She sells seashells\r\n',
        'She\nsells\nseashells\r\n',
        '\n\nShe\n\nsells\n\nseashells\n\n',
    ],
)
async def test_detect_language_with_newline(session_client: AsyncTestClient[Litestar], text: str) -> None:
    response = await detect_language(session_client, text)
    assert get_language(response) == 'eng_Latn'


@mark.anyio
@mark.parametrize(
    ('text', 'language'),
    [
        ('Die kat sit op die mat', 'afr_Latn'),
        ('Macja ulet mbi pemë', 'als_Latn'),
        ('القطة تجلس على الحصيرة', 'arb_Latn'),
        ('Կատուն նստած է գորգի վրա', 'hye_Armn'),
        ('Pişik xalçanın üstündə oturur', 'azj_Latn'),  # noqa: RUF001
        ('Katua estera gainean dago', 'eus_Latn'),
        ('Кот сядзіць на дыванчыку', 'bel_Cyrl'),
        ('বিড়াল মাদুরের উপর বসে আছে', 'ben_Beng'),
        ('Solen skinner over Oslo', 'nob_Latn'),
        ('Mačka sjedi na prostirci', 'bos_Latn'),
        ('Котката седи на рогозката', 'bul_Cyrl'),
        ("El gat seu sobre l'estora", 'cat_Latn'),
        ('猫坐在垫子上', 'zho_Hans'),
        ('Sunce sija iznad Zagreba', 'hrv_Latn'),
        ('Kočka sedí na rohoži', 'ces_Latn'),
        ('Katten sidder på måtten', 'dan_Latn'),
        ('Nederland is beroemd om zijn molens, tulpen en grachten', 'nld_Latn'),
        ('The quick brown fox jumps over the lazy dog', 'eng_Latn'),
        ('La kato sidas sur la mato', 'epo_Latn'),
        ('Kass istub vaiba peal', 'est_Latn'),
        ('Kissa istuu matolla', 'fin_Latn'),
        ('Le chat est assis sur le tapis', 'fra_Latn'),
        ('Omusajja atudde ku ttaka', 'lug_Latn'),
        ('კატა ზის ხალიჩაზე', 'kat_Geor'),
        ('Die Katze sitzt auf der Matte', 'deu_Latn'),
        ('Η γάτα κάθεται στο χαλάκι', 'ell_Grek'),  # noqa: RUF001
        ('બિલાડી સાદડી પર બેસે છે', 'guj_Gujr'),
        ('החתול יושב על המחצלת', 'heb_Hebr'),
        ('बिल्ली चटाई पर बैठी है', 'hin_Deva'),
        ('A macska a szőnyegen ül', 'hun_Latn'),
        ('Kötturinn situr á mottunni', 'isl_Latn'),
        ('Matahari bersinar di atas Jakarta', 'ind_Latn'),
        ('Suíonn an cat ar an mata', 'gle_Latn'),
        ('Il gatto è seduto sul tappeto', 'ita_Latn'),
        ('猫がマットの上に座っています', 'jpn_Jpan'),
        ('Мысық төсеніште отыр', 'kaz_Cyrl'),
        ('고양이가 매트 위에 앉아 있습니다', 'kor_Hang'),
        ('Kaķis sēž uz paklāja', 'lvs_Latn'),
        ('Katė sėdi ant kilimėlio', 'lit_Latn'),
        ('Сонцето грее над Скопје', 'mkd_Cyrl'),  # noqa: RUF001
        ('Kucing duduk di atas tikar', 'msa_Latn'),
        ('Kei runga te ngeru i te whāriki', 'mri_Latn'),
        ('मांजर चटईवर बसली आहे', 'mar_Deva'),
        ('Муур дэвсгэр дээр сууж байна', 'mon_Cyrl'),  # noqa: RUF001
        ('Fjordane lyser opp under sola', 'nno_Latn'),
        ('گربه روی تشک نشسته است', 'pes_Arab'),
        ('Kot siedzi na macie', 'pol_Latn'),
        ('O gato está sentado no tapete', 'por_Latn'),
        ('ਬਿੱਲਾ ਚਟਾਈ ਉੱਤੇ ਬੈਠਾ ਹੈ', 'pan_Guru'),
        ('Soarele strălucește peste București', 'ron_Latn'),
        ('Кот сидит на коврике', 'rus_Cyrl'),
        ('Сунце сија над Београдом', 'srp_Cyrl'),
        ('Katsi inogara paruva', 'sna_Latn'),
        ('Mačka sedí na rohožke', 'slk_Latn'),
        ('Mačka sedi na preprogi', 'slv_Latn'),
        ('Bisaddu waxay fadhiisataa rogga', 'som_Latn'),
        ('Katse e dutse hodimong', 'sot_Latn'),
        ('El gato está sentado en la alfombra', 'spa_Latn'),
        ('Jua linawaka juu ya Nairobi', 'swh_Latn'),
        ('Katten sitter på mattan', 'swe_Latn'),
        ('Ang pusa ay nakaupo sa banig', 'tgl_Latn'),
        ('பூனை பாயில் அமர்ந்துள்ளது', 'tam_Taml'),
        ('పిల్లి చాపపై కూర్చుంది', 'tel_Telu'),
        ('แมวนั่งอยู่บนเสื่อ', 'tha_Thai'),
        ('Mpfundla wu tshama ehenhla ka rivanti', 'tso_Latn'),
        ('Katse e tlhapologa mo letlalong', 'tsn_Latn'),
        ('Kedi paspasın üzerinde oturuyor', 'tur_Latn'),  # noqa: RUF001
        ('Кіт сидить на килимку', 'ukr_Cyrl'),
        ('بلی چٹائی پر بیٹھی ہے', 'urd_Arab'),
        ('Con mèo ngồi trên tấm thảm', 'vie_Latn'),
        ("Mae'r gath yn eistedd ar y mat", 'cym_Latn'),
        ('Ikati ihleli phezu kwendawo', 'xho_Latn'),
        ('Ologbo naa joko lori atẹ', 'yor_Latn'),
        ('Ikati ihlezi phezu kwamatha', 'zul_Latn'),
    ],
)
async def test_detect_language_with_accurate_model(
    session_client: AsyncTestClient[Litestar],
    text: str,
    language: Language,
) -> None:
    response = await detect_language(
        session_client,
        text,
        fast_model_confidence_threshold=1.1,
        accurate_model_confidence_threshold=0.0,
    )

    assert get_language(response) == language
