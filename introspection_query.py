import requests
import json

# Replace these with your actual The Graph API key and subgraph IDs
API_KEY = "93ad87fb7e48f54a5154ad1af1412a6d"

V2_SUBGRAPH_ID = "4TbqVA8p2DoBd5qDbPMwmDZv3CsJjWtxo8nVSqF2tA9a"
V3_SUBGRAPH_ID = "AwoxEZbiWLvv6e3QdvdMZw4WDURdGbvPfHmZRc8Dpfz9"

INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    types {
      name
      description
      kind
      fields {
        name
        description
        args {
          name
          description
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
          defaultValue
        }
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        name
      }
      interfaces {
        name
      }
      enumValues {
        name
      }
      possibleTypes {
        name
      }
    }
  }
}
"""

def run_introspection(api_key, subgraph_id):
    url = f"https://gateway.thegraph.com/api/{api_key}/subgraphs/id/{subgraph_id}"
    response = requests.post(url, json={"query": INTROSPECTION_QUERY})
    if response.status_code == 200:
        # Parse JSON response and pretty-print
        schema_json = response.json()
        pretty_schema_str = json.dumps(schema_json, indent=2)
        
        return pretty_schema_str
    else:
        print(f"Failed to fetch schema for {subgraph_id}. Status code: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    print("\n--- V2 Subgraph Schema ---\n")
    v2_schema = run_introspection(API_KEY, V2_SUBGRAPH_ID)
    if v2_schema:
        print(v2_schema)
        with open("schema_v2.json", "w") as f:
            f.write(v2_schema)

    print("\n--- V3 Subgraph Schema ---\n")
    v3_schema = run_introspection(API_KEY, V3_SUBGRAPH_ID)
    if v3_schema:
        print(v3_schema)
        with open("schema_v3.json", "w") as f:
            f.write(v3_schema)
