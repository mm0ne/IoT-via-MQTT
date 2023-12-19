from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions


def create_instance(
    schema: str = "public", url: str = "", key: str = ""
) -> Client:
    supabase_instance = create_client(supabase_url=url, supabase_key=key, options=ClientOptions(schema=schema))
    supabase_instance.schema = schema

    return supabase_instance