from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions


def create_instance(
    schema: str = "public", url: str = "https://lunlukxreicvgpvkwxys.supabase.co", key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx1bmx1a3hyZWljdmdwdmt3eHlzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMTQwMTYxMiwiZXhwIjoyMDE2OTc3NjEyfQ.y9oOdw44Vp3I-_L7iiAl1kZthZxG9tO5-ah55PBKB6U"
) -> Client:
    supabase_instance = create_client(supabase_url=url, supabase_key=key, options=ClientOptions(schema=schema))
    supabase_instance.schema = schema

    return supabase_instance