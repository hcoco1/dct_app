# SESSION 4: HANDS-ON GUIDE

## /------------- s3.upload.py ---------------/

a) `python3 s3_upload/s3_upload.py`
b) `ls -l s3_upload/csv_files`
c) `chmod 200 s3_upload/csv_files/FILENAME`
d) `chmod 644 s3_upload/csv_files/FILENAME`

## /--------------- AWS CDK -----------------/

e) `source .venv/bin/activate`
f) `cdk deploy`
g) `cdk destroy`

## /--------------- LAMBDA ------------------/

h) `table = 'DctAppStack-PropertiesTable324F3970-NEBNY78RCM74'`
i) `sam local invoke -e event.json`

j) 
```python
required_keys = ['zpid', 'creationDate', 'streetAddress', 'unit', 'bedrooms', 
                 'bathrooms', 'homeType', 'priceChange', 'zipcode', 'city', 
                 'state', 'country', 'livingArea', 'taxAssessedValue', 
                 'priceReduction', 'datePriceChanged', 'homeStatus', 'price']
```
