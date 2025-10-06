# Release Guide - MCP Package Hero

This guide covers how to release MCP Package Hero to PyPI and create GitHub releases.

---

## 🎯 Quick Answer

**YES! The package is ready for PyPI release.**

All requirements are met:
- ✅ Package builds successfully
- ✅ All tests passing (8/8)
- ✅ Type checking passing (mypy)
- ✅ Documentation complete
- ✅ License included (MIT)
- ✅ Version 1.0.0 set
- ✅ Production/Stable classifier

---

## 📋 Pre-Release Checklist

Before releasing, verify:

- [ ] **All changes committed to git**
  ```bash
  git status  # Should be clean or only have release commits
  ```

- [ ] **Version number updated** (if needed)
  - Check `pyproject.toml` version field
  - Update CHANGELOG.md

- [ ] **Tests passing**
  ```bash
  uv run pytest -v
  ```

- [ ] **Type checking passing**
  ```bash
  uv run mypy src/
  ```

- [ ] **Documentation updated**
  - README.md accurate
  - CHANGELOG.md has latest version entry
  - All examples working

- [ ] **Clean build**
  ```bash
  rm -rf dist/ build/ *.egg-info
  uv build
  ```

---

## 🚀 Publishing to PyPI

### Step 1: Set Up PyPI Account

1. **Create PyPI account**: https://pypi.org/account/register/
2. **Create API token**: https://pypi.org/manage/account/token/
   - Token name: `mcp-package-hero-upload`
   - Scope: Entire account (or specific to this project after first upload)
