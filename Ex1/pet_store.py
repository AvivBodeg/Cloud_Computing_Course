from flask import Flask, jsonify, request
import requests
import uuid

ANIMALS_URL = "https://api-ninjas.com/v1/animals"
KEY = 'pSgkQKYWrLDlQI0Sg3zmLQ==RrHpVdqh8aCzByaQ'
app = Flask(__name__)
pet_types = {}

@app.route('/pet-types', methods=['GET'])
def get_pet_types():
    try:
        return jsonify(list(pet_types.values())), 200
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"server error": str(e)}), 500


@app.route('/pets', methods=['POST'])
def add_pet_type():
    print("POST /pets")

    try:
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({"error": "Expected application/json"}), 415

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        if 'name' not in data:
            return jsonify({"error": "Missing required field: 'name'"}), 400

        print("Sending request to Animal API...")
        resp = requests.get(
            "https://api.api-ninjas.com/v1/animals",
            headers={"X-Api-Key": KEY},
            params={"name": data['name']}
        )

        print("API status code:", resp.status_code)
        print("API raw response:", resp.text[:200], "...")

        if resp.status_code != 200:
            return jsonify({"error": "Animal API request failed", "api_response": resp.text}), 502

        try:
            animals = resp.json()
        except Exception:
            return jsonify({"error": "API did not return JSON", "api_response": resp.text}), 502

        if not animals:
            return jsonify({"error": "No matching animals found from API"}), 404

        input_name = data["name"].lower()
        matched_animal = next(
            (a for a in animals if a.get("name", "").lower() == input_name),
            None
        )

        if not matched_animal:
            return jsonify({"error": f"No exact match found for '{data['name']}'"}), 404

        # 3. Create new pet entry
        newID = str(uuid.uuid4())
        taxonomy = matched_animal.get("taxonomy", {})
        pet_type = {
            "id": newID,
            "name": data["name"],
            "family": taxonomy.get("family"),
            "genus": taxonomy.get("genus")
        }

        pet_types[newID] = pet_type

        print("New pet added:", pet_type)

        return jsonify(pet_type), 201

    except Exception as e:
        print("Server Exception:", e)
        return jsonify({"server error": str(e)}), 500

if __name__ == "__main__":
    print("Starting pet_store.py")
    app.run(host='0.0.0.0', port=5001, debug=True)