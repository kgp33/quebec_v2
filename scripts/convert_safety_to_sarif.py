import json
import sys

def convert_safety_to_sarif(safety_json, sarif_file):
    #read json results of safety scan from workflow
    try:
        with open(safety_json, 'r') as f:
            safety_data = json.load(f)
    except FileNotFoundError:
            print(f"Error: The file {safety_json} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {safety_json} was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {safety_json}.")
        sys.exit(1)
    
    #just want to see the json data
    print("Safety JSON structure:", safety_data)

    #setting up the data structure to hold the results of the safety scan
    sarif_data = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Safety",
                        "version": "1.0"
                    }
                },
                "results": []
            }
        ]
    }

    #checking to see if vulnerabilities exists in the safety data
    issues = safety_data.get('vulnerabilities', safety_data.get('issues', []))

    if not issues:
        print("No issues found in the Safety JSON. Skipping SARIF conversion.")
        sys.exit(0)

    for issue in safety_data.get('vulnerabilities', []):
        #want to handle issues with data appropriately
        #mark rule_id as 'UNKNOWN' if vuln_id is missing
        rule_id = issue.get('vuln_id', 'UNKNOWN')
        description = issue.get('description', 'No description available.')
        package_name = issue.get('package_name', 'Unknown package')
        #default to 'LOW' if no severity is provided
        severity = issue.get('severity', 'LOW').upper()

        #placeholder for line number if available in the issue data
        start_line = issue.get('line', 1)
    
        #converting the results of safety scan to sarif format
        sarif_data['runs'][0]['results'].append({
            "ruleId": rule_id,
            "message": {
                "text": description
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": package_name
                        },
                        "region": {
                            "startLine": start_line
                        }
                    }
                }
            ],
            "severity": severity
        })
    
    #write the data into the the sarif file that will get uploaded
    try:
        with open(sarif_file, 'w') as f:
            json.dump(sarif_data, f, indent=2)
        print(f"Converted Safety results to SARIF and saved to {sarif_file}")
    except IOError:
        print(f"Error: Failed to write to {sarif_file}.")
        sys.exit(1)

if __name__ == "__main__":
    #confirm number of arguments
    if len(sys.argv) != 3:
        print("Usage: python convert_safety_to_sarif.py <input_json> <output_sarif>")
        sys.exit(1)

    #get input and output file paths
    safety_json = sys.argv[1]
    sarif_file = sys.argv[2]
    
    #run the function
    convert_safety_to_sarif(safety_json, sarif_file)
