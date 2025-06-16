"""
Configurações globais do Sistema RAG
"""
import os
from typing import Optional
from dataclasses import dataclass


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
    vendor_multimodal_model: str = "openai-gpt4o"
    max_wait_time: int = 300
    poll_interval: int = 5


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


# Instância global das configurações
settings = GlobalSettings()