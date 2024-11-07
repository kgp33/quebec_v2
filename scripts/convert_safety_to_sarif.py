import json
import sys
import os

def load_requirements(requirements_file):
    with open(requirements_file, 'r') as f:
        lines = f.readlines()
    return [
        line.strip()
        for line in lines
        if line.strip()
    ]

def find_files_for_package(package_name, source_dir="src"):
    matched_files = []
    # Traverse the source directory
    for root, subdirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):  # Look for Python files
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if package_name in content:  # Search for import of the package
                        matched_files.append(os.path.relpath(os.path.join(root, file)))
    return matched_files

def convert_safety_to_sarif(safety_json, sarif_file, requirements_file):
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

    dependencies = load_requirements(requirements_file)
    
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

    vulns = []

    # Traverse through the projects and dependencies to check for vulnerabilities
    for project in safety_data.get('scan_results', {}).get('projects', []):
        for file in project.get('files', []):
            for dependency in file.get('results', {}).get('dependencies', []):
                #get the known vulnerabilities for each dependency
                for specification in dependency.get('specifications', []):
                    #extract package
                    raw_spec = specification.get('raw', None)
                    if raw_spec:
                        package_name = raw_spec.split('==')[0]
                        package_version = raw_spec.split('==')[1]
                    
                    known_vulnerabilities = specification.get('vulnerabilities', {}).get('known_vulnerabilities', [])
                    if known_vulnerabilities:
                        for vuln in known_vulnerabilities:
                            vulns.append({
                                'id': vuln.get('id', 'UNKNOWN'),
                                'description': vuln.get('description', 'No description available.'),
                                'package_name': package_name,
                                'package_version': package_version,
                                'severity': vuln.get('severity', 'LOW').upper(),
                                'line': vuln.get('line', 1),
                                'vulnerable_spec': vuln.get('vulnerable_spec', ''),
                                'rule_id': vuln.get('id', 'UNKNOWN'),
                            })



                        vulns.extend(known_vulnerabilities)

    if not vulns:
        print("No vulnerabilities found in the Safety JSON. Skipping SARIF conversion.")
        sys.exit(0)

    for vuln in vulns:
        print(f"Processing vulnerability: {vuln}")

        if f"{vuln['package_name']}=={vuln['package_version']}" in dependencies:
            matched_files = find_files_for_package(vuln['package_name'], source_dir="src")

            #converting the results of safety scan to sarif format
            for matched_file in matched_files:
                uri_value = f"file://{os.path.abspath(matched_file)}"
                sarif_data['runs'][0]['results'].append({
                    "ruleId": vuln['rule_id'],
                    "message": {
                        "text": vuln['description']
                    },
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {
                                    "uri": uri_value
                                },
                                "region": {
                                    "startLine": vuln['line']
                                }
                            }
                        }
                    ],
                    "properties": {
                        "severity": vuln['severity']
                    },
                    "packageName": f"{vuln['package_name']}=={vuln['package_version']}"
                })
        else:
            print(f"Package '{package_name}' is not in the requirements.txt. Skipping SARIF entry.")
    
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
    if len(sys.argv) != 4:
        print("Usage: python convert_safety_to_sarif.py <input_json> <output_sarif> <requirements.txt>")
        sys.exit(1)

    #get input and output file paths
    safety_json = sys.argv[1]
    sarif_file = sys.argv[2]
    requirements_file = sys.argv[3]
    
    #run the function
    convert_safety_to_sarif(safety_json, sarif_file, requirements_file)
