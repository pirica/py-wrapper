import datetime
import fortnite_api as fn_api

from .test_async import (
    TEST_ACCOUNT_ID,
    TEST_ACCOUNT_NAME,
    TEST_COSMETIC_ID,
    TEST_CREATOR_CODE,
    TEST_DEFAULT_PLAYLIST,
    _test_game_mode_news,
    _test_playlist,
)


def test_sync_aes():
    with fn_api.SyncFortniteAPI() as client:
        aes = client.fetch_aes()

        # Ensure that the AES can be fetched with BASE64
        aes_b64 = client.fetch_aes(key_format=fn_api.KeyFormat.BASE64)

    assert isinstance(aes, fn_api.Aes)
    assert aes.main_key
    assert aes.build
    assert aes.version

    assert aes.updated
    assert isinstance(aes.updated, datetime.datetime)

    assert aes != None

    # Ensure that the AES can be fetched with BASE64
    assert aes_b64.build == aes.build
    assert aes_b64.version == aes.version

    # NOTE: Comparison functions will not account for separate key formats, if the two instances have different values they are deemed unequal. Maybe change this in the future.
    assert aes_b64 != aes


def test_sync_banners():
    with fn_api.SyncFortniteAPI() as client:
        banners = client.fetch_banners()

    for banner in banners:
        assert isinstance(banner, fn_api.Banner)

        assert banner.id
        assert banner.name
        assert banner.dev_name
        assert banner.description
        assert banner.category
        assert banner.full_usage_rights is not None
        # TODO: Banner images tests (not added because of pending Images class implementation)


def test_sync_banner_colors():
    with fn_api.SyncFortniteAPI() as client:
        banner_colors = client.fetch_banner_colors()

    for color in banner_colors:
        assert isinstance(color, fn_api.BannerColor)

        assert color.id
        assert color.color
        assert color.category
        assert color.sub_category_group is not None

    if banner_colors:
        first = banner_colors[0]
        assert first == first

        if len(banner_colors) >= 2:
            assert first != banner_colors[1]


def test_sync_creator_code():
    with fn_api.SyncFortniteAPI() as client:
        creator_code = client.fetch_creator_code(name=TEST_CREATOR_CODE)

    assert isinstance(creator_code, fn_api.CreatorCode)
    assert creator_code.code == TEST_CREATOR_CODE

    mock_account_payload = dict(id=TEST_ACCOUNT_ID, name=TEST_ACCOUNT_NAME)
    assert creator_code.account == fn_api.Account(mock_account_payload)

    assert creator_code.status is fn_api.CreatorCodeStatus.ACTIVE
    assert creator_code.disabled is False
    assert creator_code.verified is False


def test_sync_fetch_playlist():
    with fn_api.SyncFortniteAPI() as client:
        playlists = client.fetch_playlists()
        playlists_en = client.fetch_playlists()

    assert len(playlists), "Playlists should not be empty"

    first = playlists[0]
    assert first == first

    if len(playlists) >= 2:
        assert first != playlists[1]

    assert playlists == playlists_en


def test_sync_fetch_cosmetics_cars():
    with fn_api.SyncFortniteAPI() as client:
        cosmetics_cars = client.fetch_cosmetics_cars()

    for cosmetic in cosmetics_cars:
        assert isinstance(cosmetic, fn_api.CosmeticCar)


def test_sync_fetch_cosmetics_instruments():
    with fn_api.SyncFortniteAPI() as client:
        cosmetics_instruments = client.fetch_cosmetics_instruments()

    for cosmetic in cosmetics_instruments:
        assert isinstance(cosmetic, fn_api.CosmeticInstrument)


def test_sync_fetch_cosmetics_lego_kits():
    with fn_api.SyncFortniteAPI() as client:
        lego_kits = client.fetch_cosmetics_lego_kits()

    for kit in lego_kits:
        assert isinstance(kit, fn_api.CosmeticLegoKit)


def test_sync_fetch_cosmetics_tracks():
    with fn_api.SyncFortniteAPI() as client:
        cosmetics_tracks = client.fetch_cosmetics_tracks()

    for cosmetic in cosmetics_tracks:
        assert isinstance(cosmetic, fn_api.CosmeticTrack)


def test_sync_fetch_cosmetics_br():
    with fn_api.SyncFortniteAPI() as client:
        cosmetics_br = client.fetch_cosmetics_br()

    for cosmetic in cosmetics_br:
        assert isinstance(cosmetic, fn_api.CosmeticBr)


def test_sync_fetch_cosmetic_br():
    with fn_api.SyncFortniteAPI() as client:
        cosmetic_br = client.fetch_cosmetic_br(TEST_COSMETIC_ID)

    assert isinstance(cosmetic_br, fn_api.CosmeticBr)
    assert cosmetic_br.id == TEST_COSMETIC_ID


def test_sync_fetch_cosmetics_br_new():
    with fn_api.SyncFortniteAPI() as client:
        new_cosmetics_br = client.fetch_cosmetics_br_new()

    assert isinstance(new_cosmetics_br, fn_api.NewBrCosmetics)

    assert isinstance(new_cosmetics_br.date, datetime.datetime)
    assert new_cosmetics_br.build
    assert new_cosmetics_br.previous_build


def test_sync_fetch_cosmetics_new():
    with fn_api.SyncFortniteAPI() as client:
        new_cosmetics = client.fetch_cosmetics_new()

    assert isinstance(new_cosmetics, fn_api.NewCosmetics)

    assert new_cosmetics.global_hash
    assert new_cosmetics.date
    assert new_cosmetics.global_last_addition
    assert new_cosmetics.build
    assert new_cosmetics.previous_build

    assert isinstance(new_cosmetics.br, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.tracks, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.instruments, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.cars, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.lego, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.lego_kits, fn_api.NewCosmetic)


def test_sync_map():
    with fn_api.SyncFortniteAPI() as client:
        map = client.fetch_map()

    assert isinstance(map, fn_api.Map)
    assert isinstance(map.images, fn_api.MapImages)

    assert map.images.blank
    assert map.images.pois

    assert map.pois

    first_poi = map.pois[0]
    assert isinstance(first_poi, fn_api.POI)
    assert map.get_poi(first_poi.id) == first_poi

    for poi in map.pois:
        assert isinstance(poi, fn_api.POI)
        assert poi.id
        assert poi.name
        assert isinstance(poi.location, fn_api.POILocation)


def test_fetch_news():
    with fn_api.SyncFortniteAPI() as client:
        news = client.fetch_news()

    assert isinstance(news, fn_api.News)
    assert news.raw_data


def test_fetch_news_methods():
    with fn_api.SyncFortniteAPI() as client:
        news_br = client.fetch_news_br()
        news_stw = client.fetch_news_stw()

    assert isinstance(news_stw, fn_api.GameModeNews)
    _test_game_mode_news(news_br)

    assert isinstance(news_stw, fn_api.GameModeNews)
    _test_game_mode_news(news_stw)


def test_sync_fetch_playlists():
    with fn_api.SyncFortniteAPI() as client:
        playlists = client.fetch_playlists()

    for playlist in playlists:
        _test_playlist(playlist)


def test_sync_fetch_playlist_by_id():
    with fn_api.SyncFortniteAPI() as client:
        playlist = client.fetch_playlist(TEST_DEFAULT_PLAYLIST)

    assert playlist.id == TEST_DEFAULT_PLAYLIST
    _test_playlist(playlist)
