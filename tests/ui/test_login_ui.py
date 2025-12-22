def test_sample_ui(page):
    page.goto("https://example.com")
    assert "Example" in page.title()
