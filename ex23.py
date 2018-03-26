# Imports module that tells compiler that we will be using future syntax that has not been standardly released yet to ease migration
from __future__ import print_function

#imports pandas, data analysis view
import pandas as pd
#imports googles api  client
import six
from apiclient.discovery
#google analytics api authorization
import build
from oauth2client.service_account
 import ServiceAccountCredentials

#print out version information from google api client
print(six.__version__)

#sets variable to analytics reporting
ANALYTICS_SERVICE = 'analyticsreporting'
#sets variable to analytics version no
ANALYTICS_SERVICE_VERSION = 'v4'

#sets variable scopes to this URL which gives read only access to analytics API
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

#sets key file name to json file with credentials
KEY_FILE = 'google_service_account_credentials.json'
#sets data file to a csv on alexs machine for author benchmarks
DATA_FILE = '/Users/alexandermclaughlin/data_requests/AP/author_benchmarks/2001-3000_author-articles_2017-09-01_2018-01-26.csv'

#creates key value pair dictionary of views within GA that we will be referencing
VIEW_IDS = {
    'Who What Wear': '1794175',
    'Byrdie': '73724826',
    'MyDomaine': '76360909'
}

#sets the range of dates that we will be pulling traffic for through key value pair list
DATE_RANGE = {
    'startDate': '2017-09-01',
    'endDate': '2018-01-26'
}

#creates list of metrics that we will want to recieve
METRICS = [
    'ga:users',
    'ga:pageviews',
    'ga:pageviewsPerSession',
    'ga:timeOnPage',
    'ga:avgTimeOnPage',
    'ga:bounceRate',
    'ga:avgSessionDuration'
]

#sets variable to page slug
URL_COLUMN = 'slug'
#sets site column to GA site
SITE_COLUMN = 'site'
#holds the name of our output file
OUTPUT_NAME = '2001-3000_author-articles_2017-09-01_2018-01-26_output'
#holds the name of our input file
INPUT_NAME = '2001-3000_author-articles_2017-09-01_2018-01-26'

#defines a function called handle
def handle():
    # LOAD DATA FRAME - opens and reads our data file using pandas
    articles = pd.read_csv(DATA_FILE)

    # AUTHENTICATE GA API CLIENT - passes credentials to allow access
    analytics_api = authenticate_service(
        service_name=ANALYTICS_SERVICE,
        api_version=ANALYTICS_SERVICE_VERSION
    )

#traverses our rows in our article list
    for index, row in articles.iterrows():
        # GET SLUG FROM URL
        #removes faulty characters in pagePath
        clean_url = row[URL_COLUMN].split('?')[0]
        #removes slide numbers from URL
        article_url = clean_url.split('/slide')[0].strip('/')
        #returns the index of backslash in current URL *** adds 1 to that?
        slug = article_url[article_url.rfind('/') + 1:]
        #prints out key value pair of slug and stripped URL by passing in through variable
        print('slug: {0}'.format(slug))

#sets our traffic filters to be organic and US only; puts a variable opening in page filter
        filters = 'ga:sourceMedium!~jungroup|Instant|keywee|taboola|' \
          'outbrain|vip-social|aka-pinterest|paid|^tpc|rpm-api;' \
          'ga:country==United States;' \
          'ga:pagePath=~{0}'

        # CREATE REQUEST BODY
        body = {
        #list of reports that we are askinf GA for
            'reportRequests': [{
            #Passses our view ID list into GA
                'viewId': VIEW_IDS[row[SITE_COLUMN]],
                #passes our date range filter to GA
                'dateRanges': [DATE_RANGE],
                #passes the metrics that we are looking for to GA
                'metrics': [{'expression': metric} for metric in METRICS],
                #sets our filter and sets the pagePath filter to a slug
                'filtersExpression': filters.format(slug)
            }]
        }

        # MAKE REQUEST
        #sets variable response to the batch gotten reports
        response = analytics_api.reports().batchGet(
        #sets body of batchget to previously defined
            body=body
            #executes pull
        ).execute()

        # GET RESULTS
        #sets report variable to response to reports list ****?
        report = response['reports'][0]
        #creates list of title row of our reports?
        metric_header_entries = report['columnHeader']['metricHeader']['metricHeaderEntries']
        #creates list of sets the ????
        metric_headers = [entry['name'] for entry in metric_header_entries]
        #sets the row values from our reports****
        metric_values = report['data']['totals'][0]['values']
        #looks like its compressing our values into a dictorinary of all results
        results = dict(zip(metric_headers, metric_values))

        # ADD RESULTS TO DATAFRAME
        #for every metric in metric headers
        for metric in metric_headers:
            #locate within pandas window an articles metric then set it
            articles.loc[index, metric] = results[metric]
            #then set its matching slug column to the correct one
            articles.loc[index, 'slug'] = slug

#call something that will rename our data file to its final name and transfer to CSV to save it as our output
    articles.to_csv(
        DATA_FILE.replace(INPUT_NAME, OUTPUT_NAME),
        index=False
    )


#create a function that authenticates our google pull
def authenticate_service(service_name, api_version):
    '''authenticate google analytics service using service account'''

    # CREATE CREDENTIALS OBJECT
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
    #pass our key files
        filename=KEY_FILE,
        #pass the URL we previously defined
        scopes=SCOPES
    )

#set up GA connection? or prefernces of the reporting that we are working from in GA
    service = build(
        ANALYTICS_SERVICE,
        ANALYTICS_SERVICE_VERSION,
        credentials=credentials
    )
    #outputs this
    return service


# One reason for doing this is that sometimes you write a module (a .py file) where it can be executed directly. Alternatively, it can also be imported and used in another module. By doing the main check, you can have that code only execute when you want to run the module as a program and not have it execute when someone just wants to import your module and call your functions themselves.
if __name__ == '__main__':
    #throw error
    handle()
