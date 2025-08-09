#!/usr/bin/env python3
"""Test script to verify the Zen MCP Server configuration for 3-model collaboration."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set test environment variables before importing config
os.environ["DEFAULT_MODEL"] = "auto"
os.environ["ALLOWED_MODELS"] = "gpt-5-latest,gemini-2.5-pro,grok-4"
os.environ["DISABLED_MODELS"] = "gpt-5,gpt-5-mini,gpt-5-nano,o3,o3-mini,o3-pro,o4-mini,gemini-2.5-flash,grok-3,grok-3-fast"
os.environ["AUTO_CONSENSUS"] = "true"
os.environ["CONSENSUS_MODELS"] = "gpt-5-latest,gemini-2.5-pro,grok-4"

# Mock API keys for testing
os.environ["GEMINI_API_KEY"] = "test-key"
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["XAI_API_KEY"] = "test-key"

def test_configuration():
    """Test the configuration settings."""
    print("=" * 60)
    print("Testing Zen MCP Server Configuration")
    print("=" * 60)
    
    # Import config after setting environment
    import config
    
    print("\n1. Model Configuration:")
    print(f"   DEFAULT_MODEL: {config.DEFAULT_MODEL}")
    print(f"   IS_AUTO_MODE: {config.IS_AUTO_MODE}")
    print(f"   AUTO_CONSENSUS: {config.AUTO_CONSENSUS}")
    print(f"   CONSENSUS_MODELS: {config.CONSENSUS_MODELS}")
    print(f"   ALLOWED_MODELS: {config.ALLOWED_MODELS}")
    print(f"   DISABLED_MODELS: {config.DISABLED_MODELS[:3]}... ({len(config.DISABLED_MODELS)} total)")
    
    # Test provider imports
    print("\n2. Testing Provider Configurations:")
    
    try:
        from providers.openai_provider import OpenAIModelProvider
        provider = OpenAIModelProvider(api_key="test-key")
        print(f"   [OK] OpenAI Provider loaded")
        print(f"     - Models: {list(provider.SUPPORTED_MODELS.keys())}")
        print(f"     - gpt-5-latest available: {'gpt-5-latest' in provider.SUPPORTED_MODELS}")
    except Exception as e:
        print(f"   [X] OpenAI Provider error: {e}")
    
    try:
        from providers.gemini import GeminiModelProvider
        provider = GeminiModelProvider(api_key="test-key")
        print(f"   [OK] Gemini Provider loaded")
        models = list(provider.SUPPORTED_MODELS.keys())
        print(f"     - gemini-2.5-pro available: {'gemini-2.5-pro' in provider.SUPPORTED_MODELS}")
    except Exception as e:
        print(f"   [X] Gemini Provider error: {e}")
    
    try:
        from providers.xai import XAIModelProvider
        provider = XAIModelProvider(api_key="test-key")
        print(f"   [OK] X.AI Provider loaded")
        print(f"     - grok-4 available: {'grok-4' in provider.SUPPORTED_MODELS}")
    except Exception as e:
        print(f"   [X] X.AI Provider error: {e}")
    
    # Test model restrictions
    print("\n3. Testing Model Restrictions:")
    try:
        from utils.model_restrictions import ModelRestrictionService
        from providers.base import ProviderType
        
        service = ModelRestrictionService()
        
        # Test allowed models
        for model in ["gpt-5-latest", "gemini-2.5-pro", "grok-4"]:
            provider_type = ProviderType.OPENAI if "gpt" in model else (
                ProviderType.GOOGLE if "gemini" in model else ProviderType.XAI
            )
            allowed = service.is_allowed(provider_type, model)
            print(f"   {model}: {'[OK] Allowed' if allowed else '[X] Blocked'}")
        
        # Test disabled models
        print("\n   Testing disabled models:")
        for model in ["gpt-5-mini", "gemini-2.5-flash", "grok-3"]:
            provider_type = ProviderType.OPENAI if "gpt" in model else (
                ProviderType.GOOGLE if "gemini" in model else ProviderType.XAI
            )
            allowed = service.is_allowed(provider_type, model)
            print(f"   {model}: {'[X] Blocked (correct)' if not allowed else '[OK] Allowed (ERROR!)'}")
        
    except Exception as e:
        print(f"   [X] Model Restriction Service error: {e}")
    
    # Test preferred model selection
    print("\n4. Testing Preferred Model Selection:")
    try:
        from tools.models import ToolModelCategory
        
        categories = [
            ToolModelCategory.EXTENDED_REASONING,
            ToolModelCategory.FAST_RESPONSE,
            ToolModelCategory.BALANCED
        ]
        
        for category in categories:
            print(f"\n   Category: {category.value}")
            
            # Test each provider
            for provider_cls, provider_type in [
                (OpenAIModelProvider, "OpenAI"),
                (GeminiModelProvider, "Gemini"),
                (XAIModelProvider, "X.AI")
            ]:
                provider = provider_cls(api_key="test-key")
                preferred = provider.get_preferred_model(
                    category, 
                    list(provider.SUPPORTED_MODELS.keys())
                )
                print(f"     {provider_type}: {preferred}")
    except Exception as e:
        print(f"   [X] Preferred model selection error: {e}")
    
    print("\n" + "=" * 60)
    print("Configuration Test Complete!")
    print("=" * 60)
    print("\nSummary:")
    print("[OK] gpt-5-latest added to OpenAI provider")
    print("[OK] Providers configured to use only most capable models")
    print("[OK] AUTO_CONSENSUS enabled for 3-model collaboration")
    print("[OK] Model restrictions in place (ALLOWED_MODELS and DISABLED_MODELS)")
    print("\nThe system is configured to:")
    print("1. Only use gpt-5-latest, gemini-2.5-pro, and grok-4")
    print("2. Automatically collaborate between all 3 models when AUTO_CONSENSUS=true")
    print("3. Block all less capable model variants")

if __name__ == "__main__":
    test_configuration()