3. **Save token securely** (you'll only see it once!)

### Step 2: Configure Credentials

Create `~/.pypirc`:

```bash
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEI...YOUR_PYPI_TOKEN_HERE...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEI...YOUR_TEST_PYPI_TOKEN_HERE...
EOF

chmod 600 ~/.pypirc
```

### Step 3: Install Twine

```bash
uv pip install twine
```

### Step 4: Build Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build fresh
uv build

# Verify build succeeded
ls -lh dist/
```

### Step 5: Check Package

```bash
# Validate distribution
twine check dist/*

# Should output:
# Checking dist/mcp_package_hero-1.0.0-py3-none-any.whl: PASSED
# Checking dist/mcp_package_hero-1.0.0.tar.gz: PASSED
```

### Step 6A: Upload to TestPyPI (Recommended First)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# You'll be prompted if credentials not in ~/.pypirc
# Or it will use your token automatically

# Output should show:
# Uploading distributions to https://test.pypi.org/legacy/
# Uploading mcp_package_hero-1.0.0-py3-none-any.whl
# Uploading mcp_package_hero-1.0.0.tar.gz
```

**Test installation from TestPyPI:**

```bash
# Create test environment
python -m venv test-env
source test-env/bin/activate

# Install from TestPyPI (with PyPI for dependencies)
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    mcp-package-hero

# Verify it works
python -c "from mcp_package_hero import __version__; print(__version__)"
# Should print: 1.0.0

# Test the CLI
python -m mcp_package_hero.server --help

# Clean up
deactivate
rm -rf test-env
```

### Step 6B: Upload to PyPI (Production)

Once TestPyPI installation works:

```bash
# Upload to production PyPI
twine upload dist/*

# Output:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading mcp_package_hero-1.0.0-py3-none-any.whl
# Uploading mcp_package_hero-1.0.0.tar.gz
# View at: https://pypi.org/project/mcp-package-hero/1.0.0/
```

**Verify on PyPI:**

Visit: https://pypi.org/project/mcp-package-hero/

**Test installation:**

```bash
# In a fresh environment
pip install mcp-package-hero

# Verify
python -c "from mcp_package_hero import __version__; print(__version__)"
```

---

## 🏷️ GitHub Release

### Step 1: Tag the Release

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0 - Production Ready"

# Push tag to GitHub
git push origin v1.0.0
```

### Step 2: Create GitHub Release

1. Go to: https://github.com/moinsen-dev/mcp-package-hero/releases/new
2. Choose tag: `v1.0.0`
3. Release title: `v1.0.0 - Production Release`
4. Description: Copy from CHANGELOG.md v1.0.0 section
5. Attach files (optional):
   - `dist/mcp_package_hero-1.0.0-py3-none-any.whl`
   - `dist/mcp_package_hero-1.0.0.tar.gz`
6. Check "Set as the latest release"
7. Click "Publish release"

---

## 🔄 Post-Release Steps

### 1. Verify Installation

```bash
# Test installation from PyPI
pip install mcp-package-hero

# Test the package works
python -c "from mcp_package_hero.server import mcp; print('Success!')"
```

### 2. Update Documentation

If PyPI URL changes, update:
- README.md badges
- Documentation links
- Installation instructions

### 3. Announce Release

- Create GitHub Discussion post
- Share on social media (if applicable)
- Notify users/community

### 4. Monitor

- Check PyPI download stats: https://pypistats.org/packages/mcp-package-hero
- Watch for issues: https://github.com/moinsen-dev/mcp-package-hero/issues
- Monitor discussions

---

## 🐛 Troubleshooting

### Issue: Package Name Already Taken

```bash
# Error: The name 'mcp-package-hero' is already taken
```

**Solution**: Choose a different name:
1. Update `name` in `pyproject.toml`
2. Rebuild: `uv build`
3. Try again

### Issue: Version Already Exists

```bash
# Error: File already exists
```

**Solution**: Bump version:
1. Update `version` in `pyproject.toml`
2. Update CHANGELOG.md
3. Rebuild and re-upload

### Issue: Invalid Credentials

```bash
# Error: Invalid or non-existent authentication information
```

**Solution**:
1. Verify `~/.pypirc` exists and has correct format
2. Check token is not expired
3. Ensure using `__token__` as username (not your username)

### Issue: Missing Dependencies

```bash
# Error: No matching distribution found
```

**Solution**:
1. Check all dependencies exist on PyPI
2. Verify version constraints are correct
3. Test in clean environment

---

## 📊 Release Workflow Summary

```
┌─────────────────────────────────────────────────┐
│ 1. Pre-Release Checks                           │
│    - Tests pass                                 │
│    - Docs updated                               │
│    - Version bumped                             │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 2. Build Package                                │
│    - uv build                                   │
│    - twine check dist/*                         │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 3. Test on TestPyPI (Optional but Recommended)  │
│    - twine upload --repository testpypi dist/*  │
│    - pip install from TestPyPI                  │
│    - Verify functionality                       │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 4. Upload to PyPI                               │
│    - twine upload dist/*                        │
│    - Verify on https://pypi.org                 │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 5. Create GitHub Release                        │
│    - git tag v1.0.0                             │
│    - git push --tags                            │
│    - Create release on GitHub                   │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 6. Post-Release                                 │
│    - Test installation                          │
│    - Announce release                           │
│    - Monitor for issues                         │
└─────────────────────────────────────────────────┘
```

---

## 📝 Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **Major (x.0.0)**: Breaking changes
- **Minor (1.x.0)**: New features, backward compatible
- **Patch (1.0.x)**: Bug fixes, backward compatible

### Examples:
- `1.0.0` → `1.0.1`: Bug fix
- `1.0.0` → `1.1.0`: New feature (caching)
- `1.0.0` → `2.0.0`: Breaking API change

---

## 🔐 Security Best Practices

1. **Never commit credentials** to git
2. **Use API tokens**, not passwords
3. **Limit token scope** to specific projects when possible
4. **Rotate tokens** periodically
5. **Use 2FA** on PyPI account
6. **Keep ~/.pypirc** with chmod 600

---

## 📚 Additional Resources

- **PyPI Documentation**: https://packaging.python.org/
- **Twine Documentation**: https://twine.readthedocs.io/
- **PEP 517/518**: Modern Python packaging
- **Semantic Versioning**: https://semver.org/
- **Keep a Changelog**: https://keepachangelog.com/

---

## ✅ Current Status

**Package**: `mcp-package-hero`
**Version**: `1.0.0`
**Status**: Ready for PyPI release
**Build**: ✅ Successful
**Tests**: ✅ Passing (8/8)
**Docs**: ✅ Complete

**Next Step**: Follow Step 1 to set up PyPI account and upload!

---

*Last Updated: 2025-10-06*
