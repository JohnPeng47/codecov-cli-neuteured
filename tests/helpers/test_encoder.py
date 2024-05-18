import pytest

from codecov_cli.helpers.encoder import (
    decode_slug,
    encode_slug,
    slug_encoded_incorrectly,
    slug_without_subgroups_is_invalid,
)












@pytest.mark.parametrize(
    "encoded_slug",
    [
        ("owner::::repo"),
        ("owner:::subgroup::::repo"),
    ],
)
def test_valid_encoded_slug(encoded_slug):
    assert not slug_encoded_incorrectly(encoded_slug)


@pytest.mark.parametrize(
    "encoded_slug, decoded_slug",
    [
        ("owner::::repo", "owner/repo"),
        ("owner:::subgroup::::repo", "owner/subgroup/repo"),
    ],
)
def test_decode_slug(encoded_slug, decoded_slug):
    expected_encoded_slug = decode_slug(encoded_slug)
    assert expected_encoded_slug == decoded_slug
