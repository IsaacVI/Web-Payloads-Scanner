# Web Payloads Scanner

Example usage:
`webPayloadsScanner.py -u https://example.com?parameter={payload}  -p payloads.txt`

Help:


    usage: webPayloadsScanner.py [-h] -u URL -p PAYLOADS [-r REPLACE] [-P POST] [-d DEFAULT_PAYLOAD] [-l] [-c COOKIES] [-H HEADERS] [-b BYTE_DIFFERENCE] [-v]
    
    Try to use payloads on target website
    
    optional arguments:
      -h, --help            show this help message and exit
      -u URL, --url URL     target URL
      -p PAYLOADS, --payloads PAYLOADS
                            file with payloads
      -r REPLACE, --replace REPLACE
                            change default replacing string, Default: {payload}
      -P POST, --post POST  post data
      -d DEFAULT_PAYLOAD, --default_payload DEFAULT_PAYLOAD
                            add default payload what will be used to compare otherwise will be randomised
      -l, --simple-length   dont calculate differences in payloads lengths to reduce results
      -c COOKIES, --cookies COOKIES
                            additional cookies
      -H HEADERS, --headers HEADERS
                            additional headers
      -b BYTE_DIFFERENCE, --byte-difference BYTE_DIFFERENCE
                            max difference in size from default response in bytes to not mark as suspicious
      -v, --verbose         show additional info

## POST
`-P "post1=value1; post2={payload}"`

## Cookies
`-c "cookie1=value1; cookie2=value2"`

## Headers
`-H "header1=value1; header2=value2"`
