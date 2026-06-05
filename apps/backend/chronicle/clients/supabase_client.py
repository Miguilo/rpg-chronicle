import os
from functools import lru_cache
from supabase import Client, create_client


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    
    supabase_url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

    return create_client(supabase_url, supabase_key)