# Requirements for running selenium:
* Selenium is a portable software-testing framework for web applications.
* It also provides a test domain-specific language (Selenese) to write 
* tests in a number of popular programming languages, including C#, 
* Groovy, Java, Perl, PHP, Python, Ruby and Scala.
* The tests can then run against most modern web browsers. 
* Selenium deploys on Windows, Linux, and macOS platforms. 
* It is open-source software, released under the Apache 2.0 license: 
* web developers can download and use it without charge.

## Downloading Python bindings for Selenium
```
pip install selenium
```
or
```
pip install -r requirements.txt
```
## Drivers
* Selenium requires a driver to interface with the chosen browser. 
* Firefox, for example, requires geckodriver, which needs to be installed 
* before the below examples can be run. Make sure it’s in your PATH, e. g., p
* lace it in /usr/bin or /usr/local/bin.
*
* | DRIVER     | URL                                                                   |
* |------------|-----------------------------------------------------------------------|
* | Chrome:    | https://sites.google.com/a/chromium.org/chromedriver/downloads        |
* | Edge:      | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ |
* | Firfeox:   | https://github.com/mozilla/geckodriver/releases                       |
* | Safari:    | https://webkit.org/blog/6900/webdriver-support-in-safari-10/          |
*
*