
<div align="center"><h1>Ivan Arias</h1></div>
<div align="center"><h2>Full-Stack Developer | Junior Penetration Tester | AWS Enthusiast </h2></div>

<div id="badges" align="center">
  <a href="https://www.linkedin.com/in/hcoco1/">
    <img src="https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge"/>
  </a>
  <a href="https://www.youtube.com/channel/UCban0ilP3jBC9rdmL-fPy_Q">
    <img src="https://img.shields.io/badge/YouTube-red?style=for-the-badge&logo=youtube&logoColor=white" alt="Youtube Badge"/>
  </a>
  <a href="https://twitter.com/hcoco1">
    <img src="https://img.shields.io/badge/Twitter-blue?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter Badge"/>
  </a>
</div>  



<div align="center"><h3>Python and DevOps on AWS Bootcamp</h3></div>
<div align="center"><h4>Session 4: Hands On Guide</h4></div>

 /------------- s3.upload.py ---------------/ # https://github.com/hcoco1/s3_upload

- `python3 s3_upload/s3_upload.py`
- `ls -l s3_upload/csv_files`
- `chmod 200 s3_upload/csv_files/FILENAME`
- `chmod 644 s3_upload/csv_files/FILENAME`

 /--------------- AWS CDK -----------------/

- `source .venv/bin/activate`
- `cdk deploy`
- `cdk destroy`

 /--------------- LAMBDA ------------------/

- `table = 'DctAppStack-PropertiesTable324F3970-NEBNY78RCM74'`
- `sam local invoke -e event.json`

 
```python
required_keys = ['zpid', 'creationDate', 'streetAddress', 'unit', 'bedrooms', 
                 'bathrooms', 'homeType', 'priceChange', 'zipcode', 'city', 
                 'state', 'country', 'livingArea', 'taxAssessedValue', 
                 'priceReduction', 'datePriceChanged', 'homeStatus', 'price']
```


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
