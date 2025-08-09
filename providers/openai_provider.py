"""OpenAI model provider implementation."""

import logging
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from tools.models import ToolModelCategory

from .base import (
    ModelCapabilities,
    ModelResponse,
    ProviderType,
    create_temperature_constraint,
)
from .openai_compatible import OpenAICompatibleProvider

logger = logging.getLogger(__name__)


class OpenAIModelProvider(OpenAICompatibleProvider):
    """Official OpenAI API provider (api.openai.com)."""

    # Model configurations using ModelCapabilities objects
    SUPPORTED_MODELS = {
        "gpt-5-latest": ModelCapabilities(
            provider=ProviderType.OPENAI,
            model_name="gpt-5-latest",
            friendly_name="OpenAI (GPT-5 Latest)",
            context_window=400_000,  # 400K tokens
            max_output_tokens=128_000,  # 128K max output tokens
            supports_extended_thinking=True,  # Supports reasoning tokens
            supports_system_prompts=True,
            supports_streaming=True,
            supports_function_calling=True,
            supports_json_mode=True,
            supports_images=True,  # GPT-5 supports vision
            max_image_size_mb=20.0,  # 20MB per OpenAI docs
            supports_temperature=True,  # Regular models accept temperature parameter
            temperature_constraint=create_temperature_constraint("fixed"),
            description="GPT-5 Latest (400K context, 128K output) - Most advanced GPT-5 model with reasoning support",
            aliases=["gpt5-latest", "gpt-5-latest", "gpt5", "gpt-5", "openai"],
        ),
        "gpt-4.1": ModelCapabilities(
            provider=ProviderType.OPENAI,
            model_name="gpt-4.1",
            friendly_name="OpenAI (GPT 4.1)",
            context_window=1_000_000,  # 1M tokens
            max_output_tokens=32_768,
            supports_extended_thinking=False,
            supports_system_prompts=True,
            supports_streaming=True,
            supports_function_calling=True,
            supports_json_mode=True,
            supports_images=True,  # GPT-4.1 supports vision
            max_image_size_mb=20.0,  # 20MB per OpenAI docs
            supports_temperature=True,  # Regular models accept temperature parameter
            temperature_constraint=create_temperature_constraint("range"),
            description="GPT-4.1 (1M context) - Advanced reasoning model with large context window",
            aliases=["gpt4.1", "gpt-4.1"],
        ),
    }

    def __init__(self, api_key: str, **kwargs):
        """Initialize OpenAI provider with API key."""
        # Set default OpenAI base URL, allow override for regions/custom endpoints
        kwargs.setdefault("base_url", "https://api.openai.com/v1")
        super().__init__(api_key, **kwargs)

    def get_capabilities(self, model_name: str) -> ModelCapabilities:
        """Get capabilities for a specific OpenAI model."""
        # First check if it's a key in SUPPORTED_MODELS
        if model_name in self.SUPPORTED_MODELS:
            # Check if model is allowed by restrictions
            from utils.model_restrictions import get_restriction_service

            restriction_service = get_restriction_service()
            if not restriction_service.is_allowed(ProviderType.OPENAI, model_name, model_name):
                raise ValueError(f"OpenAI model '{model_name}' is not allowed by restriction policy.")
            return self.SUPPORTED_MODELS[model_name]

        # Try resolving as alias
        resolved_name = self._resolve_model_name(model_name)

        # Check if resolved name is a key
        if resolved_name in self.SUPPORTED_MODELS:
            # Check if model is allowed by restrictions
            from utils.model_restrictions import get_restriction_service

            restriction_service = get_restriction_service()
            if not restriction_service.is_allowed(ProviderType.OPENAI, resolved_name, model_name):
                raise ValueError(f"OpenAI model '{model_name}' is not allowed by restriction policy.")
            return self.SUPPORTED_MODELS[resolved_name]

        # Finally check if resolved name matches any API model name
        for key, capabilities in self.SUPPORTED_MODELS.items():
            if resolved_name == capabilities.model_name:
                # Check if model is allowed by restrictions
                from utils.model_restrictions import get_restriction_service

                restriction_service = get_restriction_service()
                if not restriction_service.is_allowed(ProviderType.OPENAI, key, model_name):
                    raise ValueError(f"OpenAI model '{model_name}' is not allowed by restriction policy.")
                return capabilities

        raise ValueError(f"Unsupported OpenAI model: {model_name}")

    def get_provider_type(self) -> ProviderType:
        """Get the provider type."""
        return ProviderType.OPENAI

    def validate_model_name(self, model_name: str) -> bool:
        """Validate if the model name is supported and allowed."""
        resolved_name = self._resolve_model_name(model_name)

        # First check if model is supported
        if resolved_name not in self.SUPPORTED_MODELS:
            return False

        # Then check if model is allowed by restrictions
        from utils.model_restrictions import get_restriction_service

        restriction_service = get_restriction_service()
        if not restriction_service.is_allowed(ProviderType.OPENAI, resolved_name, model_name):
            logger.debug(f"OpenAI model '{model_name}' -> '{resolved_name}' blocked by restrictions")
            return False

        return True

    def generate_content(
        self,
        prompt: str,
        model_name: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_output_tokens: Optional[int] = None,
        **kwargs,
    ) -> ModelResponse:
        """Generate content using OpenAI API with proper model name resolution."""
        # Resolve model alias before making API call
        resolved_model_name = self._resolve_model_name(model_name)

        # Call parent implementation with resolved model name
        return super().generate_content(
            prompt=prompt,
            model_name=resolved_model_name,
            system_prompt=system_prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            **kwargs,
        )

    def supports_thinking_mode(self, model_name: str) -> bool:
        """Check if the model supports extended thinking mode."""
        # GPT-5 models support reasoning tokens (extended thinking)
        resolved_name = self._resolve_model_name(model_name)
        if resolved_name in ["gpt-5-latest"]:
            return True
        return False

    def get_preferred_model(self, category: "ToolModelCategory", allowed_models: list[str]) -> Optional[str]:
        """Get OpenAI's preferred model for a given category from allowed models.

        Args:
            category: The tool category requiring a model
            allowed_models: Pre-filtered list of models allowed by restrictions

        Returns:
            Preferred model name or None
        """
        from tools.models import ToolModelCategory

        if not allowed_models:
            return None

        # Always return gpt-5-latest if it's in the allowed models
        if "gpt-5-latest" in allowed_models:
            return "gpt-5-latest"
        
        # Fallback to first allowed model if gpt-5-latest is not available
        return allowed_models[0] if allowed_models else None
