import requests
import json

API_KEY = "93ad87fb7e48f54a5154ad1af1412a6d"  # Insert your actual The Graph API key
SUBGRAPH_ID = "5nwMCSHaTqG3Kd2gHznbTXEnZ9QNWsssQfbHhDqQSQFp"

url = f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/{SUBGRAPH_ID}"

query = """
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

response = requests.post(url, json={"query": query})
if response.status_code == 200:
    with open("compound_v3_introspection.json", "w") as f:
        json.dump(response.json(), f, indent=2)
    print("Schema saved to compound_v3_introspection.json")
else:
    print(f"Failed: {response.status_code} {response.text}")
