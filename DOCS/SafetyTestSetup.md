1. Create requirements.txt file, which is required for safety scan
```
pipreqs . --force --debug
```

4. Installed a vulnerable package```
```
pip install urllib3==1.25.6
```

5. Created a file called trigger_safety.py and imported the vulnerable package.
```
#this is just a file to trigger a safety scan

import urllib3

http = urllib3.PoolManager()

response = http.request('GET', 'https://httpbin.org/ip')

print(response.data)
```

7. Update requirements.txt file to include vulnerable package.
```
pipreqs . --force --debug
```

8. Pushing these changes to GitHub.
```
git add .
git commit -m "created a new vulnerable file that imports vulnerable 'urllib3' package to test safety scan detection and generate alerts in code scanning alerts."
git push origin secure_coding_updates
```

9. 6 Code scanning alerts were generated as a result of this vulnerable package being imported.
<img width="704" alt="image" src="https://github.com/user-attachments/assets/d1cfe39f-79e4-476c-8c1d-89778ade3674">
