# State Tracker: MCP Package Version Servers

**Last Updated:** 2025-10-06  
**Context:** Investigation into MCP servers for checking latest package versions across different technology stacks

---

## 🎯 Current Objective

Find or create MCP server(s) that can check the latest package versions for:
- ✅ Python (PyPI)
- ✅ TypeScript/JavaScript (npm)
- ❌ Flutter/Dart (pub.dev)
- ❌ Rust (crates.io)

---

## 📊 Current State

### Existing Solutions

#### 1. **mcp-package-version** (Primary Multi-Registry Server)
- **Repository:** https://github.com/sammcj/mcp-package-version
- **Language:** Go
- **Status:** Active, moving to mcp-devtools

**Supported Registries:**
- ✅ npm (Node.js/JavaScript)
- ✅ PyPI (Python)
- ✅ Maven Central (Java)
- ✅ Go Proxy (Go)
- ✅ Swift Packages
- ✅ AWS Bedrock (AI Models)
- ✅ Docker Hub
- ✅ GitHub Container Registry
- ✅ GitHub Actions

**Missing:**
- ❌ pub.dev (Flutter/Dart)
- ❌ crates.io (Rust)

**Installation:**
```bash
go install github.com/sammcj/mcp-package-version/v2@HEAD
```

#### 2. **Dart/Flutter MCP Server** (Official)
- **Documentation:** https://dart.dev/tools/mcp-server
- **Language:** Dart
- **Status:** Official, requires Dart SDK 3.9+ / Flutter 3.35 beta+

**Capabilities:**
- ✅ Search pub.dev for packages
- ✅ Manage dependencies in pubspec.yaml
- ✅ Run tests and analyze code
- ✅ Introspect running applications
- ❌ NOT focused on version checking across registries

**Note:** This is a specialized development server, not a version lookup tool

#### 3. **Rust MCP Server**
- **Package:** rust-mcp-server (crates.io)
- **Status:** Exists for Rust development tasks
- ❌ Does NOT provide crates.io version checking
- Focus: cargo commands, building, testing

---

## ✅ What Works

1. **Python & TypeScript:** Fully covered by mcp-package-version
2. **Dart/Flutter:** Official MCP server exists but serves different purpose
3. **Multi-transport support:** stdio, SSE available in mcp-package-version

---

## ❌ Gaps & Issues

### High Priority

1. **No unified pub.dev version checking**
   - Official Dart MCP server focuses on development, not cross-registry version checks
   - Need integration with pub.dev API for version lookups
   - Should follow same pattern as npm/PyPI in mcp-package-version

2. **No crates.io support**
   - No existing MCP server checks Rust package versions
   - rust-mcp-server exists but doesn't expose version checking
   - Need integration with crates.io API

### Medium Priority

3. **Fragmentation of tools**
   - Need separate MCP servers for different ecosystems
   - No "one-stop-shop" for all our tech stack (Flutter, Python, TypeScript, Rust)

4. **Version constraint handling**
   - Need to verify how mcp-package-version handles semantic versioning
   - Important for dependency management across stacks

---

## 💡 Ideas & Solutions

### Option 1: Contribute to mcp-package-version (Recommended)

**Add pub.dev support:**
- Implement pub.dev API client in Go
- Follow existing pattern from npm/PyPI implementations
- Support both `check_dart_versions` and `check_flutter_versions` tools
- Handle pubspec.yaml format

**Add crates.io support:**
- Implement crates.io API client
- Support Cargo.toml parsing
- Handle version constraints (^, ~, etc.)

**Benefits:**
- ✅ Unified solution across all our stacks
- ✅ Maintainer seems active and responsive
- ✅ Already established in community

**Challenges:**
- Need to learn Go (beneficial long-term)
- Need to understand API specifics for pub.dev and crates.io

### Option 2: Create Separate MCP Servers

**Create mcp-pubdev-version:**
- Dart/TypeScript implementation
- Focused on pub.dev version checking
- Could integrate with official Dart MCP server later

**Create mcp-crates-version:**
- Rust implementation
- Focused on crates.io version checking

**Benefits:**
- ✅ Use native languages for each ecosystem
- ✅ Can start quickly without learning Go

**Challenges:**
- ❌ Tool fragmentation
- ❌ Maintenance burden
- ❌ Less unified experience

### Option 3: Wrapper/Orchestrator Server

Create a meta-MCP server that:
- Delegates to mcp-package-version for npm/PyPI
- Delegates to custom servers for pub.dev/crates.io
- Provides unified interface

**Benefits:**
- ✅ Leverages existing tools
- ✅ Clean separation of concerns

**Challenges:**
- ❌ Additional complexity layer
- ❌ Multiple processes to manage

---

## 📋 Action Items

### Immediate Actions

- [ ] **Test mcp-package-version** with current Python/TypeScript projects
  - Verify npm version checking works as expected
  - Test PyPI integration
  - Document any issues

