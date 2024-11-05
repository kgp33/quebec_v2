#### Install Both
```
pip install bandit safety
```

#### Created Insecure File
```
#filename is insecure_code.py

#hardcoded token/password in code
token = ";alkjdsalfjieajlh"

#manually working with files in temp directory is not safe

temp_dir = "/tmp"
```

#### Executed Bandit
```
#make sure you saved insecure_code.py before executing this command

bandit insecure_code.py
```
<img width="653" alt="image" src="https://github.com/user-attachments/assets/7bf61fa9-6342-4cc5-b517-6564ddd1751e">

#### Executing Bandit with Options
```
#This doesn't change any metrics or anything, it only changes what it reports to you.

#sets logging level to "warning" - least verbose
bandit insecure_code.py -l

#sets logging level to "info"
bandit insecure_code.py -ll

#sets logging level to "debug" -  most verbose
bandit insecure_code.py -lll

#scanning an entire directory
bandit -r .


```

#### NOSEC
```
#If you add the bandit code and prepend it with "nosec" as shown below, it will remove that scanning result from the metrics.


#hardcoded token/password in code
token = ";alkjdsalfjieajlh" # nosec: B105

#manually working with files in temp directory is not safe

temp_dir = "/tmp"
```
#### Ignoring Something Throughout Entire Program Instead of One by One with nosec
```
bandit insecure_code.py -s B105
```

#### Safety 
```
#checks your project's dependencies for known security vulnerabilities

#to demonstrate its usage and value, I've installed a version of numpy that has a known security vulnerability.

pip install numpy==1.22.1

safety check

#to get more details
safety check --full-report
```
<img width="644" alt="image" src="https://github.com/user-attachments/assets/2b2f18ec-beb5-4319-bb8a-d9764324c0a7">

##### Full-Report Details
<img width="650" alt="image" src="https://github.com/user-attachments/assets/dc6bdadc-d80d-4d2e-8ce3-f130ad84247f">

