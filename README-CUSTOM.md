# Zen MCP Server - Custom 3-Model Collaboration Configuration

This is a customized fork of [BeehiveInnovations/zen-mcp-server](https://github.com/BeehiveInnovations/zen-mcp-server) configured for exclusive use of the most capable AI models with automatic 3-model collaboration.

## Custom Configuration Features

### 🚀 Only Most Capable Models
This fork is configured to use ONLY the most advanced models from each provider:
- **OpenAI**: `gpt-5-latest` (400K context, 128K output)
- **Google**: `gemini-2.5-pro` (1M+ context)
- **X.AI**: `grok-4` (256K context, multimodal)

All lesser model variants are blocked to ensure consistent high-quality results.

### 🤝 Automatic 3-Model Collaboration
When `AUTO_CONSENSUS=true` is set, the system automatically:
- Consults all three models for important decisions
- Cross-verifies outputs between models
- Provides consensus-based recommendations
- Ensures maximum accuracy through multi-model validation

### 🔒 Model Restrictions
- **ALLOWED_MODELS**: Only permits `gpt-5-latest`, `gemini-2.5-pro`, and `grok-4`
- **DISABLED_MODELS**: Blocks all lesser variants (gpt-5, o3 series, gemini-flash, grok-3, etc.)
- Providers are hardcoded to always select their most capable model

## Quick Start

### 1. Clone This Fork
```bash
git clone https://github.com/TotalFreedomLife/zen-mcp-server.git
cd zen-mcp-server
```

### 2. Set Up Environment
```bash
# Copy the example .env file
cp .env .env.local

# Edit .env.local and add your API keys:
# GEMINI_API_KEY=your-actual-gemini-key
# OPENAI_API_KEY=your-actual-openai-key
# XAI_API_KEY=your-actual-xai-key
```

### 3. Install and Configure
```bash
# Run the setup script
./run-server.sh

# Or on Windows:
./run-server.ps1
```

### 4. Verify Configuration
```bash
# Test that only the most capable models are available
python test_configuration.py
```

## Configuration File (.env)

```env
# API Keys (all three required for 3-model collaboration)
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key
XAI_API_KEY=your-xai-api-key

# Model Configuration (pre-configured for best models only)
DEFAULT_MODEL=auto
ALLOWED_MODELS=gpt-5-latest,gemini-2.5-pro,grok-4
DISABLED_MODELS=gpt-5,gpt-5-mini,gpt-5-nano,o3,o3-mini,o3-pro,o4-mini,gemini-2.5-flash,grok-3,grok-3-fast

# 3-Model Collaboration (enable for automatic consensus)
AUTO_CONSENSUS=true
CONSENSUS_MODELS=gpt-5-latest,gemini-2.5-pro,grok-4

# Thinking Mode (high for maximum reasoning depth)
DEFAULT_THINKING_MODE_THINKDEEP=high
```

## What's Changed from Original

### Provider Modifications
1. **OpenAI Provider** (`providers/openai_provider.py`)
   - Added `gpt-5-latest` as primary model
   - Removed all other GPT-5 variants and O3/O4 models
   - `get_preferred_model()` always returns `gpt-5-latest`

2. **Gemini Provider** (`providers/gemini.py`)
   - Configured to always use `gemini-2.5-pro`
   - Removed preference logic for Flash models
   - `get_preferred_model()` always returns `gemini-2.5-pro`

3. **X.AI Provider** (`providers/xai.py`)
   - Configured to always use `grok-4`
   - Removed fallback to grok-3 variants
   - `get_preferred_model()` always returns `grok-4`

### Configuration Updates
- **config.py**: Added `AUTO_CONSENSUS`, `CONSENSUS_MODELS`, `ALLOWED_MODELS`, `DISABLED_MODELS`
- **model_restrictions.py**: Enhanced with global allowed/disabled model lists
- **CLAUDE.md**: Added documentation for 3-model collaboration setup

### Testing
- **test_configuration.py**: New test script to verify model restrictions and configuration

## Usage with Claude

Once configured, use naturally with Claude:

```
# Claude automatically selects the best model for each task
"Use zen to analyze this architecture"

# Or specify models explicitly
"Use zen with gpt-5-latest to review this code"
"Get consensus from all three models on this API design"

# Automatic 3-model collaboration (when AUTO_CONSENSUS=true)
"Perform a code review with zen" # Automatically consults all 3 models
```

## Benefits of This Configuration

1. **Maximum Capability**: Always uses the most advanced model from each provider
2. **Cross-Verification**: Three different AI architectures validate each other's outputs
3. **No Compromise**: Blocks all lesser models to prevent quality degradation
4. **Automatic Collaboration**: No need to manually coordinate between models
5. **Cost Optimization**: While using premium models, the restriction prevents accidental use of multiple lesser models

## Syncing with Upstream

To get updates from the original repository while keeping your customizations:

```bash
# Add upstream remote (one-time setup)
git remote add upstream https://github.com/BeehiveInnovations/zen-mcp-server.git

# Fetch and merge updates
git fetch upstream
git checkout main
git merge upstream/main

# Resolve any conflicts, keeping your custom configurations
# Then push to your fork
git push origin main
```

## License

This fork maintains the Apache 2.0 License from the original [BeehiveInnovations/zen-mcp-server](https://github.com/BeehiveInnovations/zen-mcp-server).

## Credits

Original Zen MCP Server by [BeehiveInnovations](https://github.com/BeehiveInnovations) - Fahad Gilani and contributors.

Custom 3-model collaboration configuration by [TotalFreedomLife](https://github.com/TotalFreedomLife).

---

*This configuration ensures you're always using the cutting edge of AI capability with automatic cross-validation between the three most powerful models available.*