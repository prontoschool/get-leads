.. code:: robotframework
*** Settings ***
| Resource | ../resources/common_res.txt
Test Teardown    Close All Browsers
Test Setup       Open Site 
Documentation    First tc

*** Test Cases ***
Visit contact page
	Go To     ${Get Leads URL}/contact/
	Page Should Contain    Contact Form
	Input Text    xpath=//input[@name='firstname']     Steve
	Input Text    xpath=//input[@name='lastname']      Roger
	Click Button      Submit
	Page Should Contain     Thank You!
