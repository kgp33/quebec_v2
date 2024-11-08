import json
import sys
import os
import hashlib


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
    package_name = package_name.lower()
    #go through the source directory
    for root, subdirs, files in os.walk(source_dir):
        for file in files:
            #only care about python files
            if file.endswith(".py"):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    #specifically looking for "import" statements
                    if f"import {package_name}" in content.lower() or f"from {package_name} import" in content.lower():
                        matched_files.append(os.path.relpath(os.path.join(root, file)))
    return matched_files

def generate_fingerprint(uri, line):
    #combine the file path and line number to create a unique fingerprint (this is required by sarif format)
    data = f"{uri}-{line}".encode('utf-8')
    return hashlib.sha256(data).hexdigest()

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

    #we're looking at the requirements file
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
    processed_vulnerabilities = {}

    #traversing through the projects and dependencies to check for vulnerabilities
    for project in safety_data.get('scan_results', {}).get('projects', []):
        for file in project.get('files', []):
            for dependency in file.get('results', {}).get('dependencies', []):
                # Get the known vulnerabilities for each dependency
                for specification in dependency.get('specifications', []):
                    raw_spec = specification.get('raw', None)
                    print(f"*******{raw_spec}******")
                    if not raw_spec:
                        print(f"Skipping dependency {dependency.get('name', 'Unknown')} because raw_spec is missing.")
                        continue

                    try:
                        package_name, package_version = raw_spec.split('==')
                    except ValueError as e:
                        print(f"Error splitting raw spec: {raw_spec}. Error: {str(e)}")
                        continue
                    
                    # Skip if we've already processed this vulnerability
                    if package_name in processed_vulnerabilities:
                        processed_vulnerabilities[package_name].extend(
                            [vuln for vuln in specification.get('vulnerabilities', {}).get('known_vulnerabilities', [])]
                        )
                        continue

                    # Otherwise, add this package with its vulnerabilities
                    processed_vulnerabilities[package_name] = specification.get('vulnerabilities', {}).get('known_vulnerabilities', [])

    # Now process the vulnerabilities and generate SARIF results
    for package_name, vulnerabilities in processed_vulnerabilities.items():
        print(f"Found {len(vulnerabilities)} vulnerabilities for package '{package_name}'.")

        # Get files that import this package (only once per package)
        matched_files = find_files_for_package(package_name, source_dir=".")
        if not matched_files:
            print(f"No Python files found that import {package_name}.")
        else:
            print(f"Found {len(matched_files)} files that import {package_name}.")

        # Process each vulnerability for the package
        for vuln in vulnerabilities:
            vuln_id = vuln.get('id', 'UNKNOWN')
            description = vuln.get('description', '')

            # If no description, provide a URL to the details
            if not description:
                description = f"See details at: https://data.safetycli.com/v/{vuln_id}/eda"

            severity = vuln.get('severity', 'LOW').upper()
            line = vuln.get('line', 1)
            vulnerable_spec = vuln.get('vulnerable_spec', '')
            rule_id = vuln.get('id', 'UNKNOWN')
                            
            vuln_data = {
                'vuln_id': vuln_id,
                'description': description,
                'package_name': package_name,
                'package_version': package_version,
                'severity': severity,
                'line': line,
                'vulnerable_spec': vulnerable_spec,
                'rule_id': rule_id
            }

            #converting the results of safety scan to sarif format
            for matched_file in matched_files:
                uri_value = os.path.relpath(matched_file, start=os.getcwd())
                fingerprint = generate_fingerprint(uri_value, vuln['line'])
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
                    "fingerprints": {
                        "primary": fingerprint
                    }
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
