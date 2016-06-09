.. code:: robotframework
*** Settings ***
| Resource | ../resources/test_server_res.txt
Test Teardown    Close All Browsers
Test Setup       Open Site 
Documentation    First tc

*** Test Cases ***
Visit contact page
	Go To     ${Get Leads URL}/contact/
	Page Should Contain     Good Afternoon, intern! 
