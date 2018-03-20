import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    
    try:
        s3 = boto3.resource('s3')
        sns = boto3.resource('sns')
        topic = sns.Topic('arn:aws:sns:us-east-1:928252719086:deployPortfolio')
        portfolio_bucket = s3.Bucket('portfolio.stevenpowell.xyz')
        build_bucket = s3.Bucket('portfoliobuild.stevenpowell.xyz')
        
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
    
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
            
        print "Mission Complete"
        topic.publish(Subject="portfolio deployed", Message="Mission Comprete. You are winrar!")
    except:
        topic.publish(Subject="portfolio not deployed", Message="Fission Mailed")
    return 'Hello from Lambda'