- [ ] **Research pub.dev API**
  - API documentation: https://pub.dev/help/api
  - Authentication requirements
  - Rate limits
  - Version query format

- [ ] **Research crates.io API**
  - API documentation: https://crates.io/data-access
  - Version query endpoints
  - Response format

### Short-term (1-2 weeks)

- [ ] **Decide on approach**
  - Evaluate: Contribute vs. Build separate vs. Wrapper
  - Consider: Maintenance, learning curve, time investment

- [ ] **Set up development environment** (if contributing)
  - Install Go development tools
  - Fork mcp-package-version repository
  - Study existing codebase structure

- [ ] **Create proof-of-concept**
  - Start with simplest: pub.dev version lookup
  - Validate API integration
  - Test with real packages

### Medium-term (1 month)

- [ ] **Implement pub.dev support**
  - Create API client
  - Implement version checking tool
  - Add pubspec.yaml parsing
  - Write tests

- [ ] **Implement crates.io support**
  - Create API client
  - Implement version checking tool
  - Add Cargo.toml parsing
  - Write tests

- [ ] **Submit pull requests** (if contributing)
  - Follow project contribution guidelines
  - Include documentation
  - Add examples

### Long-term

- [ ] **Integration testing**
  - Test all stacks together
  - Verify constraint handling
  - Performance testing

- [ ] **Documentation**
  - Write usage examples for Flutter projects
  - Write usage examples for Rust projects
  - Create migration guides

---

## 🐛 Potential Issues to Open

### On mcp-package-version

1. **Feature Request: Add pub.dev support**
   - **Title:** Add support for Dart/Flutter packages (pub.dev)
   - **Description:** Request to add pub.dev registry support for checking Flutter/Dart package versions
   - **Labels:** enhancement, feature-request
   - **Justification:** Dart/Flutter is widely used, official Dart MCP server doesn't focus on cross-registry version checking

2. **Feature Request: Add crates.io support**
   - **Title:** Add support for Rust packages (crates.io)
   - **Description:** Request to add crates.io registry support for checking Rust package versions
   - **Labels:** enhancement, feature-request
   - **Justification:** Rust ecosystem growing, no existing MCP solution for version checking

3. **Question: Semantic versioning handling**
   - **Title:** How are semantic version constraints handled?
   - **Description:** Clarify how constraints like ^, ~, >= are processed across different registries
   - **Labels:** question, documentation

### On Dart/Flutter MCP Server

4. **Feature Request: Version checking tool**
   - **Title:** Add tool for checking latest pub.dev package versions
   - **Description:** Request tool similar to pub outdated but accessible via MCP
   - **Labels:** enhancement
   - **Context:** Current server focuses on development tasks, not version management

---

## 🔗 Useful Links

### Documentation
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [pub.dev API Documentation](https://pub.dev/help/api)
- [crates.io Data Access](https://crates.io/data-access)
- [Dart MCP Server](https://dart.dev/tools/mcp-server)

### Repositories
- [mcp-package-version](https://github.com/sammcj/mcp-package-version)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Dart MCP SDK](https://github.com/dart-lang/dart_mcp)

### API Endpoints
- **pub.dev:** `https://pub.dev/api/packages/<package-name>`
- **crates.io:** `https://crates.io/api/v1/crates/<crate-name>`

---

## 📝 Notes

### Technology Stack Priorities
1. **Flutter/Dart** - Primary mobile development
2. **Python** - Backend services ✅ (covered)
3. **TypeScript** - Backend services ✅ (covered)
4. **Rust** - Performance-critical components (future)

### Development Philosophy
- Domain modeling first approach
- Working backwards from end goal
- Prefer analogies for learning new concepts

### Decision Criteria
- **Maintainability:** Can we maintain this long-term?
- **Community:** Is there active development/support?
- **Integration:** How well does it fit our workflow?
- **Learning:** What skills do we gain?

---

## 🎓 Learning Opportunities

### If Contributing to mcp-package-version
- Go programming language
- API integration patterns
- Open source contribution workflow
- MCP protocol implementation

### If Building Separate Tools
- MCP server development in Dart/Rust
- Native ecosystem tooling
- Server architecture patterns

---

## 🤔 Open Questions

1. Is the mcp-package-version maintainer receptive to new registry additions?
2. What's the typical PR review timeline for the project?
3. Are there any architectural constraints for adding new registries?
4. Would a Dart/Rust implementation be preferred for native registries?
5. How do other developers handle multi-language dependency management?

---

## 📊 Success Metrics

### Definition of Done
- [ ] Can check latest versions for Flutter/Dart packages
- [ ] Can check latest versions for Rust packages
- [ ] Works seamlessly with existing Python/TypeScript checking
- [ ] Integrated into development workflow
- [ ] Documentation complete
- [ ] Tests passing

### Nice-to-Have
- [ ] Batch checking across all project dependencies
- [ ] Version constraint validation
- [ ] Upgrade path suggestions
- [ ] Breaking change warnings

---

*This document is a living tracker. Update regularly as progress is made.*
