from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class LLModelDetails(BaseModel):
    parent_model: str
    format: str
    family: str
    families: List[str]
    parameter_size: str
    quantization_level: str


class LLModel(BaseModel):
    name: Optional[str]
    model: Optional[str]
    modified_at: Optional[datetime]
    digest: Optional[str]
    size: Optional[int]
    details: Optional[LLModelDetails]


class LLModelsList(BaseModel):
    models: List[LLModel]


class LLMInformation(BaseModel):
    architecture: str = Field(alias="general.architecture")
    basename: str = Field(alias="general.basename")
    file_type: int = Field(alias="general.file_type")
    finetune: str = Field(alias="general.finetune")
    # Base model info
    base_model_count: int = Field(alias="general.base_model.count")
    # License info
    license: str = Field(alias="general.license")
    license_link: str = Field(alias="general.license.link")
    license_name: str = Field(alias="general.license.name")

    parameter_count: int = Field(alias="general.parameter_count")
    quantization_version: int = Field(alias="general.quantization_version")
    size_label: str = Field(alias="general.size_label")
    type: str = Field(alias="general.type")
    add_bos_token: bool = Field(alias="tokenizer.ggml.add_bos_token")
    bos_token_id: int = Field(alias="tokenizer.ggml.bos_token_id")
    eos_token_id: int = Field(alias="tokenizer.ggml.eos_token_id")
    merges: Optional[List] = Field(alias="tokenizer.ggml.merges", default=None)
    model: str = Field(alias="tokenizer.ggml.model")
    padding_token_id: int = Field(alias="tokenizer.ggml.padding_token_id")
    pre: str = Field(alias="tokenizer.ggml.pre")
    token_type: Optional[List] = Field(
        alias="tokenizer.ggml.token_type",
        default=None
    )
    tokens: Optional[List] = Field(
        alias="tokenizer.ggml.tokens",
        default=None
    )


class LLMFullDetails(BaseModel):
    """
    Full LLM details
    """
    system: str
    modified_at: str
    details: Optional[LLModelDetails]
    model_info: LLMInformation
    capabilities: List[str]
