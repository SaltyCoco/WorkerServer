# WorkerServer
Snippets from a personal test environment.
This pulls data, processes it and updates databases (etl)
It then creates plotly and html visuals to email to people.

#DataPull
Many times I run into sites where it is bogged down in javascript.  When this occurs I use Selenium to walk through the DOM and either download the files or scrape by elements.  Obviously, pulling from an api would be ideal but in some cases there is no data api.

#Email
Sending emails with analytics in them is a pain and should be avoided at all costs.  Regardless, in my experience many people like to recieve info this way.  These are a few different ways to send them.  O capitan my capitan............

#Report
In actual use this would be broken up into pieces but I put everything together so that you can get the soup to nuts on how a robust, well robust for me, report would be completed.  This basically is pulling data from an rds postgres db that the DataPull would push data to.  I use a mix of pandas and sql to create the metrics.  I am sure there is a super fancy method to this but in reality etween using sql and pandas to process the metrics you have two ways to do everything.  Pick the one that is easiest for you.  Next step is to create plotly visuals.  After that you make a html email referencing the variables you just made.  Do be like me and append a giant string, the formating is a nightmare.  Use the built in injection way where you reference them at the end.

#Production
I have made several worker servers like this.  The production versions are huge processing up to 1000s of jobs daily and communicating between a lot of different resources.  Some of these are intergrated into an api if preformance allows for it.  To trigger the actions you can use an aws lambda or framework (i.e celery, redis, ect).
