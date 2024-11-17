**Quebec Secure Coding Standard**  
**Updated:** October 22, 2024  

**Issued By:** Quebec Project Team  
**Owner:** Molly Herforth  

**This document was derived from the Center for Internet Security's Secure Coding Standard Template**[^1]
[^1]:https://www.cisecurity.org/wp-content/uploads/2020/06/Secure-Coding-Standard.docx


# 1.0 Purpose and Benefits

Organizations are under constant cyber-attacks that attempt to exploit vulnerabilities within computer systems and thereby threaten the confidentiality, integrity, and availability of information. A large number of vulnerabilities that are successfully exploited are due to software coding weaknesses and coding implementation flaws.

The objective of this coding standard is to ensure that code written is resilient to high-risk threats and to avoid the occurrence of the most common coding errors which create serious vulnerabilities in software. While it is impossible to write code that is completely impervious to all possible attacks, implementing these coding standards throughout information systems will significantly reduce the risk of disclosure, alteration or destruction of information due to software vulnerabilities.

# 2.0 Information Statement

In accordance with Quebec's SecDevOps mindset, all software written for or deployed on systems must incorporate secure coding practices, to avoid the occurrence of common coding vulnerabilities and to be resilient to high-risk threats, before being deployed in production.

The items enumerated in this standard are not an exhaustive list of high-risk attacks and common coding errors but rather a list of the most damaging and pervasive. Therefore, code written must contain mitigating controls not only for the items specifically articulated in the standard below, but also for any medium and high-risk threats that are identified during a system’s life cycle.

High risk threats include, but are not limited to:

1. Code Injection
2. Cross-site scripting (XSS)
3. Cross-site request forgery (CSRF)
4. Information leakage and improper error handling
5. Missing Authentication for Critical Function
6. Missing Encryption of Sensitive Data
7. URL Redirection to Untrusted Site ('Open Redirect')

