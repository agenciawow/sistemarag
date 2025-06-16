"""
Configurações globais do Sistema RAG
"""
import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


@dataclass
class APISettings:
    """Configurações das APIs externas"""
    openai_api_key: Optional[str] = None
    voyage_api_key: Optional[str] = None
    llama_cloud_api_key: Optional[str] = None
    astra_db_token: Optional[str] = None
    astra_db_api_endpoint: Optional[str] = None
    r2_endpoint: Optional[str] = None
    r2_auth_token: Optional[str] = None

    def __post_init__(self):
        """Carrega variáveis de ambiente se não fornecidas"""
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.voyage_api_key:
            self.voyage_api_key = os.getenv("VOYAGE_API_KEY")
        if not self.llama_cloud_api_key:
            self.llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        if not self.astra_db_token:
            self.astra_db_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        if not self.astra_db_api_endpoint:
            self.astra_db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
        if not self.r2_endpoint:
            self.r2_endpoint = os.getenv("R2_ENDPOINT")
        if not self.r2_auth_token:
            self.r2_auth_token = os.getenv("R2_AUTH_TOKEN")


@dataclass
class LlamaParseSettings:
    """Configurações do LlamaParse"""
    api_endpoint: str = "https://api.cloud.llamaindex.ai/"
    parse_mode: str = "parse_page_with_agent"
    output_format: str = "markdown"
    take_screenshot: bool = True
    # Configurações do modo multimodal (gera screenshots automaticamente)
    use_vendor_multimodal_model: bool = True
    vendor_multimodal_model_name: str = "anthropic-sonnet-3.5"
    vendor_multimodal_api_key: Optional[str] = None
    max_wait_time: int = 300
    poll_interval: int = 5
    
    def __post_init__(self):
        """Carrega chave do modelo multimodal se não fornecida"""
        if not self.vendor_multimodal_api_key:
            # Tentar diferentes variáveis de ambiente baseadas no modelo
            if "anthropic" in self.vendor_multimodal_model_name.lower():
                self.vendor_multimodal_api_key = os.getenv("ANTHROPIC_API_KEY")
            elif "openai" in self.vendor_multimodal_model_name.lower():
                self.vendor_multimodal_api_key = os.getenv("OPENAI_API_KEY")
            elif "gemini" in self.vendor_multimodal_model_name.lower():
                self.vendor_multimodal_api_key = os.getenv("GOOGLE_API_KEY")


@dataclass
class VoyageSettings:
    """Configurações do Voyage AI"""
    api_endpoint: str = "https://api.voyageai.com/v1/multimodalembeddings"
    model: str = "voyage-multimodal-3"
    batch_size: int = 10
    max_text_length: int = 5000


@dataclass
class AstraDBSettings:
    """Configurações do Astra DB"""
    keyspace: str = "default_keyspace"
    collection_name: str = "agenciawow"
    batch_size: int = 50
    max_text_length: int = 7000


@dataclass
class CloudflareR2Settings:
    """Configurações do Cloudflare R2"""
    timeout: int = 60
    replace_existing: bool = True
    keep_original_base64: bool = False


@dataclass
class OpenAIModelSettings:
    """Configurações dos modelos OpenAI"""
    # Modelo para reranking
    rerank_model: str = "gpt-4o"
    
    # Modelo para query transformation
    query_transform_model: str = "gpt-4o-mini"
    
    # Modelo para geração de respostas finais
    answer_generation_model: str = "gpt-4o"
    
    # Modelo para extração de dados estruturados
    extraction_model: str = "gpt-4o"
    
    # Temperaturas para cada uso
    rerank_temperature: float = 0.1
    query_transform_temperature: float = 0.3
    answer_generation_temperature: float = 0.7
    extraction_temperature: float = 0.1
    
    def __post_init__(self):
        """Carrega modelos das variáveis de ambiente se definidas"""
        self.rerank_model = os.getenv("OPENAI_RERANK_MODEL", self.rerank_model)
        self.query_transform_model = os.getenv("OPENAI_QUERY_TRANSFORM_MODEL", self.query_transform_model)
        self.answer_generation_model = os.getenv("OPENAI_ANSWER_GENERATION_MODEL", self.answer_generation_model)
        self.extraction_model = os.getenv("OPENAI_EXTRACTION_MODEL", self.extraction_model)
        
        # Temperaturas
        if os.getenv("OPENAI_RERANK_TEMPERATURE"):
            self.rerank_temperature = float(os.getenv("OPENAI_RERANK_TEMPERATURE"))
        if os.getenv("OPENAI_QUERY_TRANSFORM_TEMPERATURE"):
            self.query_transform_temperature = float(os.getenv("OPENAI_QUERY_TRANSFORM_TEMPERATURE"))
        if os.getenv("OPENAI_ANSWER_GENERATION_TEMPERATURE"):
            self.answer_generation_temperature = float(os.getenv("OPENAI_ANSWER_GENERATION_TEMPERATURE"))
        if os.getenv("OPENAI_EXTRACTION_TEMPERATURE"):
            self.extraction_temperature = float(os.getenv("OPENAI_EXTRACTION_TEMPERATURE"))


@dataclass
class GlobalSettings:
    """Configurações globais do sistema"""
    session_id: str = "123456"
    temp_dir: str = "/tmp/sistema_rag"
    max_file_size_mb: int = 100
    request_timeout: int = 30
    
    # Configurações dos componentes
    api: APISettings = None
    llama_parse: LlamaParseSettings = None
    voyage: VoyageSettings = None
    astra_db: AstraDBSettings = None
    cloudflare_r2: CloudflareR2Settings = None
    openai_models: OpenAIModelSettings = None

    def __post_init__(self):
        """Inicializa sub-configurações se não fornecidas"""
        if self.api is None:
            self.api = APISettings()
        if self.llama_parse is None:
            self.llama_parse = LlamaParseSettings()
        if self.voyage is None:
            self.voyage = VoyageSettings()
        if self.astra_db is None:
            self.astra_db = AstraDBSettings()
        if self.cloudflare_r2 is None:
            self.cloudflare_r2 = CloudflareR2Settings()
        if self.openai_models is None:
            self.openai_models = OpenAIModelSettings()


# Instância global das configurações
settings = GlobalSettings()