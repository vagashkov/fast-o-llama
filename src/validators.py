from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class LLModelDetails(BaseModel):
    parent_model: Optional[str]
    format: Optional[str]
    family: Optional[str]
    families: Optional[List[str]]
    parameter_size: Optional[str]
    quantization_level: Optional[str]


class LLModel(BaseModel):
    name: Optional[str]
    model: Optional[str]
    modified_at: Optional[datetime]
    digest: Optional[str]
    size: Optional[int]
    details: Optional[LLModelDetails]


class LLMInformation(BaseModel):
    architecture: Optional[str]
    file_type: Optional[int]
    parameter_count: Optional[int]
    quantization_version: Optional[int]
    attention_head_count: Optional[int]
    attention_head_count_kv: Optional[int]
    attention_layer_norm_rms_epsilon: Optional[float]
    block_count: Optional[int]
    context_length: Optional[int]
    embedding_length: Optional[int]
    feed_forward_length: Optional[int]
    rope_dimension_count: Optional[int]
    rope_freq_base: Optional[int]
    vocab_size: Optional[int]
    ggml_bos_token_id: Optional[int]
    ggml_eos_token_id: Optional[int]
    ggml_merges: Optional[List]
    ggml_model: Optional[str]
    ggml_pre: Optional[str]
    ggml_token_type: Optional[List]
    ggml_tokens: Optional[List]
