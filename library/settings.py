"""Settings for the project."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class EmbeddingsSettings:
    """Settings for embeddings configuration."""
    round_decimals: int


@dataclass_json
@dataclass
class BaseModelSettings:
    """Settings for the base model defaults."""
    base_dim: int
    distilled_dim: int
    embeddings: EmbeddingsSettings = field(
        default_factory=EmbeddingsSettings)  # type: ignore


@dataclass_json
@dataclass
class LanguageModelSettings:
    """Settings for a specific language model."""
    name: str
    base_dim: int
    distilled_dim: int
    embeddings: EmbeddingsSettings = field(
        default_factory=EmbeddingsSettings)  # type: ignore


@dataclass_json
@dataclass
class LanguageSettings:
    """Settings for a specific language configuration."""
    type: str
    code: str
    model: LanguageModelSettings


@dataclass_json
@dataclass
class ModelsSettings:
    """Settings for models configuration."""
    dir: str
    defaults: BaseModelSettings


@dataclass_json
@dataclass
class IconsSettings:
    """Settings for icons configuration."""
    source_file: str
    stripped_file: str
    translations_file: str
    embeddings_file: str


@dataclass_json
@dataclass
class SynonymsSettings:
    """Settings for synonyms generation configuration."""
    count: int


@dataclass_json
@dataclass
class TranslationSettings:
    """Settings for translation configuration."""
    file: str
    model: str
    context_window: int
    max_tokens: int


@dataclass_json
@dataclass
class ProjectSettings:
    """Top-level project settings that match the YAML structure."""
    models: ModelsSettings = field(
        default_factory=ModelsSettings)  # type: ignore
    icons: IconsSettings = field(default_factory=IconsSettings)  # type: ignore
    synonyms: SynonymsSettings = field(
        default_factory=SynonymsSettings)  # type: ignore
    translation: TranslationSettings = field(
        default_factory=TranslationSettings)  # type: ignore
    languages: List[LanguageSettings] = field(default_factory=list)


@dataclass_json
@dataclass
class PrepareModelSettings:
    """Settings specifically for the prepare_models.py script."""
    models: ModelsSettings = field(
        default_factory=ModelsSettings)  # type: ignore
    languages: List[LanguageSettings] = field(default_factory=list)

    def get_dimensions_for_language(
        self, language_code: str
    ) -> tuple[int, int]:
        """Get the base and small dimensions for a specific language."""
        # First check language-specific settings
        for lang in self.languages:
            if lang.code == language_code:
                return lang.model.base_dim, lang.model.distilled_dim

        # Fall back to model defaults
        return (self.models.defaults.base_dim,
                self.models.defaults.distilled_dim)
