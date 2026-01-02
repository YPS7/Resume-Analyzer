import requests
import json

BASE_URL = "http://localhost:8080/api"

def test_resume_analysis():
    print("1. Creating Resume...")
    resume_payload = {
        "contentText": "Experienced Java Developer with 5 years of experience in Spring Boot, Microservices, and SQL.",
        "sourceType": "TEST_SCRIPT",
        "checksum": "12345"
    }
    
    try:
        resume_response = requests.post(f"{BASE_URL}/resumes", json=resume_payload)
        resume_response.raise_for_status()
        resume_data = resume_response.json()
        resume_id = resume_data.get("id")
        print(f"   Success! Resume ID: {resume_id}")
    except Exception as e:
        print(f"   Failed to create resume: {e}")
        try:
            print(f"   Response: {resume_response.text}")
        except:
            pass
        return

    print("\n2. Creating Job Description...")
    jd_payload = {
        "title": "Senior Java Engineer",
        "contentText": "We are looking for a Senior Java Engineer with strong Spring Boot and Microservices skills. SQL experience is required.",
        "checksum": "67890"
    }

    try:
        jd_response = requests.post(f"{BASE_URL}/job-descriptions", json=jd_payload)
        jd_response.raise_for_status()
        jd_data = jd_response.json()
        jd_id = jd_data.get("id")
        print(f"   Success! JD ID: {jd_id}")
    except Exception as e:
        print(f"   Failed to create JD: {e}")
        try:
            print(f"   Response: {jd_response.text}")
        except:
            pass
        return

    print("\n3. Analyzing Match...")
    try:
        analyze_url = f"{BASE_URL}/analyze?resumeId={resume_id}&jdId={jd_id}"
        analyze_response = requests.post(analyze_url)
        analyze_response.raise_for_status()
        result = analyze_response.json()
        print("   Success! Analysis Result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"   Failed to analyze: {e}")
        try:
            print(f"   Response: {analyze_response.text}")
        except:
            pass

if __name__ == "__main__":
    test_resume_analysis()