At a minimum, code must eliminate or mitigate the threats identified in the current version of the [Open Web Application Security Project (OWASP) Top 10 Most Critical Application Security Risks (‘OWASP Top 10’)](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project) and the [Common Weakness Enumeration (CWE)/SANS Top 25 Most Dangerous Software Errors (‘CWE/SANS Top 25’)](http://cwe.mitre.org/top25/) publications (see [Appendix A](#AppendixA)).

Both OWASP and CWE/SANS periodically reissue their respective lists based on changes in vulnerability and exploitation patterns. Developers are required to independently remain aware of updates to these lists and incorporate any new recommendations.

Use of common security control libraries and common API’s, that have undergone security testing, is required to ensure a consistent approach that minimizes defects and prevents exploitation. When available, publicly available or vendor-supplied libraries or APIs should be used unless there’s a business case developed and exception granted by the Information Security Officer (ISO)/designated security representative to develop a custom library.

To prevent defects or detect and remove them early, thereby realizing significant cost and schedule benefits to the entity, code must be checked for errors throughout development and during maintenance.

# 3.0 Best Practices

### 3.1 Input Validation

Quebec is a Python application that processes client-provided financial data. This data needs to be validated to safeguard against malicious or unintended inputs that could compromise data integrity and system stability.[^2] Injection vulnerabilities, such as SQL and command injection, are prevalent in Python programs and input validation mitigates this risk. Validating input also minimizes the risk of unexpected behavior and crashes within the application. 

Qwiet AI recommends the following steps be taken for proper input validation: [^3]

1. **Define the Input**: Clearly define what kind of data is acceptable. If it’s a string, should it be alphanumeric? If it’s a number, what range is okay?
2. **Validate Against Criteria**: Always check that the incoming data matches your requirements. This isn’t just about type checking; it’s about confirming the data fits the expected format and length and adheres to the expected pattern.
3. **Handle Invalid Input**: When data doesn’t pass validation, have a plan. You might log the issue, throw an exception, or ask the user to re-enter the data, but don’t just let it slide.
4. **Secure Default Values**: Use safe default values to handle unexpected inputs. If something slips through the cracks, your application won’t suddenly behave unpredictably.
5. **Regular Updates**: Keep your validation logic up-to-date. As new threats emerge, you must adjust your rules to stay one step ahead of attackers.

### 3.2 Static Analysis

Static analysis techniques are used to evaluate a source code's formatting consistency, adherence to coding standards, documentation conventions, and security vulnerabilities **without** executing it. The Quebec development team has decided to implement static analysis testing early in the software development lifecycle to expedite the identification of security flaws within our code before they become problematic. Per Snyk.io, "static code analysis will enable us to detect code bugs or vulnerabilities that other testing methods and tools, such as manual code reviews and compilers, frequently miss." [^4] 

Static Application Security Testing (SAST) is a subset of static analysis testing that our team has decided to focus on. SAST prioritizes the detection of security vulnerabilities as opposed to things like code style deviations and optimization issues. SAST tools are "designed specifically to find security issues with high accuracy, striving for low false positive and false negative rates, and providing detailed information about root causes and remedies of spotted vulnerabilities."[^5] 

The first tool we've decided to use for SAST is [Bandit](https://bandit.readthedocs.io/en/latest/). Per their documentation, "Bandit is a tool designed to find common security issues in Python code. To do this, Bandit processes each file, builds an Abstract Syntax Tree (AST) from it, and runs appropriate plugins against the AST nodes. Once Bandit has finished scanning all the files, it generates a report."[^6]

The second tool we've decided to use for SAST is [Safety CLI](https://safetycli.com). Per their documentation, "Safety CLI is a Python dependency vulnerability scanner designed to enhance software supply chain security and enable the secure use of Python packages."[^7] In order for Safety CLI to work, our repository's dependencies must be stored in a `requirements.txt` file.

#### 3.2.1 Static Analysis Implmentation

The Quebec team has incorporated Bandit and Safety into its Continuous Integration/Continuous Delivery (CI/CD) pipeline via GitHub Actions. In doing so, we've automated the static application analysis testing of our source code. Our repository's Bandit and Safety scan settings can be found and customized in the `security.yml` workflow located at `.github/workflows/security.yml`.

Usage information for Bandit can be found [here](https://github.com/kgp33/quebec_v2/blob/main/DOCS/Bandit.md).

In order for the safety scan to yield accurate results, repository contributors **MUST** update the `requirements.txt` file before pushing changes to the remote repository. That can be done using the following command:

```python
pipreqs . --force --debug
``` 

The current `security.yml` workflow uses Molly's API key to run a safety scan then saves the results to a json file and converts them to a SARIF file via a script called `convert_safety_to_sarif.py`. This script is  located in the "scripts" directory. 

Alerts for both tools can be viewed under the Security tab the our repository, in the "Code scanning" section. Pull requests that yield Code scanning alerts will **NOT** be merged to main.

Currently, the following events trigger these static scans:

- Changes pushed to the any branch
- A pull request targeting the any branch is created or updated
- A cron job that runs every Tuesday at 22:26 UTC regardless of any pushes or pull requests

### 3.3 Dyanmic Analysis

Per the Software Engineering Body of Knowledge (SWEBOK), published by the IEEE Computer Society, "dynamic analysis techniques involve executing or simulating the software code, looking for errors and defects."[^8] Put simply, dyanmic analysis is used to evaluate an application's behavior **at runtime** when provided a variety of inputs to detect security vulnerabilities, logic flaws, performance issues, etc.

[Hypothesis](https://hypothesis.works) is a tool that the Quebec team is using to implement dyanmic analysis testing into our software development lifecycle. Hypothesis integrates with [pytest](https://docs.pytest.org/en/stable/) and uses property-based testing to test our code against a much wider range of scenarios than a human tester could, finding edge cases that would have otherwise been missed.[^9]

#### 3.3.1 Dyanmic Analysis Implmentation

The Quebec team is utilizing [Hypothesis](https://hypothesis.works), as well as [hypothesis_jsonschema](https://pypi.org/project/hypothesis-jsonschema/) to test the robustness of our json schema, as defined in `Schemas/stock-schema.json`. The test is configured in `UnitTests/test_schema_hypothesis.py` and confirms that our program can properly process valid and invalid input. 

Fuzz Testing Implementation:
The Quebec team has implemented fuzz tests using Hypothesis to evaluate the portfolio valuation and Sharpe ratio calculations. These tests dynamically generate random portfolios and historical price data to ensure the program's robustness against a wide variety of input scenarios.

Usage and setup information for Hypothesis can be found [here](https://github.com/kgp33/quebec_v2/blob/main/DOCS/Hypothesis_Info%26Setup.md).

[^2]: https://fintechpython.pages.oit.duke.edu/jupyternotebooks/1-Core%20Python/answers/rq-22-answers.html
[^3]: https://qwiet.ai/securing-your-python-codebase-best-practices-for-developers/
[^4]: https://snyk.io/learn/open-source-static-code-analysis/
[^5]: https://snyk.io/learn/open-source-static-code-analysis/
[^6]: https://bandit.readthedocs.io/en/latest/index.html
[^7]: https://safetycli.com
[^8]: H. Washizaki, eds., Guide to the Software Engineering Body of Knowledge (SWEBOK Guide), Version 4.0, IEEE Computer Society, 2024; www.swebok.org
[^9]: https://hypothesis.works

# 4.0 Compliance

This standard shall take effect upon publication. Compliance is expected with all enterprise policies and standards. Policies and standards may be amended at any time.

If compliance with this standard is not feasible or technically possible, or if deviation from this policy is necessary to support a business function, entities shall request an exception through the Chief Information Security Officer’s exception process.

# 5.0 Definitions of Key Terms

| **Term** | Definition |
| --- | --- |
|     |     |

# 6.0 Revision History

This standard shall be subject to periodic review to ensure relevance.

| **Date** | **Description of Change** | **Reviewer** |
| --- | --- | --- |
|     |     |     |

# 7.0 Related Documents

[Open Web Application Security Project (OWASP) Top 10 Most Critical Application Security Risks (‘OWASP Top 10’)](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project)

[Open Web Application Security Project (OWASP) Developer Cheat Sheets](https://www.owasp.org/index.php/Cheat_Sheets)

[Open Web Application Security Project (OWASP) Enterprise Security API](https://www.owasp.org/index.php/Category:OWASP_Enterprise_Security_API#tab=Home)

[Common Weakness Enumeration (CWE)/SANS Top 25 Most Dangerous Software Errors ‘CWE/SANS Top 25’)](http://cwe.mitre.org/top25/)

[Common Weakness Enumeration (CWE) List](http://cwe.mitre.org/data/index.html)

[Carnegie Mellon Software Engineering Institute CERT Secure Coding Standards](http://www.cert.org/secure-coding/research/secure-coding-standards.cfm?"%20\t%20"_blank)

**Appendix A: Coding Resources**

**Open Web Application Security Project (OWASP)**

The OWASP Top 10 is authored by OWASP, an open-source application security community project which aims to raise security awareness of web application security risks. Although OWASP is focused on web application security, the standards and controls presented by this organization are generally also applicable to non-web based information systems.

In addition to the “Top 10” list, OWASP also produces the [Enterprise Security API (ESAPI) library](https://www.owasp.org/index.php/Category:OWASP_Enterprise_Security_API#tab=Home) and [developer cheat sheets](https://www.owasp.org/index.php/Cheat_Sheets). The ESAPI library is an open source, web application security control library designed to mitigate risks to web applications. The ESAPI library provides a framework to implement code to address the risks listed within the OWASP Top Ten project. The cheat sheets provide a concise collection of high value information on specific web application security topics.

Additional information regarding OWASP, the ESAPI library and the Top Ten project is available at <https://www.owasp.org/>.

**Common Weakness Enumeration/SANS**

The CWE/SANS Top 25 Most Dangerous Software Errors publication is the result of collaboration between the SANS Institute, MITRE, and many top software security experts in the US and Europe. The publication is a list of the most widespread and critical errors that can lead to serious vulnerabilities in software. They are often easy to find, and easy to exploit. They are dangerous because they will frequently allow attackers to completely take over the software, steal data, or prevent the software from working at all.

The MITRE website provides detailed guidance to software programmers for mitigating and avoiding each of the common weaknesses enumerated within the Top 25 list with the [Common Weakness Enumeration (CWE) List](http://cwe.mitre.org/data/index.html).
