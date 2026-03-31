---
name: pypi-package-publish
description: Publish or update a Python package on PyPI with metadata optimized for discoverability
tool: twine
difficulty: Setup
---

# PyPI Package Publish

Publish a Python package to the Python Package Index (PyPI) with metadata configured for developer discoverability.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| twine | `twine upload` | https://twine.readthedocs.io/en/stable/ |
| PyPI API (Trusted Publishers) | OIDC-based publish from CI | https://docs.pypi.org/trusted-publishers/ |
| GitHub Actions | `pypa/gh-action-pypi-publish` | https://github.com/pypa/gh-action-pypi-publish |
| flit | `flit publish` | https://flit.pypa.io/ |
| poetry | `poetry publish` | https://python-poetry.org/docs/cli/#publish |

## Authentication

- **twine:** Set `TWINE_USERNAME=__token__` and `TWINE_PASSWORD=pypi-<your-api-token>`. Generate tokens at https://pypi.org/manage/account/token/
- **Trusted Publishers (preferred for CI):** Configure in PyPI project settings to allow GitHub Actions to publish without static tokens.

## Instructions

### 1. Configure pyproject.toml for discoverability

```toml
[project]
name = "your-package-name"
version = "1.0.0"
description = "Verb-first description with primary search keyword."
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
keywords = ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development :: Libraries",
]

[project.urls]
Homepage = "https://yoursite.com/docs/sdk/python?utm_source=pypi&utm_medium=registry&utm_campaign=python-sdk"
Documentation = "https://yoursite.com/docs/sdk/python"
Repository = "https://github.com/org/python-sdk"
Changelog = "https://github.com/org/python-sdk/blob/main/CHANGELOG.md"
```

Rules for metadata:
- `name`: Use the search term developers would type. Hyphens preferred over underscores for PyPI search.
- `description`: Under 200 characters. Start with a verb. Include the problem domain keyword.
- `keywords`: 5-10 keywords covering: product name, problem domain, API category, framework names.
- `classifiers`: Include all supported Python versions. Use the correct Development Status.
- `project.urls`: Every URL should have UTM parameters on your domain links.

### 2. Build and publish

```bash
# Build the distribution
python -m build

# Check the distribution for issues
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

### 3. Verify publication

```bash
# Check the package exists
pip index versions your-package-name

# Verify README renders correctly
# Visit: https://pypi.org/project/your-package-name/
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Forbidden` | Token invalid or lacks scope | Generate a new API token scoped to this project |
| `400 File already exists` | Version already uploaded | Bump version number; PyPI does not allow overwriting |
| `400 description content-type not supported` | README not rendering | Ensure `readme = "README.md"` is set and README is valid Markdown |
| `HTTPError 409` | Package name conflict | Check https://pypi.org/project/your-name/ and pick a unique name |

## Notes

- **README on PyPI:** PyPI renders the README as the package landing page. Include a CTA section with `utm_source=pypi`.
- **TestPyPI:** Validate first with `twine upload --repository testpypi dist/*` at https://test.pypi.org.
- **Yanking:** To soft-remove a version without breaking installs: `pip install your-package-name==1.0.0` still works but `pip install your-package-name` skips it. Yank via PyPI web UI.
